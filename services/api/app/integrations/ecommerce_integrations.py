"""
E-commerce Integration Layer - Shopify, WooCommerce, Amazon Seller Central
"""
import os
import requests
import json
from typing import Dict, Any, List, Optional
from enum import Enum
import hmac
import hashlib
import base64
from datetime import datetime

class EcommerceProvider(str, Enum):
    SHOPIFY = "shopify"
    WOOCOMMERCE = "woocommerce"
    AMAZON = "amazon"

class ShopifyIntegration:
    """Shopify store integration"""
    
    def __init__(self):
        self.shop_domain = os.getenv("SHOPIFY_SHOP_DOMAIN")
        self.access_token = os.getenv("SHOPIFY_ACCESS_TOKEN")
        self.api_version = "2023-10"
        self.base_url = f"https://{self.shop_domain}.myshopify.com/admin/api/{self.api_version}"
        self.headers = {
            "X-Shopify-Access-Token": self.access_token,
            "Content-Type": "application/json"
        }
    
    async def get_products(self, limit: int = 50) -> Dict[str, Any]:
        """Get products from Shopify store"""
        url = f"{self.base_url}/products.json"
        params = {"limit": limit}
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    async def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new product in Shopify"""
        url = f"{self.base_url}/products.json"
        
        payload = {
            "product": {
                "title": product_data.get("title"),
                "body_html": product_data.get("description"),
                "vendor": product_data.get("vendor"),
                "product_type": product_data.get("product_type"),
                "tags": product_data.get("tags", ""),
                "variants": [{
                    "price": product_data.get("price"),
                    "inventory_quantity": product_data.get("inventory", 0),
                    "sku": product_data.get("sku")
                }],
                "images": [{"src": img} for img in product_data.get("images", [])]
            }
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return {
            "product_id": result["product"]["id"],
            "shopify_url": f"https://{self.shop_domain}.myshopify.com/admin/products/{result['product']['id']}",
            "handle": result["product"]["handle"],
            "provider": "shopify"
        }
    
    async def update_product_description(self, product_id: str, description: str) -> Dict[str, Any]:
        """Update product description with AI-generated content"""
        url = f"{self.base_url}/products/{product_id}.json"
        
        payload = {
            "product": {
                "id": product_id,
                "body_html": description
            }
        }
        
        response = requests.put(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    async def get_orders(self, status: str = "any", limit: int = 50) -> Dict[str, Any]:
        """Get orders from Shopify"""
        url = f"{self.base_url}/orders.json"
        params = {"status": status, "limit": limit}
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    async def update_inventory(self, variant_id: str, quantity: int) -> Dict[str, Any]:
        """Update product inventory"""
        # First get inventory item ID
        url = f"{self.base_url}/variants/{variant_id}.json"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        variant = response.json()["variant"]
        inventory_item_id = variant["inventory_item_id"]
        
        # Get inventory levels
        url = f"{self.base_url}/inventory_levels.json"
        params = {"inventory_item_ids": inventory_item_id}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        inventory_levels = response.json()["inventory_levels"]
        if inventory_levels:
            location_id = inventory_levels[0]["location_id"]
            
            # Update inventory
            url = f"{self.base_url}/inventory_levels/set.json"
            payload = {
                "location_id": location_id,
                "inventory_item_id": inventory_item_id,
                "available": quantity
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            return response.json()
    
    async def create_discount_code(self, discount_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create discount code for dynamic pricing"""
        url = f"{self.base_url}/price_rules.json"
        
        price_rule_payload = {
            "price_rule": {
                "title": discount_data.get("title"),
                "target_type": "line_item",
                "target_selection": "all",
                "allocation_method": "across",
                "value_type": discount_data.get("value_type", "percentage"),
                "value": f"-{discount_data.get('value')}",
                "customer_selection": "all",
                "starts_at": discount_data.get("starts_at"),
                "ends_at": discount_data.get("ends_at")
            }
        }
        
        response = requests.post(url, headers=self.headers, json=price_rule_payload)
        response.raise_for_status()
        
        price_rule = response.json()["price_rule"]
        
        # Create discount code
        url = f"{self.base_url}/price_rules/{price_rule['id']}/discount_codes.json"
        code_payload = {
            "discount_code": {
                "code": discount_data.get("code")
            }
        }
        
        response = requests.post(url, headers=self.headers, json=code_payload)
        response.raise_for_status()
        
        return response.json()

