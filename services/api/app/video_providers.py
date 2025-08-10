"""
Video generation providers integration
"""
import os
import requests
import asyncio
from typing import Dict, Any, Optional, List
from enum import Enum

class VideoProvider(str, Enum):
    RUNWAY = "runway"
    PIKA = "pika"
    LUMA = "luma"
    HAILUO = "hailuo"

class RunwayClient:
    """Runway ML video generation client"""
    
    def __init__(self):
        self.api_key = os.getenv("RUNWAY_API_KEY")
        self.base_url = "https://api.runwayml.com/v1"
        
    async def text_to_video(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate video from text prompt"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "model": kwargs.get("model", "gen3a_turbo"),
            "duration": kwargs.get("duration", 5),
            "resolution": kwargs.get("resolution", "1280x768"),
            "seed": kwargs.get("seed"),
            "watermark": kwargs.get("watermark", False)
        }
        
        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}
        
        response = requests.post(
            f"{self.base_url}/image_to_video",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    async def image_to_video(self, image_url: str, prompt: str = "", **kwargs) -> Dict[str, Any]:
        """Generate video from image"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "image": image_url,
            "prompt": prompt,
            "model": kwargs.get("model", "gen3a_turbo"),
            "duration": kwargs.get("duration", 5),
            "resolution": kwargs.get("resolution", "1280x768"),
            "motion_strength": kwargs.get("motion_strength", 5),
            "seed": kwargs.get("seed"),
            "watermark": kwargs.get("watermark", False)
        }
        
        payload = {k: v for k, v in payload.items() if v is not None}
        
        response = requests.post(
            f"{self.base_url}/image_to_video",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()

class PikaClient:
    """Pika Labs video generation client"""
    
    def __init__(self):
        self.api_key = os.getenv("PIKA_API_KEY")
        self.base_url = "https://api.pika.art/v1"
        
    async def text_to_video(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate video from text prompt"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "aspect_ratio": kwargs.get("aspect_ratio", "16:9"),
            "duration": kwargs.get("duration", 3),
            "fps": kwargs.get("fps", 24),
            "guidance_scale": kwargs.get("guidance_scale", 12),
            "negative_prompt": kwargs.get("negative_prompt", "")
        }
        
        response = requests.post(
            f"{self.base_url}/generate",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()

class LumaClient:
    """Luma AI video generation client"""
    
    def __init__(self):
        self.api_key = os.getenv("LUMA_API_KEY")
        self.base_url = "https://api.lumalabs.ai/dream-machine/v1"
        
    async def text_to_video(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate video from text prompt"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "aspect_ratio": kwargs.get("aspect_ratio", "16:9"),
            "loop": kwargs.get("loop", False)
        }
        
        response = requests.post(
            f"{self.base_url}/generations",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    async def image_to_video(self, image_url: str, prompt: str = "", **kwargs) -> Dict[str, Any]:
        """Generate video from image"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "keyframes": {
                "frame0": {
                    "type": "image",
                    "url": image_url
                }
            },
            "aspect_ratio": kwargs.get("aspect_ratio", "16:9"),
            "loop": kwargs.get("loop", False)
        }
        
        response = requests.post(
            f"{self.base_url}/generations",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()

class HailuoClient:
    """Hailuo AI video generation client"""
    
    def __init__(self):
        self.api_key = os.getenv("HAILUO_API_KEY")
        self.base_url = "https://api.hailuoai.com/v1"
        
    async def text_to_video(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate video from text prompt"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "duration": kwargs.get("duration", 5),
            "resolution": kwargs.get("resolution", "720p"),
            "style": kwargs.get("style", "realistic")
        }
        
        response = requests.post(
            f"{self.base_url}/video/generate",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()

class VideoProviderFactory:
    """Factory for video generation providers"""
    
    @staticmethod
    def get_client(provider: VideoProvider):
        """Get client for specified provider"""
        if provider == VideoProvider.RUNWAY:
            return RunwayClient()
        elif provider == VideoProvider.PIKA:
            return PikaClient()
        elif provider == VideoProvider.LUMA:
            return LumaClient()
        elif provider == VideoProvider.HAILUO:
            return HailuoClient()
        else:
            raise ValueError(f"Unsupported video provider: {provider}")

async def generate_video(
    provider: VideoProvider,
    prompt: str,
    video_type: str = "text_to_video",
    image_url: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """Generate video using specified provider"""
    client = VideoProviderFactory.get_client(provider)
    
    if video_type == "text_to_video":
        return await client.text_to_video(prompt, **kwargs)
    elif video_type == "image_to_video":
        if not image_url:
            raise ValueError("image_url required for image_to_video")
        return await client.image_to_video(image_url, prompt, **kwargs)
    else:
        raise ValueError(f"Unsupported video type: {video_type}")

async def get_video_status(provider: VideoProvider, job_id: str) -> Dict[str, Any]:
    """Get video generation status"""
    client = VideoProviderFactory.get_client(provider)
    
    if provider == VideoProvider.RUNWAY:
        headers = {"Authorization": f"Bearer {client.api_key}"}
        response = requests.get(f"{client.base_url}/tasks/{job_id}", headers=headers)
    elif provider == VideoProvider.LUMA:
        headers = {"Authorization": f"Bearer {client.api_key}"}
        response = requests.get(f"{client.base_url}/generations/{job_id}", headers=headers)
    else:
        # Implement for other providers
        return {"status": "unknown", "provider": provider}
    
    response.raise_for_status()
    return response.json()
