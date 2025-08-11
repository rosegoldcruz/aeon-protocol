"""
Advanced AI Agent Orchestration System for AEON Platform
Enables sophisticated agent chaining and workflow automation
"""
import asyncio
import json
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent, AgentType, AgentOrchestrator, ChainStep, AgentOutput
from .content_agents import ScreenwriterAgent, VideoEditorAgent, ContentOptimizerAgent, SEOContentAgent
from .business_agents import SalesAgent, CustomerServiceAgent, MarketingAgent, AnalyticsAgent

class AEONAgentOrchestrator(AgentOrchestrator):
    """Enhanced orchestrator with AEON-specific workflows"""
    
    def __init__(self):
        super().__init__()
        self._initialize_agents()
        self._register_workflows()
    
    def _initialize_agents(self):
        """Initialize and register all AEON agents"""
        # Content Creation Agents
        self.register_agent(ScreenwriterAgent())
        self.register_agent(VideoEditorAgent())
        self.register_agent(ContentOptimizerAgent())
        self.register_agent(SEOContentAgent())
        
        # Business Automation Agents
        self.register_agent(SalesAgent())
        self.register_agent(CustomerServiceAgent())
        self.register_agent(MarketingAgent())
        self.register_agent(AnalyticsAgent())
    
    def _register_workflows(self):
        """Register predefined workflows"""
        self.workflows = {
            "multi_scene_video_production": self._create_video_production_workflow(),
            "content_marketing_campaign": self._create_marketing_campaign_workflow(),
            "sales_automation_pipeline": self._create_sales_pipeline_workflow(),
            "seo_content_optimization": self._create_seo_optimization_workflow()
        }
    
    def _create_video_production_workflow(self) -> List[ChainStep]:
        """Create the revolutionary multi-scene video production workflow"""
        return [
            ChainStep(
                agent_type=AgentType.SCREENWRITER,
                input_mapping={
                    "concept": "concept",
                    "genre": "genre", 
                    "target_duration": "target_duration",
                    "target_audience": "target_audience",
                    "style": "style"
                }
            ),
            ChainStep(
                agent_type=AgentType.VIDEO_EDITOR,
                input_mapping={
                    "scenes": "scenes",
                    "platform": "platform",
                    "style": "style",
                    "video_provider": "video_provider",
                    "voice_id": "voice_id"
                }
            ),
            ChainStep(
                agent_type=AgentType.CONTENT_OPTIMIZER,
                input_mapping={
                    "content_type": "video",
                    "platform": "platform",
                    "target_metrics": "engagement"
                },
                condition="execution_plan['ready_for_production'] == True"
            )
        ]
    
    def _create_marketing_campaign_workflow(self) -> List[ChainStep]:
        """Create comprehensive marketing campaign workflow"""
        return [
            ChainStep(
                agent_type=AgentType.MARKETING,
                input_mapping={
                    "campaign_goals": "campaign_goals",
                    "target_audience": "target_audience",
                    "budget": "budget",
                    "channels": "channels"
                }
            ),
            ChainStep(
                agent_type=AgentType.SEO_CONTENT,
                input_mapping={
                    "content_type": "blog_post",
                    "keywords": "keywords",
                    "target_audience": "target_audience"
                }
            ),
            ChainStep(
                agent_type=AgentType.ANALYTICS,
                input_mapping={
                    "data_sources": "campaign_data",
                    "metrics": "campaign_metrics",
                    "time_period": "campaign_duration"
                }
            )
        ]
    
    def _create_sales_pipeline_workflow(self) -> List[ChainStep]:
        """Create automated sales pipeline workflow"""
        return [
            ChainStep(
                agent_type=AgentType.SALES,
                input_mapping={
                    "task_type": "lead_qualification",
                    "lead_data": "lead_data"
                }
            ),
            ChainStep(
                agent_type=AgentType.SALES,
                input_mapping={
                    "task_type": "proposal_generation",
                    "client_info": "qualified_lead",
                    "service_details": "service_details"
                },
                condition="qualified_lead['score'] >= 7"
            ),
            ChainStep(
                agent_type=AgentType.CUSTOMER_SERVICE,
                input_mapping={
                    "task_type": "follow_up",
                    "client_info": "client_info",
                    "proposal_status": "proposal_status"
                }
            )
        ]
    
    def _create_seo_optimization_workflow(self) -> List[ChainStep]:
        """Create SEO content optimization workflow"""
        return [
            ChainStep(
                agent_type=AgentType.SEO_CONTENT,
                input_mapping={
                    "content_type": "content_type",
                    "keywords": "keywords",
                    "target_audience": "target_audience"
                }
            ),
            ChainStep(
                agent_type=AgentType.CONTENT_OPTIMIZER,
                input_mapping={
                    "content_type": "content_type",
                    "platform": "search_engines",
                    "target_metrics": "seo_ranking"
                }
            ),
            ChainStep(
                agent_type=AgentType.ANALYTICS,
                input_mapping={
                    "data_sources": "seo_data",
                    "metrics": "ranking_metrics",
                    "content_id": "content_id"
                }
            )
        ]
    
    async def execute_workflow(self, workflow_name: str, input_data: Dict[str, Any]) -> List[AgentOutput]:
        """Execute a predefined workflow"""
        if workflow_name not in self.workflows:
            raise ValueError(f"Unknown workflow: {workflow_name}")
        
        workflow_steps = self.workflows[workflow_name]
        return await self.execute_chain(workflow_steps, input_data)
    
    async def execute_custom_chain(self, agent_types: List[str], input_data: Dict[str, Any], 
                                 input_mappings: Optional[List[Dict[str, str]]] = None) -> List[AgentOutput]:
        """Execute a custom agent chain"""
        if not input_mappings:
            # Default mapping - pass all data to each agent
            input_mappings = [{"*": "*"} for _ in agent_types]
        
        chain_steps = []
        for i, agent_type_str in enumerate(agent_types):
            try:
                agent_type = AgentType(agent_type_str)
                mapping = input_mappings[i] if i < len(input_mappings) else {"*": "*"}
                
                chain_steps.append(ChainStep(
                    agent_type=agent_type,
                    input_mapping=mapping
                ))
            except ValueError:
                raise ValueError(f"Invalid agent type: {agent_type_str}")
        
        return await self.execute_chain(chain_steps, input_data)
    
    def get_available_workflows(self) -> Dict[str, Dict[str, Any]]:
        """Get information about available workflows"""
        return {
            "multi_scene_video_production": {
                "description": "Revolutionary multi-scene video generation and stitching",
                "agents": ["screenwriter", "video_editor", "content_optimizer"],
                "estimated_time": "5-10 minutes",
                "output": "Complete professional video with multiple scenes"
            },
            "content_marketing_campaign": {
                "description": "Complete marketing campaign with content and analytics",
                "agents": ["marketing", "seo_content", "analytics"],
                "estimated_time": "3-5 minutes",
                "output": "Marketing strategy, SEO content, and performance tracking"
            },
            "sales_automation_pipeline": {
                "description": "Automated lead qualification and proposal generation",
                "agents": ["sales", "sales", "customer_service"],
                "estimated_time": "2-3 minutes",
                "output": "Qualified leads, proposals, and follow-up plans"
            },
            "seo_content_optimization": {
                "description": "SEO-optimized content with performance tracking",
                "agents": ["seo_content", "content_optimizer", "analytics"],
                "estimated_time": "2-4 minutes",
                "output": "SEO content, optimization recommendations, and analytics"
            }
        }
    
    def get_agent_capabilities(self) -> Dict[str, Dict[str, Any]]:
        """Get detailed information about each agent's capabilities"""
        return {
            agent_type.value: {
                "description": agent.get_system_prompt()[:200] + "...",
                "available": True,
                "processing_time": "30-60 seconds"
            }
            for agent_type, agent in self.agents.items()
        }

# Global orchestrator instance
aeon_orchestrator = AEONAgentOrchestrator()
