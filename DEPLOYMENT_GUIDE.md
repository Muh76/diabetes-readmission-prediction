# 🚀 **Deployment Guide - Get Your Working Hosted Links**

## 🎯 **What You Need for Presentation**

To present your project professionally, you need these **working hosted links**:

1. **🌐 FastAPI App**: `https://your-app.azurewebsites.net`
2. **📊 MLflow Dashboard**: `https://your-mlflow.azurewebsites.net`
3. **📈 Dashboards**: `https://your-dashboards.azurewebsites.net`
4. **🔗 CI/CD Status**: GitHub Actions badges
5. **🐳 Docker Hub**: `https://hub.docker.com/r/yourusername/diabetes-readmission`

## 🚀 **Option 1: Azure Deployment (Recommended)**

### **Prerequisites**
- Azure account with Container Apps enabled
- GitHub repository with secrets configured

### **Step 1: Configure Azure Secrets**
Add these secrets to your GitHub repository (`Settings > Secrets and variables > Actions`):

```bash
# Azure Container Registry
ACR_USERNAME=your-acr-username
ACR_PASSWORD=your-acr-password

# Azure Service Principal
AZURE_CLIENT_ID=your-client-id
AZURE_TENANT_ID=your-tenant-id
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_CLIENT_SECRET=your-client-secret
```

### **Step 2: Deploy**
```bash
# Your workflow is already configured!
# Just push to trigger deployment
git push origin master
```

### **Step 3: Get Your Links**
After deployment, you'll get:
- **FastAPI**: `https://diabetes-ml-api.azurecontainerapps.io`
- **MLflow**: `https://diabetes-mlflow.azurecontainerapps.io`
- **Dashboards**: `https://diabetes-dashboards.azurecontainerapps.io`

## 🚀 **Option 2: Railway (Quick & Free)**

### **Step 1: Go to Railway**
1. Visit [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project"

### **Step 2: Deploy Your App**
1. Select "Deploy from GitHub repo"
2. Choose your repository
3. Railway will auto-detect FastAPI and deploy

### **Step 3: Get Your Link**
- **FastAPI**: `https://your-app-name.railway.app`

## 🚀 **Option 3: Render (Free Tier)**

### **Step 1: Go to Render**
1. Visit [render.com](https://render.com)
2. Sign in with GitHub
3. Click "New +" > "Web Service"

### **Step 2: Deploy**
1. Connect your repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn notebooks.app:app --host 0.0.0.0 --port $PORT`

### **Step 3: Get Your Link**
- **FastAPI**: `https://your-app-name.onrender.com`

## 🚀 **Option 4: Heroku (Free Tier Ended)**

### **Alternative: Use Render or Railway instead**

## 📊 **MLflow Deployment**

### **Option 1: Azure ML**
```bash
# Deploy MLflow to Azure ML
az ml workspace create --name diabetes-mlflow --resource-group your-rg
az ml online-endpoint create --name mlflow-endpoint --workspace diabetes-mlflow
```

### **Option 2: Railway/Render**
Deploy MLflow as a separate service with the same method as FastAPI.

## 📈 **Dashboard Deployment**

### **Option 1: Azure Static Web Apps**
```bash
# Deploy dashboards to Azure Static Web Apps
az staticwebapp create --name diabetes-dashboards --resource-group your-rg
```

### **Option 2: GitHub Pages**
1. Create a `gh-pages` branch
2. Push your dashboard HTML files
3. Enable GitHub Pages in repository settings

## 🔧 **Quick Local Testing**

Before deploying, test locally:

```bash
# Test FastAPI
uvicorn notebooks.app:app --reload --host 0.0.0.0 --port 8000

# Test MLflow
mlflow ui --host 0.0.0.0 --port 5000

# Test Dashboards
python scripts/serve_dashboards.py
```

## 📋 **Deployment Checklist**

- [ ] **Azure credentials configured**
- [ ] **GitHub secrets set**
- [ ] **Docker image builds successfully**
- [ ] **Azure Container Apps deployed**
- [ ] **MLflow accessible**
- [ ] **Dashboards served**
- [ ] **All links working**
- [ ] **CI/CD pipeline green**

## 🚨 **Common Issues & Solutions**

### **Issue: Azure Container Apps not accessible**
**Solution**: Check network rules and CORS settings in your FastAPI app

### **Issue: MLflow not loading**
**Solution**: Ensure MLflow backend is properly configured

### **Issue: Dashboards not rendering**
**Solution**: Check if all HTML files are properly served

## 🎯 **Next Steps**

1. **Choose your deployment option** (Azure recommended)
2. **Configure credentials and secrets**
3. **Deploy using the provided workflows**
4. **Test all endpoints**
5. **Update README with working links**
6. **Present your project!**

## 📞 **Need Help?**

- **Azure Issues**: Check Azure Container Apps logs
- **GitHub Actions**: Check workflow run logs
- **Local Testing**: Use the quick local testing commands above

---

**🚀 Ready to deploy? Choose your option and get those working links!**
