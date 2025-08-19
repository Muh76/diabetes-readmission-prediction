# 🚀 Azure Container Apps Deployment Guide

## 📋 Overview

This guide covers deploying your Diabetic Readmission ML API to **Azure Container Apps**, providing a fully managed, serverless container platform with automatic scaling and built-in monitoring.

## 🏗️ Azure Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitHub        │    │   Azure         │    │   Azure         │
│   Actions       │◄──►│   Container     │◄──►│   Container     │
│   CI/CD         │    │   Registry      │    │   Apps          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Code Push     │    │   Docker Image  │    │   ML API       │
│   → Trigger     │    │   Storage       │    │   Endpoints    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## ✅ **What We've Already Set Up**

### **Azure Resources Created**
- ✅ **Resource Group**: `Muh_Azure_ML` (eastus2)
- ✅ **Container Registry**: `diabetesmlacr.azurecr.io`
- ✅ **Container Apps Environment**: `diabetes-ml-env`
- ✅ **GitHub Actions Workflow**: `.github/workflows/azure-deploy.yml`
- ✅ **Deployment Script**: `azure-deploy.sh`

### **Current Status**
- 🟢 **ACR**: Ready for image storage
- 🟢 **Container Apps Environment**: Ready for deployment
- 🟡 **Container App**: Needs to be created
- 🟡 **GitHub Secrets**: Need to be configured

---

## 🚀 **Step-by-Step Deployment**

### **Step 1: Configure GitHub Secrets**

You need to add these secrets to your GitHub repository:

1. **Go to your GitHub repo** → **Settings** → **Secrets and variables** → **Actions**
2. **Add the following secrets**:

#### **Azure Container Registry (ACR) Secrets**
```
ACR_USERNAME: diabetesmlacr
ACR_PASSWORD: [Get from Azure CLI: az acr credential show --name diabetesmlacr --query "passwords[0].value" --output tsv]
```

#### **Azure Authentication Secrets**
```
AZURE_CREDENTIALS: [Service Principal JSON - See instructions below]
AZURE_SUBSCRIPTION_ID: 7cae84d4-0b6d-4648-ac82-736fe15afced
```

### **Step 2: Create Azure Service Principal**

Run these commands to create a service principal for GitHub Actions:

```bash
# Create service principal
az ad sp create-for-rbac --name "github-actions-ml-api" \
    --role contributor \
    --scopes /subscriptions/7cae84d4-0b6d-4648-ac82-736fe15afced/resourceGroups/Muh_Azure_ML \
    --sdk-auth

# Copy the entire JSON output and add it as AZURE_CREDENTIALS secret
```

### **Step 3: Deploy via GitHub Actions**

1. **Push your code** to trigger the workflow:
   ```bash
   git add .
   git commit -m "🚀 Ready for Azure deployment"
   git push origin master
   ```

2. **Monitor the deployment** in GitHub Actions:
   - Go to **Actions** tab in your repo
   - Click on **"Deploy ML API to Azure Container Apps"**
   - Watch the deployment progress

### **Step 4: Verify Deployment**

Once deployed, your API will be available at:
- **Main API**: `https://[your-app-name].[env-name].eastus2.azurecontainerapps.io`
- **Health Check**: `/health`
- **API Docs**: `/docs`
- **Models Info**: `/models`

---

## 🛠️ **Alternative: Manual Deployment**

If you prefer to deploy manually, use our deployment script:

### **Prerequisites**
```bash
# Ensure you're logged into Azure
az login

# Set your subscription
az account set --subscription 7cae84d4-0b6d-4648-ac82-736fe15afced
```

### **Deploy**
```bash
# Make script executable
chmod +x azure-deploy.sh

# Deploy to Azure
./azure-deploy.sh deploy

# Check status
./azure-deploy.sh info

# Test API
./azure-deploy.sh test
```

---

## 📊 **Azure Container Apps Features**

### **🚀 Automatic Scaling**
- **Min replicas**: 1 (always available)
- **Max replicas**: 3 (auto-scale based on load)
- **Scale to zero**: Available for cost optimization

### **🔒 Security**
- **Managed identity** support
- **VNet integration** available
- **HTTPS endpoints** with custom domains
- **Private endpoints** for internal access

### **📈 Monitoring**
- **Built-in logging** via Log Analytics
- **Application Insights** integration
- **Custom metrics** and alerts
- **Health checks** and readiness probes

### **💰 Cost Optimization**
- **Consumption plan**: Pay per request
- **Dedicated plan**: Fixed pricing for high-traffic apps
- **Scale to zero**: No cost when not in use

---

## 🔧 **Configuration Options**

### **Environment Variables**
```bash
# Set via Azure CLI
az containerapp update \
  --name diabetes-ml-api \
  --resource-group Muh_Azure_ML \
  --set-env-vars \
    PYTHONPATH=/app \
    PORT=8000 \
    LOG_LEVEL=INFO \
    MODEL_CACHE_TTL=3600
```

### **Resource Limits**
```bash
# CPU and Memory
--cpu 1.0 --memory 2.0Gi

# Scaling
--min-replicas 1 --max-replicas 5

# Concurrency
--max-concurrent-requests 100
```

### **Custom Domains**
```bash
# Add custom domain
az containerapp hostname add \
  --hostname api.yourdomain.com \
  --name diabetes-ml-api \
  --resource-group Muh_Azure_ML
```

---

## 📈 **Monitoring & Logging**

### **View Logs**
```bash
# Real-time logs
az containerapp logs show \
  --name diabetes-ml-api \
  --resource-group Muh_Azure_ML \
  --follow

# Historical logs
az containerapp logs show \
  --name diabetes-ml-api \
  --resource-group Muh_Azure_ML \
  --since 1h
```

