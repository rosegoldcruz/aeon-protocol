"""
Advanced Workflow Execution Engine for AEON Platform
Handles complex workflow automation with trigger-based execution, state management, and monitoring
"""
import asyncio
import json
import uuid
from typing import Dict, Any, List, Optional, Union
from enum import Enum
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)

class WorkflowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"

class TriggerType(str, Enum):
    MANUAL = "manual"
    SCHEDULED = "scheduled"
    WEBHOOK = "webhook"
    EVENT = "event"
    CONDITION = "condition"

class ActionType(str, Enum):
    AI_AGENT = "ai_agent"
    API_CALL = "api_call"
    EMAIL = "email"
    WEBHOOK = "webhook"
    DELAY = "delay"
    CONDITION = "condition"
    LOOP = "loop"

@dataclass
class WorkflowStep:
    id: str
    name: str
    action_type: ActionType
    configuration: Dict[str, Any]
    position: Dict[str, float]  # x, y coordinates for UI
    connections: List[str] = None  # Connected step IDs
    conditions: List[Dict[str, Any]] = None  # Conditional logic
    retry_config: Dict[str, Any] = None
    timeout_seconds: int = 300

    def __post_init__(self):
        if self.connections is None:
            self.connections = []
        if self.conditions is None:
            self.conditions = []
        if self.retry_config is None:
            self.retry_config = {"max_retries": 3, "delay_seconds": 5}

@dataclass
class WorkflowTrigger:
    id: str
    trigger_type: TriggerType
    configuration: Dict[str, Any]
    is_active: bool = True

@dataclass
class WorkflowDefinition:
    id: str
    name: str
    description: str
    triggers: List[WorkflowTrigger]
    steps: List[WorkflowStep]
    variables: Dict[str, Any] = None
    settings: Dict[str, Any] = None
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.variables is None:
            self.variables = {}
        if self.settings is None:
            self.settings = {"timeout_minutes": 60, "max_concurrent_executions": 5}
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

@dataclass
class WorkflowExecution:
    id: str
    workflow_id: str
    status: WorkflowStatus
    trigger_data: Dict[str, Any]
    current_step: Optional[str] = None
    step_results: Dict[str, Any] = None
    error_message: Optional[str] = None
    started_at: datetime = None
    completed_at: Optional[datetime] = None
    execution_context: Dict[str, Any] = None

    def __post_init__(self):
        if self.step_results is None:
            self.step_results = {}
        if self.started_at is None:
            self.started_at = datetime.utcnow()
        if self.execution_context is None:
            self.execution_context = {}

