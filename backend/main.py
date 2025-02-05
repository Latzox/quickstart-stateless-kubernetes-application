import os
import logging
from fastapi import FastAPI
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

app = FastAPI()

# Read message from ConfigMap
BACKEND_MESSAGE = os.getenv("BACKEND_MESSAGE", "Default backend message")

# Namespace to filter (change this if needed)
NAMESPACE_FILTER = os.getenv("NAMESPACE_FILTER", "default")

# Load Kubernetes Config
try:
    config.load_incluster_config()  # Load from within Kubernetes
    v1 = client.CoreV1Api()
except Exception as e:
    v1 = None
    logging.error(f"Kubernetes client could not be initialized: {e}")

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

    try:
        # Get node info
        nodes = v1.list_node().items
        node_info = [{"name": node.metadata.name, "status": node.status.conditions[-1].type} for node in nodes]

        # Get pods only from the specified namespace
        pods = v1.list_namespaced_pod(namespace=NAMESPACE_FILTER).items
        pod_info = [{"name": pod.metadata.name, "namespace": pod.metadata.namespace, "status": pod.status.phase} for pod in pods]

        return {"nodes": node_info, "pods": pod_info}

    except ApiException as e:
        logging.error(f"Error fetching cluster data: {e}")
        return {"error": "Failed to fetch cluster data", "details": str(e)}
