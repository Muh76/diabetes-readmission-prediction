# Troubleshooting Guide

## Api Not Starting

### Symptoms
- API returns connection refused
- Docker container exits immediately

### Causes
- Port conflicts
- Missing environment variables
- Model file not found

### Solutions
- Check if port 8000 is available: netstat -tulpn | grep 8000
- Verify environment variables: docker-compose logs api
- Ensure model file exists: ls -la models/
- Check container logs: docker-compose logs api

## Model Loading Errors

### Symptoms
- Model file not found error
- Pickle loading failed

### Causes
- Incorrect model path
- Corrupted model file
- Python version mismatch

### Solutions
- Verify model path in environment.env
- Check model file integrity: file models/catboost.pkl
- Ensure Python version compatibility
- Re-download or retrain the model

## Database Connection Issues

### Symptoms
- Database connection timeout
- Connection refused

### Causes
- Database service not running
- Incorrect connection string
- Network issues

### Solutions
- Check database service: docker-compose ps database
- Verify connection string format
- Test network connectivity: docker-compose exec api ping database
- Restart database service: docker-compose restart database

## Memory Issues

### Symptoms
- Out of memory errors
- Slow response times
- Container crashes

### Causes
- Insufficient RAM
- Memory leaks
- Large model size

### Solutions
- Increase container memory limits in docker-compose.yml
- Monitor memory usage: docker stats
- Optimize model loading and caching
- Consider model quantization for production

## Performance Degradation

### Symptoms
- Slow API responses
- High latency
- Timeout errors

### Causes
- High CPU usage
- I/O bottlenecks
- Network latency

### Solutions
- Monitor system resources: htop, iostat
- Check API performance metrics: /metrics endpoint
- Optimize database queries and indexing
- Implement caching strategies
