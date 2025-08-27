# Deployment Guide

## System Requirements

### Minimum
- **CPU:** 2 cores
- **RAM:** 4 GB
- **STORAGE:** 20 GB SSD
- **OS:** Ubuntu 20.04 LTS or CentOS 8

### Recommended
- **CPU:** 4+ cores
- **RAM:** 8+ GB
- **STORAGE:** 100 GB SSD
- **OS:** Ubuntu 22.04 LTS or RHEL 9

### Production
- **CPU:** 8+ cores
- **RAM:** 16+ GB
- **STORAGE:** 500 GB SSD
- **OS:** Ubuntu 22.04 LTS or RHEL 9

## Installation Steps

### Clone Repository
Clone the project repository to your local machine
```bash
git clone https://github.com/Muh76/diabetes-readmission-prediction.git
```

### Navigate to Project Directory
Change to the project directory
```bash
cd diabetes-readmission-prediction
```

### Set Environment Variables
Copy the example environment file and configure your settings
```bash
cp environment.env.example environment.env
```

### Configure Environment Variables
Edit environment.env with your specific configuration

### Build Docker Images
Build the Docker images for the application
```bash
docker-compose build
```

### Start Services
Start all services in detached mode
```bash
docker-compose up -d
```

### Verify Deployment
Check if the API is running and healthy
```bash
curl http://localhost:8000/health
```
