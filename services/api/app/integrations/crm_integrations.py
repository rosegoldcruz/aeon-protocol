"""
CRM Integration Layer - HubSpot, Salesforce, Pipedrive
"""
import os
import requests
import json
from typing import Dict, Any, List, Optional
from enum import Enum
from datetime import datetime
import base64

class CRMProvider(str, Enum):
    HUBSPOT = "hubspot"
    SALESFORCE = "salesforce"
    PIPEDRIVE = "pipedrive"

class HubSpotIntegration:
    """HubSpot CRM integration with full API support"""
    
    def __init__(self):
        self.api_key = os.getenv("HUBSPOT_API_KEY")
        self.base_url = "https://api.hubapi.com"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def create_contact(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new contact in HubSpot"""
        url = f"{self.base_url}/crm/v3/objects/contacts"
        
        payload = {
            "properties": {
                "email": contact_data.get("email"),
                "firstname": contact_data.get("first_name"),
                "lastname": contact_data.get("last_name"),
                "phone": contact_data.get("phone"),
                "company": contact_data.get("company"),
                "jobtitle": contact_data.get("job_title"),
                "website": contact_data.get("website"),
                "lifecyclestage": contact_data.get("lifecycle_stage", "lead")
            }
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return {
            "contact_id": result["id"],
            "hubspot_url": f"https://app.hubspot.com/contacts/{result['id']}",
            "created_at": result["createdAt"],
            "provider": "hubspot"
        }
    
    async def create_deal(self, deal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new deal in HubSpot"""
        url = f"{self.base_url}/crm/v3/objects/deals"
        
        payload = {
            "properties": {
                "dealname": deal_data.get("name"),
                "amount": deal_data.get("amount"),
                "dealstage": deal_data.get("stage", "appointmentscheduled"),
                "pipeline": deal_data.get("pipeline", "default"),
                "closedate": deal_data.get("close_date"),
                "hubspot_owner_id": deal_data.get("owner_id")
            }
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return {
            "deal_id": result["id"],
            "hubspot_url": f"https://app.hubspot.com/deals/{result['id']}",
            "created_at": result["createdAt"],
            "provider": "hubspot"
        }
    
    async def get_contacts(self, limit: int = 100, properties: List[str] = None) -> Dict[str, Any]:
        """Get contacts from HubSpot"""
        url = f"{self.base_url}/crm/v3/objects/contacts"
        
        params = {"limit": limit}
        if properties:
            params["properties"] = ",".join(properties)
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    async def update_contact(self, contact_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update contact in HubSpot"""
        url = f"{self.base_url}/crm/v3/objects/contacts/{contact_id}"
        
        payload = {"properties": updates}
        
        response = requests.patch(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    async def create_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create task/activity in HubSpot"""
        url = f"{self.base_url}/crm/v3/objects/tasks"
        
        payload = {
            "properties": {
                "hs_task_subject": task_data.get("subject"),
                "hs_task_body": task_data.get("body"),
                "hs_task_status": task_data.get("status", "NOT_STARTED"),
                "hs_task_priority": task_data.get("priority", "MEDIUM"),
                "hs_timestamp": task_data.get("due_date")
            }
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()

class SalesforceIntegration:
    """Salesforce CRM integration"""
    
    def __init__(self):
        self.client_id = os.getenv("SALESFORCE_CLIENT_ID")
        self.client_secret = os.getenv("SALESFORCE_CLIENT_SECRET")
        self.username = os.getenv("SALESFORCE_USERNAME")
        self.password = os.getenv("SALESFORCE_PASSWORD")
        self.security_token = os.getenv("SALESFORCE_SECURITY_TOKEN")
        self.base_url = os.getenv("SALESFORCE_INSTANCE_URL", "https://login.salesforce.com")
        self.access_token = None
    
    async def authenticate(self) -> str:
        """Authenticate with Salesforce and get access token"""
        url = f"{self.base_url}/services/oauth2/token"
        
        payload = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": self.username,
            "password": f"{self.password}{self.security_token}"
        }
        
        response = requests.post(url, data=payload)
        response.raise_for_status()
        
        result = response.json()
        self.access_token = result["access_token"]
        self.instance_url = result["instance_url"]
        
        return self.access_token
    
    async def create_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create lead in Salesforce"""
        if not self.access_token:
            await self.authenticate()
        
        url = f"{self.instance_url}/services/data/v58.0/sobjects/Lead"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "FirstName": lead_data.get("first_name"),
            "LastName": lead_data.get("last_name"),
            "Email": lead_data.get("email"),
            "Phone": lead_data.get("phone"),
            "Company": lead_data.get("company"),
            "Title": lead_data.get("job_title"),
            "LeadSource": lead_data.get("source", "Web"),
            "Status": lead_data.get("status", "Open - Not Contacted")
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return {
            "lead_id": result["id"],
            "salesforce_url": f"{self.instance_url}/lightning/r/Lead/{result['id']}/view",
            "success": result["success"],
            "provider": "salesforce"
        }
    
    async def create_opportunity(self, opp_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create opportunity in Salesforce"""
        if not self.access_token:
            await self.authenticate()
        
        url = f"{self.instance_url}/services/data/v58.0/sobjects/Opportunity"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "Name": opp_data.get("name"),
            "Amount": opp_data.get("amount"),
            "StageName": opp_data.get("stage", "Prospecting"),
            "CloseDate": opp_data.get("close_date"),
            "AccountId": opp_data.get("account_id"),
            "LeadSource": opp_data.get("source", "Web")
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return {
            "opportunity_id": result["id"],
            "salesforce_url": f"{self.instance_url}/lightning/r/Opportunity/{result['id']}/view",
            "success": result["success"],
            "provider": "salesforce"
        }

class PipedriveIntegration:
    """Pipedrive CRM integration"""
    
    def __init__(self):
        self.api_token = os.getenv("PIPEDRIVE_API_TOKEN")
        self.company_domain = os.getenv("PIPEDRIVE_COMPANY_DOMAIN")
        self.base_url = f"https://{self.company_domain}.pipedrive.com/api/v1"
    
    async def create_person(self, person_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create person in Pipedrive"""
        url = f"{self.base_url}/persons"
        
        params = {"api_token": self.api_token}
        
        payload = {
            "name": f"{person_data.get('first_name', '')} {person_data.get('last_name', '')}".strip(),
            "email": [{"value": person_data.get("email"), "primary": True}],
            "phone": [{"value": person_data.get("phone"), "primary": True}],
            "org_id": person_data.get("organization_id")
        }
        
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return {
            "person_id": result["data"]["id"],
            "pipedrive_url": f"https://{self.company_domain}.pipedrive.com/person/{result['data']['id']}",
            "success": result["success"],
            "provider": "pipedrive"
        }
    
    async def create_deal(self, deal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create deal in Pipedrive"""
        url = f"{self.base_url}/deals"
        
        params = {"api_token": self.api_token}
        
        payload = {
            "title": deal_data.get("title"),
            "value": deal_data.get("value"),
            "currency": deal_data.get("currency", "USD"),
            "person_id": deal_data.get("person_id"),
            "org_id": deal_data.get("organization_id"),
            "stage_id": deal_data.get("stage_id"),
            "status": deal_data.get("status", "open"),
            "expected_close_date": deal_data.get("expected_close_date")
        }
        
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return {
            "deal_id": result["data"]["id"],
            "pipedrive_url": f"https://{self.company_domain}.pipedrive.com/deal/{result['data']['id']}",
            "success": result["success"],
            "provider": "pipedrive"
        }
    
    async def get_deals(self, status: str = "all_not_deleted") -> Dict[str, Any]:
        """Get deals from Pipedrive"""
        url = f"{self.base_url}/deals"
        
        params = {
            "api_token": self.api_token,
            "status": status
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        return response.json()

# Lead scoring and automation functions
async def score_lead(lead_data: Dict[str, Any]) -> Dict[str, Any]:
    """AI-powered lead scoring"""
    score = 0
    factors = []
    
    # Email domain scoring
    email = lead_data.get("email", "")
    if email:
        domain = email.split("@")[-1]
        if domain in ["gmail.com", "yahoo.com", "hotmail.com"]:
            score += 10
            factors.append("Personal email domain")
        else:
            score += 25
            factors.append("Business email domain")
    
    # Company size scoring
    company = lead_data.get("company", "")
    if company:
        score += 20
        factors.append("Has company information")
    
    # Job title scoring
    job_title = lead_data.get("job_title", "").lower()
    if any(title in job_title for title in ["ceo", "founder", "director", "manager", "vp"]):
        score += 30
        factors.append("Decision maker title")
    elif any(title in job_title for title in ["developer", "engineer", "analyst"]):
        score += 15
        factors.append("Technical role")
    
    # Phone number scoring
    if lead_data.get("phone"):
        score += 15
        factors.append("Phone number provided")
    
    # Website scoring
    if lead_data.get("website"):
        score += 10
        factors.append("Website provided")
    
    # Determine lead grade
    if score >= 80:
        grade = "A"
        priority = "High"
    elif score >= 60:
        grade = "B"
        priority = "Medium"
    elif score >= 40:
        grade = "C"
        priority = "Low"
    else:
        grade = "D"
        priority = "Very Low"
    
    return {
        "score": score,
        "grade": grade,
        "priority": priority,
        "factors": factors,
        "recommendation": f"Lead scored {score}/100 - {priority} priority for follow-up"
    }

async def automated_lead_nurturing(lead_id: str, crm_provider: CRMProvider, nurture_sequence: str) -> Dict[str, Any]:
    """Automated lead nurturing workflow"""
    
    sequences = {
        "welcome": [
            {"delay": 0, "action": "send_email", "template": "welcome_email"},
            {"delay": 3, "action": "send_email", "template": "value_proposition"},
            {"delay": 7, "action": "create_task", "task": "Follow up call"},
            {"delay": 14, "action": "send_email", "template": "case_study"}
        ],
        "demo_request": [
            {"delay": 0, "action": "create_task", "task": "Schedule demo"},
            {"delay": 1, "action": "send_email", "template": "demo_confirmation"},
            {"delay": 7, "action": "send_email", "template": "demo_follow_up"},
            {"delay": 14, "action": "create_task", "task": "Proposal follow-up"}
        ]
    }
    
    sequence = sequences.get(nurture_sequence, sequences["welcome"])
    
    # This would integrate with email automation and task creation
    scheduled_actions = []
    for step in sequence:
        scheduled_actions.append({
            "lead_id": lead_id,
            "action": step["action"],
            "delay_days": step["delay"],
            "template": step.get("template"),
            "task": step.get("task"),
            "status": "scheduled"
        })
    
    return {
        "lead_id": lead_id,
        "sequence": nurture_sequence,
        "scheduled_actions": scheduled_actions,
        "total_steps": len(sequence),
        "provider": crm_provider
    }

class CRMIntegrationFactory:
    """Factory for CRM integrations"""
    
    @staticmethod
    def get_integration(provider: CRMProvider):
        """Get CRM integration instance"""
        if provider == CRMProvider.HUBSPOT:
            return HubSpotIntegration()
        elif provider == CRMProvider.SALESFORCE:
            return SalesforceIntegration()
        elif provider == CRMProvider.PIPEDRIVE:
            return PipedriveIntegration()
        else:
            raise ValueError(f"Unsupported CRM provider: {provider}")
