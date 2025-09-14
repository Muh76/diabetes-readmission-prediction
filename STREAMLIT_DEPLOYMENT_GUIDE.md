# Streamlit Cloud Deployment Guide

## 🚀 Deploy Your Diabetes Readmission Dashboard to Streamlit Cloud

This guide will help you deploy your Streamlit dashboard to `share.streamlit.io` for external access.

### 📋 Prerequisites

1. **GitHub Account**: You need a GitHub account
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Streamlit Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)

### 🔧 Step 1: Prepare Your Repository

Make sure your GitHub repository contains:

```
diabetes-readmission-prediction/
├── streamlit_app_production.py    # Main Streamlit app
├── requirements_streamlit.txt     # Dependencies
├── README.md                      # Project documentation
└── .streamlit/                    # Optional: Streamlit config
    └── config.toml
```

### 🌐 Step 2: Get Your Google Cloud Run URL

First, you need to get your deployed Google Cloud Run API URL:

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Navigate to **Cloud Run**
3. Find your `diabetes-readmission-api` service
4. Copy the **Service URL** (it looks like: `https://diabetes-readmission-api-xxxxx-uc.a.run.app`)

### 🔗 Step 3: Update API URL

Update the `API_URL` in `streamlit_app_production.py`:

```python
# Replace this line:
API_URL = os.getenv("API_URL", "https://diabetes-readmission-api-xxxxx-uc.a.run.app")

# With your actual Google Cloud Run URL:
API_URL = os.getenv("API_URL", "https://your-actual-gcr-url.a.run.app")
```

### 📤 Step 4: Push to GitHub

```bash
# Add the new files
git add streamlit_app_production.py requirements_streamlit.txt

# Commit changes
git commit -m "Add Streamlit Cloud deployment files"

# Push to GitHub
git push origin main
```

### 🚀 Step 5: Deploy on Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in** with your GitHub account
3. **Click "New app"**
4. **Fill in the details**:
   - **Repository**: Select your `diabetes-readmission-prediction` repository
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `streamlit_app_production.py`
   - **App URL**: Choose a custom URL (e.g., `diabetes-readmission-dashboard`)
5. **Click "Deploy!"**

### ⚙️ Step 6: Configure Environment Variables (Optional)

If you want to use environment variables for the API URL:

1. In your Streamlit Cloud app settings
2. Go to **Settings** → **Secrets**
3. Add:
   ```
   API_URL = "https://your-actual-gcr-url.a.run.app"
   ```

### 🔍 Step 7: Verify Deployment

1. **Wait for deployment** (usually 2-3 minutes)
2. **Visit your app URL**: `https://diabetes-readmission-dashboard.streamlit.app`
3. **Test the prediction feature** to ensure API connectivity
4. **Check all pages** work correctly

### 🛠️ Troubleshooting

#### Common Issues:

1. **API Connection Failed**:
   - Verify your Google Cloud Run URL is correct
   - Check if your GCR service is running
   - Ensure CORS is enabled on your FastAPI

2. **Import Errors**:
   - Check `requirements_streamlit.txt` has all dependencies
   - Ensure all imports are available

3. **Deployment Failed**:
   - Check GitHub repository is public
   - Verify file paths are correct
   - Check Streamlit Cloud logs for errors

### 📊 Your Dashboard Features

Once deployed, your dashboard will have:

- ✅ **Real-time Predictions** via Google Cloud Run API
- 📈 **Model Performance** visualization
- 💰 **Business Impact** analysis
- 🔬 **Data Exploration** tools
- 📋 **Technical Documentation**
- 📱 **Responsive Design** for mobile/tablet

### 🔗 Final URLs

After deployment, you'll have:

- **Streamlit Dashboard**: `https://your-app-name.streamlit.app`
- **API Endpoint**: `https://your-gcr-url.a.run.app`
- **MLflow UI**: `http://your-mlflow-url:5000` (if deployed)

### 🎉 Success!

Your diabetes readmission prediction dashboard is now live and accessible worldwide!

---

## 📝 Notes

- **Free Tier**: Streamlit Cloud offers free hosting with some limitations
- **Custom Domain**: You can use a custom domain with Streamlit Cloud Pro
- **Scaling**: Streamlit Cloud automatically handles scaling
- **Updates**: Push to GitHub to automatically update your deployed app