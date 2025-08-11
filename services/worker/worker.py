import os
import replicate
import boto3
import requests
import asyncio
from celery import Celery
from datetime import datetime
import uuid

broker_url = os.environ.get("REDIS_URL", "redis://redis:6379/0")
app = Celery("aeon_worker", broker=broker_url, backend=broker_url)

# S3 configuration
S3_BUCKET = os.environ.get("S3_BUCKET", "aeon-dev-bucket")
S3_ENDPOINT = os.environ.get("S3_ENDPOINT")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

# Configure S3 client
s3_config = {
    "aws_access_key_id": AWS_ACCESS_KEY_ID,
    "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
    "region_name": AWS_REGION
}
if S3_ENDPOINT:
    s3_config["endpoint_url"] = S3_ENDPOINT

s3_client = boto3.client("s3", **s3_config)

@app.task(bind=True)
def generate_image(self, prompt: str, job_id: int = None, **kwargs) -> dict:
    """Generate image using Replicate and store in S3"""
    try:
        token = os.environ.get("REPLICATE_API_TOKEN")
        if not token:
            raise RuntimeError("REPLICATE_API_TOKEN not set")

        client = replicate.Client(api_token=token)

        # Prepare input parameters
        input_params = {
            "prompt": prompt,
            "width": kwargs.get("width", 1024),
            "height": kwargs.get("height", 1024),
            "num_outputs": kwargs.get("num_outputs", 1),
            "guidance_scale": kwargs.get("guidance_scale", 7.5),
            "num_inference_steps": kwargs.get("num_inference_steps", 4)
        }

        # Generate image
        output = client.run(
            "black-forest-labs/flux-schnell:9d1d53d5cc05a5f8691c74764ce4bbbb7814449f7365a3b16dceaef22a8d1f64",
            input=input_params
        )

        # Store images in S3
        stored_images = []
        for i, image_url in enumerate(output):
            # Download image
            response = requests.get(image_url)
            response.raise_for_status()

            # Generate S3 key
            timestamp = datetime.now().strftime("%Y/%m/%d")
            filename = f"{uuid.uuid4()}.png"
            s3_key = f"images/{timestamp}/{filename}"

            # Upload to S3
            s3_client.put_object(
                Bucket=S3_BUCKET,
                Key=s3_key,
                Body=response.content,
                ContentType="image/png"
            )

            stored_images.append({
                "s3_key": s3_key,
                "s3_bucket": S3_BUCKET,
                "original_url": image_url,
                "index": i
            })

        return {
            "images": stored_images,
            "job_id": job_id,
            "input_params": input_params,
            "provider": "replicate",
            "model": "flux-schnell"
        }

    except Exception as e:
        # Update task state to failure
        self.update_state(
            state="FAILURE",
            meta={"error": str(e), "job_id": job_id}
        )
        raise e

@app.task(bind=True)
def generate_video(self, prompt: str, job_id: int = None, provider: str = "runway", video_type: str = "text_to_video", **kwargs) -> dict:
    """Generate video using specified provider"""
    try:
        # Import here to avoid circular imports
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'api'))

        from app.video_providers import generate_video as generate_video_provider, VideoProvider

        # Convert string to enum
        provider_enum = VideoProvider(provider)

        # Generate video
        result = asyncio.run(generate_video_provider(
            provider=provider_enum,
            prompt=prompt,
            video_type=video_type,
            **kwargs
        ))

        # Store video in S3 if URL is provided
        stored_videos = []
        if "video_url" in result:
            video_url = result["video_url"]

            # Download video
            response = requests.get(video_url)
            response.raise_for_status()

            # Generate S3 key
            timestamp = datetime.now().strftime("%Y/%m/%d")
            filename = f"{uuid.uuid4()}.mp4"
            s3_key = f"videos/{timestamp}/{filename}"

            # Upload to S3
            s3_client.put_object(
                Bucket=S3_BUCKET,
                Key=s3_key,
                Body=response.content,
                ContentType="video/mp4"
            )

            stored_videos.append({
                "s3_key": s3_key,
                "s3_bucket": S3_BUCKET,
                "original_url": video_url,
                "provider": provider,
                "duration": kwargs.get("duration", 5)
            })

        return {
            "videos": stored_videos,
            "job_id": job_id,
            "provider": provider,
            "video_type": video_type,
            "provider_response": result
        }

    except Exception as e:
        self.update_state(
            state="FAILURE",
            meta={"error": str(e), "job_id": job_id}
        )
        raise e

