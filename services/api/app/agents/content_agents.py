"""
Content Creation AI Agents
"""
import json
from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentType

class ScreenwriterAgent(BaseAgent):
    """AI agent for advanced script generation with story structure analysis"""
    
    def __init__(self):
        super().__init__(AgentType.SCREENWRITER)
    
    def get_system_prompt(self) -> str:
        return """You are an expert screenwriter and story analyst specializing in video content creation. You excel at:

1. **Story Structure**: Three-act structure, character arcs, compelling narratives
2. **Scene Breakdown**: Breaking scripts into precise, timed scenes for video generation
3. **Visual Storytelling**: Rich visual descriptions optimized for AI video generation
4. **Character Development**: Multi-dimensional characters with clear motivations
5. **Dialogue Excellence**: Natural, engaging dialogue that serves the story
6. **Production Optimization**: Scripts designed for seamless video production workflows

You create scripts specifically optimized for multi-scene video generation, with each scene designed to be 8-12 seconds for perfect video stitching."""
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate script with story analysis"""
        self.validate_input(input_data, ["concept", "genre"])
        
        concept = input_data["concept"]
        genre = input_data["genre"]
        length = input_data.get("length", "short")
        target_audience = input_data.get("target_audience", "general")
        
        # Create detailed prompt
        user_prompt = f"""
        Create a {length} {genre} script based on this concept: {concept}
        Target audience: {target_audience}
        
        Please provide:
        1. Complete script with proper formatting
        2. Story structure analysis
        3. Character development notes
        4. Dialogue quality assessment
        5. Commercial viability analysis
        6. Suggestions for improvement
        """
        
        messages = self.create_messages(user_prompt)
        response = self.chat_completion(messages, temperature=0.8, max_tokens=4000)
        
        # Parse the response to extract structured scene data
        scenes = self._parse_scenes_from_script(response, 10, 12.0)

        return {
            "script": response,
            "scenes": scenes,
            "concept": concept,
            "genre": genre,
            "length": length,
            "target_audience": target_audience,
            "agent_type": self.agent_type,
            "ready_for_video_generation": True
        }

    def _parse_scenes_from_script(self, script: str, scene_count: int, scene_duration: float) -> List[Dict[str, Any]]:
        """Parse the script response to extract structured scene data"""
        scenes = []
        lines = script.split('\n')
        current_scene = None

        for line in lines:
            line = line.strip()
            if line.startswith('**SCENE ') and line.endswith('**'):
                # Save previous scene
                if current_scene:
                    scenes.append(current_scene)

                # Start new scene
                scene_num = len(scenes) + 1
                current_scene = {
                    "scene_number": scene_num,
                    "duration": scene_duration,
                    "start_time": (scene_num - 1) * scene_duration,
                    "end_time": scene_num * scene_duration,
                    "visual": "",
                    "audio": "",
                    "mood": "",
                    "transition": ""
                }
            elif current_scene and line.startswith('- VISUAL:'):
                current_scene["visual"] = line.replace('- VISUAL:', '').strip()
            elif current_scene and line.startswith('- AUDIO/VOICEOVER:'):
                current_scene["audio"] = line.replace('- AUDIO/VOICEOVER:', '').strip()
            elif current_scene and line.startswith('- MOOD:'):
                current_scene["mood"] = line.replace('- MOOD:', '').strip()
            elif current_scene and line.startswith('- TRANSITION:'):
                current_scene["transition"] = line.replace('- TRANSITION:', '').strip()

        # Add the last scene
        if current_scene:
            scenes.append(current_scene)

        # Ensure we have the expected number of scenes
        while len(scenes) < scene_count:
            scenes.append({
                "scene_number": len(scenes) + 1,
                "duration": scene_duration,
                "start_time": len(scenes) * scene_duration,
                "end_time": (len(scenes) + 1) * scene_duration,
                "visual": f"Scene {len(scenes) + 1} placeholder",
                "audio": f"Scene {len(scenes) + 1} audio",
                "mood": "neutral",
                "transition": "fade"
            })

        return scenes[:scene_count]

class VideoEditorAgent(BaseAgent):
    """AI agent for automated multi-scene video generation, assembly, and stitching"""

    def __init__(self):
        super().__init__(AgentType.VIDEO_EDITOR)

    def get_system_prompt(self) -> str:
        return """You are an expert video editor and production specialist with advanced AI video generation capabilities. You excel at:

1. **Multi-Scene Video Generation**: Creating individual video clips from scene descriptions
2. **Intelligent Video Stitching**: Seamlessly combining multiple scenes with transitions
3. **Audio-Visual Synchronization**: Perfect timing between voiceover and visual content
4. **Transition Mastery**: Creating smooth, engaging transitions between scenes
5. **Platform Optimization**: Formatting for different social media platforms
6. **Production Workflow**: Managing complex video generation pipelines

