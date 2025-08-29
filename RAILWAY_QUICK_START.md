# 🚀 Railway Quick Start Guide

## ⚡ Deploy in 5 Minutes

### 1. Push Your Code to GitHub
```bash
git add .
git commit -m "Add Railway deployment files"
git push origin main
```

### 2. Deploy via Railway Dashboard

#### Option A: Manual Deployment (Recommended for first time)
1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Choose "Deploy from Dockerfile"
5. Set Dockerfile Path: `Dockerfile.fastapi`
6. Service Name: `diabetes-api-fastapi`
7. Deploy!

#### Option B: Use Our Script
```bash
./deploy-railway.sh
```

### 3. Deploy Streamlit Dashboard
1. In the same project, click "New Service"
2. Choose "Deploy from GitHub repo"
3. Set Dockerfile Path: `Dockerfile.streamlit`
4. Service Name: `diabetes-dashboard-streamlit`
5. Deploy!

### 4. Access Your Services
- **FastAPI:** `https://diabetes-api-fastapi-production.up.railway.app`
- **Streamlit:** `https://diabetes-dashboard-streamlit-production.up.railway.app`

## 🔧 What Gets Deployed

### FastAPI Service
- ✅ ML Model Endpoints
- ✅ Health Checks
- ✅ API Documentation
- ✅ CORS Support

### Streamlit Dashboard
- ✅ Interactive Dashboard
- ✅ Real-time Predictions
- ✅ Data Visualizations
- ✅ Model Performance Metrics

## 📊 Monitor Deployment
- Check Railway dashboard for build status
- View logs in real-time
- Monitor resource usage
- Set up alerts

## 🎯 Next Steps
1. Test your endpoints
2. Configure custom domains
3. Set up monitoring
4. Scale as needed

---

**Need help?** Check the full [RAILWAY_DEPLOYMENT_GUIDE.md](RAILWAY_DEPLOYMENT_GUIDE.md)
