"""
Base AI Agent class for all AEON agents with orchestration capabilities
"""
import os
import json
import openai
import asyncio
from typing import Dict, Any, List, Optional, Union, Callable
from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass, asdict

class AgentType(str, Enum):
    SCREENWRITER = "screenwriter"
    VIDEO_EDITOR = "video_editor"
    CONTENT_OPTIMIZER = "content_optimizer"
    SEO_CONTENT = "seo_content"
    SALES = "sales"
    CUSTOMER_SERVICE = "customer_service"
    MARKETING = "marketing"
    ANALYTICS = "analytics"

@dataclass
class AgentOutput:
    """Standardized agent output format for chaining"""
    agent_type: str
    success: bool
    data: Dict[str, Any]
    metadata: Dict[str, Any]
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ChainStep:
    """Represents a step in an agent chain"""
    agent_type: AgentType
    input_mapping: Dict[str, str]  # Maps previous output keys to input keys
    parameters: Dict[str, Any] = None
    condition: Optional[str] = None  # Optional condition to execute this step

class BaseAgent(ABC):
    """Base class for all AI agents with chaining capabilities"""

    def __init__(self, agent_type: AgentType, model: str = "gpt-4"):
        self.agent_type = agent_type
        self.model = model
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.chain_context: Dict[str, Any] = {}

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent"""
        pass

    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return results"""
        pass

    def process_with_output(self, input_data: Dict[str, Any]) -> AgentOutput:
        """Process input and return standardized output for chaining"""
        try:
            result = self.process(input_data)
            return AgentOutput(
                agent_type=self.agent_type.value,
                success=True,
                data=result,
                metadata={
                    "model": self.model,
                    "timestamp": asyncio.get_event_loop().time(),
                    "input_keys": list(input_data.keys())
                }
            )
        except Exception as e:
            return AgentOutput(
                agent_type=self.agent_type.value,
                success=False,
                data={},
                metadata={"error_type": type(e).__name__},
                error=str(e)
            )

    def set_chain_context(self, context: Dict[str, Any]):
        """Set context from previous agents in chain"""
        self.chain_context = context

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

class AgentOrchestrator:
    """Orchestrates multiple agents in a chain or workflow"""

    def __init__(self):
        self.agents: Dict[AgentType, BaseAgent] = {}
        self.execution_history: List[AgentOutput] = []

    def register_agent(self, agent: BaseAgent):
        """Register an agent for orchestration"""
        self.agents[agent.agent_type] = agent

    async def execute_chain(self, chain_steps: List[ChainStep], initial_input: Dict[str, Any]) -> List[AgentOutput]:
        """Execute a chain of agents"""
        self.execution_history = []
        current_data = initial_input

        for step in chain_steps:
            # Check condition if specified
            if step.condition and not self._evaluate_condition(step.condition, current_data):
                continue

            # Get agent
            if step.agent_type not in self.agents:
                raise ValueError(f"Agent {step.agent_type} not registered")

            agent = self.agents[step.agent_type]

            # Map input data
            mapped_input = self._map_input(current_data, step.input_mapping)
            if step.parameters:
                mapped_input.update(step.parameters)

            # Set chain context
            agent.set_chain_context({
                "previous_outputs": self.execution_history,
                "current_step": len(self.execution_history),
                "total_steps": len(chain_steps)
            })

            # Execute agent
            output = agent.process_with_output(mapped_input)
            self.execution_history.append(output)

            if not output.success:
                break

            # Update current data for next step
            current_data.update(output.data)

        return self.execution_history

    def _map_input(self, source_data: Dict[str, Any], mapping: Dict[str, str]) -> Dict[str, Any]:
        """Map source data keys to target keys"""
        mapped = {}
        for target_key, source_key in mapping.items():
            if source_key in source_data:
                mapped[target_key] = source_data[source_key]
        return mapped

    def _evaluate_condition(self, condition: str, data: Dict[str, Any]) -> bool:
        """Evaluate a simple condition (basic implementation)"""
        # Simple condition evaluation - can be enhanced
        try:
            return eval(condition, {"__builtins__": {}}, data)
        except:
            return False
