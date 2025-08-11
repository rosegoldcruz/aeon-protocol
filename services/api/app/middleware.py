"""
AEON Platform Middleware Components
"""
import time
import logging
from typing import Callable
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Global error handling middleware to catch and format exceptions"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            response = await call_next(request)
            return response
        except HTTPException as e:
            # FastAPI HTTPExceptions should be handled normally
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "error": e.detail,
                    "status_code": e.status_code,
                    "path": str(request.url.path)
                }
            )
        except Exception as e:
            # Log the full error for debugging
            logger.error(f"Unhandled exception in {request.method} {request.url.path}: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            # Return a generic error response
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "status_code": 500,
                    "path": str(request.url.path),
                    "request_id": getattr(request.state, 'request_id', None)
                }
            )

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests and responses"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate request ID
        import uuid
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Log request
        start_time = time.time()
        logger.info(f"[{request_id}] {request.method} {request.url.path} - Started")
        
        try:
            response = await call_next(request)
            
            # Log response
            process_time = time.time() - start_time
            logger.info(
                f"[{request_id}] {request.method} {request.url.path} - "
                f"Completed {response.status_code} in {process_time:.3f}s"
            )
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            
            return response
            
        except Exception as e:
            # Log error
            process_time = time.time() - start_time
            logger.error(
                f"[{request_id}] {request.method} {request.url.path} - "
                f"Failed in {process_time:.3f}s: {str(e)}"
            )
            raise

class RateLimitingMiddleware(BaseHTTPMiddleware):
    """Simple rate limiting middleware"""
    
    def __init__(self, app: ASGIApp, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.clients = {}
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Skip rate limiting for health checks
        if request.url.path in ["/healthz", "/health", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)
        
        current_time = time.time()
        
        # Clean old entries
        self.clients = {
            ip: timestamps for ip, timestamps in self.clients.items()
            if any(t > current_time - self.period for t in timestamps)
        }
        
        # Check rate limit
        if client_ip in self.clients:
            # Filter recent requests
            recent_requests = [
                t for t in self.clients[client_ip] 
                if t > current_time - self.period
            ]
            
            if len(recent_requests) >= self.calls:
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "Rate limit exceeded",
                        "status_code": 429,
                        "retry_after": self.period
                    }
                )
            
            self.clients[client_ip] = recent_requests + [current_time]
        else:
            self.clients[client_ip] = [current_time]
        
        return await call_next(request)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to responses"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        return response
