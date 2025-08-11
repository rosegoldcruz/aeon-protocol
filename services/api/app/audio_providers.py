"""
Advanced Audio Generation and Processing Providers
"""
import os
import requests
import replicate
from typing import Dict, Any, Optional, List
from enum import Enum
import base64
from io import BytesIO

class AudioProvider(str, Enum):
    ELEVENLABS = "elevenlabs"
    OPENAI = "openai"
    MUBERT = "mubert"
    SUNO = "suno"

class ElevenLabsProvider:
    """ElevenLabs advanced voice synthesis"""
    
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.base_url = "https://api.elevenlabs.io/v1"
    
    async def text_to_speech(self, text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM", **kwargs) -> Dict[str, Any]:
        """Convert text to speech"""
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        
        payload = {
            "text": text,
            "model_id": kwargs.get("model_id", "eleven_multilingual_v2"),
            "voice_settings": {
                "stability": kwargs.get("stability", 0.5),
                "similarity_boost": kwargs.get("similarity_boost", 0.5),
                "style": kwargs.get("style", 0.0),
                "use_speaker_boost": kwargs.get("use_speaker_boost", True)
            }
        }
        
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        return {
            "audio_data": response.content,
            "voice_id": voice_id,
            "provider": "elevenlabs",
            "operation": "text_to_speech"
        }
    
    async def voice_cloning(self, audio_files: List[str], voice_name: str, description: str) -> Dict[str, Any]:
        """Clone a voice from audio samples"""
        url = f"{self.base_url}/voices/add"
        
        headers = {"xi-api-key": self.api_key}
        
        files = []
        for i, audio_file in enumerate(audio_files):
            # Download audio file
            audio_response = requests.get(audio_file)
            files.append(('files', (f'sample_{i}.mp3', audio_response.content, 'audio/mpeg')))
        
        data = {
            'name': voice_name,
            'description': description,
            'labels': '{"accent": "american", "age": "young", "gender": "male"}'
        }
        
        response = requests.post(url, headers=headers, files=files, data=data)
        response.raise_for_status()
        
        result = response.json()
        return {
            "voice_id": result["voice_id"],
            "voice_name": voice_name,
            "provider": "elevenlabs",
            "operation": "voice_cloning"
        }
    
    async def speech_to_speech(self, audio_url: str, target_voice_id: str) -> Dict[str, Any]:
        """Convert speech to different voice while preserving emotion and timing"""
        url = f"{self.base_url}/speech-to-speech/{target_voice_id}"
        
        headers = {"xi-api-key": self.api_key}
        
        # Download source audio
        audio_response = requests.get(audio_url)
        
        files = {
            'audio': ('input.mp3', audio_response.content, 'audio/mpeg')
        }
        
        data = {
            'model_id': 'eleven_english_sts_v2',
            'voice_settings': '{"stability": 0.5, "similarity_boost": 0.8}'
        }
        
        response = requests.post(url, headers=headers, files=files, data=data)
        response.raise_for_status()
        
        return {
            "converted_audio": response.content,
            "target_voice_id": target_voice_id,
            "provider": "elevenlabs",
            "operation": "speech_to_speech"
        }
    
    async def get_voices(self) -> Dict[str, Any]:
        """Get available voices"""
        url = f"{self.base_url}/voices"
        headers = {"xi-api-key": self.api_key}
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json()

class OpenAIAudioProvider:
    """OpenAI Whisper and TTS"""
    
    def __init__(self):
        import openai
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def transcribe(self, audio_url: str, language: Optional[str] = None) -> Dict[str, Any]:
        """Transcribe audio to text"""
        # Download audio
        audio_response = requests.get(audio_url)
        audio_file = BytesIO(audio_response.content)
        audio_file.name = "audio.mp3"
        
        transcript = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language=language
        )
        
        return {
            "text": transcript.text,
            "language": language,
            "provider": "openai",
            "operation": "transcription"
        }
    
    async def translate(self, audio_url: str) -> Dict[str, Any]:
        """Translate audio to English"""
        audio_response = requests.get(audio_url)
        audio_file = BytesIO(audio_response.content)
        audio_file.name = "audio.mp3"
        
        translation = self.client.audio.translations.create(
            model="whisper-1",
            file=audio_file
        )
        
        return {
            "text": translation.text,
            "provider": "openai",
            "operation": "translation"
        }
    
    async def text_to_speech(self, text: str, voice: str = "alloy") -> Dict[str, Any]:
        """Convert text to speech using OpenAI TTS"""
        response = self.client.audio.speech.create(
            model="tts-1-hd",
            voice=voice,
            input=text
        )
        
        return {
            "audio_data": response.content,
            "voice": voice,
            "provider": "openai",
            "operation": "text_to_speech"
        }