### **Application Insights**
```bash
# Enable Application Insights
az monitor app-insights component create \
  --app diabetes-ml-insights \
  --location eastus2 \
  --resource-group Muh_Azure_ML \
  --application-type web
```

### **Custom Metrics**
```bash
# Send custom metrics
az monitor metrics list \
  --resource /subscriptions/7cae84d4-0b6d-4648-ac82-736fe15afced/resourceGroups/Muh_Azure_ML/providers/Microsoft.App/containerApps/diabetes-ml-api \
  --metric ContainerAppHttpServerRequests
```

---

## 🔄 **CI/CD Pipeline**

### **Automatic Deployment**
- **Push to master** → Triggers deployment
- **Pull requests** → Run tests only
- **Manual trigger** → Available via GitHub UI

### **Deployment Stages**
1. **Test** → Python testing and linting
2. **Build** → Docker image creation
3. **Push** → Upload to Azure Container Registry
4. **Deploy** → Deploy to Azure Container Apps
5. **Verify** → Test API endpoints
6. **Security** → Vulnerability scanning

### **Rollback Strategy**
```bash
# List revisions
az containerapp revision list \
  --name diabetes-ml-api \
  --resource-group Muh_Azure_ML

# Rollback to previous revision
az containerapp revision set-mode \
  --name diabetes-ml-api \
  --resource-group Muh_Azure_ML \
  --mode single \
  --revision [revision-name]
```

---

## 🚨 **Troubleshooting**

### **Common Issues**

#### **1. Container App Won't Start**
```bash
# Check logs
az containerapp logs show \
  --name diabetes-ml-api \
  --resource-group Muh_Azure_ML

# Check status
az containerapp show \
  --name diabetes-ml-api \
  --resource-group Muh_Azure_ML \
  --query properties.provisioningState
```

#### **2. Image Pull Issues**
```bash
# Verify ACR credentials
az acr credential show --name diabetesmlacr

# Check image exists
az acr repository list --name diabetesmlacr
```

#### **3. API Not Responding**
```bash
# Check ingress configuration
az containerapp show \
  --name diabetes-ml-api \
  --resource-group Muh_Azure_ML \
  --query properties.configuration.ingress

# Test health endpoint
curl -f "https://[your-app-url]/health"
```

### **Debug Commands**
```bash
# Get detailed app info
az containerapp show \
  --name diabetes-ml-api \
  --resource-group Muh_Azure_ML \
  --output json

# Check environment
az containerapp env show \
  --name diabetes-ml-env \
  --resource-group Muh_Azure_ML
```

---

## 💰 **Cost Estimation**

### **Azure Container Apps Pricing**
- **Consumption Plan**: $0.000024/vCPU-second + $0.0000025/GiB-second
- **Dedicated Plan**: $0.000024/vCPU-second + $0.0000025/GiB-second

### **Estimated Monthly Costs**
- **Low traffic** (1 replica, 8 hours/day): ~$5-10/month
- **Medium traffic** (2 replicas, 24 hours/day): ~$20-30/month
- **High traffic** (3+ replicas, 24 hours/day): ~$40-60/month

### **Cost Optimization Tips**
1. **Use consumption plan** for development/testing
2. **Set appropriate min/max replicas**
3. **Enable scale to zero** for non-critical apps
4. **Monitor usage** with Azure Cost Management

---

## 🎯 **Next Steps After Deployment**

### **1. Test Your API**
```bash
# Health check
curl https://[your-app-url]/health

# Get models info
curl https://[your-app-url]/models

# Make prediction
curl -X POST https://[your-app-url]/predict \
  -H "Content-Type: application/json" \
  -d '{"num_medications": 5, "time_in_hospital": 7, "number_diagnoses": 3, "num_procedures": 1, "num_lab_procedures": 25}'
```

### **2. Set Up Monitoring**
- Configure Application Insights
- Set up alerts for errors
- Monitor performance metrics

### **3. Custom Domain (Optional)**
- Purchase domain name
- Configure DNS
- Add SSL certificate

### **4. Production Hardening**
- Implement authentication
- Add rate limiting
- Set up backup strategies

---

## 📚 **Additional Resources**

### **Azure Documentation**
- [Container Apps Overview](https://docs.microsoft.com/en-us/azure/container-apps/)
- [Container Apps CLI Reference](https://docs.microsoft.com/en-us/cli/azure/containerapp)
- [Container Apps Samples](https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.app/container-apps)

### **GitHub Actions**
- [Azure Login Action](https://github.com/Azure/login)
- [Docker Login Action](https://github.com/Azure/docker-login)
- [Container Apps Action](https://github.com/Azure/container-apps-deploy-action)

### **Support**
- **Azure Support**: Available with your subscription
- **GitHub Issues**: For CI/CD pipeline issues
- **Community**: Stack Overflow, Azure forums

---

## 🏆 **Success Checklist**

- [ ] GitHub secrets configured
- [ ] Service principal created
- [ ] Code pushed to trigger deployment
- [ ] GitHub Actions workflow completed
- [ ] Container App deployed successfully
- [ ] API endpoints responding
- [ ] Health checks passing
- [ ] Monitoring configured
- [ ] Cost monitoring enabled

---

**🚀 Your ML API is now ready for Azure deployment!**

Once you configure the GitHub secrets and push your code, the automated pipeline will handle everything else. You'll have a production-ready, scalable ML API running in Azure Container Apps with full CI/CD automation.
