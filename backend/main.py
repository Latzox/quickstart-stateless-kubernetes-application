import os
import redis
import json
from fastapi import FastAPI
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

app = FastAPI()

# Connect to Redis
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Read backend message from ConfigMap
BACKEND_MESSAGE = os.getenv("BACKEND_MESSAGE", "Default backend message")

# Load Kubernetes Config
try:
    config.load_incluster_config()
    v1 = client.CoreV1Api()
except Exception as e:
    v1 = None

@app.get("/api")
def read_root():
    return {"message": BACKEND_MESSAGE}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/cluster-info")
def cluster_info():
    if v1 is None:
        return {"error": "Backend is not running inside Kubernetes"}

    # Check cache first
    cached_data = redis_client.get("cluster_info")
    if cached_data:
        return json.loads(cached_data)

    try:
        # Get node info
        nodes = v1.list_node().items
        node_info = [{"name": node.metadata.name, "status": node.status.conditions[-1].type} for node in nodes]

        # Get pod info
        pods = v1.list_namespaced_pod(namespace="default").items
        pod_info = [{"name": pod.metadata.name, "namespace": pod.metadata.namespace, "status": pod.status.phase} for pod in pods]

        cluster_data = {"nodes": node_info, "pods": pod_info}

        # Cache result for 30 seconds
        redis_client.setex("cluster_info", 30, json.dumps(cluster_data))

        return cluster_data

    except ApiException as e:
        return {"error": "Failed to fetch cluster data", "details": str(e)}
