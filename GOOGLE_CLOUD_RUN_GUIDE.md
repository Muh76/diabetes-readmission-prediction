# 🚀 Google Cloud Run FastAPI Deployment Guide

## 🎯 Why Google Cloud Run?
- ✅ **No file size limits** (unlike Vercel's 300MB)
- ✅ **Always available** (no sleep mode)
- ✅ **Free tier:** 2 million requests/month
- ✅ **Very reliable** - guaranteed deployment
- ✅ **Professional URLs** - `your-app.run.app`

## 📋 Prerequisites
1. **Google Cloud Account** (free $300 credit)
2. **Google Cloud CLI** installed
3. **Docker** (optional, Cloud Run builds automatically)

## 🚀 Quick Deployment Steps

### Step 1: Setup Google Cloud
```bash
# Install Google Cloud CLI
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Login to Google Cloud
gcloud auth login

# Create new project (or use existing)
gcloud projects create diabetes-fastapi-project
gcloud config set project diabetes-fastapi-project

# Enable Cloud Run API
gcloud services enable run.googleapis.com
```

### Step 2: Deploy
```bash
# Make deployment script executable
chmod +x deploy-cloudrun.sh

# Run deployment
./deploy-cloudrun.sh
```

### Step 3: Get Your URLs
After deployment, you'll get:
- **API URL:** `https://diabetes-fastapi-us-central1.a.run.app`
- **API Docs:** `https://diabetes-fastapi-us-central1.a.run.app/docs`
- **Health Check:** `https://diabetes-fastapi-us-central1.a.run.app/health`

## 🔧 Manual Deployment (Alternative)

If you prefer manual deployment:

```bash
# Deploy directly
gcloud run deploy diabetes-fastapi \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10
```

## ✅ Success Indicators
- ✅ Build completes successfully
- ✅ Service shows "Ready" status
- ✅ Health check returns 200 OK
- ✅ API documentation loads
- ✅ Predictions work correctly

## 🎉 Benefits
- **Always available** - no sleep mode
- **Professional URLs** - perfect for presentations
- **Free tier generous** - 2 million requests/month
- **No file size issues** - handles large repositories
- **Fast deployment** - 5-10 minutes
- **Reliable** - Google's infrastructure

## 🆘 Troubleshooting

### If Build Fails:
- Check `Dockerfile.cloudrun` syntax
- Verify all files exist
- Check Google Cloud permissions

### If Service Won't Start:
- Check logs: `gcloud logs read --limit=50`
- Verify port configuration
- Check memory allocation

## 💰 Cost
- **Free tier:** 2 million requests/month
- **After free tier:** Pay per use (very cheap)
- **No monthly fees** - only pay for usage

## 🎯 Perfect for Your Use Case
- ✅ **Presentations** - always available
- ✅ **Recruiters** - professional URLs
- ✅ **Large files** - no size limits
- ✅ **ML models** - handles all dependencies
- ✅ **FastAPI** - native support
