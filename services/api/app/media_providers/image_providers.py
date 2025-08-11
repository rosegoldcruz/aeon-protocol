"""
Advanced Image Generation Providers
"""
import os
import requests
import replicate
from typing import Dict, Any, Optional, List
from enum import Enum
import base64
from io import BytesIO
from PIL import Image

class ImageProvider(str, Enum):
    FLUX = "flux"
    IDEOGRAM = "ideogram"
    DALLE = "dalle"
    MIDJOURNEY = "midjourney"

class FluxProvider:
    """FLUX image generation via Replicate"""
    
    def __init__(self):
        self.client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))
    
    async def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate image with FLUX"""
        model = kwargs.get("model", "flux-schnell")
        
        if model == "flux-schnell":
            model_id = "black-forest-labs/flux-schnell"
        elif model == "flux-dev":
            model_id = "black-forest-labs/flux-dev"
        else:
            model_id = "black-forest-labs/flux-schnell"
        
        input_params = {
            "prompt": prompt,
            "width": kwargs.get("width", 1024),
            "height": kwargs.get("height", 1024),
            "num_outputs": kwargs.get("num_outputs", 1),
            "guidance_scale": kwargs.get("guidance_scale", 7.5),
            "num_inference_steps": kwargs.get("num_inference_steps", 4),
            "seed": kwargs.get("seed")
        }
        
        # Remove None values
        input_params = {k: v for k, v in input_params.items() if v is not None}
        
        output = self.client.run(model_id, input=input_params)
        return {"images": output, "provider": "flux", "model": model}
    
    async def upscale(self, image_url: str, scale: int = 4) -> Dict[str, Any]:
        """Upscale image using Real-ESRGAN"""
        output = self.client.run(
            "nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d7b",
            input={
                "image": image_url,
                "scale": scale,
                "face_enhance": True
            }
        )
        return {"upscaled_image": output, "provider": "flux", "operation": "upscale"}
    
    async def remove_background(self, image_url: str) -> Dict[str, Any]:
        """Remove background from image"""
        output = self.client.run(
            "cjwbw/rembg:fb8af171cfa1616ddcf1242c093f9c46bcada5ad4cf6f2fbe8b81b330ec5c003",
            input={"image": image_url}
        )
        return {"processed_image": output, "provider": "flux", "operation": "background_removal"}

class IdeogramProvider:
    """Ideogram image generation"""
    
    def __init__(self):
        self.api_key = os.getenv("IDEOGRAM_API_KEY")
        self.base_url = "https://api.ideogram.ai/generate"
    
    async def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate image with Ideogram"""
        headers = {
            "Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "image_request": {
                "prompt": prompt,
                "aspect_ratio": kwargs.get("aspect_ratio", "ASPECT_1_1"),
                "model": kwargs.get("model", "V_2"),
                "magic_prompt_option": kwargs.get("magic_prompt", "AUTO"),
                "seed": kwargs.get("seed"),
                "style_type": kwargs.get("style_type", "AUTO")
            }
        }
        
        response = requests.post(self.base_url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return {"images": [img["url"] for img in result["data"]], "provider": "ideogram"}

class DalleProvider:
    """DALL-E image generation via OpenAI"""
    
    def __init__(self):
        import openai
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate image with DALL-E"""
        model = kwargs.get("model", "dall-e-3")
        size = kwargs.get("size", "1024x1024")
        quality = kwargs.get("quality", "standard")
        n = kwargs.get("num_outputs", 1)
        
        response = self.client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality=quality,
            n=n
        )
        
        images = [img.url for img in response.data]
        return {"images": images, "provider": "dalle", "model": model}
    
    async def edit(self, image_url: str, mask_url: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """Edit image with DALL-E"""
        # Download images
        image_response = requests.get(image_url)
        mask_response = requests.get(mask_url)
        
        response = self.client.images.edit(
            image=BytesIO(image_response.content),
            mask=BytesIO(mask_response.content),
            prompt=prompt,
            n=kwargs.get("num_outputs", 1),
            size=kwargs.get("size", "1024x1024")
        )
        
        images = [img.url for img in response.data]
        return {"images": images, "provider": "dalle", "operation": "edit"}
    
    async def variation(self, image_url: str, **kwargs) -> Dict[str, Any]:
        """Create variations of image"""
        image_response = requests.get(image_url)
        
        response = self.client.images.create_variation(
            image=BytesIO(image_response.content),
            n=kwargs.get("num_outputs", 1),
            size=kwargs.get("size", "1024x1024")
        )
        
        images = [img.url for img in response.data]
        return {"images": images, "provider": "dalle", "operation": "variation"}

class ImageProviderFactory:
    """Factory for image generation providers"""
    
    @staticmethod
    def get_provider(provider: ImageProvider):
        """Get provider instance"""
        if provider == ImageProvider.FLUX:
            return FluxProvider()
        elif provider == ImageProvider.IDEOGRAM:
            return IdeogramProvider()
        elif provider == ImageProvider.DALLE:
            return DalleProvider()
        else:
            raise ValueError(f"Unsupported image provider: {provider}")

# Advanced image processing functions
async def generate_with_face_preservation(
    prompt: str,
    reference_face_url: str,
    provider: ImageProvider = ImageProvider.FLUX,
    **kwargs
) -> Dict[str, Any]:
    """Generate image while preserving specific face identity"""
    # Use InstantID or similar face preservation model
    client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))
    
    output = client.run(
        "tencentarc/photomaker:ddfc2b08d209f9fa8c1eca692712918bd449f695dabb4a958da31802a9570fe4",
        input={
            "prompt": prompt,
            "input_image": reference_face_url,
            "num_steps": kwargs.get("num_steps", 50),
            "style_strength_ratio": kwargs.get("style_strength", 20),
            "num_outputs": kwargs.get("num_outputs", 1)
        }
    )
    
    return {"images": output, "provider": "photomaker", "operation": "face_preservation"}

async def batch_generate_images(
    prompts: List[str],
    provider: ImageProvider = ImageProvider.FLUX,
    **kwargs
) -> Dict[str, Any]:
    """Generate multiple images in batch"""
    provider_instance = ImageProviderFactory.get_provider(provider)
    results = []
    
    for i, prompt in enumerate(prompts):
        try:
            result = await provider_instance.generate(prompt, **kwargs)
            results.append({
                "index": i,
                "prompt": prompt,
                "success": True,
                "result": result
            })
        except Exception as e:
            results.append({
                "index": i,
                "prompt": prompt,
                "success": False,
                "error": str(e)
            })
    
    return {"batch_results": results, "total": len(prompts)}

async def style_transfer(
    content_image_url: str,
    style_image_url: str,
    strength: float = 0.8
) -> Dict[str, Any]:
    """Apply style transfer to image"""
    client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))
    
    output = client.run(
        "tencentarc/photomaker-style:467d062309da518648ba89d226490e02b8ed09b5abc15026e54e31c5a8cd8085",
        input={
            "input_image": content_image_url,
            "style_image": style_image_url,
            "style_strength": strength
        }
    )
    
    return {"styled_image": output, "operation": "style_transfer"}

async def image_restoration(image_url: str) -> Dict[str, Any]:
    """Restore/enhance old or damaged images"""
    client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))
    
    output = client.run(
        "tencentarc/gfpgan:9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3",
        input={
            "img": image_url,
            "version": "v1.4",
            "scale": 2
        }
    )
    
    return {"restored_image": output, "operation": "restoration"}
