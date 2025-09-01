# 🏥 Diabetes Readmission Prediction System

## 🚀 **Professional Portfolio: End-to-End ML Healthcare System**

This repository contains a comprehensive **Diabetes Readmission Prediction system** with both FastAPI backend and Streamlit dashboard components. The system analyzes 101,766 patient records to predict 30-day hospital readmission risk with exceptional accuracy.

## 🎯 **Live Demo Links**

### 🌐 **Hosted Applications:**
- **📊 Interactive Dashboard:** [https://diabetes-readmission-prediction-drvwuus2xt7arfkucmvreq.streamlit.app/](https://diabetes-readmission-prediction-drvwuus2xt7arfkucmvreq.streamlit.app/)
- **🔌 FastAPI Endpoint:** [https://fastapi-diabetes-production.up.railway.app/](https://fastapi-diabetes-production.up.railway.app/)
- **📚 API Documentation:** [https://fastapi-diabetes-production.up.railway.app/docs](https://fastapi-diabetes-production.up.railway.app/docs)

## 📊 **What This Repository Contains:**

### **🎯 Core Applications:**
- **`streamlit_app_comprehensive.py`** - Professional portfolio dashboard (8 sections)
- **`streamlit_app.py`** - Original Streamlit dashboard application
- **`notebooks/app.py`** - FastAPI production application
- **`01_Diabetic_Readmission_Complete_Pipeline.ipynb`** - Complete ML pipeline notebook

### **🚀 Deployment Files:**
- **`Dockerfile.streamlit`** - Docker configuration for Streamlit
- **`Dockerfile.comprehensive`** - Docker configuration for comprehensive dashboard
- **`requirements-streamlit.txt`** - Python dependencies for Streamlit
- **`requirements-streamlit-cloud.txt`** - Dependencies for Streamlit Cloud
- **`railway.json`** - Railway deployment configuration

### **📚 Documentation:**
- **`COMPREHENSIVE_DASHBOARD_GUIDE.md`** - Complete deployment guide
- **`DEPLOYMENT_GUIDE.md`** - General deployment instructions
- **`feature_documentation.md`** - Feature engineering documentation
- **`models/MODEL_CARD.md`** - Model performance and specifications

## 🌟 **Key Achievements:**

- ✅ **95.32% ROC-AUC** performance
- ✅ **93.1% accuracy** with 99.5% precision
- ✅ **101,766 patient records** analyzed
- ✅ **15 engineered features** created
- ✅ **Production-ready deployment** on multiple platforms
- ✅ **End-to-end project execution** from EDA to deployment

## 📱 **Dashboard Features:**

### **🏠 Executive Summary:**
- Project overview and timeline
- Key performance indicators
- Business impact analysis

### **📈 Model Performance Analysis:**
- Model comparisons (XGBoost, Random Forest, LightGBM)
- Detailed performance metrics
- ROC-AUC and accuracy comparisons

### **🔍 Feature Analysis & SHAP:**
- SHAP feature importance analysis
- Advanced feature engineering details
- Clinical validation insights

### **🎯 LIME Interpretability:**
- Individual patient risk assessment
- Local interpretable model explanations
- Personalized prediction insights

### **💰 Business Impact & ROI:**
- Financial impact projections
- ROI calculations and cost-benefit analysis
- Performance evolution tracking

### **⚙️ Technical Architecture:**
- System architecture overview
- Model specifications and technical stack
- Deployment and MLOps pipeline

### **📊 EDA Insights:**
- Dataset overview and statistics
- Clinical risk stratification
- Treatment complexity analysis

### **🚀 Deployment & MLOps:**
- Production components
- Cloud deployment options
- API endpoints and monitoring

## 🏗️ **Architecture:**

- **Frontend:** Streamlit (Interactive Dashboard)
- **Backend:** FastAPI (Production API)
- **ML Framework:** XGBoost, Scikit-learn
- **Deployment:** Streamlit Cloud, Railway, Docker
- **Data:** Diabetes readmission dataset (101,766 records)

## 🔧 **Local Development:**

```bash
# Install dependencies
pip install -r requirements-streamlit-cloud.txt

# Run comprehensive dashboard locally
streamlit run streamlit_app_comprehensive.py

# Run FastAPI locally
cd notebooks
uvicorn app:app --reload
```

## 🚀 **Deployment Options:**

### **Streamlit Cloud (Recommended):**
- Automatic deployment from GitHub
- Free hosting with custom domain
- Easy updates with git push

### **Railway:**
- Fast deployment with Docker
- Auto-scaling capabilities
- Production-ready infrastructure

### **Docker:**
```bash
# Build and run comprehensive dashboard
docker build -f Dockerfile.comprehensive -t diabetes-dashboard .
docker run -p 8501:8501 diabetes-dashboard
```

## 📊 **Model Performance:**

| Metric | Value | Improvement |
|--------|-------|-------------|
| **ROC-AUC** | 95.32% | +20.32% vs Baseline |
| **Accuracy** | 93.1% | +18.1% vs Baseline |
| **Precision** | 99.5% | Outstanding |
| **Recall** | 86.7% | +11.7% vs Baseline |
| **F1-Score** | 92.7% | +17.7% vs Baseline |

## 🎯 **Perfect for:**

- **Recruiters** - Showcases end-to-end project execution
- **Stakeholders** - Demonstrates business value and ROI
- **Technical Interviews** - Proves ML and deployment skills
- **Portfolio** - Professional presentation of capabilities

## 🔗 **Related Links:**

- **GitHub Repository:** [diabetes-readmission-prediction](https://github.com/Muh76/diabetes-readmission-prediction)
- **Live Dashboard:** [https://diabetes-readmission-prediction-drvwuus2xt7arfkucmvreq.streamlit.app/](https://diabetes-readmission-prediction-drvwuus2xt7arfkucmvreq.streamlit.app/)
- **API Endpoint:** [https://fastapi-diabetes-production.up.railway.app/](https://fastapi-diabetes-production.up.railway.app/)
- **API Docs:** [https://fastapi-diabetes-production.up.railway.app/docs](https://fastapi-diabetes-production.up.railway.app/docs)

## 📄 **License:**

MIT License - see LICENSE file for details.