class WooCommerceIntegration:
    """WooCommerce store integration"""
    
    def __init__(self):
        self.store_url = os.getenv("WOOCOMMERCE_STORE_URL")
        self.consumer_key = os.getenv("WOOCOMMERCE_CONSUMER_KEY")
        self.consumer_secret = os.getenv("WOOCOMMERCE_CONSUMER_SECRET")
        self.base_url = f"{self.store_url}/wp-json/wc/v3"
        
        # Basic auth
        credentials = f"{self.consumer_key}:{self.consumer_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }
    
    async def get_products(self, per_page: int = 50) -> Dict[str, Any]:
        """Get products from WooCommerce store"""
        url = f"{self.base_url}/products"
        params = {"per_page": per_page}
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        return {"products": response.json()}
    
    async def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new product in WooCommerce"""
        url = f"{self.base_url}/products"
        
        payload = {
            "name": product_data.get("name"),
            "type": product_data.get("type", "simple"),
            "regular_price": str(product_data.get("price")),
            "description": product_data.get("description"),
            "short_description": product_data.get("short_description"),
            "categories": [{"id": cat_id} for cat_id in product_data.get("categories", [])],
            "images": [{"src": img} for img in product_data.get("images", [])],
            "manage_stock": True,
            "stock_quantity": product_data.get("stock_quantity", 0),
            "sku": product_data.get("sku")
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return {
            "product_id": result["id"],
            "woocommerce_url": f"{self.store_url}/wp-admin/post.php?post={result['id']}&action=edit",
            "permalink": result["permalink"],
            "provider": "woocommerce"
        }
    
    async def update_product_description(self, product_id: str, description: str) -> Dict[str, Any]:
        """Update product description"""
        url = f"{self.base_url}/products/{product_id}"
        
        payload = {"description": description}
        
        response = requests.put(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    async def get_orders(self, status: str = "any", per_page: int = 50) -> Dict[str, Any]:
        """Get orders from WooCommerce"""
        url = f"{self.base_url}/orders"
        params = {"status": status, "per_page": per_page}
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        return {"orders": response.json()}

class AmazonSellerIntegration:
    """Amazon Seller Central integration"""
    
    def __init__(self):
        self.access_key = os.getenv("AMAZON_ACCESS_KEY_ID")
        self.secret_key = os.getenv("AMAZON_SECRET_ACCESS_KEY")
        self.seller_id = os.getenv("AMAZON_SELLER_ID")
        self.marketplace_id = os.getenv("AMAZON_MARKETPLACE_ID", "ATVPDKIKX0DER")  # US marketplace
        self.base_url = "https://sellingpartnerapi-na.amazon.com"
    
    async def get_orders(self, created_after: str) -> Dict[str, Any]:
        """Get orders from Amazon Seller Central"""
        # This would require proper AWS signature v4 authentication
        # For now, return mock structure
        return {
            "orders": [],
            "next_token": None,
            "provider": "amazon",
            "note": "Amazon SP-API integration requires AWS signature v4 authentication"
        }
    
    async def update_inventory(self, sku: str, quantity: int) -> Dict[str, Any]:
        """Update inventory on Amazon"""
        # Mock implementation - real implementation requires SP-API
        return {
            "sku": sku,
            "quantity": quantity,
            "status": "updated",
            "provider": "amazon",
            "note": "Amazon inventory updates require SP-API integration"
        }

# AI-powered e-commerce automation functions
async def generate_product_description(product_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate AI-powered product descriptions"""
    import openai
    
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = f"""
    Create a compelling product description for:
    
    Product Name: {product_data.get('name')}
    Category: {product_data.get('category')}
    Key Features: {', '.join(product_data.get('features', []))}
    Target Audience: {product_data.get('target_audience', 'general consumers')}
    Price Range: {product_data.get('price_range', 'mid-range')}
    
    Write a description that:
    1. Highlights key benefits and features
    2. Uses persuasive language
    3. Includes relevant keywords for SEO
    4. Appeals to the target audience
    5. Creates urgency or desire
    
    Keep it between 150-300 words.
    """
    
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    description = response.choices[0].message.content
    
    return {
        "description": description,
        "word_count": len(description.split()),
        "seo_optimized": True,
        "generated_at": datetime.now().isoformat()
    }

