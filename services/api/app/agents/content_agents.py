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
        """Generate script with detailed scene breakdown for video production pipeline"""
        self.validate_input(input_data, ["concept", "genre"])

        concept = input_data["concept"]
        genre = input_data["genre"]
        length = input_data.get("length", 120)  # Default 2 minutes in seconds
        target_audience = input_data.get("target_audience", "general")
        platform = input_data.get("platform", "social_media")

        # Calculate optimal scene breakdown
        if length <= 60:
            scene_duration = 8
            scene_count = max(6, length // scene_duration)
        elif length <= 120:
            scene_duration = 10
            scene_count = max(8, length // scene_duration)
        else:
            scene_duration = 12
            scene_count = max(10, length // scene_duration)

        # Ensure total duration matches
        scene_count = min(scene_count, length // 5)  # Minimum 5 seconds per scene
        actual_scene_duration = length / scene_count

        user_prompt = f"""
        Create a compelling {genre} video script optimized for AI video generation pipeline.

        SPECIFICATIONS:
        - Concept: {concept}
        - Total Duration: {length} seconds
        - Target Scenes: {scene_count} scenes
        - Scene Duration: {actual_scene_duration:.1f} seconds each
        - Target Audience: {target_audience}
        - Platform: {platform}

        CRITICAL: Return ONLY valid JSON in this exact format:
        {{
            "title": "Engaging Video Title",
            "summary": "Brief compelling summary",
            "total_duration": {length},
            "scene_count": {scene_count},
            "scenes": [
                {{
                    "scene_number": 1,
                    "duration": {actual_scene_duration:.1f},
                    "start_time": 0,
                    "end_time": {actual_scene_duration:.1f},
                    "visual_description": "Extremely detailed visual description for AI video generation - be specific about objects, people, actions, lighting, colors, composition",
                    "voiceover_text": "Exact narration text that will be spoken",
                    "mood": "specific emotional tone",
                    "camera_style": "camera angle and movement",
                    "transition_to_next": "transition type",
                    "key_visual_elements": ["element1", "element2", "element3"],
                    "video_prompt": "Optimized prompt for video AI model"
                }}
            ],
            "story_arc": {{
                "setup_scenes": [1, 2],
                "development_scenes": [3, 4, 5, 6],
                "climax_scenes": [7, 8],
                "resolution_scenes": [9, 10]
            }},
            "production_metadata": {{
                "total_voiceover_words": 150,
                "pacing": "dynamic/steady/slow",
                "visual_style": "cinematic/documentary/animated",
                "music_style": "upbeat/dramatic/ambient",
                "platform_optimization": "specific platform notes"
            }}
        }}

        REQUIREMENTS:
        1. Each visual_description must be detailed enough for AI video generation
        2. Each video_prompt should be optimized for video AI models (Runway, Pika, Luma)
        3. Voiceover text should be natural and engaging
        4. Scene timing must be precise
        5. Visual elements should flow logically between scenes
        6. Include smooth transitions
        7. Optimize for {platform} platform

        Generate {scene_count} scenes that tell a complete, engaging story in exactly {length} seconds.
        """

        messages = self.create_messages(user_prompt)
        response = self.chat_completion(messages, temperature=0.7, max_tokens=4000)

        # Parse JSON response with error handling
        try:
            script_data = json.loads(response.strip())

            # Validate and enhance scene data
            if "scenes" in script_data:
                for i, scene in enumerate(script_data["scenes"]):
                    scene["scene_number"] = i + 1
                    scene["start_time"] = i * actual_scene_duration
                    scene["end_time"] = (i + 1) * actual_scene_duration

                    # Ensure required fields exist
                    if "video_prompt" not in scene:
                        scene["video_prompt"] = scene.get("visual_description", "")
                    if "key_visual_elements" not in scene:
                        scene["key_visual_elements"] = []

            parsing_success = True

        except json.JSONDecodeError as e:
            # Fallback parsing if JSON fails
            script_data = {
                "title": f"{concept} - {genre} Video",
                "summary": concept,
                "total_duration": length,
                "scene_count": scene_count,
                "scenes": self._create_fallback_scenes(concept, genre, scene_count, actual_scene_duration),
                "raw_response": response,
                "parsing_error": str(e)
            }
            parsing_success = False

        return {
            "script_data": script_data,
            "concept": concept,
            "genre": genre,
            "length": length,
            "target_audience": target_audience,
            "platform": platform,
            "scene_count": scene_count,
            "scene_duration": actual_scene_duration,
            "agent_type": self.agent_type,
            "ready_for_video_generation": parsing_success,
            "parsing_success": parsing_success
        }

    def _create_fallback_scenes(self, concept: str, genre: str, scene_count: int, scene_duration: float) -> List[Dict[str, Any]]:
        """Create fallback scene structure when JSON parsing fails"""
        scenes = []

        # Basic scene templates based on genre
        scene_templates = {
            "action": [
                "Dynamic action sequence with fast movement",
                "Close-up of protagonist with determined expression",
                "Wide shot of dramatic environment",
                "Intense confrontation scene",
                "Climactic action moment",
                "Resolution with calm aftermath"
            ],
            "drama": [
                "Emotional character introduction",
                "Conflict setup with tension building",
                "Character reaction and internal struggle",
                "Pivotal dramatic moment",
                "Emotional climax",
                "Thoughtful resolution"
            ],
            "comedy": [
                "Humorous setup with character introduction",
                "Comedic situation development",
                "Funny misunderstanding or mishap",
                "Escalating comedic chaos",
                "Peak comedy moment",
                "Satisfying comedic resolution"
            ]
        }

        templates = scene_templates.get(genre.lower(), scene_templates["drama"])

        for i in range(scene_count):
            template_index = i % len(templates)
            scene = {
                "scene_number": i + 1,
                "duration": scene_duration,
                "start_time": i * scene_duration,
                "end_time": (i + 1) * scene_duration,
                "visual_description": f"{templates[template_index]} related to {concept}",
                "voiceover_text": f"Scene {i + 1} narration about {concept}",
                "mood": "engaging",
                "camera_style": "dynamic",
                "transition_to_next": "smooth fade" if i < scene_count - 1 else "end",
                "key_visual_elements": [concept, genre, "engaging visuals"],
                "video_prompt": f"{templates[template_index]} related to {concept}, {genre} style, high quality"
            }
            scenes.append(scene)

        return scenes

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

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete multi-scene video from structured scene data - REVOLUTIONARY CAPABILITY"""
        # Accept either script_data from ScreenwriterAgent or direct scenes
        if "script_data" in input_data:
            script_data = input_data["script_data"]
            scenes = script_data.get("scenes", [])
            title = script_data.get("title", "Generated Video")
        elif "scenes" in input_data:
            scenes = input_data["scenes"]
            script_data = {"title": "Generated Video", "scenes": scenes}
            title = "Generated Video"
        else:
            raise ValueError("Either 'script_data' or 'scenes' must be provided")

        if not scenes:
            raise ValueError("No scenes provided for video generation")

        platform = input_data.get("platform", "youtube")
        style = input_data.get("style", "cinematic")
        video_provider = input_data.get("video_provider", "runway")
        voice_id = input_data.get("voice_id", "21m00Tcm4TlvDq8ikWAM")

        total_duration = sum(scene.get("duration", 10) for scene in scenes)
        scene_count = len(scenes)

        # Create comprehensive video generation and stitching plan
        video_production_plan = {
            "title": title,
            "total_duration": total_duration,
            "scene_count": scene_count,
            "platform": platform,
            "video_provider": video_provider,

            # Step 1: Individual Scene Generation
            "scene_generation": {
                "provider": video_provider,
                "quality": "high",
                "style": style,
                "scenes_to_generate": [
                    {
                        "scene_number": scene.get("scene_number", i + 1),
                        "duration": scene.get("duration", 10),
                        "video_prompt": scene.get("video_prompt", scene.get("visual_description", "")),
                        "voiceover_text": scene.get("voiceover_text", ""),
                        "mood": scene.get("mood", "neutral"),
                        "camera_style": scene.get("camera_style", "cinematic"),
                        "key_elements": scene.get("key_visual_elements", [])
                    }
                    for i, scene in enumerate(scenes)
                ]
            },

            # Step 2: Audio Generation
            "audio_generation": {
                "voice_id": voice_id,
                "audio_segments": [
                    {
                        "scene_number": scene.get("scene_number", i + 1),
                        "text": scene.get("voiceover_text", ""),
                        "duration": scene.get("duration", 10),
                        "start_time": sum(s.get("duration", 10) for s in scenes[:i]),
                        "mood": scene.get("mood", "neutral")
                    }
                    for i, scene in enumerate(scenes)
                ]
            },

            # Step 3: Transition Generation
            "transitions": [
                {
                    "from_scene": i + 1,
                    "to_scene": i + 2,
                    "transition_type": scenes[i].get("transition_to_next", "fade"),
                    "duration": 0.5
                }
                for i in range(len(scenes) - 1)
            ],

            # Step 4: Final Assembly
            "assembly": {
                "platform_optimization": self._get_platform_settings(platform),
                "final_effects": ["color_grading", "audio_mixing", "stabilization"],
                "output_format": "mp4",
                "quality": "1080p"
            }
        }

        return {
            "video_production_plan": video_production_plan,
            "execution_ready": True,
            "revolutionary_achievement": f"UNPRECEDENTED: Generating {total_duration}s video from {scene_count} AI-generated scenes!",
            "scenes": scenes,
            "platform": platform,
            "video_provider": video_provider,
            "agent_type": self.agent_type,
            "estimated_processing_time": scene_count * 45,  # 45 seconds per scene including stitching
            "workflow_status": "ready_for_worker_execution"
        }

    def _get_platform_settings(self, platform: str) -> Dict[str, Any]:
        """Get platform-specific video settings"""
        platform_settings = {
            "youtube": {
                "aspect_ratio": "16:9",
                "resolution": "1920x1080",
                "max_duration": 300,
                "bitrate": "8000k",
                "fps": 30
            },
            "tiktok": {
                "aspect_ratio": "9:16",
                "resolution": "1080x1920",
                "max_duration": 180,
                "bitrate": "6000k",
                "fps": 30
            },
            "instagram": {
                "aspect_ratio": "1:1",
                "resolution": "1080x1080",
                "max_duration": 90,
                "bitrate": "5000k",
                "fps": 30
            },
            "twitter": {
                "aspect_ratio": "16:9",
                "resolution": "1280x720",
                "max_duration": 140,
                "bitrate": "4000k",
                "fps": 30
            }
        }

        return platform_settings.get(platform, platform_settings["youtube"])

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
