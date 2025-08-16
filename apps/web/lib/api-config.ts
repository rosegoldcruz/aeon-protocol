/**
 * AEON Platform API Configuration
 * Centralized configuration for API endpoints and environment-specific settings
 */

// Environment-based API URL configuration
const getApiBaseUrl = (): string => {
  // Check for explicit API URL override (highest priority)
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL;
  }

  // Environment-based defaults
  switch (process.env.NODE_ENV) {
    case 'production':
      // Production: Use domain-based API endpoint
      return 'https://api.aeonprotocol.com';
    case 'development':
      // Development: Use local backend
      return 'http://localhost:8000/api';
    default:
      // Preview/staging: Use domain-based API endpoint
      return 'https://api.aeonprotocol.com';
  }
};

export const API_CONFIG = {
  BASE_URL: getApiBaseUrl(),
  TIMEOUT: 30000, // 30 seconds
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000, // 1 second
} as const;

// API Endpoints
export const API_ENDPOINTS = {
  // Health Check
  HEALTH: '/health',
  
  // Authentication
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    REFRESH: '/auth/refresh',
    LOGOUT: '/auth/logout',
  },

  // AI Agents
  AGENTS: {
    // Content Creation Agents
    SCREENWRITER: '/agents/content/screenwriter',
    VIDEO_EDITOR: '/agents/content/video-editor',
    CONTENT_OPTIMIZER: '/agents/content/content-optimizer',
    SEO_CONTENT: '/agents/content/seo-content',
    
    // Business Automation Agents
    SALES: '/agents/business/sales',
    CUSTOMER_SERVICE: '/agents/business/customer-service',
    MARKETING: '/agents/business/marketing',
    ANALYTICS: '/agents/business/analytics',
    
    // Revolutionary Workflows
    SCRIPT_TO_VIDEO: '/agents/revolutionary/script-to-video',
    MULTI_SCENE_VIDEO: '/agents/content/multi-scene-video',
  },

  // Media Generation
  MEDIA: {
    // Video Generation
    VIDEO_GENERATE: '/media/videos/generate',
    VIDEO_STATUS: '/media/videos/status',
    IMAGE_TO_VIDEO: '/media/videos/image-to-video',
    
    // Image Generation
    IMAGE_GENERATE: '/media/images/generate',
    IMAGE_UPSCALE: '/media/images/upscale',
    IMAGE_EDIT: '/media/images/edit',
    
    // Audio Generation
    AUDIO_GENERATE: '/media/audio/generate',
    VOICE_CLONE: '/media/audio/voice-clone',
  },

  // AI Coder
  AI_CODER: {
    GENERATE: '/ai-coder/generate',
    STATUS: '/ai-coder/status',
    PREVIEW: '/ai-coder/preview',
    DEPLOY: '/ai-coder/deploy',
    DOWNLOAD: '/ai-coder/download',
  },

  // Workflows
  WORKFLOWS: {
    LIST: '/workflows',
    CREATE: '/workflows',
    GET: '/workflows/:id',
    UPDATE: '/workflows/:id',
    DELETE: '/workflows/:id',
    TRIGGER: '/workflows/:id/trigger',
    EXECUTE: '/workflows/orchestration/execute-workflow',
  },

  // Jobs & Status
  JOBS: {
    LIST: '/jobs',
    GET: '/jobs/:id',
    CANCEL: '/jobs/:id/cancel',
    RETRY: '/jobs/:id/retry',
  },
} as const;

// Helper function to build full API URLs
export const buildApiUrl = (endpoint: string, params?: Record<string, string | number>): string => {
  let url = `${API_CONFIG.BASE_URL}${endpoint}`;
  
  // Replace path parameters
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      url = url.replace(`:${key}`, String(value));
    });
  }
  
  return url;
};

// HTTP Client configuration
export const HTTP_CONFIG = {
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  timeout: API_CONFIG.TIMEOUT,
} as const;

// Error handling configuration
export const ERROR_CONFIG = {
  NETWORK_ERROR: 'Network error occurred. Please check your connection.',
  TIMEOUT_ERROR: 'Request timed out. Please try again.',
  SERVER_ERROR: 'Server error occurred. Please try again later.',
  UNAUTHORIZED: 'Authentication required. Please log in.',
  FORBIDDEN: 'Access denied. Insufficient permissions.',
  NOT_FOUND: 'Resource not found.',
  VALIDATION_ERROR: 'Invalid input data. Please check your request.',
} as const;

// Development utilities
export const isDevelopment = process.env.NODE_ENV === 'development';
export const isProduction = process.env.NODE_ENV === 'production';

// API client factory
export const createApiClient = () => {
  const baseURL = API_CONFIG.BASE_URL;
  
  return {
    get: async (endpoint: string, options?: RequestInit) => {
      const response = await fetch(`${baseURL}${endpoint}`, {
        method: 'GET',
        ...HTTP_CONFIG,
        ...options,
      });
      return response;
    },
    
    post: async (endpoint: string, data?: any, options?: RequestInit) => {
      const response = await fetch(`${baseURL}${endpoint}`, {
        method: 'POST',
        ...HTTP_CONFIG,
        body: data ? JSON.stringify(data) : undefined,
        ...options,
      });
      return response;
    },
    
    put: async (endpoint: string, data?: any, options?: RequestInit) => {
      const response = await fetch(`${baseURL}${endpoint}`, {
        method: 'PUT',
        ...HTTP_CONFIG,
        body: data ? JSON.stringify(data) : undefined,
        ...options,
      });
      return response;
    },
    
    delete: async (endpoint: string, options?: RequestInit) => {
      const response = await fetch(`${baseURL}${endpoint}`, {
        method: 'DELETE',
        ...HTTP_CONFIG,
        ...options,
      });
      return response;
    },
  };
};

// Export default API client instance
export const apiClient = createApiClient();

// Logging utility for development
export const logApiCall = (method: string, url: string, data?: any) => {
  if (isDevelopment) {
    console.log(`🌐 API ${method.toUpperCase()}: ${url}`, data ? { data } : '');
  }
};

// Environment validation
export const validateEnvironment = () => {
  const requiredEnvVars = [
    'REPLICATE_API_TOKEN',
  ];
  
  const missing = requiredEnvVars.filter(envVar => !process.env[envVar]);
  
  if (missing.length > 0) {
    console.warn('⚠️ Missing environment variables:', missing);
    if (isProduction) {
      throw new Error(`Missing required environment variables: ${missing.join(', ')}`);
    }
  }
  
  console.log('✅ API Configuration loaded:', {
    baseUrl: API_CONFIG.BASE_URL,
    environment: process.env.NODE_ENV,
    hasReplicateToken: !!process.env.REPLICATE_API_TOKEN,
  });
};

// Initialize validation on import
if (typeof window === 'undefined') {
  // Only run on server side
  validateEnvironment();
}
