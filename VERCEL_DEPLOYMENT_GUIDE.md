# 🚀 Vercel FastAPI Deployment Guide

## 📋 Prerequisites
- GitHub account
- Vercel account (free)

## 🎯 Deployment Steps

### 1. Sign Up for Vercel
- Go to [vercel.com](https://vercel.com)
- Sign up with your GitHub account
- Authorize Vercel to access your repositories

### 2. Import Your Repository
- Click "New Project"
- Select "Import Git Repository"
- Choose your `diabetes hospital readmission` repository
- Click "Import"

### 3. Configure Deployment Settings
- **Framework Preset:** Other
- **Root Directory:** `./` (leave as default)
- **Build Command:** Leave empty (Vercel will auto-detect)
- **Output Directory:** Leave empty
- **Install Command:** Leave empty
- **Start Command:** Leave empty (Vercel will use vercel.json)

### 4. Environment Variables (Optional)
- Add `PORT=8000` if needed
- Add any other environment variables

### 5. Deploy
- Click "Deploy"
- Wait for deployment to complete (2-3 minutes)

## 🔧 Configuration Files

### vercel.json
- Routes all requests to `notebooks/app_improved.py`
- Sets max function duration to 30 seconds
- Uses Python runtime

### requirements-vercel.txt
- Contains all necessary Python dependencies
- Optimized for Vercel deployment

## 🌐 After Deployment

### Your API URLs:
- **Main API:** `https://your-app-name.vercel.app`
- **Health Check:** `https://your-app-name.vercel.app/health`
- **API Docs:** `https://your-app-name.vercel.app/docs`

### Test Your API:
```bash
curl https://your-app-name.vercel.app/health
```

## ✅ Success Indicators
- ✅ Build completes successfully
- ✅ Health check returns 200 OK
- ✅ API documentation loads
- ✅ Predictions work correctly

## 🆘 Troubleshooting

### If Build Fails:
- Check `requirements-vercel.txt` for missing dependencies
- Verify `vercel.json` configuration
- Check file paths in `app_improved.py`

### If Health Check Fails:
- Verify model files are being loaded
- Check startup logs in Vercel dashboard
- Ensure all dependencies are installed

## 🎉 Benefits of Vercel
- ✅ Always available (no sleep mode)
- ✅ Fast deployment
- ✅ Professional URLs
- ✅ Built-in monitoring
- ✅ Automatic scaling
- ✅ Free tier is generous
