"""
CRM Integration Connectors for HubSpot, Salesforce, Pipedrive
"""
import os
import requests
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from enum import Enum

class CRMProvider(str, Enum):
    HUBSPOT = "hubspot"
    SALESFORCE = "salesforce"
    PIPEDRIVE = "pipedrive"

class BaseCRMConnector(ABC):
    """Base class for CRM connectors"""
    
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self._setup_auth()
    
    @abstractmethod
    def _setup_auth(self):
        """Setup authentication for the CRM"""
        pass
    
    @abstractmethod
    def create_contact(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new contact"""
        pass
    
    @abstractmethod
    def update_contact(self, contact_id: str, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing contact"""
        pass
    
    @abstractmethod
    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """Get contact by ID"""
        pass
    
    @abstractmethod
    def create_deal(self, deal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new deal/opportunity"""
        pass
    
    @abstractmethod
    def update_deal(self, deal_id: str, deal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing deal"""
        pass

class HubSpotConnector(BaseCRMConnector):
    """HubSpot CRM connector"""
    
    def __init__(self, api_key: str = None):
        api_key = api_key or os.getenv("HUBSPOT_API_KEY")
        super().__init__(api_key, "https://api.hubapi.com")
    
    def _setup_auth(self):
        """Setup HubSpot authentication"""
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
    
    def create_contact(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new HubSpot contact"""
        url = f"{self.base_url}/crm/v3/objects/contacts"
        
        # Transform data to HubSpot format
        hubspot_data = {
            "properties": {
                "email": contact_data.get("email"),
                "firstname": contact_data.get("first_name"),
                "lastname": contact_data.get("last_name"),
                "company": contact_data.get("company"),
                "phone": contact_data.get("phone"),
                "website": contact_data.get("website"),
                "lifecyclestage": contact_data.get("lifecycle_stage", "lead")
            }
        }
        
        response = self.session.post(url, json=hubspot_data)
        response.raise_for_status()
        return response.json()
    
    def update_contact(self, contact_id: str, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update HubSpot contact"""
        url = f"{self.base_url}/crm/v3/objects/contacts/{contact_id}"
        
        hubspot_data = {
            "properties": {
                k: v for k, v in contact_data.items() if v is not None
            }
        }
        
        response = self.session.patch(url, json=hubspot_data)
        response.raise_for_status()
        return response.json()
    
    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """Get HubSpot contact"""
        url = f"{self.base_url}/crm/v3/objects/contacts/{contact_id}"
        
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def create_deal(self, deal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create HubSpot deal"""
        url = f"{self.base_url}/crm/v3/objects/deals"
        
        hubspot_data = {
            "properties": {
                "dealname": deal_data.get("name"),
                "amount": deal_data.get("amount"),
                "dealstage": deal_data.get("stage", "appointmentscheduled"),
                "pipeline": deal_data.get("pipeline", "default"),
                "closedate": deal_data.get("close_date"),
                "hubspot_owner_id": deal_data.get("owner_id")
            }
        }
        
        response = self.session.post(url, json=hubspot_data)
        response.raise_for_status()
        return response.json()
    
    def update_deal(self, deal_id: str, deal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update HubSpot deal"""
        url = f"{self.base_url}/crm/v3/objects/deals/{deal_id}"
        
        hubspot_data = {
            "properties": {
                k: v for k, v in deal_data.items() if v is not None
            }
        }
        
        response = self.session.patch(url, json=hubspot_data)
        response.raise_for_status()
        return response.json()

class SalesforceConnector(BaseCRMConnector):
    """Salesforce CRM connector"""
    
    def __init__(self, username: str = None, password: str = None, security_token: str = None):
        self.username = username or os.getenv("SALESFORCE_USERNAME")
        self.password = password or os.getenv("SALESFORCE_PASSWORD")
        self.security_token = security_token or os.getenv("SALESFORCE_SECURITY_TOKEN")
        self.instance_url = None
        self.access_token = None
        super().__init__("", "https://login.salesforce.com")
        
    def _setup_auth(self):
        """Setup Salesforce authentication"""
        auth_url = f"{self.base_url}/services/oauth2/token"
        
        auth_data = {
            "grant_type": "password",
            "client_id": os.getenv("SALESFORCE_CLIENT_ID"),
            "client_secret": os.getenv("SALESFORCE_CLIENT_SECRET"),
            "username": self.username,
            "password": f"{self.password}{self.security_token}"
        }
        
        response = requests.post(auth_url, data=auth_data)
        response.raise_for_status()
        
        auth_result = response.json()
        self.access_token = auth_result["access_token"]
        self.instance_url = auth_result["instance_url"]
        
        self.session.headers.update({
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        })
    
    def create_contact(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create Salesforce contact"""
        url = f"{self.instance_url}/services/data/v57.0/sobjects/Contact"
        
        sf_data = {
            "Email": contact_data.get("email"),
            "FirstName": contact_data.get("first_name"),
            "LastName": contact_data.get("last_name"),
            "Phone": contact_data.get("phone"),
            "Title": contact_data.get("title"),
            "Department": contact_data.get("department")
        }
        
        response = self.session.post(url, json=sf_data)
        response.raise_for_status()
        return response.json()
    
    def update_contact(self, contact_id: str, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update Salesforce contact"""
        url = f"{self.instance_url}/services/data/v57.0/sobjects/Contact/{contact_id}"
        
        response = self.session.patch(url, json=contact_data)
        response.raise_for_status()
        return {"success": True}
    
    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """Get Salesforce contact"""
        url = f"{self.instance_url}/services/data/v57.0/sobjects/Contact/{contact_id}"
        
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def create_deal(self, deal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create Salesforce opportunity"""
        url = f"{self.instance_url}/services/data/v57.0/sobjects/Opportunity"
        
        sf_data = {
            "Name": deal_data.get("name"),
            "Amount": deal_data.get("amount"),
            "StageName": deal_data.get("stage", "Prospecting"),
            "CloseDate": deal_data.get("close_date"),
            "Probability": deal_data.get("probability", 10)
        }
        
        response = self.session.post(url, json=sf_data)
        response.raise_for_status()
        return response.json()
    
    def update_deal(self, deal_id: str, deal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update Salesforce opportunity"""
        url = f"{self.instance_url}/services/data/v57.0/sobjects/Opportunity/{deal_id}"
        
        response = self.session.patch(url, json=deal_data)
        response.raise_for_status()
        return {"success": True}

class PipedriveConnector(BaseCRMConnector):
    """Pipedrive CRM connector"""
    
    def __init__(self, api_key: str = None, company_domain: str = None):
        api_key = api_key or os.getenv("PIPEDRIVE_API_KEY")
        self.company_domain = company_domain or os.getenv("PIPEDRIVE_COMPANY_DOMAIN")
        super().__init__(api_key, f"https://{self.company_domain}.pipedrive.com/api/v1")
    
    def _setup_auth(self):
        """Setup Pipedrive authentication"""
        # Pipedrive uses API key in URL params
        pass
    
    def _make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make authenticated request to Pipedrive"""
        url = f"{self.base_url}/{endpoint}?api_token={self.api_key}"
        
        if method.upper() == "GET":
            response = self.session.get(url)
        elif method.upper() == "POST":
            response = self.session.post(url, json=data)
        elif method.upper() == "PUT":
            response = self.session.put(url, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    
    def create_contact(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create Pipedrive person"""
        data = {
            "name": f"{contact_data.get('first_name', '')} {contact_data.get('last_name', '')}".strip(),
            "email": contact_data.get("email"),
            "phone": contact_data.get("phone"),
            "org_id": contact_data.get("organization_id")
        }
        
        return self._make_request("POST", "persons", data)
    
    def update_contact(self, contact_id: str, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update Pipedrive person"""
        return self._make_request("PUT", f"persons/{contact_id}", contact_data)
    
    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """Get Pipedrive person"""
        return self._make_request("GET", f"persons/{contact_id}")
    
    def create_deal(self, deal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create Pipedrive deal"""
        data = {
            "title": deal_data.get("name"),
            "value": deal_data.get("amount"),
            "currency": deal_data.get("currency", "USD"),
            "stage_id": deal_data.get("stage_id", 1),
            "person_id": deal_data.get("person_id"),
            "org_id": deal_data.get("organization_id")
        }
        
        return self._make_request("POST", "deals", data)
    
    def update_deal(self, deal_id: str, deal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update Pipedrive deal"""
        return self._make_request("PUT", f"deals/{deal_id}", deal_data)

class CRMConnectorFactory:
    """Factory for CRM connectors"""
    
    @staticmethod
    def get_connector(provider: CRMProvider, **kwargs) -> BaseCRMConnector:
        """Get CRM connector for specified provider"""
        if provider == CRMProvider.HUBSPOT:
            return HubSpotConnector(**kwargs)
        elif provider == CRMProvider.SALESFORCE:
            return SalesforceConnector(**kwargs)
        elif provider == CRMProvider.PIPEDRIVE:
            return PipedriveConnector(**kwargs)
        else:
            raise ValueError(f"Unsupported CRM provider: {provider}")

# Convenience functions
async def sync_contact_to_crm(provider: CRMProvider, contact_data: Dict[str, Any]) -> Dict[str, Any]:
    """Sync contact to specified CRM"""
    connector = CRMConnectorFactory.get_connector(provider)
    return connector.create_contact(contact_data)

async def sync_deal_to_crm(provider: CRMProvider, deal_data: Dict[str, Any]) -> Dict[str, Any]:
    """Sync deal to specified CRM"""
    connector = CRMConnectorFactory.get_connector(provider)
    return connector.create_deal(deal_data)
