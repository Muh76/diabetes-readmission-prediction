"""
ML API Metrics Collection Module
Tracks performance, predictions, and system health metrics
"""

import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Optional

import psutil

logger = logging.getLogger(__name__)


@dataclass
class PredictionMetrics:
    """Metrics for individual predictions"""

    timestamp: str
    model_name: str
    processing_time_ms: float
    prediction: bool
    probability: float
    confidence_level: str
    success: bool
    error_message: Optional[str] = None


@dataclass
class SystemMetrics:
    """System health metrics"""

    timestamp: str
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    disk_percent: float
    uptime_seconds: float


@dataclass
class ModelMetrics:
    """Model performance metrics"""

    model_name: str
    total_predictions: int
    successful_predictions: int
    failed_predictions: int
    avg_processing_time_ms: float
    last_used: str


class MetricsCollector:
    """Centralized metrics collection and reporting"""

    def __init__(self):
        self.prediction_metrics: list[PredictionMetrics] = []
        self.system_metrics: list[SystemMetrics] = []
        self.model_metrics: dict[str, ModelMetrics] = {}
        self.startup_time = datetime.now()

        # Initialize model metrics
        self._init_model_metrics()

    def _init_model_metrics(self):
        """Initialize metrics for all available models"""
        models = [
            "xgboost",
            "lightgbm",
            "catboost",
            "random_forest",
            "logistic_regression",
        ]
        for model in models:
            self.model_metrics[model] = ModelMetrics(
                model_name=model,
                total_predictions=0,
                successful_predictions=0,
                failed_predictions=0,
                avg_processing_time_ms=0.0,
                last_used="Never",
            )

    def record_prediction(
        self,
        model_name: str,
        processing_time_ms: float,
        prediction: bool,
        probability: float,
        confidence_level: str,
        success: bool = True,
        error_message: Optional[str] = None,
    ):
        """Record metrics for a prediction request"""
        try:
            metric = PredictionMetrics(
                timestamp=datetime.now().isoformat(),
                model_name=model_name,
                processing_time_ms=processing_time_ms,
                prediction=prediction,
                probability=probability,
                confidence_level=confidence_level,
                success=success,
                error_message=error_message,
            )

            self.prediction_metrics.append(metric)

            # Update model metrics
            if model_name in self.model_metrics:
                model_metric = self.model_metrics[model_name]
                model_metric.total_predictions += 1
                model_metric.last_used = datetime.now().isoformat()

                if success:
                    model_metric.successful_predictions += 1
                else:
                    model_metric.failed_predictions += 1

                # Update average processing time
                if model_metric.avg_processing_time_ms == 0:
                    model_metric.avg_processing_time_ms = processing_time_ms
                else:
                    model_metric.avg_processing_time_ms = (
                        model_metric.avg_processing_time_ms + processing_time_ms
                    ) / 2

            # Keep only last 1000 predictions to prevent memory issues
            if len(self.prediction_metrics) > 1000:
                self.prediction_metrics = self.prediction_metrics[-1000:]

        except Exception as e:
            logger.error(f"Failed to record prediction metrics: {e}")

    def record_system_metrics(self):
        """Record current system metrics"""
        try:
            current_time = datetime.now()
            uptime = (current_time - self.startup_time).total_seconds()

            # Get system metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            metric = SystemMetrics(
                timestamp=current_time.isoformat(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_used_mb=memory.used / (1024 * 1024),
                disk_percent=(disk.used / disk.total) * 100,
                uptime_seconds=uptime,
            )

            self.system_metrics.append(metric)

            # Keep only last 100 system metrics
            if len(self.system_metrics) > 100:
                self.system_metrics = self.system_metrics[-100:]

        except Exception as e:
            logger.error(f"Failed to record system metrics: {e}")

    def get_summary_metrics(self) -> dict[str, Any]:
        """Get summary of all collected metrics"""
        try:
            current_time = datetime.now()
            uptime = (current_time - self.startup_time).total_seconds()

            # Calculate prediction summary
            total_predictions = len(self.prediction_metrics)
            successful_predictions = len(
                [m for m in self.prediction_metrics if m.success]
            )
            failed_predictions = total_predictions - successful_predictions

            avg_processing_time = 0.0
            if total_predictions > 0:
                avg_processing_time = (
                    sum(m.processing_time_ms for m in self.prediction_metrics)
                    / total_predictions
                )

            # Get latest system metrics
            latest_system = self.system_metrics[-1] if self.system_metrics else None

            summary = {
                "timestamp": current_time.isoformat(),
                "uptime_seconds": round(uptime, 2),
                "predictions": {
                    "total": total_predictions,
                    "successful": successful_predictions,
                    "failed": failed_predictions,
                    "success_rate": round(
                        (successful_predictions / total_predictions * 100), 2
                    )
                    if total_predictions > 0
                    else 0,
                    "avg_processing_time_ms": round(avg_processing_time, 2),
                },
                "models": {
                    name: {
                        "total_predictions": metric.total_predictions,
                        "successful_predictions": metric.successful_predictions,
                        "failed_predictions": metric.failed_predictions,
                        "avg_processing_time_ms": round(
                            metric.avg_processing_time_ms, 2
                        ),
                        "last_used": metric.last_used,
                    }
                    for name, metric in self.model_metrics.items()
                },
                "system": {
                    "cpu_percent": round(latest_system.cpu_percent, 2)
                    if latest_system
                    else 0,
                    "memory_percent": round(latest_system.memory_percent, 2)
                    if latest_system
                    else 0,
                    "memory_used_mb": round(latest_system.memory_used_mb, 2)
                    if latest_system
                    else 0,
                    "disk_percent": round(latest_system.disk_percent, 2)
                    if latest_system
                    else 0,
                }
                if latest_system
                else {},
            }

            return summary

        except Exception as e:
            logger.error(f"Failed to get summary metrics: {e}")
            return {"error": str(e)}

    def export_metrics(self, filepath: str):
        """Export all metrics to a JSON file"""
        try:
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "summary": self.get_summary_metrics(),
                "prediction_metrics": [
                    asdict(m) for m in self.prediction_metrics[-100:]
                ],  # Last 100
                "system_metrics": [
                    asdict(m) for m in self.system_metrics[-50:]
                ],  # Last 50
                "model_metrics": {
                    name: asdict(metric) for name, metric in self.model_metrics.items()
                },
            }

            with open(filepath, "w") as f:
                json.dump(export_data, f, indent=2, default=str)

            logger.info(f"Metrics exported to {filepath}")

        except Exception as e:
            logger.error(f"Failed to export metrics: {e}")


# Global metrics collector instance
metrics_collector = MetricsCollector()


# Convenience functions
def record_prediction(*args, **kwargs):
    """Record prediction metrics"""
    metrics_collector.record_prediction(*args, **kwargs)


def record_system_metrics():
    """Record system metrics"""
    metrics_collector.record_system_metrics()


def get_summary_metrics():
    """Get summary metrics"""
    return metrics_collector.get_summary_metrics()


def export_metrics(filepath: str):
    """Export metrics to file"""
    metrics_collector.export_metrics(filepath)
