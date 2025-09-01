#!/bin/bash

# Comprehensive Diabetes Readmission Dashboard Deployment Script
# This script deploys the professional portfolio dashboard to Railway

echo "🚀 Deploying Comprehensive Diabetes Readmission Dashboard..."

# Check if we're in the right directory
if [ ! -f "streamlit_app_comprehensive.py" ]; then
    echo "❌ Error: streamlit_app_comprehensive.py not found in current directory"
    exit 1
fi

# Create requirements file for the comprehensive dashboard
echo "📦 Creating requirements file..."
cat > requirements-comprehensive.txt << EOF
streamlit>=1.28.0
pandas>=1.5.0
plotly>=5.15.0
numpy>=1.24.0
scikit-learn>=1.3.0
xgboost>=1.7.0
shap>=0.42.0
lime>=0.2.0
EOF

# Create Railway configuration
echo "🚂 Creating Railway configuration..."
cat > railway-comprehensive.json << EOF
{
  "build": {
    "builder": "nixpacks"
  },
  "deploy": {
    "startCommand": "streamlit run streamlit_app_comprehensive.py --server.port \$PORT --server.address 0.0.0.0",
    "healthcheckPath": "/",
    "healthcheckTimeout": 300,
    "restartPolicyType": "on_failure",
    "restartPolicyMaxRetries": 10
  }
}
EOF

# Create Dockerfile for comprehensive dashboard
echo "🐳 Creating Dockerfile..."
cat > Dockerfile.comprehensive << EOF
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    curl \\
    software-properties-common \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements-comprehensive.txt .
RUN pip install -r requirements-comprehensive.txt

# Copy application files
COPY streamlit_app_comprehensive.py .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
ENTRYPOINT ["streamlit", "run", "streamlit_app_comprehensive.py", "--server.port=8501", "--server.address=0.0.0.0"]
EOF

echo "✅ Configuration files created successfully!"

# Instructions for deployment
echo ""
echo "📋 DEPLOYMENT INSTRUCTIONS:"
echo ""
echo "1. 🚂 Railway Deployment (Recommended):"
echo "   - Go to https://railway.app"
echo "   - Sign in with GitHub"
echo "   - Click 'New Project' → 'Deploy from GitHub repo'"
echo "   - Select your repository"
echo "   - Railway will auto-detect and deploy"
echo ""
echo "2. 🐳 Docker Deployment:"
echo "   - Build: docker build -f Dockerfile.comprehensive -t diabetes-dashboard ."
echo "   - Run: docker run -p 8501:8501 diabetes-dashboard"
echo ""
echo "3. ☁️ Render Deployment:"
echo "   - Go to https://render.com"
echo "   - Create new Web Service"
echo "   - Connect your GitHub repository"
echo "   - Build Command: pip install -r requirements-comprehensive.txt"
echo "   - Start Command: streamlit run streamlit_app_comprehensive.py --server.port \$PORT --server.address 0.0.0.0"
echo ""
echo "4. 🔧 Local Testing:"
echo "   - Install: pip install -r requirements-comprehensive.txt"
echo "   - Run: streamlit run streamlit_app_comprehensive.py"
echo ""

# Check if Railway CLI is installed
if command -v railway &> /dev/null; then
    echo "🚂 Railway CLI detected! You can deploy directly:"
    echo "   railway login"
    echo "   railway init"
    echo "   railway up"
else
    echo "💡 Install Railway CLI for easier deployment:"
    echo "   npm install -g @railway/cli"
fi

echo ""
echo "🎯 Your comprehensive dashboard will include:"
echo "   ✅ Executive Summary with project overview"
echo "   ✅ Model Performance Analysis with comparisons"
echo "   ✅ Feature Analysis & SHAP interpretability"
echo "   ✅ LIME Local Interpretability"
echo "   ✅ Business Impact & ROI Analysis"
echo "   ✅ Technical Architecture details"
echo "   ✅ EDA Insights and visualizations"
echo "   ✅ Deployment & MLOps information"
echo ""
echo "🌟 Perfect for recruiters and stakeholders!"
echo ""
