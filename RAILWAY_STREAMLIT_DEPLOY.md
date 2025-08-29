# 🚀 Railway Streamlit Dashboard Deployment Guide

## 📋 **Prerequisites**
- ✅ FastAPI service already deployed on Railway
- ✅ GitHub repository connected to Railway
- ✅ Railway account active

## 🎯 **Deploy Streamlit Dashboard on Railway**

### **Step 1: Create New Railway Service**
1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click **"New Project"** or use existing project
3. Select **"Deploy from GitHub repo"**
4. Choose your repository: `diabetes-readmission-prediction`

### **Step 2: Configure Streamlit Service**
1. **Service Name:** `diabetes-streamlit-dashboard`
2. **Branch:** `master`
3. **Root Directory:** `/` (root of repo)
4. **Build Command:** Leave empty (uses Dockerfile)
5. **Start Command:** Leave empty (uses Dockerfile)

### **Step 3: Set Environment Variables**
Add these environment variables in Railway:
```
PORT=8501
```

### **Step 4: Deploy**
1. Click **"Deploy"**
2. Wait for build to complete (2-3 minutes)
3. Railway will automatically assign a URL

## 🔧 **Configuration Files Used**

### **`railway-streamlit.json`**
- Points to `Dockerfile.streamlit`
- Sets health check path to `/`
- 5-minute health check timeout

### **`Dockerfile.streamlit`**
- Python 3.11 slim image
- Installs Streamlit dependencies
- Copies dashboard assets and models
- Runs on Railway's assigned port

## 🌐 **Expected URLs After Deployment**

- **Streamlit Dashboard:** `https://your-streamlit-service.up.railway.app/`
- **FastAPI API:** `https://your-fastapi-service.up.railway.app/`

## ✅ **Verification Steps**

1. **Check Build Logs:**
   - Should show successful Streamlit installation
   - No dependency errors

2. **Check Health Status:**
   - Service should show "ACTIVE" status
   - Health checks should pass

3. **Test Dashboard:**
   - Visit the Streamlit URL
   - Dashboard should load with interactive elements

## 🚨 **Troubleshooting**

### **Build Fails:**
- Check Python version compatibility
- Verify requirements-streamlit.txt exists

### **Health Check Fails:**
- Increase healthcheckTimeout in railway.json
- Check Streamlit logs for startup errors

### **Port Issues:**
- Ensure PORT environment variable is set
- Check Dockerfile exposes correct port

## 🎉 **Success Indicators**

- ✅ Service shows "ACTIVE" status
- ✅ Health checks pass
- ✅ Dashboard loads in browser
- ✅ Interactive elements work
- ✅ No error messages in logs

## 🔗 **Final Demo Links**

Once both services are deployed:
- **📊 Streamlit Dashboard:** `https://streamlit-service.up.railway.app/`
- **🔌 FastAPI Endpoint:** `https://fastapi-service.up.railway.app/`
- **📚 API Docs:** `https://fastapi-service.up.railway.app/docs`

**Both services will be live and accessible for your demo!** 🚀
