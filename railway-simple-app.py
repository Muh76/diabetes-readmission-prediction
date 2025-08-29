#!/usr/bin/env python3
"""
Simple FastAPI app for Railway deployment
This app is guaranteed to work and respond to health checks
"""

import os

import uvicorn
from fastapi import FastAPI

# Create FastAPI app
app = FastAPI(
    title="Diabetes Readmission API - Railway",
    description="Simple API for Railway deployment",
    version="1.0.0",
)


@app.get("/")
async def root():
    """Root endpoint - Railway health check"""
    return {
        "status": "healthy",
        "message": "Diabetes Readmission API is running on Railway!",
        "service": "FastAPI",
        "platform": "Railway",
        "endpoints": {"health": "/health", "ready": "/ready", "docs": "/docs"},
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2025-08-29T22:00:00Z"}


@app.get("/ready")
async def ready():
    """Readiness check endpoint"""
    return {"ready": True, "message": "Service is ready to handle requests"}


@app.get("/test")
async def test():
    """Test endpoint"""
    return {
        "message": "Test endpoint working!",
        "port": os.environ.get("PORT", "Not set"),
        "environment": "Railway",
    }


if __name__ == "__main__":
    # Get port from Railway environment
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting FastAPI server on port {port}")
    print("✅ Root endpoint: /")
    print("✅ Health endpoint: /health")
    print("✅ Ready endpoint: /ready")
    print("✅ Test endpoint: /test")

    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
