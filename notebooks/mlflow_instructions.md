
# 🚀 MLFLOW UI ACCESS INSTRUCTIONS

## 📊 View Your Experiments

### Option 1: Local MLflow UI
```bash
# Start MLflow UI
mlflow ui --host 0.0.0.0 --port 5000

# Access in browser
http://localhost:5000
```

### Option 2: Docker MLflow UI
```bash
# Start with docker-compose
docker-compose up mlflow

# Access in browser
http://localhost:5000
```

### Option 3: Direct Database Access
```bash
# View SQLite database
sqlite3 mlflow.db
.tables
SELECT * FROM experiments;
```

## 🔍 What You'll See
- **Experiment**: diabetic_readmission_pipeline
- **Run**: phase1_complete_pipeline
- **Parameters**: Dataset size, features, class balance
- **Metrics**: Data quality, feature count, samples
- **Artifacts**: CSV files, reports

## 📈 Key Metrics Tracked
- Data quality score
- Feature engineering results
- Train-test split statistics
- Processing performance
- Memory usage

## �� Next Steps
1. View experiment in MLflow UI
2. Compare different runs
3. Track model performance
4. Export results for reporting
