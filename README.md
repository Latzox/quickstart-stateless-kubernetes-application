# quickstart-stateless-kubernetes-application

This repository contains code and configuration for a sample stateless application designed to run on kubernetes

# How to setup

## Requirements

- Docker

## Create Frontend Service

```
cd frontend
```

```
docker build -t <your-registry>/quickstart-k8s-frontend:latest .
```

## Create Backend Service

```
cd backend
```

```
docker build -t <your-registry>/quickstart-k8s-backend:latest .
```

## Push Docker Images

```
docker push <your-registry>/quickstart-k8s-backend:latest
docker push <your-registry>/quickstart-k8s-frontend:latest
```

## Apply Kubernetes Manifests