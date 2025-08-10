"""
Business Automation AI Agents
"""
import json
from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentType

class SalesAgent(BaseAgent):
    """AI agent for lead qualification, proposal generation, and contract automation"""
    
    def __init__(self):
        super().__init__(AgentType.SALES)
    
    def get_system_prompt(self) -> str:
        return """You are an expert sales professional and business development specialist. You excel at:

1. **Lead Qualification**: BANT (Budget, Authority, Need, Timeline) analysis
2. **Proposal Generation**: Compelling, customized proposals that close deals
3. **Contract Automation**: Professional contract drafting and negotiation
4. **Sales Pipeline Management**: Opportunity scoring and next-step recommendations
5. **Relationship Building**: Personalized communication strategies

Provide sales solutions that:
- Qualify leads effectively and prioritize high-value opportunities
- Generate persuasive proposals with clear value propositions
- Automate contract processes while maintaining personalization
- Optimize sales funnels for maximum conversion
- Build long-term customer relationships"""
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process sales automation request"""
        self.validate_input(input_data, ["task_type"])
        
        task_type = input_data["task_type"]
        
        if task_type == "lead_qualification":
            return self._qualify_lead(input_data)
        elif task_type == "proposal_generation":
            return self._generate_proposal(input_data)
        elif task_type == "contract_automation":
            return self._automate_contract(input_data)
        else:
            raise ValueError(f"Unsupported task type: {task_type}")
    
    def _qualify_lead(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Qualify a lead using BANT criteria"""
        lead_info = input_data.get("lead_info", {})
        
        user_prompt = f"""
        Qualify this lead using BANT criteria:
        Lead Information: {json.dumps(lead_info, indent=2)}
        
        Provide:
        1. BANT score (Budget, Authority, Need, Timeline) - each 1-10
        2. Overall lead quality score (1-100)
        3. Qualification summary and reasoning
        4. Recommended next steps
        5. Potential deal size estimation
        6. Risk factors and mitigation strategies
        """
        
        messages = self.create_messages(user_prompt)
        response = self.chat_completion(messages, temperature=0.3)
        
        return {
            "qualification_analysis": response,
            "lead_info": lead_info,
            "task_type": "lead_qualification",
            "agent_type": self.agent_type
        }
    
    def _generate_proposal(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a customized sales proposal"""
        client_info = input_data.get("client_info", {})
        service_details = input_data.get("service_details", {})
        
        user_prompt = f"""
        Generate a compelling sales proposal:
        Client Information: {json.dumps(client_info, indent=2)}
        Service Details: {json.dumps(service_details, indent=2)}
        
        Create a professional proposal including:
        1. Executive summary with clear value proposition
        2. Client needs analysis and solution mapping
        3. Detailed service/product description
        4. Pricing structure with ROI justification
        5. Implementation timeline and milestones
        6. Terms and conditions
        7. Next steps and call-to-action
        """
        
        messages = self.create_messages(user_prompt)
        response = self.chat_completion(messages, temperature=0.4, max_tokens=3000)
        
        return {
            "proposal": response,
            "client_info": client_info,
            "service_details": service_details,
            "task_type": "proposal_generation",
            "agent_type": self.agent_type
        }

class CustomerServiceAgent(BaseAgent):
    """AI agent for multi-channel support, ticket routing, and response automation"""
    
    def __init__(self):
        super().__init__(AgentType.CUSTOMER_SERVICE)
    
    def get_system_prompt(self) -> str:
        return """You are an expert customer service professional specializing in:

1. **Multi-Channel Support**: Email, chat, phone, social media consistency
2. **Ticket Routing**: Intelligent categorization and priority assignment
3. **Response Automation**: Personalized, helpful automated responses
4. **Escalation Management**: Knowing when and how to escalate issues
5. **Customer Satisfaction**: Turning problems into positive experiences

Provide customer service solutions that:
- Resolve issues quickly and effectively
- Maintain consistent brand voice across channels
- Automate routine inquiries while preserving personalization
- Identify upselling and retention opportunities
- Build customer loyalty and satisfaction"""
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process customer service request"""
        self.validate_input(input_data, ["task_type"])
        
        task_type = input_data["task_type"]
        
        if task_type == "ticket_routing":
            return self._route_ticket(input_data)
        elif task_type == "response_generation":
            return self._generate_response(input_data)
        elif task_type == "escalation_analysis":
            return self._analyze_escalation(input_data)
        else:
            raise ValueError(f"Unsupported task type: {task_type}")
    
    def _route_ticket(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Route and categorize customer service ticket"""
        ticket_content = input_data.get("ticket_content", "")
        customer_info = input_data.get("customer_info", {})
        
        user_prompt = f"""
        Analyze and route this customer service ticket:
        Ticket Content: {ticket_content}
        Customer Info: {json.dumps(customer_info, indent=2)}
        
        Provide:
        1. Ticket category and subcategory
        2. Priority level (Low, Medium, High, Critical)
        3. Recommended department/agent assignment
        4. Estimated resolution time
        5. Required resources or information
        6. Suggested initial response approach
        """
        
        messages = self.create_messages(user_prompt)
        response = self.chat_completion(messages, temperature=0.2)
        
        return {
            "routing_analysis": response,
            "ticket_content": ticket_content,
            "customer_info": customer_info,
            "task_type": "ticket_routing",
            "agent_type": self.agent_type
        }

class MarketingAgent(BaseAgent):
    """AI agent for campaign creation, audience targeting, and performance optimization"""
    
    def __init__(self):
        super().__init__(AgentType.MARKETING)
    
    def get_system_prompt(self) -> str:
        return """You are an expert marketing strategist and campaign manager specializing in:

1. **Campaign Creation**: Multi-channel marketing campaigns that convert
2. **Audience Targeting**: Precise demographic and psychographic targeting
3. **Performance Optimization**: Data-driven campaign improvement
4. **Content Marketing**: Engaging content that builds brand awareness
5. **ROI Maximization**: Cost-effective marketing with measurable results

Create marketing solutions that:
- Generate qualified leads and drive conversions
- Build brand awareness and customer loyalty
- Optimize marketing spend across channels
- Leverage data for continuous improvement
- Integrate seamlessly with sales processes"""
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process marketing automation request"""
        self.validate_input(input_data, ["task_type"])
        
        task_type = input_data["task_type"]
        
        if task_type == "campaign_creation":
            return self._create_campaign(input_data)
        elif task_type == "audience_targeting":
            return self._target_audience(input_data)
        elif task_type == "performance_optimization":
            return self._optimize_performance(input_data)
        else:
            raise ValueError(f"Unsupported task type: {task_type}")
    
    def _create_campaign(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive marketing campaign"""
        campaign_goals = input_data.get("campaign_goals", [])
        target_audience = input_data.get("target_audience", {})
        budget = input_data.get("budget", 0)
        channels = input_data.get("channels", [])
        
        user_prompt = f"""
        Create a comprehensive marketing campaign:
        Goals: {campaign_goals}
        Target Audience: {json.dumps(target_audience, indent=2)}
        Budget: ${budget}
        Channels: {channels}
        
        Develop:
        1. Campaign strategy and messaging framework
        2. Channel-specific tactics and content plans
        3. Budget allocation across channels
        4. Timeline and milestone schedule
        5. KPI definitions and success metrics
        6. Creative brief and content requirements
        7. Testing and optimization plan
        """
        
        messages = self.create_messages(user_prompt)
        response = self.chat_completion(messages, temperature=0.6, max_tokens=3500)
        
        return {
            "campaign_plan": response,
            "campaign_goals": campaign_goals,
            "target_audience": target_audience,
            "budget": budget,
            "channels": channels,
            "task_type": "campaign_creation",
            "agent_type": self.agent_type
        }

class AnalyticsAgent(BaseAgent):
    """AI agent for cross-platform data analysis, automated insights, and reporting"""
    
    def __init__(self):
        super().__init__(AgentType.ANALYTICS)
    
    def get_system_prompt(self) -> str:
        return """You are an expert data analyst and business intelligence specialist focusing on:

1. **Cross-Platform Analysis**: Unified insights across all business channels
2. **Automated Insights**: AI-driven pattern recognition and trend analysis
3. **Predictive Analytics**: Forecasting and trend prediction
4. **Performance Reporting**: Clear, actionable business reports
5. **Data Visualization**: Compelling charts and dashboards

Provide analytics solutions that:
- Transform raw data into actionable business insights
- Identify trends, patterns, and opportunities
- Predict future performance and outcomes
- Automate reporting and monitoring processes
- Enable data-driven decision making"""
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process analytics request"""
        self.validate_input(input_data, ["task_type", "data_sources"])
        
        task_type = input_data["task_type"]
        data_sources = input_data["data_sources"]
        
        if task_type == "performance_analysis":
            return self._analyze_performance(input_data)
        elif task_type == "trend_prediction":
            return self._predict_trends(input_data)
        elif task_type == "report_generation":
            return self._generate_report(input_data)
        else:
            raise ValueError(f"Unsupported task type: {task_type}")
    
    def _analyze_performance(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze business performance across platforms"""
        data_sources = input_data["data_sources"]
        metrics = input_data.get("metrics", [])
        time_period = input_data.get("time_period", "last_30_days")
        
        user_prompt = f"""
        Analyze business performance:
        Data Sources: {data_sources}
        Key Metrics: {metrics}
        Time Period: {time_period}
        
        Provide:
        1. Performance summary with key findings
        2. Trend analysis and pattern identification
        3. Cross-platform correlation insights
        4. Performance benchmarking
        5. Opportunity identification
        6. Actionable recommendations
        7. Risk factors and mitigation strategies
        """
        
        messages = self.create_messages(user_prompt)
        response = self.chat_completion(messages, temperature=0.3, max_tokens=3000)
        
        return {
            "performance_analysis": response,
            "data_sources": data_sources,
            "metrics": metrics,
            "time_period": time_period,
            "task_type": "performance_analysis",
            "agent_type": self.agent_type
        }
