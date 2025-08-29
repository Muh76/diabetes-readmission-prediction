#!/bin/bash

echo "🚀 Quick Deployment Script for Diabetes Readmission Prediction"
echo "=============================================================="
echo ""

echo "📋 This script will help you deploy both services quickly:"
echo "  1. FastAPI App (Prediction API)"
echo "  2. Streamlit Dashboard (Interactive UI)"
echo ""

echo "🌐 Choose your deployment platform:"
echo "  1) Railway (Recommended - 5 minutes)"
echo "  2) Render (Free tier)"
echo "  3) Azure (Professional)"
echo ""

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🚂 Deploying to Railway..."
        echo ""
        echo "📋 Steps:"
        echo "  1. Go to https://railway.app"
        echo "  2. Sign in with GitHub"
        echo "  3. Click 'New Project'"
        echo "  4. Select 'Deploy from GitHub repo'"
        echo "  5. Choose your repository"
        echo ""
        echo "🔧 For FastAPI:"
        echo "  - Railway will auto-detect FastAPI"
        echo "  - Build command: pip install -r requirements.txt"
        echo "  - Start command: uvicorn notebooks.app:app --host 0.0.0.0 --port $PORT"
        echo ""
        echo "🎨 For Streamlit:"
        echo "  - Create another project"
        echo "  - Build command: pip install -r requirements-streamlit.txt"
        echo "  - Start command: streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0"
        echo ""
        ;;
    2)
        echo ""
        echo "🎨 Deploying to Render..."
        echo ""
        echo "📋 Steps:"
        echo "  1. Go to https://render.com"
        echo "  2. Sign in with GitHub"
        echo "  3. Click 'New +' > 'Web Service'"
        echo "  4. Connect your repository"
        echo ""
        echo "🔧 For FastAPI:"
        echo "  - Build command: pip install -r requirements.txt"
        echo "  - Start command: uvicorn notebooks.app:app --host 0.0.0.0 --port $PORT"
        echo ""
        echo "🎨 For Streamlit:"
        echo "  - Create another web service"
        echo "  - Build command: pip install -r requirements-streamlit.txt"
        echo "  - Start command: streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0"
        echo ""
        ;;
    3)
        echo ""
        echo "☁️ Deploying to Azure..."
        echo ""
        echo "📋 Steps:"
        echo "  1. Your Azure workflow is already configured!"
        echo "  2. Just push to GitHub: git push origin master"
        echo "  3. Check GitHub Actions for deployment status"
        echo ""
        echo "🔧 Azure Container Apps will be deployed automatically"
        echo "🎨 For Streamlit, deploy as a separate Container App"
        echo ""
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "✅ After deployment, you'll get:"
echo "  - FastAPI URL: https://your-app-name.railway.app (or similar)"
echo "  - Streamlit URL: https://your-dashboard-name.railway.app (or similar)"
echo ""
echo "🔗 Update your README.md with these working links!"
echo ""
echo "�� Happy deploying!"
