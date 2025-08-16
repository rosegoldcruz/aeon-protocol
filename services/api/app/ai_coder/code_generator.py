"""
AI Coder: Natural Language to Web App Generation System
Revolutionary feature that generates complete web applications from descriptions
"""
import os
import json
import openai
import tempfile
import zipfile
from typing import Dict, Any, List, Optional
from pathlib import Path
from dataclasses import dataclass

@dataclass
class GeneratedApp:
    """Represents a generated web application"""
    app_id: str
    name: str
    description: str
    framework: str
    files: Dict[str, str]  # filename -> content
    preview_url: Optional[str] = None
    deployment_url: Optional[str] = None
    metadata: Dict[str, Any] = None

class AICodeGenerator:
    """Core AI code generation engine"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.supported_frameworks = {
            "react": "React with TypeScript and Tailwind CSS",
            "vue": "Vue.js 3 with TypeScript and Tailwind CSS", 
            "svelte": "SvelteKit with TypeScript and Tailwind CSS",
            "vanilla": "Vanilla HTML, CSS, and JavaScript",
            "next": "Next.js 14 with TypeScript and Tailwind CSS"
        }
    
    async def generate_app(self, description: str, app_type: str = "web", 
                          features: str = "", style: str = "", 
                          framework: str = "react") -> GeneratedApp:
        """Generate a complete web application from natural language description"""
        
        if framework not in self.supported_frameworks:
            framework = "react"  # Default fallback
        
        # Create comprehensive prompt for code generation
        system_prompt = self._get_code_generation_prompt(framework)
        
        user_prompt = f"""
        Generate a complete {framework} web application with the following specifications:
        
        DESCRIPTION: {description}
        APP TYPE: {app_type}
        FEATURES: {features}
        STYLE: {style}
        FRAMEWORK: {framework}
        
        Requirements:
        1. Create a fully functional web application
        2. Include all necessary files (HTML, CSS, JS, config files)
        3. Use modern best practices and responsive design
        4. Include proper error handling and loading states
        5. Add comments explaining key functionality
        6. Ensure the app is production-ready
        
        Structure your response as a JSON object with this exact format:
        {{
            "app_name": "descriptive-app-name",
            "description": "Brief description of the generated app",
            "framework": "{framework}",
            "files": {{
                "filename.ext": "file content here",
                "another-file.ext": "content here"
            }},
            "package_json": {{
                "name": "app-name",
                "dependencies": {{}},
                "scripts": {{}}
            }},
            "setup_instructions": "Step by step setup instructions",
            "features_implemented": ["feature1", "feature2"],
            "deployment_notes": "Deployment instructions"
        }}
        
        CRITICAL: Ensure all code is complete, functional, and follows best practices.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.3,
            max_tokens=4000
        )
        
        # Parse the response
        try:
            app_data = json.loads(response.choices[0].message.content)
            
            # Generate unique app ID
            import uuid
            app_id = str(uuid.uuid4())[:8]
            
            generated_app = GeneratedApp(
                app_id=app_id,
                name=app_data.get("app_name", "generated-app"),
                description=app_data.get("description", description),
                framework=framework,
                files=app_data.get("files", {}),
                metadata={
                    "package_json": app_data.get("package_json", {}),
                    "setup_instructions": app_data.get("setup_instructions", ""),
                    "features_implemented": app_data.get("features_implemented", []),
                    "deployment_notes": app_data.get("deployment_notes", ""),
                    "original_description": description,
                    "generated_at": "2024-01-01T00:00:00Z"  # Would use actual timestamp
                }
            )
            
            return generated_app
            
        except json.JSONDecodeError:
            # Fallback: create a simple app if JSON parsing fails
            return self._create_fallback_app(description, framework)
    
    def _get_code_generation_prompt(self, framework: str) -> str:
        """Get framework-specific system prompt"""
        base_prompt = """You are an elite AI coding specialist and full-stack developer. You transform natural language into complete, production-ready web applications. You excel at:

1. **Advanced Web Architecture**: Modern frameworks, design patterns, scalable structures
2. **Responsive Design Systems**: Mobile-first, accessible, cross-platform interfaces
3. **Code Excellence**: Clean, maintainable, well-documented, type-safe code
4. **Performance Engineering**: Optimized bundles, lazy loading, caching strategies
5. **User Experience**: Intuitive, engaging, professional interfaces
6. **Production Readiness**: Error handling, testing, deployment optimization

CRITICAL: You generate COMPLETE, FUNCTIONAL applications that work immediately after setup.
Return ONLY valid JSON with all necessary files, configurations, and setup instructions."""
        
        framework_specifics = {
            "react": """
            Specialize in React with TypeScript, using:
            - Functional components with hooks
            - Tailwind CSS for styling
            - Modern React patterns (Context, custom hooks)
            - Proper TypeScript types and interfaces
            - Error boundaries and loading states
            """,
            "vue": """
            Specialize in Vue.js 3 with Composition API:
            - TypeScript support
            - Tailwind CSS for styling
            - Pinia for state management
            - Vue Router for navigation
            - Proper component composition
            """,
            "next": """
            Specialize in Next.js 14 with:
            - App Router architecture
            - TypeScript and Tailwind CSS
            - Server and client components
            - API routes and middleware
            - Optimized performance and SEO
            """
        }
        
        return base_prompt + framework_specifics.get(framework, "")
    
    def _create_fallback_app(self, description: str, framework: str) -> GeneratedApp:
        """Create a simple fallback app if main generation fails"""
        import uuid
        app_id = str(uuid.uuid4())[:8]
        
        # Simple HTML app as fallback
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Generated App</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                h1 {{ color: #333; }}
                .description {{ background: #f5f5f5; padding: 15px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Generated Web Application</h1>
                <div class="description">
                    <h3>Description:</h3>
                    <p>{description}</p>
                </div>
                <p>This is a basic web application generated from your description. 
                   The AI Coder is continuously improving to provide more sophisticated applications.</p>
            </div>
        </body>
        </html>
        """
        
        return GeneratedApp(
            app_id=app_id,
            name="fallback-app",
            description=description,
            framework="vanilla",
            files={"index.html": html_content},
            metadata={
                "fallback": True,
                "original_description": description
            }
        )
    
    async def create_preview(self, app: GeneratedApp) -> str:
        """Create a preview URL for the generated app"""
        # This would integrate with a preview service
        # For now, return a placeholder URL
        return f"https://preview.aeon.ai/apps/{app.app_id}"
    
    async def deploy_app(self, app: GeneratedApp, deployment_config: Dict[str, Any]) -> str:
        """Deploy the generated app to a hosting service"""
        # This would integrate with deployment services like Vercel, Netlify, etc.
        # For now, return a placeholder URL
        return f"https://{app.name}-{app.app_id}.aeon-apps.com"
    
    def export_app(self, app: GeneratedApp) -> bytes:
        """Export the app as a downloadable ZIP file"""
        zip_buffer = tempfile.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add all app files
            for filename, content in app.files.items():
                zip_file.writestr(filename, content)
            
            # Add package.json if available
            if app.metadata and "package_json" in app.metadata:
                zip_file.writestr("package.json", json.dumps(app.metadata["package_json"], indent=2))
            
            # Add README
            readme_content = f"""# {app.name}

{app.description}

## Setup Instructions
{app.metadata.get('setup_instructions', 'No specific setup instructions provided.')}

## Features Implemented
{chr(10).join('- ' + feature for feature in app.metadata.get('features_implemented', []))}

## Deployment Notes
{app.metadata.get('deployment_notes', 'Standard deployment process applies.')}

Generated by AEON AI Coder
"""
            zip_file.writestr("README.md", readme_content)
        
        zip_buffer.seek(0)
        return zip_buffer.getvalue()

# Global code generator instance
ai_code_generator = AICodeGenerator()
