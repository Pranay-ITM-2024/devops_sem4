# 🛡️ SOC Automation Platform

**A full-stack, DevOps-automated Security Operations Center platform.**  
*Built as a comprehensive DevOps Exam Project.*

## 📋 Overview
This project simulates a SOC automation dashboard where analysts can view security alerts and trigger automated playbooks. 

The primary goal is **not** to build a complex cybersecurity product, but to demonstrate a complete, end-to-end **DevOps lifecycle** around a functional web application.

## ✨ Features
* **Flask Dashboard:** Server-rendered UI for SOC analysts.
* **FastAPI Backend:** REST API with automatic Swagger docs (`/docs`).
* **Alert Simulator:** Auto-generates mock security alerts (ransomware, brute force, etc.).
* **PostgreSQL:** Stores alert history and playbook logs.

## 🛠️ DevOps Stack (The 14 Deliverables)
1. **Source Code:** GitHub Monorepo
2. **Containerization:** Docker & Docker Compose
3. **CI/CD Pipeline:** Jenkins (Jenkinsfile)
4. **Infrastructure as Code:** Terraform
5. **Orchestration:** Kubernetes (Deployments, Services, HPA, ConfigMaps, Ingress)
6. **Monitoring:** Prometheus & Grafana
7. **Logging:** ELK Stack (Elasticsearch, Kibana)
8. **Secrets:** HashiCorp Vault

## 🚀 Quick Start (Local Development)
Run the application locally without Kubernetes using Docker Compose:

```bash
# Start all services
docker compose up -d --build

# View the dashboard
open http://localhost:5001

# View the API Swagger docs
open http://localhost:8000/docs
```

## ☸️ Kubernetes Deployment
To deploy the full stack to a local Minikube cluster:

```bash
# 1. Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192

# 2. Apply all manifests
kubectl apply -f k8s/namespaces/
kubectl apply -f k8s/app/secrets.yaml
kubectl apply -f k8s/app/configmap.yaml
kubectl apply -f k8s/database/
kubectl apply -f k8s/app/
kubectl apply -f k8s/simulator/

# 3. Access the application
minikube service flask-service -n soc-app
```

## 📚 Documentation
* **[Learning Guide](Learning.md):** Step-by-step instructions on every concept and tool used.
* **[System Requirements (SRD)](SRD.md):** Full project requirements and architecture definitions.
* **[Disaster Recovery](docs/disaster-recovery.md):** Backup, restore, and self-healing tests.
* **[Project Handover](ProjectHandover.md):** Task checklist and effort estimation.
