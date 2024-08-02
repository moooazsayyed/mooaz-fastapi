# mooaz-fastapi 
FastAPI Kubernetes Deployment Manager
This project is a FastAPI application designed to automate the deployment of Docker images on a Kubernetes cluster. It provides functionalities to deploy images, monitor the number of running pods, and integrate with Prometheus for robust metrics collection.

Table of Contents
Features
Architecture
Installation
Usage
API Endpoints
Monitoring with Prometheus
Contributing
License
Features
Deployment Management: Automate the deployment of Docker images to a Kubernetes cluster using the Kubernetes client.
Pod Monitoring: Retrieve and display the number of running pods in the cluster.
Prometheus Integration: Collect and expose metrics for enhanced observability and performance analysis.
RESTful API: Utilize GET and POST requests for deployment management and monitoring.
Architecture
The application is built using:

FastAPI: A modern, fast (high-performance) web framework for building APIs with Python 3.6+.
Kubernetes Client: A Python client library for interacting with Kubernetes clusters.
Prometheus: A monitoring and alerting toolkit for collecting and analyzing metrics.

Installation
To set up the FastAPI Kubernetes Deployment Manager, follow these steps:

Prerequisites
Python 3.6+
Docker
Kubernetes Cluster
Prometheus
Setup
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/fastapi-k8s-deployment-manager.git
cd fastapi-k8s-deployment-manager
Create a virtual environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Configure Kubernetes access:

Ensure you have access to your Kubernetes cluster and that your kubeconfig file is set up correctly.

Run the application:

bash
Copy code
uvicorn main:app --reload
Usage
Once the application is running, you can interact with it using HTTP requests or via the provided API documentation at /docs.

API Endpoints
Deploy Docker Image
Endpoint: /deploy
Method: POST
Description: Deploy a Docker image to the Kubernetes cluster.
Request Body:
json
Copy code
{
  "image_name": "your-docker-image",
  "namespace": "default"
}
Response:
json
Copy code
{
  "status": "success",
  "message": "Deployment initiated"
}
Get Running Pods
Endpoint: /pods
Method: GET
Description: Retrieve the number of running pods.
Response:
json
Copy code
{
  "namespace": "default",
  "running_pods": 5
}
Monitoring with Prometheus
The application exposes metrics for Prometheus to scrape. Ensure Prometheus is configured to collect metrics from the application's endpoint.

Configure Prometheus:

Add the following scrape configuration to your prometheus.yml:

```
scrape_configs:
  - job_name: 'fastapi-k8s-manager'
    static_configs:
      - targets: ['localhost:8000']
View Metrics:```

Access the Prometheus dashboard to view metrics and set up alerts as needed.

Contributing
We welcome contributions! Please follow these steps:

Fork the repository.
Create a new branch for your feature or bug fix.
Implement your changes and write tests if applicable.
Submit a pull request with a detailed description of your changes.
License
This project is licensed under the MIT License. See the LICENSE file for more details.


