# Diabetes Readmission Prediction 🏥

An end-to-end ML system to predict 30-day readmission risk for diabetic patients using MLOps best practices.

## 🎯 Project Overview

**Goal**: Build a production-ready ML system to predict 30-day readmission risk for diabetic patients
**Timeline**: 30 days (6 hours/day = 180 total hours)
**Dataset**: UCI Diabetes Dataset (~101,766 records)
**Target**: Binary classification (readmitted within 30 days: Yes/No)

## 🏗️ Architecture

- **Data Layer**: Pandas + Pandera validation
- **ML Platform**: MLflow + Azure ML
- **Models**: LightGBM, XGBoost, CatBoost + SHAP interpretability
- **Serving**: FastAPI + Docker + Azure Container Apps
- **Dashboard**: Streamlit + Plotly visualizations
- **Monitoring**: Evidently AI + MLflow metrics
- **GenAI**: Azure OpenAI for insights and explanations
- **CI/CD**: GitHub Actions + Azure Container Registry

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Docker
- Azure CLI (for deployment)
- Git

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd diabetes-readmission-prediction

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Setup pre-commit hooks
pre-commit install
```

### 2. Environment Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env with your Azure credentials
# AZURE_ML_WORKSPACE_NAME=your-workspace
# AZURE_ACR_NAME=your-acr
# AZURE_OPENAI_ENDPOINT=your-openai-endpoint
```

### 3. Start Development

```bash
# Start MLflow tracking server
make mlflow-ui

# Run initial EDA
jupyter notebook notebooks/01_initial_eda.ipynb

# Train baseline model
make train-model

# Run tests
make test

# Format code
make format
```

## 📁 Project Structure

```
diabetes-readmission-prediction/
├── src/                    # Source code
│   ├── data/              # Data loading and validation
│   ├── features/          # Feature engineering
│   ├── models/            # Model training and evaluation
│   ├── api/               # FastAPI service
│   ├── app/               # Streamlit dashboard
│   └── utils/             # Utility functions
├── notebooks/             # Jupyter notebooks
├── reports/               # Generated reports and plots
├── tests/                 # Test suite
├── configs/               # Configuration files
├── app/                   # Application files
├── .github/workflows/     # CI/CD pipelines
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project configuration
├── Dockerfile            # Container configuration
├── Makefile              # Development commands
└── README.md             # This file
```

## 🛠️ Development Commands

```bash
# View all available commands
make help

# Code quality
make lint          # Run linting checks
make format        # Format code
make test          # Run tests with coverage

# Development
make mlflow-ui     # Start MLflow tracking server
make notebook      # Start Jupyter notebook
make run-api       # Run FastAPI locally
make run-streamlit # Run Streamlit locally

# Data and models
make data-exploration  # Run initial data exploration
make train-model       # Train baseline model
make evaluate-model    # Evaluate trained model

# Deployment
make build            # Build Docker image
make deploy           # Deploy to Azure Container Apps
```

## 📊 Data Pipeline

1. **Data Loading**: Load `diabetic_data.csv` with memory optimization
2. **Target Creation**: `readmission_30d = (readmitted == "<30")`
3. **Validation**: Pandera schema validation for data quality
4. **Feature Engineering**: Encoding, scaling, and domain features
5. **Splitting**: Stratified train/validation/test split

## 🤖 Model Development

### Baseline Models
- **Logistic Regression**: Linear baseline with interpretability
- **LightGBM**: Fast gradient boosting with categorical support
- **XGBoost**: Robust gradient boosting with regularization
- **CatBoost**: Advanced gradient boosting with categorical handling

### Hyperparameter Optimization
- **Optuna**: Bayesian optimization with early stopping
- **Budget**: 50-100 trials per model
- **Metrics**: AUC-ROC, PR-AUC, F1-score

### Interpretability
- **SHAP**: Global and local feature importance
- **Fairness**: Demographic parity, equalized odds
- **Bias Analysis**: Cross-group performance analysis

## 🌐 API & Dashboard

### FastAPI Service
- **Endpoints**: `/health`, `/predict`
- **Input Validation**: Pydantic schemas
- **PHI Safety**: Secure logging and data handling
- **Performance**: Target < 100ms latency

### Streamlit Dashboard
- **Upload**: CSV file processing
- **Batch Inference**: Multiple patient predictions
- **Visualizations**: Risk distribution, feature importance
- **Export**: Results and explanations

## 📈 Monitoring & Observability

### Model Monitoring
- **Data Drift**: Evidently AI batch monitoring
- **Performance**: MLflow metrics tracking
- **Alerts**: Automated drift detection

### Application Monitoring
- **Health Checks**: API endpoint monitoring
- **Performance**: Latency and throughput metrics
- **Logs**: Structured logging with PHI protection

## 🔄 CI/CD Pipeline

### GitHub Actions
1. **CI**: Lint, test, build Docker image
2. **CD**: Push to Azure Container Registry
3. **Deploy**: Update Azure Container Apps
4. **Monitoring**: Automated drift detection

### Quality Gates
- Code coverage > 80%
- All tests passing
- Linting standards met
- Security scans passed

## 🚀 Deployment

### Azure Services
- **Azure ML**: Model registry and tracking
- **Azure Container Registry**: Docker image storage
- **Azure Container Apps**: Serverless deployment
- **Azure Monitor**: Application insights

### Deployment Steps
1. Build and push Docker image
2. Deploy to Azure Container Apps
3. Configure monitoring and alerts
4. Update DNS and load balancer

## 📚 Documentation

- **Technical Docs**: API reference, architecture diagrams
- **User Guides**: Clinical decision support usage
- **Model Cards**: Performance, fairness, limitations
- **Dataset Sheets**: Data provenance and quality

## 🎯 Success Metrics

### Technical Metrics
- **Model Performance**: AUC-ROC > 0.75
- **API Latency**: P95 < 100ms
- **System Uptime**: > 99.5%
- **Code Coverage**: > 80%

### Business Impact
- **Cost Savings**: Reduced readmission costs
- **Clinical Integration**: Workflow feasibility
- **ROI Analysis**: Implementation cost vs. savings

## 🔬 Research Value

### Academic Contributions
- **Methodology**: Rigorous experimental design
- **Fairness**: Bias detection and mitigation
- **Interpretability**: Clinical decision support
- **Reproducibility**: Open-source implementation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- UCI Machine Learning Repository for the dataset
- MLflow, Optuna, and Evidently AI teams
- Azure ML and Container Apps services

## 📞 Support

For questions or issues:
- Create an issue in the repository
- Check the documentation
- Review the TODO.md for current tasks

---

**Status**: 🚧 In Development (Week 1 of 4)
**Next Milestone**: Complete EDA and baseline model training
