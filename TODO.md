Diabetes Readmission Prediction — TODOs (for TODO Tree)

Note: Each actionable line starts with "TODO:" so it appears in the TODO Tree. Priority tags: [P0]=critical, [P1]=high, [P2]=nice, [Stretch]=optional. Weeks indicated as [W1]–[W4].

================================================================================
🎯 THIS WEEK DELIVERABLES (Week 1: Aug 11-17, 2025)
================================================================================

✅ COMPLETED TODAY (Aug 11):
✅ Environment setup and virtual environment
✅ Git repository initialization
✅ All dependencies installed (including LightGBM OpenMP fix)
✅ MLflow server running on port 5001
✅ Project structure and scaffolding complete
✅ Pre-commit hooks configured
✅ Makefile commands working

📋 REMAINING WEEK 1 TASKS (Priority Order):

TODO: [W1][P0] 🔍 START DATA EXPLORATION: Open EDA notebook and begin analysis
TODO: [W1][P0] 📊 LOAD DATASET: Implement data loader for diabetic_data.csv with memory optimization
TODO: [W1][P0] 🎯 CREATE TARGET: Define readmission_30d = 1 if readmitted == "<30" else 0
TODO: [W1][P0] 📋 DATA VALIDATION: Draft pandera schema for critical columns (ranges, categories, nullability)
TODO: [W1][P0] 📈 COMPLETE EDA: Missingness, class balance, leakage checks, target stability; save plots to reports/
TODO: [W1][P0] 🏗️ FEATURE STRATEGY: Decide CatBoost native categoricals vs one-hot/target encoding approach
TODO: [W1][P0] ⚙️ FEATURE PIPELINE: Implement minimal pipeline (impute, encode, scale where needed)
TODO: [W1][P0] 🤖 BASELINE MODEL: Train Logistic Regression with CV; log to MLflow
TODO: [W1][P1] 🧪 UNIT TESTS: Create tests for data loader and pandera schema validation
TODO: [W1][P2] 📚 OPTIONAL: Set up DVC for dataset tracking

🎯 WEEK 1 SUCCESS CRITERIA:
- EDA notebook complete with insights
- Target variable properly defined
- Data validation schemas in place
- Baseline model trained and logged to MLflow
- Feature engineering strategy decided
- Ready for Week 2 model development

================================================================================
🔍 EDA WORKFLOW - COMPREHENSIVE ANALYSIS PLAN
================================================================================

📊 PHASE 1: DATA OVERVIEW & QUALITY ASSESSMENT (Day 1)
================================================================================

TODO: [EDA][P0] 📏 DATASET DIMENSIONS: Check shape, data types, memory usage, basic statistics
TODO: [EDA][P0] 🔍 MISSING VALUE ANALYSIS: Identify patterns, correlation with target variable
TODO: [EDA][P0] ✅ DATA TYPE VALIDATION: Check for mixed types, inconsistent encoding
TODO: [EDA][P0] 📋 MEMORY OPTIMIZATION: Implement efficient data loading for large CSV

🎯 PHASE 2: TARGET VARIABLE ANALYSIS (Day 1-2)
================================================================================

TODO: [EDA][P0] 🎯 READMISSION RATE DISTRIBUTION: Analyze class balance, temporal patterns
TODO: [EDA][P0] 🔗 TARGET CORRELATION: Identify strongest predictors with correlation analysis
TODO: [EDA][P0] 📊 CLASS IMBALANCE ASSESSMENT: Determine if balancing techniques needed
TODO: [EDA][P0] ⏰ TEMPORAL PATTERNS: Check for seasonal or time-based trends

🔬 PHASE 3: FEATURE EXPLORATION (Day 2-3)
================================================================================

TODO: [EDA][P0] 👥 DEMOGRAPHIC VARIABLES: Age, gender, race distributions, readmission relationship
TODO: [EDA][P0] 🏥 CLINICAL VARIABLES: Diagnosis codes, procedures, medications, lab results
TODO: [EDA][P0] ⏱️ TEMPORAL PATTERNS: Length of stay, time between visits, discharge timing
TODO: [EDA][P0] 💊 MEDICATION ANALYSIS: Drug combinations, dosage patterns, adherence indicators
TODO: [EDA][P0] 🧪 LAB RESULTS: Key biomarkers, normal ranges, abnormal patterns

🚀 PHASE 4: ADVANCED ANALYSIS (Day 3-4)
================================================================================

