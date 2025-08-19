# 🚀 ML API Deployment Guide

## 📋 Overview

This guide covers the complete deployment of the Diabetic Readmission ML API, including:
- **FastAPI Application** - Production-ready ML API
- **Docker Containerization** - Containerized deployment
- **CI/CD Pipeline** - Automated testing and deployment
- **Monitoring & Logging** - Performance tracking and health checks

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │   Docker        │    │   CI/CD         │
│   (Port 8000)   │◄──►│   Container     │◄──►│   Pipeline      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Monitoring    │    │   Health        │    │   GitHub        │
│   & Metrics     │    │   Checks        │    │   Actions       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### 1. Deploy with Docker (Recommended)

```bash
# Make script executable (if not already)
chmod +x deploy.sh

# Deploy the API
./deploy.sh deploy

# Check status
./deploy.sh status

# View logs
./deploy.sh logs
```

### 2. Manual Docker Deployment

```bash
# Build image
docker build -t diabetic-readmission-api .

# Run container
docker run -d \
  --name diabetic-readmission-api \
  -p 8000:8000 \
  -v $(pwd)/models:/app/models:ro \
  -v $(pwd)/feature_scaler.pkl:/app/feature_scaler.pkl:ro \
  diabetic-readmission-api

# Check status
docker ps
```

### 3. Docker Compose Deployment

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f ml-api

# Stop services
docker-compose down
```

## 📊 API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and status |
| `/health` | GET | Comprehensive health check |
| `/models` | GET | Information about loaded models |
| `/predict` | POST | Single patient prediction |
| `/predict/batch` | POST | Batch patient predictions |

### Health Check Response

```json
{
  "status": "healthy",
  "timestamp": "2025-08-19T18:42:56.143056",
  "uptime_seconds": 4.49,
  "models_loaded": 5,
  "memory_usage_mb": 8338.03,
  "cpu_usage_percent": 16.0,
  "disk_usage_percent": 4.49
}
```

### Prediction Request

```json
{
  "num_medications": 5,
  "time_in_hospital": 7,
  "number_diagnoses": 3,
  "num_procedures": 1,
  "num_lab_procedures": 25
}
```

### Prediction Response

```json
{
  "patient_id": "PAT_1732048976",
  "timestamp": "2025-08-19T18:42:56.143056",
  "readmission_risk": false,
  "probability": 0.23,
  "confidence_level": "Medium",
  "risk_factors": ["Multiple diagnoses"],
  "model_used": "xgboost",
  "processing_time_ms": 45.2,
  "message": "Low risk of readmission"
}
```

## 🐳 Docker Commands

### Container Management

```bash
# Start container
docker start diabetic-readmission-api

# Stop container
docker stop diabetic-readmission-api

# Restart container
docker restart diabetic-readmission-api

# Remove container
docker rm diabetic-readmission-api

# View container logs
docker logs diabetic-readmission-api

# Execute commands in container
docker exec -it diabetic-readmission-api bash
```

### Image Management

```bash
# List images
docker images

# Remove image
docker rmi diabetic-readmission-api

# Build with specific tag
docker build -t diabetic-readmission-api:v1.0 .
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

The CI/CD pipeline automatically:
1. **Tests** the application
2. **Builds** Docker images
3. **Scans** for security vulnerabilities
4. **Deploys** to production

### Manual Trigger

```bash
# Push to trigger pipeline
git push origin master

# Or manually trigger via GitHub UI
# Actions → ML API CI/CD Pipeline → Run workflow
```

### Pipeline Stages

1. **Test** - Python testing and linting
2. **Build** - Docker image creation
3. **Security** - Vulnerability scanning
4. **Deploy** - Production deployment

## 📈 Monitoring & Metrics

### Metrics Collection

The API automatically collects:
- **Prediction metrics** - Success rate, processing time
- **System metrics** - CPU, memory, disk usage
- **Model metrics** - Usage statistics per model

### Accessing Metrics

```bash
# Get summary metrics
curl http://localhost:8000/health

# Export metrics to file
curl http://localhost:8000/metrics/export
```

### Prometheus Integration

```bash
# Start monitoring stack
docker-compose up -d monitoring

# Access Prometheus
open http://localhost:9090
```

## 🛠️ Development

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
cd notebooks
python app.py

# Run with auto-reload
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
cd notebooks
python -m pytest -v

# Run with coverage
python -m pytest --cov=app --cov-report=html
```

### Code Quality

```bash
# Format code
black notebooks/app.py

# Sort imports
isort notebooks/app.py

# Lint code
ruff check notebooks/app.py
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 8000 | API port |
| `LOG_LEVEL` | INFO | Logging level |
| `PYTHONPATH` | /app | Python path |

### Docker Configuration

```yaml
# docker-compose.yml
services:
  ml-api:
    environment:
      - PORT=8000
      - LOG_LEVEL=INFO
    volumes:
      - ./models:/app/models:ro
      - ./logs:/app/logs
```

## 📝 Logging

### Log Files

- **Application logs**: `logs/app.log`
- **Container logs**: `docker logs diabetic-readmission-api`
- **System logs**: Available via `/health` endpoint

### Log Levels

- **INFO** - General application information
- **WARNING** - Non-critical issues
- **ERROR** - Errors and exceptions
- **DEBUG** - Detailed debugging information

## 🚨 Troubleshooting

### Common Issues

#### 1. Port Already in Use

```bash
# Check what's using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
export PORT=8001
```

#### 2. Container Won't Start

```bash
# Check container logs
docker logs diabetic-readmission-api

# Check Docker daemon
docker info

# Restart Docker
sudo systemctl restart docker
```

#### 3. Models Not Loading

```bash
# Check model files exist
ls -la models/

# Check container volumes
docker inspect diabetic-readmission-api

# Verify file permissions
chmod 644 models/*.pkl
```

#### 4. API Not Responding

```bash
# Check container health
docker ps

# Test health endpoint
curl http://localhost:8000/health

# Check container logs
docker logs diabetic-readmission-api
```

### Debug Mode

```bash
# Run with debug logging
export LOG_LEVEL=DEBUG
./deploy.sh deploy

# Or modify docker-compose.yml
environment:
  - LOG_LEVEL=DEBUG
```

## 🔒 Security

### Security Features

- **Non-root user** in container
- **Read-only model files**
- **Input validation** with Pydantic
- **CORS configuration**
- **Rate limiting** (configurable)
- **Security scanning** in CI/CD

### Best Practices

1. **Never expose** model files publicly
2. **Use HTTPS** in production
3. **Implement authentication** for production use
4. **Regular security updates**
5. **Monitor access logs**

## 📚 Additional Resources

### Documentation

- **FastAPI Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Monitoring

- **Prometheus**: http://localhost:9090
- **Health Check**: http://localhost:8000/health
- **Metrics**: http://localhost:8000/metrics

### Support

- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: This README and inline code comments
- **Logs**: Check application and container logs

## 🎯 Next Steps

After successful deployment:

1. **Test all endpoints** thoroughly
2. **Monitor performance** and metrics
3. **Set up alerts** for critical issues
4. **Implement authentication** if needed
5. **Scale horizontally** with load balancer
6. **Set up backup** and recovery procedures

---

**🚀 Your ML API is now production-ready!**

For questions or issues, check the logs and this documentation first, then create a GitHub issue.
