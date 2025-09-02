#!/bin/bash

# Improved FastAPI Deployment Script for Railway
# This script deploys the comprehensive API with all documentation improvements

echo "🚀 Deploying Improved Diabetes Readmission API to Railway..."

# Check if we're in the right directory
if [ ! -f "notebooks/app_improved.py" ]; then
    echo "❌ Error: notebooks/app_improved.py not found in current directory"
    exit 1
fi

# Create requirements file for the improved API
echo "📦 Creating requirements file..."
cat > requirements-improved-api.txt << EOF
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
pandas>=1.5.0
scikit-learn>=1.3.0
xgboost>=1.7.0
lightgbm>=4.0.0
catboost>=1.2.0
joblib>=1.3.0
psutil>=5.9.0
python-multipart>=0.0.6
EOF

# Create Railway configuration for improved API
echo "🚂 Creating Railway configuration..."
cat > railway-improved-api.json << EOF
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd notebooks && python app_improved.py",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF

# Create a simple deployment script
echo "📝 Creating deployment script..."
cat > deploy_railway_improved.py << EOF
#!/usr/bin/env python3
"""
Railway Deployment Script for Improved Diabetes Readmission API
"""

import os
import subprocess
import sys

def main():
    print("🚀 Deploying Improved Diabetes Readmission API to Railway...")

    # Check if Railway CLI is installed
    try:
        subprocess.run(["railway", "--version"], check=True, capture_output=True)
        print("✅ Railway CLI found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Railway CLI not found. Please install it first:")
        print("   npm install -g @railway/cli")
        print("   railway login")
        return 1

    # Deploy to Railway
    try:
        print("📦 Deploying to Railway...")
        subprocess.run(["railway", "deploy"], check=True)
        print("✅ Deployment successful!")

        # Get the deployment URL
        result = subprocess.run(["railway", "status"], check=True, capture_output=True, text=True)
        print("📊 Deployment Status:")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
EOF

# Make the deployment script executable
chmod +x deploy_railway_improved.py

echo "✅ Setup complete!"
echo ""
echo "🚀 To deploy the improved API:"
echo "1. Install Railway CLI: npm install -g @railway/cli"
echo "2. Login to Railway: railway login"
echo "3. Deploy: python deploy_railway_improved.py"
echo ""
echo "📊 The improved API includes:"
echo "   ✅ Professional documentation with examples"
echo "   ✅ Proper validation and error handling"
echo "   ✅ Batch processing with correct schemas"
echo "   ✅ Rate limiting and security"
echo "   ✅ Version information and model card links"
echo "   ✅ Fairness notes and prediction timing clarity"
echo ""
echo "🔗 Your API will be available at:"
echo "   https://your-railway-app-name.up.railway.app"
echo "   https://your-railway-app-name.up.railway.app/docs"
