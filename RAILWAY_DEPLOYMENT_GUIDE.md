# Railway Deployment Guide for Diabetes Readmission Prediction

This guide will help you deploy both the FastAPI endpoint and Streamlit dashboard on Railway.

## 🚀 Quick Start

### 1. Prerequisites
- ✅ Railway account created
- ✅ GitHub repository connected to Railway
- ✅ Your code pushed to GitHub

### 2. Deploy FastAPI Service

1. **Create New Service in Railway:**
   - Go to [Railway Dashboard](https://railway.app/dashboard)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Choose "Deploy from Dockerfile"

2. **Configure FastAPI Service:**
   - Service Name: `diabetes-api-fastapi`
   - Root Directory: `/` (root of repository)
   - Dockerfile Path: `Dockerfile.fastapi`
   - Port: `8000`

3. **Environment Variables:**
   ```
   PORT=8000
   PYTHONPATH=/app
   ```

4. **Deploy:**
   - Railway will automatically build and deploy
   - Wait for build completion
   - Note the generated URL (e.g., `https://diabetes-api-fastapi-production.up.railway.app`)

### 3. Deploy Streamlit Dashboard

1. **Create Second Service:**
   - In the same project, click "New Service" → "Deploy from GitHub repo"
   - Select the same repository
   - Choose "Deploy from Dockerfile"

2. **Configure Streamlit Service:**
   - Service Name: `diabetes-dashboard-streamlit`
   - Root Directory: `/` (root of repository)
   - Dockerfile Path: `Dockerfile.streamlit`
   - Port: `8501`

3. **Environment Variables:**
   ```
   PORT=8501
   PYTHONPATH=/app
   ```

4. **Deploy:**
   - Railway will build and deploy the Streamlit service
   - Note the generated URL (e.g., `https://diabetes-dashboard-streamlit-production.up.railway.app`)

## 📁 File Structure

```
your-repo/
├── Dockerfile.fastapi          # FastAPI service Dockerfile
├── Dockerfile.streamlit        # Streamlit service Dockerfile
├── railway-fastapi.json        # FastAPI Railway config
├── railway-streamlit.json      # Streamlit Railway config
├── requirements-railway.txt    # FastAPI dependencies
├── requirements-streamlit.txt  # Streamlit dependencies
├── notebooks/app.py            # FastAPI application
├── streamlit_app.py            # Streamlit dashboard
├── models/                     # ML models
├── assets/                     # Dashboard assets
└── feature_*.pkl              # Feature files
```

## 🔧 Configuration Files

### FastAPI Service (railway-fastapi.json)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile.fastapi"
  },
  "deploy": {
    "startCommand": "uvicorn app:app --host 0.0.0.0 --port $PORT --workers 1",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Streamlit Service (railway-streamlit.json)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile.streamlit"
  },
  "deploy": {
    "startCommand": "streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true",
    "healthcheckPath": "/",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

## 🌐 Access Your Services

### FastAPI Endpoints
- **API Documentation:** `https://your-fastapi-service.up.railway.app/docs`
- **Health Check:** `https://your-fastapi-service.up.railway.app/health`
- **Prediction Endpoint:** `https://your-fastapi-service.up.railway.app/predict`

### Streamlit Dashboard
- **Dashboard:** `https://your-streamlit-service.up.railway.app/`
- **Direct Access:** Use the Railway-generated URL

## 🔍 Monitoring & Debugging

### Railway Dashboard
- **Logs:** View real-time logs in Railway dashboard
- **Metrics:** Monitor CPU, memory, and network usage
- **Deployments:** Track deployment history and rollbacks

### Health Checks
- FastAPI: `/health` endpoint
- Streamlit: Root path `/` for availability

### Common Issues & Solutions

1. **Build Failures:**
   - Check Dockerfile syntax
   - Verify file paths in Dockerfile
   - Ensure all required files exist

2. **Runtime Errors:**
   - Check Railway logs
   - Verify environment variables
   - Check port configurations

3. **Model Loading Issues:**
   - Ensure model files are copied correctly
   - Check file permissions
   - Verify model file integrity

## 🚀 Advanced Configuration

### Custom Domains
1. Go to Railway service settings
2. Click "Custom Domains"
3. Add your domain and configure DNS

### Environment Variables
- Add production-specific variables in Railway dashboard
- Use Railway's secret management for sensitive data

### Scaling
- Railway automatically scales based on traffic
- Configure manual scaling in service settings if needed

## 📊 Performance Optimization

### FastAPI
- Uses Uvicorn with 1 worker (suitable for Railway)
- Health checks every 30 seconds
- Automatic restart on failure

### Streamlit
- Headless mode for production
- Optimized for Railway's environment
- Efficient resource usage

## 🔒 Security Considerations

- Non-root user in containers
- Health check endpoints
- CORS configuration in FastAPI
- Environment variable protection

## 📞 Support

- **Railway Documentation:** [docs.railway.app](https://docs.railway.app)
- **Railway Discord:** [discord.gg/railway](https://discord.gg/railway)
- **GitHub Issues:** Use your repository's issue tracker

## 🎯 Next Steps

1. Deploy both services following this guide
2. Test endpoints and dashboard functionality
3. Configure custom domains if needed
4. Set up monitoring and alerts
5. Optimize performance based on usage

---

**Happy Deploying! 🚀**
