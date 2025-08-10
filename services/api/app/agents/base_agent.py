"""
Base AI Agent class for all AEON agents
"""
import os
import openai
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from enum import Enum

class AgentType(str, Enum):
    SCREENWRITER = "screenwriter"
    VIDEO_EDITOR = "video_editor"
    CONTENT_OPTIMIZER = "content_optimizer"
    SEO_CONTENT = "seo_content"
    SALES = "sales"
    CUSTOMER_SERVICE = "customer_service"
    MARKETING = "marketing"
    ANALYTICS = "analytics"

class BaseAgent(ABC):
    """Base class for all AI agents"""
    
    def __init__(self, agent_type: AgentType, model: str = "gpt-4"):
        self.agent_type = agent_type
        self.model = model
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent"""
        pass
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return results"""
        pass
    
    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Get chat completion from OpenAI"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content
    
    def create_messages(self, user_input: str, context: Optional[str] = None) -> List[Dict[str, str]]:
        """Create message list for chat completion"""
        messages = [{"role": "system", "content": self.get_system_prompt()}]
        
        if context:
            messages.append({"role": "user", "content": f"Context: {context}"})
        
        messages.append({"role": "user", "content": user_input})
        return messages
    
    def validate_input(self, input_data: Dict[str, Any], required_fields: List[str]) -> bool:
        """Validate that required fields are present"""
        for field in required_fields:
            if field not in input_data or not input_data[field]:
                raise ValueError(f"Required field '{field}' is missing or empty")
        return True