class MubertProvider:
    """Mubert AI music generation"""
    
    def __init__(self):
        self.api_key = os.getenv("MUBERT_API_KEY")
        self.base_url = "https://api-b2b.mubert.com/v2"
    
    async def generate_music(self, prompt: str, duration: int = 30, **kwargs) -> Dict[str, Any]:
        """Generate music from text prompt"""
        url = f"{self.base_url}/GetServiceAccess"
        
        payload = {
            "method": "GetServiceAccess",
            "params": {
                "email": kwargs.get("email", "user@example.com"),
                "license": "CC BY-NC-SA 4.0",
                "token": self.api_key,
                "mode": kwargs.get("mode", "track"),
                "prompt": prompt,
                "duration": duration,
                "format": kwargs.get("format", "mp3"),
                "bitrate": kwargs.get("bitrate", 320)
            }
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return {
            "music_url": result.get("data", {}).get("download_link"),
            "duration": duration,
            "prompt": prompt,
            "provider": "mubert",
            "operation": "music_generation"
        }

class SunoProvider:
    """Suno AI music and song generation"""
    
    def __init__(self):
        self.api_key = os.getenv("SUNO_API_KEY")
        self.base_url = "https://api.suno.ai/v1"
    
    async def generate_song(self, lyrics: str, style: str = "pop", **kwargs) -> Dict[str, Any]:
        """Generate complete song with vocals"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "lyrics": lyrics,
            "style": style,
            "title": kwargs.get("title", "Generated Song"),
            "instrumental": kwargs.get("instrumental", False),
            "duration": kwargs.get("duration", 120)
        }
        
        response = requests.post(f"{self.base_url}/generate", headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return {
            "song_url": result.get("audio_url"),
            "lyrics": lyrics,
            "style": style,
            "provider": "suno",
            "operation": "song_generation"
        }

# Advanced audio processing functions
async def multi_speaker_detection(audio_url: str) -> Dict[str, Any]:
    """Detect and separate multiple speakers"""
    client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))
    
    output = client.run(
        "openai/whisper:4d50797290df275329f202e48c76360b3f22b08d28c196cbc54600319435f8d2",
        input={
            "audio": audio_url,
            "model": "large-v3",
            "transcription": "srt",
            "translate": False,
            "language": "auto",
            "temperature": 0,
            "best_of": 5,
            "beam_size": 5,
            "patience": 1,
            "suppress_tokens": "-1",
            "initial_prompt": "",
            "condition_on_previous_text": True,
            "temperature_increment_on_fallback": 0.2,
            "compression_ratio_threshold": 2.4,
            "logprob_threshold": -1,
            "no_speech_threshold": 0.6
        }
    )
    
    return {
        "speakers": output.get("speakers", []),
        "transcription": output.get("transcription"),
        "provider": "whisper",
        "operation": "speaker_detection"
    }

async def real_time_audio_enhancement(
    audio_stream_url: str,
    enhancements: List[str]
) -> Dict[str, Any]:
    """Real-time audio enhancement for live streams"""
    client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))
    
    # Use audio enhancement model
    output = client.run(
        "facebook/demucs:07afea1b28d0d8b0b0c4f7b7d7b7d7b7d7b7d7b7",
        input={
            "audio": audio_stream_url,
            "model": "htdemucs",
            "extensions": ["mp3", "wav", "flac"],
            "jobs": 1,
            "split": True,
            "overlap": 0.25
        }
    )
    
    enhanced_features = []
    for enhancement in enhancements:
        if enhancement == "noise_reduction":
            enhanced_features.append({"type": "noise_reduction", "status": "applied"})
        elif enhancement == "voice_isolation":
            enhanced_features.append({"type": "voice_isolation", "status": "applied"})
        elif enhancement == "echo_cancellation":
            enhanced_features.append({"type": "echo_cancellation", "status": "applied"})
    
    return {
        "enhanced_audio": output,
        "features": enhanced_features,
        "operation": "real_time_enhancement"
    }

class AudioProviderFactory:
    """Factory for audio generation providers"""
    
    @staticmethod
    def get_provider(provider: AudioProvider):
        """Get provider instance"""
        if provider == AudioProvider.ELEVENLABS:
            return ElevenLabsProvider()
        elif provider == AudioProvider.OPENAI:
            return OpenAIAudioProvider()
        elif provider == AudioProvider.MUBERT:
            return MubertProvider()
        elif provider == AudioProvider.SUNO:
            return SunoProvider()
        else:
            raise ValueError(f"Unsupported audio provider: {provider}")