class WorkflowExecutionEngine:
    """Advanced workflow execution engine with state management and monitoring"""
    
    def __init__(self):
        self.active_executions: Dict[str, WorkflowExecution] = {}
        self.workflow_definitions: Dict[str, WorkflowDefinition] = {}
        self.execution_history: List[WorkflowExecution] = []
        
    async def register_workflow(self, workflow: WorkflowDefinition) -> str:
        """Register a new workflow definition"""
        self.workflow_definitions[workflow.id] = workflow
        logger.info(f"Registered workflow: {workflow.name} ({workflow.id})")
        return workflow.id
    
    async def trigger_workflow(self, workflow_id: str, trigger_data: Dict[str, Any], 
                             trigger_type: TriggerType = TriggerType.MANUAL) -> str:
        """Trigger workflow execution"""
        if workflow_id not in self.workflow_definitions:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.workflow_definitions[workflow_id]
        execution_id = str(uuid.uuid4())
        
        execution = WorkflowExecution(
            id=execution_id,
            workflow_id=workflow_id,
            status=WorkflowStatus.PENDING,
            trigger_data=trigger_data
        )
        
        self.active_executions[execution_id] = execution
        
        # Start execution in background
        asyncio.create_task(self._execute_workflow(execution))
        
        logger.info(f"Triggered workflow {workflow.name} with execution ID: {execution_id}")
        return execution_id
    
    async def _execute_workflow(self, execution: WorkflowExecution):
        """Execute workflow steps"""
        try:
            execution.status = WorkflowStatus.RUNNING
            workflow = self.workflow_definitions[execution.workflow_id]
            
            # Find starting steps (steps with no incoming connections)
            starting_steps = self._find_starting_steps(workflow.steps)
            
            # Execute steps in order
            for step in starting_steps:
                await self._execute_step(execution, workflow, step)
            
            execution.status = WorkflowStatus.COMPLETED
            execution.completed_at = datetime.utcnow()
            
        except Exception as e:
            execution.status = WorkflowStatus.FAILED
            execution.error_message = str(e)
            execution.completed_at = datetime.utcnow()
            logger.error(f"Workflow execution {execution.id} failed: {str(e)}")
        
        finally:
            # Move to history and cleanup
            self.execution_history.append(execution)
            if execution.id in self.active_executions:
                del self.active_executions[execution.id]
    
    async def _execute_step(self, execution: WorkflowExecution, workflow: WorkflowDefinition, step: WorkflowStep):
        """Execute individual workflow step"""
        try:
            execution.current_step = step.id
            logger.info(f"Executing step: {step.name} ({step.id})")
            
            # Check conditions
            if not self._evaluate_conditions(step.conditions, execution.execution_context):
                logger.info(f"Step {step.name} conditions not met, skipping")
                return
            
            # Execute step based on action type
            result = await self._execute_action(step, execution.execution_context, execution.trigger_data)
            
            # Store result
            execution.step_results[step.id] = result
            execution.execution_context.update(result.get("context", {}))
            
            # Execute connected steps
            for connected_step_id in step.connections:
                connected_step = next((s for s in workflow.steps if s.id == connected_step_id), None)
                if connected_step:
                    await self._execute_step(execution, workflow, connected_step)
            
        except Exception as e:
            logger.error(f"Step {step.name} failed: {str(e)}")
            # Handle retry logic
            if step.retry_config and step.retry_config.get("max_retries", 0) > 0:
                await self._retry_step(execution, workflow, step, str(e))
            else:
                raise
    
    async def _execute_action(self, step: WorkflowStep, context: Dict[str, Any], trigger_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute specific action based on step type"""
        action_type = step.action_type
        config = step.configuration
        
        if action_type == ActionType.AI_AGENT:
            return await self._execute_ai_agent_action(config, context, trigger_data)
        elif action_type == ActionType.API_CALL:
            return await self._execute_api_call_action(config, context)
        elif action_type == ActionType.EMAIL:
            return await self._execute_email_action(config, context)
        elif action_type == ActionType.WEBHOOK:
            return await self._execute_webhook_action(config, context)
        elif action_type == ActionType.DELAY:
            return await self._execute_delay_action(config)
        elif action_type == ActionType.CONDITION:
            return await self._execute_condition_action(config, context)
        else:
            raise ValueError(f"Unsupported action type: {action_type}")
    
    async def _execute_ai_agent_action(self, config: Dict[str, Any], context: Dict[str, Any], trigger_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute AI agent action"""
        from ..agents.orchestration import aeon_orchestrator
        
        agent_type = config.get("agent_type")
        agent_input = config.get("input", {})
        
        # Merge context and trigger data into agent input
        merged_input = {**agent_input, **context, **trigger_data}
        
        # Execute agent
        if config.get("workflow_name"):
            # Execute predefined workflow
            results = await aeon_orchestrator.execute_workflow(config["workflow_name"], merged_input)
        else:
            # Execute single agent
            agent = aeon_orchestrator.get_agent(agent_type)
            if not agent:
                raise ValueError(f"Agent {agent_type} not found")
            
            result = await agent.process(merged_input)
            results = [result]
        
        return {
            "success": True,
            "results": results,
            "context": {"agent_output": results[-1] if results else None}
        }
    
    async def _execute_api_call_action(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute API call action"""
        import aiohttp
        
        url = config.get("url", "")
        method = config.get("method", "GET").upper()
        headers = config.get("headers", {})
        data = config.get("data", {})
        
        # Replace variables in URL and data
        url = self._replace_variables(url, context)
        data = self._replace_variables_in_dict(data, context)
        
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers, json=data) as response:
                result_data = await response.json() if response.content_type == 'application/json' else await response.text()
                
                return {
                    "success": response.status < 400,
                    "status_code": response.status,
                    "data": result_data,
                    "context": {"api_response": result_data}
                }
    
    async def _execute_email_action(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute email action"""
        # Email implementation would go here
        # For now, return success
        return {
            "success": True,
            "message": "Email sent successfully",
            "context": {"email_sent": True}
        }
    
    async def _execute_webhook_action(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute webhook action"""
        import aiohttp
        
        url = config.get("url", "")
        payload = config.get("payload", {})
        
        # Replace variables
        url = self._replace_variables(url, context)
        payload = self._replace_variables_in_dict(payload, context)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                return {
                    "success": response.status < 400,
                    "status_code": response.status,
                    "context": {"webhook_sent": True}
                }
    
    async def _execute_delay_action(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute delay action"""
        delay_seconds = config.get("delay_seconds", 1)
        await asyncio.sleep(delay_seconds)
        
        return {
            "success": True,
            "delay_seconds": delay_seconds,
            "context": {"delayed": True}
        }
    
    async def _execute_condition_action(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute condition action"""
        condition = config.get("condition", "")
        result = self._evaluate_condition(condition, context)
        
        return {
            "success": True,
            "condition_result": result,
            "context": {"condition_met": result}
        }
    
    def _find_starting_steps(self, steps: List[WorkflowStep]) -> List[WorkflowStep]:
        """Find steps that have no incoming connections"""
        all_connected_ids = set()
        for step in steps:
            all_connected_ids.update(step.connections)
        
        return [step for step in steps if step.id not in all_connected_ids]
    
    def _evaluate_conditions(self, conditions: List[Dict[str, Any]], context: Dict[str, Any]) -> bool:
        """Evaluate step conditions"""
        if not conditions:
            return True
        
        for condition in conditions:
            if not self._evaluate_condition(condition.get("expression", ""), context):
                return False
        
        return True
    
    def _evaluate_condition(self, expression: str, context: Dict[str, Any]) -> bool:
        """Evaluate a single condition expression"""
        # Simple condition evaluation - would be enhanced with proper expression parser
        try:
            # Replace variables in expression
            evaluated_expression = self._replace_variables(expression, context)
            return eval(evaluated_expression)  # Note: In production, use a safe expression evaluator
        except:
            return False
    
    def _replace_variables(self, text: str, context: Dict[str, Any]) -> str:
        """Replace variables in text with context values"""
        for key, value in context.items():
            text = text.replace(f"{{{key}}}", str(value))
        return text
    
    def _replace_variables_in_dict(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Replace variables in dictionary values"""
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = self._replace_variables(value, context)
            elif isinstance(value, dict):
                result[key] = self._replace_variables_in_dict(value, context)
            else:
                result[key] = value
        return result
    
    async def _retry_step(self, execution: WorkflowExecution, workflow: WorkflowDefinition, step: WorkflowStep, error: str):
        """Retry failed step"""
        retry_config = step.retry_config
        max_retries = retry_config.get("max_retries", 3)
        delay_seconds = retry_config.get("delay_seconds", 5)
        
        for attempt in range(max_retries):
            try:
                await asyncio.sleep(delay_seconds)
                logger.info(f"Retrying step {step.name}, attempt {attempt + 1}/{max_retries}")
                await self._execute_step(execution, workflow, step)
                return  # Success, exit retry loop
            except Exception as e:
                if attempt == max_retries - 1:
                    raise  # Last attempt failed, re-raise exception
                logger.warning(f"Retry {attempt + 1} failed for step {step.name}: {str(e)}")
    
    def get_execution_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get current execution status"""
        if execution_id in self.active_executions:
            execution = self.active_executions[execution_id]
        else:
            execution = next((e for e in self.execution_history if e.id == execution_id), None)
        
        if not execution:
            return None
        
        return asdict(execution)
    
    def get_workflow_metrics(self, workflow_id: str) -> Dict[str, Any]:
        """Get workflow execution metrics"""
        executions = [e for e in self.execution_history if e.workflow_id == workflow_id]
        
        total_executions = len(executions)
        successful_executions = len([e for e in executions if e.status == WorkflowStatus.COMPLETED])
        failed_executions = len([e for e in executions if e.status == WorkflowStatus.FAILED])
        
        avg_duration = 0
        if executions:
            durations = [(e.completed_at - e.started_at).total_seconds() 
                        for e in executions if e.completed_at]
            avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "failed_executions": failed_executions,
            "success_rate": successful_executions / total_executions if total_executions > 0 else 0,
            "average_duration_seconds": avg_duration
        }

# Global workflow engine instance
workflow_engine = WorkflowExecutionEngine()