You take structured scene data from screenwriters and transform it into complete, professional video content by:
- Generating individual video clips for each scene using AI video providers
- Creating synchronized voiceover audio for each scene
- Stitching all components together with professional transitions
- Optimizing the final output for target platforms

This is revolutionary - you create full-length videos (1-2 minutes) from multiple AI-generated scenes, something no other platform can do."""

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete multi-scene video from structured scene data"""
        self.validate_input(input_data, ["scenes"])

        scenes = input_data["scenes"]
        platform = input_data.get("platform", "youtube")
        style = input_data.get("style", "cinematic")
        video_provider = input_data.get("video_provider", "runway")
        voice_id = input_data.get("voice_id", "21m00Tcm4TlvDq8ikWAM")  # Default ElevenLabs voice

        # Validate scenes structure
        if not isinstance(scenes, list) or len(scenes) == 0:
            raise ValueError("Scenes must be a non-empty list")

        # Create video generation plan
        video_plan = self._create_video_generation_plan(scenes, platform, style, video_provider)

        # Generate execution instructions for the worker
        execution_plan = {
            "operation": "multi_scene_video_generation",
            "scenes": scenes,
            "video_plan": video_plan,
            "platform": platform,
            "style": style,
            "video_provider": video_provider,
            "voice_id": voice_id,
            "total_duration": sum(scene.get("duration", 10) for scene in scenes),
            "scene_count": len(scenes),
            "workflow_steps": [
                "generate_individual_scene_videos",
                "generate_scene_audio",
                "create_transitions",
                "stitch_videos_with_audio",
                "apply_platform_optimization",
                "generate_final_output"
            ]
        }

        return {
            "execution_plan": execution_plan,
            "video_plan": video_plan,
            "scenes": scenes,
            "platform": platform,
            "style": style,
            "video_provider": video_provider,
            "voice_id": voice_id,
            "agent_type": self.agent_type,
            "ready_for_production": True,
            "estimated_processing_time": len(scenes) * 30,  # 30 seconds per scene
            "revolutionary_feature": "Multi-scene AI video generation and stitching"
        }

    def _create_video_generation_plan(self, scenes: List[Dict[str, Any]], platform: str, style: str, provider: str) -> Dict[str, Any]:
        """Create detailed plan for video generation and stitching"""

        # Platform-specific settings
        platform_settings = {
            "youtube": {"aspect_ratio": "16:9", "resolution": "1920x1080", "max_duration": 300},
            "tiktok": {"aspect_ratio": "9:16", "resolution": "1080x1920", "max_duration": 180},
            "instagram": {"aspect_ratio": "1:1", "resolution": "1080x1080", "max_duration": 90},
            "twitter": {"aspect_ratio": "16:9", "resolution": "1280x720", "max_duration": 140}
        }

        settings = platform_settings.get(platform, platform_settings["youtube"])

        # Create individual scene generation plans
        scene_plans = []
        for i, scene in enumerate(scenes):
            scene_plan = {
                "scene_number": i + 1,
                "visual_prompt": self._enhance_visual_prompt(scene.get("visual", ""), style, settings),
                "audio_text": scene.get("audio", ""),
                "duration": scene.get("duration", 10),
                "mood": scene.get("mood", "neutral"),
                "transition_in": self._get_transition_type(scene.get("transition", "fade"), "in"),
                "transition_out": self._get_transition_type(scene.get("transition", "fade"), "out"),
                "video_provider": provider,
                "provider_settings": {
                    "resolution": settings["resolution"],
                    "aspect_ratio": settings["aspect_ratio"],
                    "duration": scene.get("duration", 10),
                    "style": style,
                    "guidance_scale": 12 if provider == "pika" else 7.5,
                    "motion_strength": 5 if provider == "runway" else None
                }
            }
            scene_plans.append(scene_plan)

        return {
            "platform_settings": settings,
            "scene_plans": scene_plans,
            "total_scenes": len(scenes),
            "stitching_plan": {
                "method": "ffmpeg_concat",
                "transition_duration": 0.5,
                "audio_sync": True,
                "color_correction": True,
                "stabilization": True
            },
            "audio_plan": {
                "voice_generation": True,
                "background_music": False,  # Can be enhanced later
                "audio_normalization": True,
                "sync_tolerance": 0.1
            },
            "optimization_plan": {
                "platform": platform,
                "compression": "h264",
                "bitrate": "high",
                "captions": True,
                "thumbnail_generation": True
            }
        }

    def _enhance_visual_prompt(self, base_prompt: str, style: str, settings: Dict[str, Any]) -> str:
        """Enhance visual prompt with style and technical specifications"""
        style_modifiers = {
            "cinematic": "cinematic lighting, professional cinematography, film grain, depth of field",
            "commercial": "bright lighting, clean composition, commercial photography style",
            "artistic": "artistic composition, creative angles, stylized visuals",
            "documentary": "natural lighting, realistic style, documentary photography",
            "viral": "eye-catching visuals, bold colors, engaging composition"
        }

        aspect_modifier = {
            "16:9": "widescreen composition, landscape orientation",
            "9:16": "vertical composition, portrait orientation, mobile-optimized",
            "1:1": "square composition, centered framing"
        }

        enhanced_prompt = f"{base_prompt}, {style_modifiers.get(style, '')}, {aspect_modifier.get(settings['aspect_ratio'], '')}, high quality, professional"

        return enhanced_prompt.strip().replace("  ", " ")

    def _get_transition_type(self, transition_name: str, direction: str) -> Dict[str, Any]:
        """Get transition configuration"""
        transitions = {
            "fade": {"type": "fade", "duration": 0.5, "easing": "ease-in-out"},
            "cut": {"type": "cut", "duration": 0.0, "easing": "linear"},
            "slide": {"type": "slide", "duration": 0.8, "easing": "ease-in-out"},
            "zoom": {"type": "zoom", "duration": 0.6, "easing": "ease-in"},
            "dissolve": {"type": "dissolve", "duration": 0.7, "easing": "ease-in-out"}
        }

        base_transition = transitions.get(transition_name, transitions["fade"])
        base_transition["direction"] = direction

        return base_transition

