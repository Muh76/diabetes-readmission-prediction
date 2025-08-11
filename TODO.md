Diabetes Readmission Prediction — TODOs (for TODO Tree)

Note: Each actionable line starts with "TODO:" so it appears in the TODO Tree. Priority tags: [P0]=critical, [P1]=high, [P2]=nice, [Stretch]=optional. Weeks indicated as [W1]–[W4].

Week 1 — Data, Repo, Baseline

TODO: [W1][P0] Create repo scaffolding: src/, notebooks/, data/, models/, configs/, tests/, app/, .github/workflows/
TODO: [W1][P0] Add dependencies file (pyproject.toml or requirements.txt): pandas, numpy, scikit-learn, lightgbm, xgboost, catboost, shap, optuna, mlflow, fastapi, uvicorn, pydantic, evidently, pandera, plotly, streamlit, pytest, black, isort, ruff/flake8, pre-commit
TODO: [W1][P0] Initialize MLflow locally; connect Azure ML workspace for remote tracking later
TODO: [W1][P0] Implement data loader for diabetic_data.csv with explicit dtypes and memory-safe reading
TODO: [W1][P0] Define target: readmission_30d = 1 if readmitted == "<30" else 0
TODO: [W1][P0] Draft pandera schema for critical columns (ranges, categories, nullability)
TODO: [W1][P0] EDA notebook: missingness, class balance, leakage checks, target stability; save plots to reports/
TODO: [W1][P0] Decide feature strategy: CatBoost native categoricals vs one-hot/target encoding; scaling needs
TODO: [W1][P0] Implement minimal feature pipeline (impute, encode, scale where needed)
TODO: [W1][P0] Baseline model: Logistic Regression with CV; log params/metrics/artifacts to MLflow
TODO: [W1][P1] Configure pre-commit with black, isort, ruff/flake8; enable on staged files
TODO: [W1][P1] Unit tests: data loader and pandera schema validation (pytest)
TODO: [W1][P2] Optional: Set up DVC for dataset tracking (remote optional)

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