TODO: [EDA][P1] 🔗 FEATURE INTERACTIONS: Age × diagnosis, gender × treatment, comorbidity combinations
TODO: [EDA][P1] 🚨 OUTLIER DETECTION: Statistical outliers vs. legitimate medical anomalies
TODO: [EDA][P1] 🧹 DATA QUALITY ISSUES: Inconsistent coding, duplicates, entry errors
TODO: [EDA][P1] 📈 CORRELATION MATRIX: Feature relationships, multicollinearity detection
TODO: [EDA][P1] 🎭 CATEGORICAL ANALYSIS: Cardinality, rare categories, encoding strategies

📊 PHASE 5: HEALTHCARE-SPECIFIC INSIGHTS (Day 4)
================================================================================

TODO: [EDA][P1] 🏥 READMISSION RISK FACTORS: Medical and non-medical predictors
TODO: [EDA][P1] 👥 DEMOGRAPHIC DISPARITIES: Identify potential bias in healthcare delivery
TODO: [EDA][P1] 💰 COST IMPLICATIONS: Length of stay vs. readmission risk
TODO: [EDA][P1] 🎯 PREVENTION OPPORTUNITIES: High-risk patient identification
TODO: [EDA][P1] 📋 CLINICAL GUIDELINES: Compare findings with medical best practices

📈 PHASE 6: VISUALIZATION & REPORTING (Day 4)
================================================================================

TODO: [EDA][P1] 📊 DISTRIBUTION PLOTS: Histograms, box plots for numerical variables
TODO: [EDA][P1] 🎯 TARGET ANALYSIS: ROC curves, precision-recall, confusion matrices
TODO: [EDA][P1] 🔗 CORRELATION HEATMAPS: Feature relationships visualization
TODO: [EDA][P1] 📈 TIME SERIES PLOTS: Temporal patterns and trends
TODO: [EDA][P1] 📋 SUMMARY STATISTICS: Tables for key findings and insights

🎯 EDA SUCCESS CRITERIA & DELIVERABLES
================================================================================

TODO: [EDA][P0] 📝 COMPLETE NOTEBOOK: All phases documented with code and insights
TODO: [EDA][P0] 📊 SAVED PLOTS: All visualizations saved to reports/eda/ directory
TODO: [EDA][P0] 📋 DATA QUALITY REPORT: Missing values, outliers, inconsistencies documented
TODO: [EDA][P0] 🎯 FEATURE PRIORITY LIST: Ranked features by importance and correlation
TODO: [EDA][P0] 🚨 RISK FACTORS IDENTIFIED: Key predictors of readmission documented
TODO: [EDA][P0] 📈 PREPROCESSING PLAN: Data cleaning and feature engineering strategy
TODO: [EDA][P0] 🏥 HEALTHCARE INSIGHTS: Medical and business implications documented

💡 EDA TOOLS & TECHNIQUES
================================================================================

TODO: [EDA][P1] 🐼 PANDAS PROFILING: Generate comprehensive data overview report
TODO: [EDA][P1] 📊 SEABORN/PLOTLY: Interactive and publication-quality visualizations
TODO: [EDA][P1] 🔬 SCIPY: Statistical tests for healthcare data validation
TODO: [EDA][P1] 📈 SKLEARN: Feature importance and correlation analysis
TODO: [EDA][P1] 🎯 CUSTOM FUNCTIONS: Healthcare-specific metrics and calculations

🚀 EDA TO ML PIPELINE INTEGRATION
================================================================================

TODO: [EDA][P0] 🎯 FEATURE SELECTION: Based on correlation and domain knowledge
TODO: [EDA][P0] 🧹 DATA PREPROCESSING: Informed by missing value and quality patterns
TODO: [EDA][P0] 🤖 MODEL CHOICE: Based on data characteristics and class balance
TODO: [EDA][P0] 📊 EVALUATION METRICS: Based on target distribution and business needs
TODO: [EDA][P0] 🎭 BIAS DETECTION: Prepare for fairness analysis in Week 3

================================================================================
📅 FULL PROJECT TIMELINE (Weeks 2-4)
================================================================================

Week 2 — GBMs, HPO, Selection