class ContentOptimizerAgent(BaseAgent):
    """AI agent for performance prediction and A/B testing"""
    
    def __init__(self):
        super().__init__(AgentType.CONTENT_OPTIMIZER)
    
    def get_system_prompt(self) -> str:
        return """You are a content optimization expert specializing in:

1. **Viral Prediction**: Analyzing content for viral potential
2. **A/B Testing Strategy**: Designing effective content experiments
3. **Trend Analysis**: Identifying and leveraging current trends
4. **Engagement Optimization**: Maximizing likes, shares, comments
5. **Platform Analytics**: Understanding algorithm preferences

Provide data-driven recommendations for:
- Content optimization strategies
- A/B testing frameworks
- Viral potential scoring
- Engagement improvement tactics
- Platform-specific optimization"""
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze and optimize content"""
        self.validate_input(input_data, ["content_type", "platform"])
        
        content_type = input_data["content_type"]
        platform = input_data["platform"]
        content_description = input_data.get("content_description", "")
        target_metrics = input_data.get("target_metrics", ["engagement", "reach"])
        
        user_prompt = f"""
        Analyze and optimize this content:
        Type: {content_type}
        Platform: {platform}
        Description: {content_description}
        Target Metrics: {target_metrics}
        
        Provide:
        1. Viral potential score (1-10) with reasoning
        2. A/B testing strategy with specific variants
        3. Trend alignment analysis
        4. Engagement optimization recommendations
        5. Platform algorithm optimization tips
        6. Performance prediction with key metrics
        """
        
        messages = self.create_messages(user_prompt)
        response = self.chat_completion(messages, temperature=0.6, max_tokens=2500)
        
        return {
            "optimization_analysis": response,
            "content_type": content_type,
            "platform": platform,
            "target_metrics": target_metrics,
            "agent_type": self.agent_type
        }

class SEOContentAgent(BaseAgent):
    """AI agent for automated blog posts, product descriptions, and meta tags"""
    
    def __init__(self):
        super().__init__(AgentType.SEO_CONTENT)
    
    def get_system_prompt(self) -> str:
        return """You are an SEO content expert specializing in:

1. **Keyword Optimization**: Strategic keyword placement and density
2. **Content Structure**: SEO-friendly headings, meta descriptions, titles
3. **User Intent**: Matching content to search intent
4. **Technical SEO**: Schema markup, internal linking, optimization
5. **Content Quality**: E-A-T (Expertise, Authoritativeness, Trustworthiness)

Create content that:
- Ranks well in search engines
- Provides genuine value to users
- Follows SEO best practices
- Converts visitors to customers
- Builds domain authority"""
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate SEO-optimized content"""
        self.validate_input(input_data, ["content_type", "primary_keyword"])
        
        content_type = input_data["content_type"]
        primary_keyword = input_data["primary_keyword"]
        secondary_keywords = input_data.get("secondary_keywords", [])
        target_audience = input_data.get("target_audience", "general")
        word_count = input_data.get("word_count", 1000)
        
        user_prompt = f"""
        Create SEO-optimized {content_type}:
        Primary Keyword: {primary_keyword}
        Secondary Keywords: {secondary_keywords}
        Target Audience: {target_audience}
        Word Count: {word_count}
        
        Provide:
        1. Complete optimized content
        2. SEO title and meta description
        3. Header structure (H1, H2, H3)
        4. Keyword density analysis
        5. Internal linking suggestions
        6. Schema markup recommendations
        """
        
        messages = self.create_messages(user_prompt)
        response = self.chat_completion(messages, temperature=0.5, max_tokens=4000)
        
        return {
            "seo_content": response,
            "primary_keyword": primary_keyword,
            "secondary_keywords": secondary_keywords,
            "content_type": content_type,
            "word_count": word_count,
            "agent_type": self.agent_type
        }
