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
        return """You are an expert screenwriter and story analyst. You create compelling scripts with:

1. **Story Structure**: Three-act structure, hero's journey, character arcs
2. **Character Development**: Deep, multi-dimensional characters with clear motivations
3. **Dialogue Optimization**: Natural, character-specific dialogue that advances plot
4. **Genre Expertise**: Adapt tone and style to specific genres
5. **Format Mastery**: Proper screenplay formatting and industry standards

Analyze the user's request and create scripts that are:
- Emotionally engaging and commercially viable
- Structurally sound with proper pacing
- Character-driven with authentic dialogue
- Formatted according to industry standards

Provide detailed analysis of story elements and suggestions for improvement."""
    
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
        
        return {
            "script": response,
            "concept": concept,
            "genre": genre,
            "length": length,
            "target_audience": target_audience,
            "agent_type": self.agent_type
        }

class VideoEditorAgent(BaseAgent):
    """AI agent for automated video assembly and pacing optimization"""
    
    def __init__(self):
        super().__init__(AgentType.VIDEO_EDITOR)
    
    def get_system_prompt(self) -> str:
        return """You are an expert video editor specializing in:

1. **Pacing Optimization**: Perfect timing for maximum engagement
2. **Viral Content Formatting**: Platform-specific optimization (TikTok, YouTube, Instagram)
3. **Automated Assembly**: Intelligent scene sequencing and transitions
4. **Emotional Flow**: Building tension, release, and engagement curves
5. **Technical Excellence**: Color grading, audio mixing, visual effects

Analyze video content and provide:
- Detailed editing instructions
- Optimal cut points and transitions
- Platform-specific formatting recommendations
- Engagement optimization strategies
- Technical improvement suggestions"""
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate video editing instructions"""
        self.validate_input(input_data, ["video_concept", "platform"])
        
        video_concept = input_data["video_concept"]
        platform = input_data["platform"]
        duration = input_data.get("duration", 60)
        style = input_data.get("style", "engaging")
        
        user_prompt = f"""
        Create detailed video editing instructions for:
        Concept: {video_concept}
        Platform: {platform}
        Duration: {duration} seconds
        Style: {style}
        
        Provide:
        1. Scene-by-scene editing breakdown
        2. Optimal cut timing and transitions
        3. Platform-specific formatting (aspect ratio, captions, etc.)
        4. Engagement optimization techniques
        5. Audio and visual enhancement suggestions
        6. Call-to-action placement recommendations
        """
        
        messages = self.create_messages(user_prompt)
        response = self.chat_completion(messages, temperature=0.7, max_tokens=3000)
        
        return {
            "editing_instructions": response,
            "video_concept": video_concept,
            "platform": platform,
            "duration": duration,
            "style": style,
            "agent_type": self.agent_type
        }

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