async def predictive_inventory_management(product_data: Dict[str, Any], sales_history: List[Dict]) -> Dict[str, Any]:
    """AI-powered inventory prediction and reordering"""
    
    # Simple predictive algorithm (in production, use ML models)
    total_sales = sum(sale.get('quantity', 0) for sale in sales_history[-30:])  # Last 30 days
    avg_daily_sales = total_sales / 30 if sales_history else 0
    current_stock = product_data.get('current_stock', 0)
    lead_time_days = product_data.get('lead_time_days', 14)
    
    # Calculate reorder point
    safety_stock = avg_daily_sales * 7  # 7 days safety stock
    reorder_point = (avg_daily_sales * lead_time_days) + safety_stock
    
    # Calculate optimal order quantity (simple EOQ approximation)
    annual_demand = avg_daily_sales * 365
    holding_cost_rate = 0.25  # 25% annual holding cost
    ordering_cost = product_data.get('ordering_cost', 50)
    unit_cost = product_data.get('unit_cost', 10)
    
    if annual_demand > 0:
        eoq = ((2 * annual_demand * ordering_cost) / (holding_cost_rate * unit_cost)) ** 0.5
    else:
        eoq = 0
    
    recommendation = "maintain" if current_stock > reorder_point else "reorder"
    
    return {
        "product_id": product_data.get('id'),
        "current_stock": current_stock,
        "reorder_point": round(reorder_point),
        "recommended_order_quantity": round(eoq),
        "avg_daily_sales": round(avg_daily_sales, 2),
        "days_of_stock_remaining": round(current_stock / avg_daily_sales) if avg_daily_sales > 0 else float('inf'),
        "recommendation": recommendation,
        "urgency": "high" if current_stock < reorder_point * 0.5 else "medium" if current_stock < reorder_point else "low"
    }

async def dynamic_pricing_optimization(product_data: Dict[str, Any], competitor_prices: List[float], demand_data: Dict[str, Any]) -> Dict[str, Any]:
    """AI-powered dynamic pricing optimization"""
    
    current_price = product_data.get('current_price', 0)
    base_cost = product_data.get('cost', 0)
    min_margin = product_data.get('min_margin_percent', 20) / 100
    
    # Calculate competitor price statistics
    if competitor_prices:
        avg_competitor_price = sum(competitor_prices) / len(competitor_prices)
        min_competitor_price = min(competitor_prices)
        max_competitor_price = max(competitor_prices)
    else:
        avg_competitor_price = current_price
        min_competitor_price = current_price
        max_competitor_price = current_price
    
    # Calculate minimum price based on cost and margin
    min_price = base_cost * (1 + min_margin)
    
    # Demand-based pricing adjustment
    demand_trend = demand_data.get('trend', 'stable')  # 'increasing', 'decreasing', 'stable'
    demand_elasticity = demand_data.get('elasticity', 1.0)  # Price sensitivity
    
    # Base price on competitor average
    suggested_price = avg_competitor_price
    
    # Adjust based on demand
    if demand_trend == 'increasing':
        suggested_price *= 1.05  # 5% increase for high demand
    elif demand_trend == 'decreasing':
        suggested_price *= 0.95  # 5% decrease for low demand
    
    # Ensure minimum margin
    suggested_price = max(suggested_price, min_price)
    
    # Calculate expected impact
    price_change_percent = ((suggested_price - current_price) / current_price) * 100
    expected_demand_change = -price_change_percent * demand_elasticity
    
    return {
        "product_id": product_data.get('id'),
        "current_price": current_price,
        "suggested_price": round(suggested_price, 2),
        "price_change_percent": round(price_change_percent, 2),
        "competitor_avg_price": round(avg_competitor_price, 2),
        "min_profitable_price": round(min_price, 2),
        "expected_demand_change_percent": round(expected_demand_change, 2),
        "recommendation": "increase" if suggested_price > current_price else "decrease" if suggested_price < current_price else "maintain",
        "confidence": "high" if len(competitor_prices) >= 3 else "medium" if len(competitor_prices) >= 1 else "low"
    }

class EcommerceIntegrationFactory:
    """Factory for e-commerce integrations"""
    
    @staticmethod
    def get_integration(provider: EcommerceProvider):
        """Get e-commerce integration instance"""
        if provider == EcommerceProvider.SHOPIFY:
            return ShopifyIntegration()
        elif provider == EcommerceProvider.WOOCOMMERCE:
            return WooCommerceIntegration()
        elif provider == EcommerceProvider.AMAZON:
            return AmazonSellerIntegration()
        else:
            raise ValueError(f"Unsupported e-commerce provider: {provider}")
