import mlflow
import mlflow.sklearn
import mlflow.lightgbm
import mlflow.xgboost
import mlflow.catboost
from mlflow.tracking import MlflowClient
from mlflow.models import infer_signature
import pandas as pd
import numpy as np
import joblib
import os
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MLflowManager:
    """MLflow manager for diabetes readmission prediction project"""
    
    def __init__(self, tracking_uri="sqlite:///mlflow.db", experiment_name="diabetes-readmission"):
        """
        Initialize MLflow manager
        
        Args:
            tracking_uri: MLflow tracking URI
            experiment_name: Name of the MLflow experiment
        """
        self.tracking_uri = tracking_uri
        self.experiment_name = experiment_name
        self.client = None
        self.experiment_id = None
        
        # Initialize MLflow
        self._setup_mlflow()
    
    def _setup_mlflow(self):
        """Setup MLflow tracking"""
        try:
            # Set tracking URI
            mlflow.set_tracking_uri(self.tracking_uri)
            
            # Create or get experiment
            try:
                self.experiment_id = mlflow.create_experiment(self.experiment_name)
                logger.info(f"Created new experiment: {self.experiment_name}")
            except:
                experiment = mlflow.get_experiment_by_name(self.experiment_name)
                self.experiment_id = experiment.experiment_id
                logger.info(f"Using existing experiment: {self.experiment_name}")
            
            # Set experiment
            mlflow.set_experiment(self.experiment_name)
            
            # Initialize client
            self.client = MlflowClient(tracking_uri=self.tracking_uri)
            
            logger.info("MLflow setup completed successfully")
            
        except Exception as e:
            logger.error(f"Error setting up MLflow: {str(e)}")
            raise
    
    def log_model_training(self, model, model_name, X_train, y_train, X_test, y_test, 
                          model_params=None, metrics=None, feature_names=None, 
                          run_name=None, tags=None):
        """
        Log model training to MLflow
        
        Args:
            model: Trained model object
            model_name: Name of the model (e.g., 'lightgbm', 'xgboost')
            X_train: Training features
            y_train: Training labels
            X_test: Test features
            y_test: Test labels
            model_params: Model parameters
            metrics: Dictionary of metrics
            feature_names: List of feature names
            run_name: Name for the run
            tags: Dictionary of tags
        """
        try:
            with mlflow.start_run(run_name=run_name) as run:
                # Log parameters
                if model_params:
                    mlflow.log_params(model_params)
                
                # Log metrics
                if metrics:
                    mlflow.log_metrics(metrics)
                
                # Log dataset info
                mlflow.log_param("train_samples", len(X_train))
                mlflow.log_param("test_samples", len(X_test))
                mlflow.log_param("features_count", X_train.shape[1])
                
                if feature_names:
                    mlflow.log_param("feature_names", ",".join(feature_names))
                
                # Log model
                if model_name.lower() == 'lightgbm':
                    mlflow.lightgbm.log_model(
                        model, 
                        "model",
                        registered_model_name=f"diabetes-readmission-{model_name}"
                    )
                elif model_name.lower() == 'xgboost':
                    mlflow.xgboost.log_model(
                        model, 
                        "model",
                        registered_model_name=f"diabetes-readmission-{model_name}"
                    )
                elif model_name.lower() == 'catboost':
                    mlflow.catboost.log_model(
                        model, 
                        "model",
                        registered_model_name=f"diabetes-readmission-{model_name}"
                    )
                else:
                    mlflow.sklearn.log_model(
                        model, 
                        "model",
                        registered_model_name=f"diabetes-readmission-{model_name}"
                    )
                
                # Log tags
                if tags:
                    mlflow.set_tags(tags)
                
                # Log model signature
                try:
                    signature = infer_signature(X_test, model.predict(X_test))
                    mlflow.models.log_model(
                        model, 
                        "model", 
                        signature=signature,
                        registered_model_name=f"diabetes-readmission-{model_name}"
                    )
                except Exception as e:
                    logger.warning(f"Could not infer model signature: {str(e)}")
                
                logger.info(f"Model {model_name} logged successfully with run ID: {run.info.run_id}")
                return run.info.run_id
                
        except Exception as e:
            logger.error(f"Error logging model {model_name}: {str(e)}")
            raise
    
    def log_pipeline_results(self, results_dict, run_name="pipeline-results"):
        """
        Log pipeline results to MLflow
        
        Args:
            results_dict: Dictionary containing pipeline results
            run_name: Name for the run
        """
        try:
            with mlflow.start_run(run_name=run_name) as run:
                # Log dataset information
                if 'dataset_info' in results_dict:
                    dataset_info = results_dict['dataset_info']
                    mlflow.log_params({
                        'total_patients': dataset_info.get('total_patients', 0),
                        'readmission_rate': dataset_info.get('readmission_rate', 0),
                        'features_tested': dataset_info.get('features_tested', 0),
                        'significant_features': dataset_info.get('significant_features', 0)
                    })
                
                # Log model performance
                if 'model_performance' in results_dict:
                    performance = results_dict['model_performance']
                    mlflow.log_metrics({
                        'best_roc_auc': performance.get('best_roc_auc', 0),
                        'best_accuracy': performance.get('best_accuracy', 0),
                        'best_precision': performance.get('best_precision', 0),
                        'best_recall': performance.get('best_recall', 0),
                        'best_f1_score': performance.get('best_f1_score', 0)
                    })
                
                # Log business impact
                if 'business_impact' in results_dict:
                    business = results_dict['business_impact']
                    mlflow.log_metrics({
                        'annual_cost_savings': business.get('annual_cost_savings', 0),
                        'readmissions_prevented': business.get('readmissions_prevented', 0),
                        'roi_percentage': business.get('roi_percentage', 0)
                    })
                
                # Log tags
                mlflow.set_tags({
                    'project': 'diabetes-readmission-prediction',
                    'dataset': 'UCI Diabetes',
                    'pipeline_version': '1.0.0',
                    'deployment_ready': 'true'
                })
                
                logger.info(f"Pipeline results logged successfully with run ID: {run.info.run_id}")
                return run.info.run_id
                
        except Exception as e:
            logger.error(f"Error logging pipeline results: {str(e)}")
            raise
    
    def get_best_model(self, metric='roc_auc', ascending=False):
        """
        Get the best model based on a metric
        
        Args:
            metric: Metric to use for comparison
            ascending: Whether to sort in ascending order
            
        Returns:
            Best run information
        """
        try:
            runs = self.client.search_runs(
                experiment_ids=[self.experiment_id],
                order_by=[f"metrics.{metric} {'ASC' if ascending else 'DESC'}"]
            )
            
            if runs:
                best_run = runs[0]
                logger.info(f"Best model found: {best_run.info.run_id} with {metric}: {best_run.data.metrics.get(metric, 'N/A')}")
                return best_run
            else:
                logger.warning("No runs found")
                return None
                
        except Exception as e:
            logger.error(f"Error getting best model: {str(e)}")
            raise
    
    def register_model_version(self, model_name, run_id, stage="Production"):
        """
        Register a model version and transition to stage
        
        Args:
            model_name: Name of the model
            run_id: Run ID containing the model
            stage: Stage to transition to (None, Staging, Production, Archived)
        """
        try:
            # Get the model URI from the run
            run = self.client.get_run(run_id)
            model_uri = f"runs:/{run_id}/model"
            
            # Create model version
            model_version = mlflow.register_model(
                model_uri=model_uri,
                name=f"diabetes-readmission-{model_name}"
            )
            
            # Transition to stage
            if stage:
                self.client.transition_model_version_stage(
                    name=f"diabetes-readmission-{model_name}",
                    version=model_version.version,
                    stage=stage
                )
            
            logger.info(f"Model {model_name} registered and transitioned to {stage}")
            return model_version
            
        except Exception as e:
            logger.error(f"Error registering model {model_name}: {str(e)}")
            raise
    
    def load_model_for_inference(self, model_name, stage="Production"):
        """
        Load model for inference
        
        Args:
            model_name: Name of the model
            stage: Stage of the model to load
            
        Returns:
            Loaded model
        """
        try:
            model_uri = f"models:/diabetes-readmission-{model_name}/{stage}"
            model = mlflow.sklearn.load_model(model_uri)
            logger.info(f"Model {model_name} loaded successfully from {stage}")
            return model
            
        except Exception as e:
            logger.error(f"Error loading model {model_name}: {str(e)}")
            raise
    
    def log_prediction_batch(self, predictions, run_name="prediction-batch"):
        """
        Log batch predictions
        
        Args:
            predictions: List of predictions
            run_name: Name for the run
        """
        try:
            with mlflow.start_run(run_name=run_name) as run:
                # Log prediction statistics
                predictions_array = np.array(predictions)
                mlflow.log_metrics({
                    'total_predictions': len(predictions),
                    'avg_prediction': float(np.mean(predictions_array)),
                    'std_prediction': float(np.std(predictions_array)),
                    'min_prediction': float(np.min(predictions_array)),
                    'max_prediction': float(np.max(predictions_array))
                })
                
                # Log tags
                mlflow.set_tags({
                    'prediction_type': 'batch',
                    'timestamp': datetime.now().isoformat()
                })
                
                logger.info(f"Batch predictions logged successfully with run ID: {run.info.run_id}")
                return run.info.run_id
                
        except Exception as e:
            logger.error(f"Error logging batch predictions: {str(e)}")
            raise
    
    def export_model_artifacts(self, run_id, output_dir="./mlflow_artifacts"):
        """
        Export model artifacts from MLflow
        
        Args:
            run_id: Run ID to export
            output_dir: Output directory for artifacts
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            # Download artifacts
            self.client.download_artifacts(run_id, "model", output_dir)
            
            # Get run info
            run = self.client.get_run(run_id)
            
            # Save run metadata
            metadata = {
                'run_id': run_id,
                'experiment_id': run.info.experiment_id,
                'status': run.info.status,
                'start_time': run.info.start_time,
                'end_time': run.info.end_time,
                'params': run.data.params,
                'metrics': run.data.metrics,
                'tags': run.data.tags
            }
            
            with open(os.path.join(output_dir, 'run_metadata.json'), 'w') as f:
                json.dump(metadata, f, indent=2, default=str)
            
            logger.info(f"Model artifacts exported to {output_dir}")
            
        except Exception as e:
            logger.error(f"Error exporting model artifacts: {str(e)}")
            raise
    
    def get_experiment_summary(self):
        """
        Get experiment summary
        
        Returns:
            Dictionary with experiment summary
        """
        try:
            runs = self.client.search_runs(experiment_ids=[self.experiment_id])
            
            summary = {
                'experiment_name': self.experiment_name,
                'total_runs': len(runs),
                'runs_by_status': {},
                'best_roc_auc': 0,
                'best_accuracy': 0,
                'latest_run': None
            }
            
            for run in runs:
                status = run.info.status
                summary['runs_by_status'][status] = summary['runs_by_status'].get(status, 0) + 1
                
                metrics = run.data.metrics
                if 'roc_auc' in metrics:
                    summary['best_roc_auc'] = max(summary['best_roc_auc'], metrics['roc_auc'])
                if 'accuracy' in metrics:
                    summary['best_accuracy'] = max(summary['best_accuracy'], metrics['accuracy'])
                
                if not summary['latest_run'] or run.info.start_time > summary['latest_run'].info.start_time:
                    summary['latest_run'] = run
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting experiment summary: {str(e)}")
            raise

# Utility functions for integration with your pipeline
def log_your_pipeline_results():
    """Log your actual pipeline results to MLflow"""
    
    # Initialize MLflow manager
    mlflow_manager = MLflowManager()
    
    # Your actual pipeline results
    pipeline_results = {
        'dataset_info': {
            'total_patients': 101766,
            'readmission_rate': 0.349,
            'features_tested': 89,
            'significant_features': 35
        },
        'model_performance': {
            'best_roc_auc': 0.6745,
            'best_accuracy': 0.6599,
            'best_precision': 0.1735,
            'best_recall': 0.5811,
            'best_f1_score': 0.2673
        },
        'business_impact': {
            'annual_cost_savings': 42600000,
            'readmissions_prevented': 2131,
            'roi_percentage': 250
        }
    }
    
    # Log pipeline results
    run_id = mlflow_manager.log_pipeline_results(pipeline_results)
    
    # Get experiment summary
    summary = mlflow_manager.get_experiment_summary()
    
    print("MLflow Pipeline Results Logged Successfully!")
    print(f"Run ID: {run_id}")
    print(f"Experiment Summary: {summary}")
    
    return run_id

if __name__ == "__main__":
    # Example usage
    log_your_pipeline_results()