TODO: [W2][P0] Train LightGBM, XGBoost, CatBoost with strong defaults; log experiments to MLflow
TODO: [W2][P0] Build evaluation script: AUC-ROC, PR-AUC, F1, calibration; save confusion matrices and plots
TODO: [W2][P0] Run Optuna HPO with fixed trials budget (50–100) and early stopping
TODO: [W2][P0] Register top model in MLflow Model Registry with descriptive tags (algo, features, seed)
TODO: [W2][P1] Create config.yml for data path, features, model params, CV folds, thresholds
TODO: [W2][P1] Reproducibility test: seeded splits return stable metrics within tolerance
TODO: [W2][P1] Generate SHAP global summary for top model; save plots and tables to reports/
TODO: [W2][P2] Compare class weights vs threshold tuning to balance precision/recall

Week 3 — Explainability, Fairness, Streamlit, GenAI

TODO: [W3][P0] Produce SHAP local explanations for a sample cohort; compute per-prediction reason codes
TODO: [W3][P0] Fairness metrics by demographics (race, gender, age bins): TPR/FPR, demographic parity, equalized odds
TODO: [W3][P0] Compile bias report with metrics + recommendations; save to reports/
TODO: [W3][P0] Build Streamlit app: CSV upload, batch inference, risk distribution, top features, patient-level explanations
TODO: [W3][P1] Add threshold slider and calibration plot to Streamlit; allow export of results
TODO: [W3][P1] Azure OpenAI: script to generate EDA and model summary narratives from stored metrics/plots
TODO: [W3][P1] Integrate LLM narrative into Streamlit with downloadable HTML/PDF
TODO: [W3][P2] Optional: Counterfactual examples for selected patients (DiCE)

Week 4 — API, Deploy, Monitoring, CI/CD, Docs

TODO: [W4][P0] FastAPI service: load model from MLflow/artifact; implement /health and /predict with pydantic schema
TODO: [W4][P0] Add request/response logging with PHI-safe redaction (no PII storage)
TODO: [W4][P0] Write Dockerfile (multi-stage) and Makefile targets: build, test, run, lint
TODO: [W4][P0] Deploy container to Azure Container Apps or Azure Container Instances (avoid AKS initially)
TODO: [W4][P0] Set up Evidently batch job for drift; schedule with GitHub Actions cron (daily/weekly)
TODO: [W4][P0] Create monitoring artifacts: data drift, prediction drift, performance snapshots in reports/monitoring/
TODO: [W4][P0] GitHub Actions CI: lint, tests, build; CD: build/push image and deploy to ACA/ACI with env gates
TODO: [W4][P1] Load test API (Locust/k6); record p50/p95 latency; target < 100ms on small payloads
TODO: [W4][P1] Security: image scan (Trivy) and dependency scan (pip-audit); remediate critical issues
TODO: [W4][P1] Documentation: MkDocs/README covering data, modeling, API, app, ops; include diagrams
TODO: [W4][P2] Wire Application Insights for logs/metrics (optional)
TODO: [W4][P2] Prepare AKS manifests and HPA config (Stretch only)

Cross-cutting Deliverables and Checks

TODO: [ALL][P0] Acceptance criteria: AUC ≥ 0.75; balanced precision/recall; API p95 latency < 100ms
TODO: [ALL][P0] Pin random seeds; log python/lib versions and dataset hash to MLflow
TODO: [ALL][P0] Code coverage ≥ 80%; enforce threshold in CI pipeline
TODO: [ALL][P1] Prepare final demo script and slide deck (problem, method, results, fairness, live demo)
TODO: [ALL][P2] Draft ROI/cost-benefit narrative with simple assumptions

Risk Controls and Contingencies

TODO: [RISK][P0] If HPO underperforms by Day 12, freeze best default GBM and proceed to Week 3
TODO: [RISK][P0] If Azure deploy blocks progress by Day 24, ship Docker + local FastAPI and use ngrok fallback
TODO: [RISK][P1] Keep 2-day buffer in Week 4 for polish and documentation

Stretch Goals (only if ahead of schedule)

TODO: [Stretch] AKS + KEDA autoscaling
TODO: [Stretch] Power BI monitoring dashboard with live connection
TODO: [Stretch] Advanced counterfactual analysis at scale

================================================================================
🚀 TOMORROW'S STARTING POINT (Aug 12, 2025)
================================================================================

1. Open terminal and activate environment: `source venv/bin/activate`
2. Start MLflow: `make mlflow-ui` (or it's already running)
3. Open EDA notebook: `jupyter notebook notebooks/01_initial_eda.ipynb`
4. Begin with first task: Load dataset and create target variable
5. Track progress in MLflow for all experiments

Good luck! 🎯
