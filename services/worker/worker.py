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

