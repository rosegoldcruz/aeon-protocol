# AEON Platform

A comprehensive AI-powered unified business automation platform that serves as the complete "full suite" AI stack for enterprises.

## Architecture

- **Frontend**: Next.js 14 with TypeScript, shadcn/ui components, dark theme
- **Backend**: Python FastAPI with async processing, Redis queues, PostgreSQL
- **Worker**: Celery workers for async AI processing
- **Storage**: AWS S3 with CDN for global asset delivery
- **Infrastructure**: Docker containers for local development

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Environment Setup

1. Copy the environment file:
```bash
cp .env.example .env.local
```

2. Add your API keys to `.env.local`:
```bash
# Required for image generation
REPLICATE_API_TOKEN=your_replicate_token_here

# Optional: Add other service keys as needed
OPENAI_API_KEY=your_openai_key
ELEVENLABS_API_KEY=your_elevenlabs_key
```

### Running the Platform

1. Start all services:
```bash
cd infra
docker-compose -f docker-compose.dev.yml up --build
```

2. Wait for all services to start, then access:
- **Web UI**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### First Use

1. Open http://localhost:3000
2. **Sign up/Sign in** using Clerk authentication
3. Choose your media type (Image, Video, or Audio)
4. Enter a prompt like "A futuristic city at sunset with flying cars"
5. Click "Generate"
6. Watch the job status update in real-time
7. View the generated media when complete

## Services

### Web (Port 3000)
- Next.js 14 frontend with real-time job tracking
- Image generation form and gallery
- Responsive design with dark theme

### API (Port 8000)
- FastAPI backend with async endpoints
- Job management and status tracking
- S3 integration for asset storage
- Database models for multi-tenancy

### Worker
- Celery workers for AI processing
- Replicate integration for image generation
- Automatic S3 upload and asset management

### Infrastructure
- PostgreSQL database
- Redis for job queues
- LocalStack for S3 development

## Development

### Database Migrations

Run migrations when models change:
```bash
cd services/api
alembic upgrade head
```

### Adding New AI Providers

1. Add provider client to `services/worker/worker.py`
2. Create new task functions
3. Update API endpoints in `services/api/app/main.py`
4. Add UI components in `apps/web/`

### Scaling

The platform is designed for horizontal scaling:
- Add more worker containers for processing
- Use external Redis and PostgreSQL for production
- Deploy to Kubernetes with the provided manifests

## API Endpoints

### Media Generation
- `POST /v1/jobs/image-generate` - Create image generation job
- `POST /v1/jobs/video-generate` - Create video generation job
- `POST /v1/jobs/audio-generate` - Create audio generation job
- `GET /v1/jobs/{id}` - Get job status and results
- `GET /v1/jobs` - List jobs with pagination
- `GET /v1/jobs/{id}/assets` - Get job assets with presigned URLs

### AI Agents
- `POST /v1/agents/content/{agent_type}` - Run content creation agents
- `POST /v1/agents/business/{agent_type}` - Run business automation agents

### Health
- `GET /healthz` - Service health check

## Features Implemented

✅ **Core Infrastructure**
- Monorepo with Next.js frontend and FastAPI backend
- Docker Compose for local development
- PostgreSQL with SQLAlchemy models
- Redis with Celery for async processing

✅ **Advanced Media Generation Suite**
- **Image Studio**: Replicate integration with FLUX model
- **Video Production Hub**: Runway, Pika, Luma, Hailuo integration
- **Audio Production Suite**: ElevenLabs TTS with voice cloning
- Real-time job status tracking across all media types
- S3 storage with presigned URLs
- Responsive media gallery (images, videos, audio)

✅ **AI Agent Ecosystem**
- **Content Creation Agents**: Screenwriter, Video Editor, Content Optimizer, SEO Content
- **Business Automation Agents**: Sales, Customer Service, Marketing, Analytics
- OpenAI GPT-4 integration for intelligent processing
- Structured agent responses with job tracking

✅ **Business Integration Layer**
- **CRM Connectors**: HubSpot, Salesforce, Pipedrive integration
- Contact and deal synchronization
- Automated lead scoring and proposal generation
- Multi-provider authentication handling

✅ **Authentication & Security**
- **Clerk Integration**: Production-ready authentication with JWT verification
- **Multi-tenancy**: Complete tenant isolation with automatic user/tenant creation
- **Role-based Access Control**: Admin, Editor, Viewer, Client roles with permission hierarchy
- **JWT Middleware**: Secure API endpoints with Clerk public key verification
- **Audit logging infrastructure**: Complete activity tracking
- **CORS Configuration**: Secure cross-origin requests for Clerk domains

## Roadmap

🚧 **Phase 1 Extensions**
- Clerk authentication integration
- Video generation (Runway, Pika, Luma)
- Audio generation (ElevenLabs)
- Batch processing

🚧 **Phase 2**
- Business automation agents
- CRM integrations
- Workflow builder
- Advanced analytics

🚧 **Phase 3**
- Enterprise features
- Custom model training
- Marketplace for plugins
- Advanced collaboration tools

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with Docker Compose
5. Submit a pull request

## License

Proprietary - AEON Investments Technologies LLC
