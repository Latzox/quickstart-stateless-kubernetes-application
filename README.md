# quickstart-stateless-kubernetes-application

This repository contains code and configuration for a sample stateless application designed to run on kubernetes

# How to setup

## Requirements

- NodeJs https://nodejs.org/en/download
- Docker

## Create Frontend Service

```
```

## Create Backend Service

```
cd backend
```

```
docker build -t sample-k8s-backend .
```

```
docker run --name backend -p 80:8000 sample-k8s-backend
```

## Push Docker Images

```
docker tag sample-k8s-backend <your-registry>/sample-k8s-backend:latest
docker push <your-registry>/sample-k8s-backend:latest

docker tag sample-k8s-frontend <your-registry>/sample-k8s-frontend:latest
docker push <your-registry>/sample-k8s-frontend:latest
```

## Apply Kubernetes Manifests