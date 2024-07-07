from fastapi import FastAPI, HTTPException
from kubernetes import client, config
from prometheus_client import CollectorRegistry, Gauge, generate_latest
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Kubernetes configuration
if os.getenv('KUBERNETES_SERVICE_HOST'):
    config.load_incluster_config()
else:
    config.load_kube_config()

k8s_apps_v1 = client.AppsV1Api()
k8s_core_v1 = client.CoreV1Api()

# Prometheus client setup
registry = CollectorRegistry()
pod_gauge = Gauge('running_pods', 'Number of running pods', registry=registry)

@app.post("/createDeployment/{deployment_name}")
async def create_deployment(deployment_name: str):
    # Ensure deployment name is valid
    deployment_name = deployment_name.strip()
    if not deployment_name.isalnum():
        raise HTTPException(status_code=400, detail="Invalid deployment name. It must be alphanumeric.")
    
    # Define the deployment
    deployment = client.V1Deployment(
        metadata=client.V1ObjectMeta(name=deployment_name),
        spec=client.V1DeploymentSpec(
            replicas=1,
            selector=client.V1LabelSelector(
                match_labels={"app": deployment_name}
            ),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(
                    labels={"app": deployment_name}
                ),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name=deployment_name,
                            image="flask-app",  # You can change this to any image you prefer
                            ports=[client.V1ContainerPort(container_port=80)]
                        )
                    ]
                )
            )
        )
    )

    # Create the deployment
    try:
        k8s_apps_v1.create_namespaced_deployment(
            namespace="default",
            body=deployment
        )
        return {"message": f"Deployment {deployment_name} created successfully"}
    except client.ApiException as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/getPromdetails")
async def get_prom_details():
    # Get all pods
    pods = k8s_core_v1.list_pod_for_all_namespaces().items
    running_pods = [pod for pod in pods if pod.status.phase == 'Running']
    
    # Update Prometheus gauge
    pod_gauge.set(len(running_pods))

    # Fetch metrics from Prometheus
    try:
        prometheus_url = 'http://localhost:3001/api/v1/query'
        response = requests.get(prometheus_url, params={'query': 'running_pods'})
        response.raise_for_status()
        prom_data = response.json()
        
        return {
            "running_pods_count": len(running_pods),
            "prometheus_data": prom_data
        }
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Prometheus data: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