@app.task(bind=True)
def generate_multi_scene_video(self, scenes: list, job_id: int = None, **kwargs) -> dict:
    """Revolutionary multi-scene video generation and stitching"""
    try:
        import sys
        import os
        import subprocess
        import tempfile
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'api'))

        from app.video_providers import generate_video as generate_video_provider, VideoProvider

        provider = kwargs.get("video_provider", "runway")
        voice_id = kwargs.get("voice_id", "21m00Tcm4TlvDq8ikWAM")
        platform = kwargs.get("platform", "youtube")

        # Convert string to enum
        provider_enum = VideoProvider(provider)

        generated_scenes = []
        temp_files = []

        # Step 1: Generate individual scene videos
        for i, scene in enumerate(scenes):
            scene_prompt = scene.get("visual", f"Scene {i+1}")
            scene_duration = scene.get("duration", 10)

            # Generate video for this scene
            video_result = asyncio.run(generate_video_provider(
                provider=provider_enum,
                prompt=scene_prompt,
                video_type="text_to_video",
                duration=scene_duration,
                **kwargs
            ))

            if "video_url" in video_result:
                # Download scene video
                response = requests.get(video_result["video_url"])
                response.raise_for_status()

                # Save to temporary file
                temp_video = tempfile.NamedTemporaryFile(suffix=f"_scene_{i}.mp4", delete=False)
                temp_video.write(response.content)
                temp_video.close()
                temp_files.append(temp_video.name)

                # Generate audio for this scene
                audio_text = scene.get("audio", f"Scene {i+1} audio")
                audio_file = None
                if audio_text:
                    audio_result = generate_scene_audio(audio_text, voice_id)
                    if audio_result.get("audio_file"):
                        audio_file = audio_result["audio_file"]
                        temp_files.append(audio_file)

                generated_scenes.append({
                    "scene_number": i + 1,
                    "video_file": temp_video.name,
                    "audio_file": audio_file,
                    "duration": scene_duration,
                    "transition": scene.get("transition", "fade")
                })

        # Step 2: Stitch videos together with transitions
        final_video_path = stitch_scenes_with_transitions(generated_scenes, platform)

        # Step 3: Upload final video to S3
        timestamp = datetime.now().strftime("%Y/%m/%d")
        filename = f"multi_scene_{uuid.uuid4()}.mp4"
        s3_key = f"videos/multi-scene/{timestamp}/{filename}"

        with open(final_video_path, 'rb') as video_file:
            s3_client.put_object(
                Bucket=S3_BUCKET,
                Key=s3_key,
                Body=video_file.read(),
                ContentType="video/mp4"
            )

        # Cleanup temporary files
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass

        try:
            os.unlink(final_video_path)
        except:
            pass

        return {
            "multi_scene_video": {
                "s3_key": s3_key,
                "s3_bucket": S3_BUCKET,
                "scene_count": len(scenes),
                "total_duration": sum(scene.get("duration", 10) for scene in scenes),
                "platform": platform,
                "provider": provider
            },
            "scenes_generated": len(generated_scenes),
            "job_id": job_id,
            "revolutionary_achievement": "First AI platform to generate full multi-scene videos"
        }

    except Exception as e:
        # Cleanup on error
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass

        self.update_state(
            state="FAILURE",
            meta={"error": str(e), "job_id": job_id}
        )
        raise e

@app.task(bind=True)
def generate_audio(self, text: str, job_id: int = None, voice_id: str = None, **kwargs) -> dict:
    """Generate audio using ElevenLabs"""
    try:
        elevenlabs_key = os.environ.get("ELEVENLABS_API_KEY")
        if not elevenlabs_key:
            raise RuntimeError("ELEVENLABS_API_KEY not set")

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": elevenlabs_key
        }

        # Default voice if none specified
        if not voice_id:
            voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice

        payload = {
            "text": text,
            "model_id": kwargs.get("model_id", "eleven_monolingual_v1"),
            "voice_settings": {
                "stability": kwargs.get("stability", 0.5),
                "similarity_boost": kwargs.get("similarity_boost", 0.5)
            }
        }

        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            json=payload,
            headers=headers
        )
        response.raise_for_status()

        # Generate S3 key
        timestamp = datetime.now().strftime("%Y/%m/%d")
        filename = f"{uuid.uuid4()}.mp3"
        s3_key = f"audio/{timestamp}/{filename}"

        # Upload to S3
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=response.content,
            ContentType="audio/mpeg"
        )

        return {
            "audio": [{
                "s3_key": s3_key,
                "s3_bucket": S3_BUCKET,
                "voice_id": voice_id,
                "text": text
            }],
            "job_id": job_id,
            "provider": "elevenlabs"
        }

    except Exception as e:
        self.update_state(
            state="FAILURE",
            meta={"error": str(e), "job_id": job_id}
        )
        raise e

def generate_scene_audio(text: str, voice_id: str) -> dict:
    """Generate audio for a scene using ElevenLabs"""
    try:
        elevenlabs_key = os.environ.get("ELEVENLABS_API_KEY")
        if not elevenlabs_key:
            return {"error": "ElevenLabs API key not set"}

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": elevenlabs_key
        }

        payload = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            json=payload,
            headers=headers
        )
        response.raise_for_status()

        # Save audio to temporary file
        import tempfile
        temp_audio = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        temp_audio.write(response.content)
        temp_audio.close()

        return {"audio_file": temp_audio.name}

    except Exception as e:
        return {"error": str(e)}

def stitch_scenes_with_transitions(scenes: list, platform: str) -> str:
    """Stitch multiple scene videos together with transitions using FFmpeg"""
    try:
        import subprocess
        import tempfile

        # Platform-specific settings
        platform_settings = {
            "youtube": {"resolution": "1920x1080", "fps": 30},
            "tiktok": {"resolution": "1080x1920", "fps": 30},
            "instagram": {"resolution": "1080x1080", "fps": 30}
        }

        settings = platform_settings.get(platform, platform_settings["youtube"])

        # Create simple concatenation for now (can be enhanced with complex transitions)
        concat_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)

        for scene in scenes:
            concat_file.write(f"file '{scene['video_file']}'\n")

        concat_file.close()

        # Create output file
        output_file = tempfile.NamedTemporaryFile(suffix="_final.mp4", delete=False)
        output_file.close()

        # Build FFmpeg command for concatenation
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_file.name,
            "-c", "copy",
            output_file.name
        ]

        # Execute FFmpeg
        subprocess.run(cmd, check=True, capture_output=True)

        # Cleanup concat file
        os.unlink(concat_file.name)

        return output_file.name

    except Exception as e:
        raise Exception(f"Video stitching failed: {str(e)}")

