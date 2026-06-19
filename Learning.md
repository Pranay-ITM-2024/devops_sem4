# 📚 SOC Automation Platform — Learning & Deployment Guide

> **Goal:** Learn every concept behind this project and deploy it step by step, from zero to a fully running DevOps pipeline.

---

## Table of Contents

1. [Understanding the Domain](#1-understanding-the-domain)
2. [Understanding the Tech Stack](#2-understanding-the-tech-stack)
3. [Prerequisites & Local Setup](#3-prerequisites--local-setup)
4. [Step 1 — Build the FastAPI Backend](#step-1--build-the-fastapi-backend)
5. [Step 2 — Build the Flask Dashboard](#step-2--build-the-flask-dashboard)
6. [Step 3 — Build the Alert Simulator](#step-3--build-the-alert-simulator)
7. [Step 4 — Dockerize Everything](#step-4--dockerize-everything)
8. [Step 5 — Push to GitHub](#step-5--push-to-github)
9. [Step 6 — Write Terraform Scripts](#step-6--write-terraform-scripts)
10. [Step 7 — Deploy on Kubernetes](#step-7--deploy-on-kubernetes)
11. [Step 8 — Set Up Jenkins CI/CD](#step-8--set-up-jenkins-cicd)
12. [Step 9 — Set Up Prometheus & Grafana](#step-9--set-up-prometheus--grafana)
13. [Step 10 — Set Up ELK Stack](#step-10--set-up-elk-stack)
14. [Step 11 — Set Up HashiCorp Vault](#step-11--set-up-hashicorp-vault)
15. [Step 12 — Disaster Recovery Testing](#step-12--disaster-recovery-testing)
16. [Step 13 — Screenshots & Documentation](#step-13--screenshots--documentation)
17. [Cheat Sheet — Key Commands](#cheat-sheet--key-commands)
18. [Common Errors & Fixes](#common-errors--fixes)
19. [Glossary](#glossary)

---

## 1. Understanding the Domain

### What is a SOC?

A **Security Operations Center (SOC)** is a team of cybersecurity analysts who monitor an organization's IT infrastructure 24/7 for security threats. Think of it like a control room in a power plant — but for cyber threats.

**What SOC analysts do every day:**
- Watch dashboards showing security alerts
- Investigate suspicious activity (Is this a real attack or a false alarm?)
- Respond to incidents (Block the attacker's IP, isolate an infected laptop)
- Write reports about what happened

### What is a SIEM?

**Security Information and Event Management (SIEM)** is software that collects logs from every system in the company (firewalls, servers, laptops, cloud) and looks for patterns that indicate an attack.

**Example SIEMs:** Splunk, IBM QRadar, Microsoft Sentinel

### What is EDR?

**Endpoint Detection and Response (EDR)** is software installed on every laptop/server that watches for malicious behavior (like ransomware encrypting files).

**Example EDRs:** CrowdStrike Falcon, SentinelOne, Microsoft Defender

### What is SOAR?

**Security Orchestration, Automation, and Response (SOAR)** automates the response to security incidents. Instead of a human manually blocking an IP, SOAR does it automatically via a **playbook** (a script of predefined actions).

### The Problem We're Solving

| Problem | What it means | Our solution |
|---------|---------------|--------------|
| **Alert fatigue** | Analysts get thousands of alerts daily, can't review them all | Dashboard filters + severity scoring |
| **Manual response** | Human manually blocks IPs, isolates hosts | Mock playbook engine automates responses |
| **Inconsistent deployments** | Different setups in different environments | Kubernetes + Terraform ensure consistency |
| **No monitoring** | Can't see if the SOC app itself is healthy | Prometheus + Grafana dashboards |
| **No centralized logging** | Logs scattered across different servers | ELK Stack aggregates all logs |

### Our Application (Simplified)

We're building a **mini SOC dashboard** — not a full enterprise system, but a working demo that shows:
1. A **web dashboard** where analysts see security alerts
2. An **API** that manages alert data
3. A **simulator** that generates fake alerts
4. **Mock playbooks** that pretend to block IPs and isolate hosts

Then we wrap it all with DevOps tools.

---

## 2. Understanding the Tech Stack

### 🐍 Python Flask — Dashboard

**What:** A lightweight Python web framework for building web applications.
**Why we use it:** To build the SOC analyst dashboard (HTML pages rendered on the server).
**Key concept:** Flask uses **Jinja2 templates** — HTML files with `{{ variable }}` placeholders that Flask fills in with data.

```python
# Simplest Flask app
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, SOC Analyst!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**Learn more:** [Flask Quickstart](https://flask.palletsprojects.com/en/latest/quickstart/)

---

### ⚡ Python FastAPI — Backend API

**What:** A modern, fast Python framework for building REST APIs.
**Why we use it:** To build the backend API that the dashboard talks to. FastAPI auto-generates Swagger documentation and supports async.
**Key concept:** FastAPI uses **Pydantic models** for request/response validation and auto-generates docs at `/docs`.

```python
# Simplest FastAPI app
from fastapi import FastAPI
app = FastAPI()

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/alerts")
def get_alerts():
    return [
        {"id": 1, "title": "Brute force detected", "severity": "high"},
        {"id": 2, "title": "Port scan detected", "severity": "medium"}
    ]
```

Run with: `uvicorn main:app --reload --port 8000`
Then open: `http://localhost:8000/docs` for Swagger UI.

**Learn more:** [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

---

### 🐳 Docker — Containerization

**What:** Docker packages your app + its dependencies into a portable "container" that runs the same everywhere.
**Why we use it:** So our app runs identically on your laptop, in Jenkins, and on Kubernetes.

**Key concepts:**
- **Dockerfile** — Recipe for building a container image
- **Image** — A snapshot of your app (like a template)
- **Container** — A running instance of an image
- **Docker Hub** — A registry where you store/share images (like GitHub for containers)

```dockerfile
# Example Dockerfile for a Python app
FROM python:3.11-slim          # Start from a Python base image
WORKDIR /app                   # Set working directory
COPY requirements.txt .        # Copy dependency list
RUN pip install -r requirements.txt  # Install dependencies
COPY . .                       # Copy app code
EXPOSE 8000                    # Document the port
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Key commands:**
```bash
docker build -t myapp:v1 .           # Build image
docker run -p 8000:8000 myapp:v1     # Run container
docker images                         # List images
docker ps                             # List running containers
docker push username/myapp:v1         # Push to Docker Hub
```

---

### 🐙 Docker Compose — Multi-Container Local Dev

**What:** A tool to run multiple Docker containers together with one command.
**Why we use it:** To run Flask + FastAPI + PostgreSQL + Simulator locally without Kubernetes.

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/soc_db
    depends_on:
      - db

  dashboard:
    build: ./app
    ports:
      - "5000:5000"
    environment:
      - API_URL=http://api:8000
    depends_on:
      - api

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=soc_db
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

**Key commands:**
```bash
docker-compose up -d          # Start all services in background
docker-compose down            # Stop all services
docker-compose logs -f api     # Follow logs from api service
docker-compose ps              # Show service status
```

---

### ☸️ Kubernetes (K8s) — Container Orchestration

**What:** Kubernetes manages containers at scale — scheduling, scaling, self-healing, networking.
**Why we use it:** To deploy our app in a production-like environment with auto-scaling and self-healing.

**Key concepts:**

| Concept | What it is | Analogy |
|---------|------------|---------|
| **Pod** | Smallest unit, runs 1+ containers | A single instance of your app |
| **Deployment** | Manages a set of identical pods | "I want 3 copies of my app running" |
| **Service** | Stable network endpoint for pods | A phone number that always reaches someone |
| **Ingress** | Routes external traffic to services | A receptionist directing visitors |
| **ConfigMap** | Non-sensitive configuration | App settings file |
| **Secret** | Sensitive data (passwords, keys) | Password vault |
| **StatefulSet** | For stateful apps (databases) | Database that remembers data across restarts |
| **PVC** | Persistent Volume Claim (disk) | External hard drive for your pod |
| **HPA** | Horizontal Pod Autoscaler | Auto-adds more pods when CPU is high |
| **CronJob** | Scheduled task | Like cron on Linux, but for K8s |
| **Namespace** | Logical isolation | Folders to organize your resources |

**Example deployment YAML:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-backend
  namespace: soc-app
spec:
  replicas: 2                    # Run 2 copies
  selector:
    matchLabels:
      app: fastapi-backend
  template:
    metadata:
      labels:
        app: fastapi-backend
    spec:
      containers:
      - name: fastapi
        image: yourusername/soc-api:v1
        ports:
        - containerPort: 8000
        livenessProbe:           # K8s checks if app is alive
          httpGet:
            path: /api/health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:          # K8s checks if app is ready for traffic
          httpGet:
            path: /api/ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "256Mi"
```

**Key commands:**
```bash
kubectl get pods -n soc-app            # List pods
kubectl get svc -n soc-app             # List services
kubectl logs <pod-name> -n soc-app     # View logs
kubectl describe pod <pod-name>        # Debug a pod
kubectl apply -f k8s/                  # Apply all YAML files
kubectl delete -f k8s/                 # Delete all resources
kubectl rollout undo deployment/fastapi-backend  # Rollback
kubectl scale deployment fastapi-backend --replicas=3  # Scale
```

---

### 🔧 Jenkins — CI/CD Pipeline

**What:** Jenkins automates building, testing, and deploying your code every time you push.
**Why we use it:** Exam requires Jenkins. It runs our pipeline: clone → build → test → scan → docker push → deploy to K8s.

**Key concept — Jenkinsfile:**
A `Jenkinsfile` defines your pipeline as code (committed to your repo).

```groovy
pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/you/soc-automation-platform.git'
            }
        }
        stage('Build') {
            steps {
                sh 'pip install -r api/requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'cd api && pytest tests/ -v'
            }
        }
        stage('Lint') {
            steps {
                sh 'flake8 api/ --max-line-length=120'
            }
        }
        stage('Security Scan') {
            steps {
                sh 'bandit -r api/ -f json -o bandit-report.json || true'
            }
        }
        stage('Docker Build & Push') {
            steps {
                sh 'docker build -t yourusername/soc-api:${BUILD_NUMBER} ./api'
                sh 'docker push yourusername/soc-api:${BUILD_NUMBER}'
            }
        }
        stage('Deploy to K8s') {
            steps {
                sh 'kubectl set image deployment/fastapi-backend fastapi=yourusername/soc-api:${BUILD_NUMBER} -n soc-app'
            }
        }
    }
    post {
        success { echo 'Pipeline completed successfully!' }
        failure { echo 'Pipeline failed!' }
    }
}
```

---

### 🏗️ Terraform — Infrastructure as Code (IaC)

**What:** Terraform lets you define infrastructure (VMs, networks, K8s clusters) in code files, then create/destroy it with one command.
**Why we use it:** Instead of clicking through cloud consoles, we write `.tf` files. Reproducible, version-controlled, auditable.

**Key concepts:**
- **Provider** — Which cloud (AWS, GCP, Azure, or local)
- **Resource** — A thing to create (VM, network, bucket)
- **Module** — Reusable group of resources
- **State** — Terraform tracks what it has created (in `terraform.tfstate`)
- **Plan** — Preview what will change before applying
- **Apply** — Actually create/modify the infrastructure

```hcl
# main.tf
provider "aws" {
  region = var.region
}

resource "aws_instance" "soc_server" {
  ami           = "ami-0abcdef1234567890"
  instance_type = var.instance_type

  tags = {
    Name = "soc-automation-server"
    Project = "SOC-DevOps-Exam"
  }
}

# variables.tf
variable "region" {
  default = "ap-south-1"
}

variable "instance_type" {
  default = "t2.medium"
}

# outputs.tf
output "server_ip" {
  value = aws_instance.soc_server.public_ip
}
```

**Key commands:**
```bash
terraform init       # Download provider plugins
terraform plan       # Preview changes (dry run)
terraform apply      # Create/update infrastructure
terraform destroy    # Tear down everything
terraform state list # List managed resources
```

---

### 📊 Prometheus + Grafana — Monitoring

**Prometheus** — Collects metrics (numbers) from your application at regular intervals (scraping).
**Grafana** — Beautiful dashboards to visualize those metrics.

**How it works:**
1. Your FastAPI app exposes a `/metrics` endpoint with numbers like `http_requests_total=1542`
2. Prometheus scrapes that endpoint every 15 seconds
3. Grafana queries Prometheus and draws graphs

**Adding metrics to FastAPI:**
```python
# In your FastAPI app
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)  # Adds /metrics endpoint
```

**What you'll monitor:**
- Request rate (requests per second)
- Error rate (% of requests returning 5xx)
- Latency (how long requests take)
- Pod CPU and memory usage
- Alert counts by severity (custom business metric)

---

### 📝 ELK Stack — Centralized Logging

**E** = **Elasticsearch** — Stores and indexes logs (searchable database for text)
**L** = **Logstash** — Collects, transforms, and sends logs to Elasticsearch
**K** = **Kibana** — Web UI to search and visualize logs

**How it works:**
1. Your Flask and FastAPI apps print logs to stdout in JSON format
2. Logstash (or Filebeat) collects those logs from K8s pods
3. Logstash sends them to Elasticsearch
4. You search and visualize in Kibana

**JSON structured logging in Python:**
```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "service": "fastapi-backend",
            "message": record.getMessage(),
            "module": record.module
        }
        return json.dumps(log_data)

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger("soc")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Usage
logger.info("Alert created", extra={"alert_id": 42, "severity": "high"})
# Output: {"timestamp": "2026-06-16 10:30:00", "level": "INFO", "service": "fastapi-backend", "message": "Alert created"}
```

---

### 🔐 HashiCorp Vault — Secret Management

**What:** Vault stores secrets (passwords, API keys, certificates) securely, so you never hardcode them.
**Why:** Putting `DB_PASSWORD=mysecret123` in your code or environment variables is a security risk. Vault stores them encrypted and provides them to your app at runtime.

**How it works:**
1. You store a secret in Vault: `vault kv put secret/soc-app db_password=supersecret`
2. Your app fetches it at startup: `vault kv get secret/soc-app`
3. Or, in K8s, the Vault sidecar injects secrets as files/env vars into your pods

**Key commands:**
```bash
vault server -dev                              # Start in dev mode
export VAULT_ADDR='http://127.0.0.1:8200'
vault kv put secret/soc-app db_password=supersecret jwt_secret=mykey123
vault kv get secret/soc-app                    # Retrieve secrets
vault kv list secret/                          # List all secret paths
```

---

## 3. Prerequisites & Local Setup

### What You Need Installed

| Tool | Install Command (Mac) | Verify |
|------|----------------------|--------|
| **Python 3.11+** | `brew install python@3.11` | `python3 --version` |
| **pip** | Comes with Python | `pip3 --version` |
| **Docker Desktop** | [Download](https://www.docker.com/products/docker-desktop/) | `docker --version` |
| **kubectl** | `brew install kubectl` | `kubectl version --client` |
| **Minikube** | `brew install minikube` | `minikube version` |
| **Terraform** | `brew install terraform` | `terraform --version` |
| **Jenkins** | Run as Docker container (see Step 8) | — |
| **Vault** | `brew install vault` | `vault --version` |
| **Git** | `brew install git` | `git --version` |
| **Helm** (optional) | `brew install helm` | `helm version` |

### Start Minikube (K8s locally)

```bash
# Start Minikube with enough resources
minikube start --cpus=4 --memory=8192 --driver=docker

# Verify
kubectl cluster-info
kubectl get nodes
```

> ⚠️ **Resource Warning:** The full stack (app + monitoring + logging + vault) needs at least **8GB RAM** and **4 CPUs** allocated to Minikube. If your machine has less, reduce replica counts to 1 and skip the ELK stack during initial development.

---

## Step 1 — Build the FastAPI Backend

### 1.1 Create the project structure

```bash
mkdir -p soc-automation-platform/api/routes
mkdir -p soc-automation-platform/api/services
mkdir -p soc-automation-platform/api/tests
cd soc-automation-platform
```

### 1.2 Create `api/requirements.txt`

```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.2
python-jose==3.3.0
passlib==1.7.4
bcrypt==4.1.2
prometheus-fastapi-instrumentator==6.1.0
python-json-logger==2.0.7
pytest==7.4.3
httpx==0.25.2
```

### 1.3 Create `api/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./soc.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 1.4 Create `api/models.py`

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    severity = Column(Enum("critical", "high", "medium", "low", name="severity_enum"), default="medium")
    status = Column(Enum("open", "in_progress", "closed", name="status_enum"), default="open")
    source = Column(String(100))
    source_ip = Column(String(45))
    dest_ip = Column(String(45))
    alert_type = Column(String(50))
    assigned_to = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    closed_at = Column(DateTime, nullable=True)

class PlaybookLog(Base):
    __tablename__ = "playbook_logs"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"))
    action = Column(String(50))
    status = Column(Enum("success", "failed", name="playbook_status_enum"), default="success")
    details = Column(Text)
    executed_at = Column(DateTime, server_default=func.now())
```

### 1.5 Create `api/schemas.py`

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AlertCreate(BaseModel):
    title: str
    description: Optional[str] = None
    severity: str = "medium"
    source: Optional[str] = None
    source_ip: Optional[str] = None
    dest_ip: Optional[str] = None
    alert_type: Optional[str] = None

class AlertUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[str] = None

class AlertResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    severity: str
    status: str
    source: Optional[str]
    source_ip: Optional[str]
    dest_ip: Optional[str]
    alert_type: Optional[str]
    assigned_to: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PlaybookRequest(BaseModel):
    action: str  # "block_ip", "isolate_host", "notify_team"

class StatsResponse(BaseModel):
    total_alerts: int
    open_alerts: int
    in_progress_alerts: int
    closed_alerts: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
```

### 1.6 Create `api/main.py`

```python
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from prometheus_fastapi_instrumentator import Instrumentator
from database import engine, get_db, Base
from models import Alert, PlaybookLog
from schemas import AlertCreate, AlertUpdate, AlertResponse, PlaybookRequest, StatsResponse
from typing import List, Optional
import logging

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SOC Automation API",
    description="Security Operations Center Alert Management API",
    version="1.0.0"
)

# Add Prometheus metrics
Instrumentator().instrument(app).expose(app)

# Logger
logger = logging.getLogger("soc-api")
logging.basicConfig(level=logging.INFO)


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}


@app.get("/api/ready")
def readiness_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "ready"}
    except Exception:
        raise HTTPException(status_code=503, detail="Database not ready")


@app.get("/api/alerts", response_model=List[AlertResponse])
def list_alerts(
    severity: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Alert)
    if severity:
        query = query.filter(Alert.severity == severity)
    if status:
        query = query.filter(Alert.status == status)
    alerts = query.order_by(Alert.created_at.desc()).offset(skip).limit(limit).all()
    logger.info(f"Listed {len(alerts)} alerts")
    return alerts


@app.get("/api/alerts/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    total = db.query(Alert).count()
    return StatsResponse(
        total_alerts=total,
        open_alerts=db.query(Alert).filter(Alert.status == "open").count(),
        in_progress_alerts=db.query(Alert).filter(Alert.status == "in_progress").count(),
        closed_alerts=db.query(Alert).filter(Alert.status == "closed").count(),
        critical_count=db.query(Alert).filter(Alert.severity == "critical").count(),
        high_count=db.query(Alert).filter(Alert.severity == "high").count(),
        medium_count=db.query(Alert).filter(Alert.severity == "medium").count(),
        low_count=db.query(Alert).filter(Alert.severity == "low").count(),
    )


@app.get("/api/alerts/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@app.post("/api/alerts", response_model=AlertResponse, status_code=201)
def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    db_alert = Alert(**alert.model_dump())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    logger.info(f"Created alert: {db_alert.id} - {db_alert.title}")
    return db_alert


@app.put("/api/alerts/{alert_id}", response_model=AlertResponse)
def update_alert(alert_id: int, alert: AlertUpdate, db: Session = Depends(get_db)):
    db_alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    if alert.status:
        db_alert.status = alert.status
    if alert.assigned_to:
        db_alert.assigned_to = alert.assigned_to
    db.commit()
    db.refresh(db_alert)
    logger.info(f"Updated alert {alert_id}: status={alert.status}")
    return db_alert


@app.delete("/api/alerts/{alert_id}", status_code=204)
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    db_alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    db.delete(db_alert)
    db.commit()
    logger.info(f"Deleted alert {alert_id}")


@app.post("/api/alerts/{alert_id}/respond")
def execute_playbook(alert_id: int, request: PlaybookRequest, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    # Mock playbook execution
    action_results = {
        "block_ip": f"Blocked IP {alert.source_ip} on firewall",
        "isolate_host": f"Isolated host {alert.dest_ip} from network",
        "notify_team": f"Notification sent to SOC team about alert {alert_id}"
    }
    result = action_results.get(request.action, f"Unknown action: {request.action}")

    log = PlaybookLog(
        alert_id=alert_id,
        action=request.action,
        status="success",
        details=result
    )
    db.add(log)
    alert.status = "in_progress"
    db.commit()

    logger.info(f"Playbook executed: {request.action} for alert {alert_id}")
    return {"alert_id": alert_id, "action": request.action, "result": result, "status": "success"}


@app.get("/api/playbook-logs")
def list_playbook_logs(db: Session = Depends(get_db)):
    logs = db.query(PlaybookLog).order_by(PlaybookLog.executed_at.desc()).limit(50).all()
    return logs
```

### 1.7 Run it locally

```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Test it:**
- Open `http://localhost:8000/docs` → Swagger UI
- Open `http://localhost:8000/api/health` → `{"status": "healthy"}`
- Open `http://localhost:8000/metrics` → Prometheus metrics

✅ **Checkpoint:** Your API is running. You can create, read, update, and delete alerts via Swagger.

---

## Step 2 — Build the Flask Dashboard

### 2.1 Create the project structure

```bash
mkdir -p app/templates app/static/css app/static/js app/tests
```

### 2.2 Create `app/requirements.txt`

```
flask==3.0.0
requests==2.31.0
python-dotenv==1.0.0
pytest==7.4.3
```

### 2.3 Create `app/app.py`

```python
from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "dev-secret-key")
API_URL = os.getenv("API_URL", "http://localhost:8000")


@app.route("/")
def dashboard():
    severity = request.args.get("severity", "")
    status = request.args.get("status", "")

    params = {}
    if severity:
        params["severity"] = severity
    if status:
        params["status"] = status

    try:
        alerts = requests.get(f"{API_URL}/api/alerts", params=params, timeout=5).json()
        stats = requests.get(f"{API_URL}/api/alerts/stats", timeout=5).json()
    except requests.exceptions.ConnectionError:
        alerts = []
        stats = {"total_alerts": 0, "open_alerts": 0, "in_progress_alerts": 0,
                 "closed_alerts": 0, "critical_count": 0, "high_count": 0,
                 "medium_count": 0, "low_count": 0}
        flash("⚠️ Cannot connect to API backend", "warning")

    return render_template("dashboard.html", alerts=alerts, stats=stats,
                           current_severity=severity, current_status=status)


@app.route("/alert/<int:alert_id>")
def alert_detail(alert_id):
    try:
        alert = requests.get(f"{API_URL}/api/alerts/{alert_id}", timeout=5).json()
    except Exception:
        flash("Alert not found", "error")
        return redirect(url_for("dashboard"))
    return render_template("alert_detail.html", alert=alert)


@app.route("/alert/<int:alert_id>/triage", methods=["POST"])
def triage_alert(alert_id):
    action = request.form.get("action")
    if action in ["acknowledge", "escalate", "close"]:
        status_map = {"acknowledge": "in_progress", "escalate": "in_progress", "close": "closed"}
        requests.put(f"{API_URL}/api/alerts/{alert_id}",
                     json={"status": status_map[action]}, timeout=5)
        flash(f"Alert {alert_id} → {action}", "success")
    return redirect(url_for("dashboard"))


@app.route("/alert/<int:alert_id>/respond", methods=["POST"])
def respond_to_alert(alert_id):
    playbook_action = request.form.get("playbook_action")
    try:
        result = requests.post(f"{API_URL}/api/alerts/{alert_id}/respond",
                               json={"action": playbook_action}, timeout=5).json()
        flash(f"✅ {result['result']}", "success")
    except Exception as e:
        flash(f"❌ Playbook failed: {e}", "error")
    return redirect(url_for("alert_detail", alert_id=alert_id))


@app.route("/playbook-logs")
def playbook_logs():
    try:
        logs = requests.get(f"{API_URL}/api/playbook-logs", timeout=5).json()
    except Exception:
        logs = []
    return render_template("playbook_logs.html", logs=logs)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
```

### 2.4 Create `app/templates/base.html`

```html
<!DOCTYPE html>
<html lang="en" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}SOC Dashboard{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark border-bottom border-secondary">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">🛡️ SOC Dashboard</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Alerts</a>
                <a class="nav-link" href="/playbook-logs">Playbook Logs</a>
            </div>
        </div>
    </nav>

    <div class="container-fluid mt-3">
        {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
        {% for category, message in messages %}
        <div class="alert alert-{{ 'success' if category == 'success' else 'warning' }} alert-dismissible fade show">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
        {% endfor %}
        {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### 2.5 Create `app/templates/dashboard.html`

```html
{% extends "base.html" %}
{% block content %}
<!-- Stats Cards -->
<div class="row mb-4">
    <div class="col-md-3">
        <div class="card bg-dark border-info text-center">
            <div class="card-body">
                <h2>{{ stats.total_alerts }}</h2>
                <p class="text-muted">Total Alerts</p>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card bg-dark border-danger text-center">
            <div class="card-body">
                <h2 class="text-danger">{{ stats.open_alerts }}</h2>
                <p class="text-muted">Open</p>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card bg-dark border-warning text-center">
            <div class="card-body">
                <h2 class="text-warning">{{ stats.in_progress_alerts }}</h2>
                <p class="text-muted">In Progress</p>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card bg-dark border-success text-center">
            <div class="card-body">
                <h2 class="text-success">{{ stats.closed_alerts }}</h2>
                <p class="text-muted">Closed</p>
            </div>
        </div>
    </div>
</div>

<!-- Filters -->
<div class="row mb-3">
    <div class="col-md-6">
        <form method="GET" class="d-flex gap-2">
            <select name="severity" class="form-select form-select-sm w-auto">
                <option value="">All Severities</option>
                <option value="critical" {% if current_severity=='critical' %}selected{% endif %}>🔴 Critical</option>
                <option value="high" {% if current_severity=='high' %}selected{% endif %}>🟠 High</option>
                <option value="medium" {% if current_severity=='medium' %}selected{% endif %}>🟡 Medium</option>
                <option value="low" {% if current_severity=='low' %}selected{% endif %}>🔵 Low</option>
            </select>
            <select name="status" class="form-select form-select-sm w-auto">
                <option value="">All Statuses</option>
                <option value="open" {% if current_status=='open' %}selected{% endif %}>Open</option>
                <option value="in_progress" {% if current_status=='in_progress' %}selected{% endif %}>In Progress</option>
                <option value="closed" {% if current_status=='closed' %}selected{% endif %}>Closed</option>
            </select>
            <button type="submit" class="btn btn-sm btn-outline-light">Filter</button>
        </form>
    </div>
</div>

<!-- Alert Table -->
<table class="table table-dark table-striped table-hover">
    <thead>
        <tr>
            <th>ID</th>
            <th>Severity</th>
            <th>Title</th>
            <th>Source IP</th>
            <th>Type</th>
            <th>Status</th>
            <th>Created</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for alert in alerts %}
        <tr>
            <td>{{ alert.id }}</td>
            <td>
                {% if alert.severity == 'critical' %}<span class="badge bg-danger">CRITICAL</span>
                {% elif alert.severity == 'high' %}<span class="badge bg-warning text-dark">HIGH</span>
                {% elif alert.severity == 'medium' %}<span class="badge bg-info">MEDIUM</span>
                {% else %}<span class="badge bg-secondary">LOW</span>{% endif %}
            </td>
            <td><a href="/alert/{{ alert.id }}">{{ alert.title }}</a></td>
            <td><code>{{ alert.source_ip or '—' }}</code></td>
            <td>{{ alert.alert_type or '—' }}</td>
            <td>
                {% if alert.status == 'open' %}<span class="badge bg-danger">Open</span>
                {% elif alert.status == 'in_progress' %}<span class="badge bg-warning text-dark">In Progress</span>
                {% else %}<span class="badge bg-success">Closed</span>{% endif %}
            </td>
            <td>{{ alert.created_at[:16] }}</td>
            <td>
                <form method="POST" action="/alert/{{ alert.id }}/triage" class="d-inline">
                    <button name="action" value="acknowledge" class="btn btn-sm btn-outline-warning">Ack</button>
                    <button name="action" value="close" class="btn btn-sm btn-outline-success">Close</button>
                </form>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

### 2.6 Create `app/templates/alert_detail.html`

```html
{% extends "base.html" %}
{% block title %}Alert #{{ alert.id }}{% endblock %}
{% block content %}
<div class="row">
    <div class="col-md-8">
        <div class="card bg-dark border-secondary">
            <div class="card-header d-flex justify-content-between">
                <h4>Alert #{{ alert.id }}: {{ alert.title }}</h4>
                {% if alert.severity == 'critical' %}<span class="badge bg-danger fs-6">CRITICAL</span>
                {% elif alert.severity == 'high' %}<span class="badge bg-warning text-dark fs-6">HIGH</span>
                {% elif alert.severity == 'medium' %}<span class="badge bg-info fs-6">MEDIUM</span>
                {% else %}<span class="badge bg-secondary fs-6">LOW</span>{% endif %}
            </div>
            <div class="card-body">
                <p><strong>Description:</strong> {{ alert.description or 'No description' }}</p>
                <p><strong>Source:</strong> {{ alert.source or '—' }}</p>
                <p><strong>Source IP:</strong> <code>{{ alert.source_ip or '—' }}</code></p>
                <p><strong>Destination IP:</strong> <code>{{ alert.dest_ip or '—' }}</code></p>
                <p><strong>Type:</strong> {{ alert.alert_type or '—' }}</p>
                <p><strong>Status:</strong> {{ alert.status }}</p>
                <p><strong>Assigned To:</strong> {{ alert.assigned_to or 'Unassigned' }}</p>
                <p><strong>Created:</strong> {{ alert.created_at }}</p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card bg-dark border-secondary">
            <div class="card-header"><h5>🎯 Triage Actions</h5></div>
            <div class="card-body">
                <form method="POST" action="/alert/{{ alert.id }}/triage">
                    <button name="action" value="acknowledge" class="btn btn-warning w-100 mb-2">Acknowledge</button>
                    <button name="action" value="escalate" class="btn btn-danger w-100 mb-2">Escalate</button>
                    <button name="action" value="close" class="btn btn-success w-100">Close</button>
                </form>
            </div>
        </div>
        <div class="card bg-dark border-secondary mt-3">
            <div class="card-header"><h5>⚡ Run Playbook</h5></div>
            <div class="card-body">
                <form method="POST" action="/alert/{{ alert.id }}/respond">
                    <button name="playbook_action" value="block_ip" class="btn btn-outline-danger w-100 mb-2">🚫 Block IP</button>
                    <button name="playbook_action" value="isolate_host" class="btn btn-outline-warning w-100 mb-2">🔒 Isolate Host</button>
                    <button name="playbook_action" value="notify_team" class="btn btn-outline-info w-100">📢 Notify Team</button>
                </form>
            </div>
        </div>
    </div>
</div>
<a href="/" class="btn btn-outline-light mt-3">← Back to Dashboard</a>
{% endblock %}
```

### 2.7 Create `app/templates/playbook_logs.html`

```html
{% extends "base.html" %}
{% block title %}Playbook Logs{% endblock %}
{% block content %}
<h3>📋 Playbook Execution Logs</h3>
<table class="table table-dark table-striped">
    <thead>
        <tr><th>ID</th><th>Alert ID</th><th>Action</th><th>Status</th><th>Details</th><th>Executed At</th></tr>
    </thead>
    <tbody>
        {% for log in logs %}
        <tr>
            <td>{{ log.id }}</td>
            <td><a href="/alert/{{ log.alert_id }}">{{ log.alert_id }}</a></td>
            <td>{{ log.action }}</td>
            <td><span class="badge bg-{{ 'success' if log.status == 'success' else 'danger' }}">{{ log.status }}</span></td>
            <td>{{ log.details }}</td>
            <td>{{ log.executed_at }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

### 2.8 Create `app/static/css/style.css`

```css
body { background-color: #1a1a2e; }
.card { transition: transform 0.2s; }
.card:hover { transform: translateY(-2px); }
.table a { color: #7dd3fc; text-decoration: none; }
.table a:hover { text-decoration: underline; }
code { color: #f472b6; }
```

### 2.9 Run it

```bash
cd app
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000` → Your SOC Dashboard is running!

✅ **Checkpoint:** Both Flask + FastAPI apps running locally. Dashboard shows alerts from the API.

---

## Step 3 — Build the Alert Simulator

### 3.1 Create `simulator/simulator.py`

```python
import requests
import random
import time
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

ALERT_TEMPLATES = [
    {"title": "Brute force login attempt", "alert_type": "brute_force", "severity": "high",
     "source": "SIEM-Splunk", "description": "Multiple failed login attempts detected from single IP"},
    {"title": "Malware detected on endpoint", "alert_type": "malware", "severity": "critical",
     "source": "EDR-CrowdStrike", "description": "Known ransomware signature detected on workstation"},
    {"title": "Phishing email reported", "alert_type": "phishing", "severity": "medium",
     "source": "Email-Gateway", "description": "User reported suspicious email with malicious link"},
    {"title": "Port scan detected", "alert_type": "port_scan", "severity": "low",
     "source": "SIEM-QRadar", "description": "Sequential port scanning activity from external IP"},
    {"title": "Privilege escalation attempt", "alert_type": "priv_escalation", "severity": "critical",
     "source": "EDR-SentinelOne", "description": "Unauthorized sudo usage detected on production server"},
    {"title": "Data exfiltration suspected", "alert_type": "data_exfil", "severity": "high",
     "source": "DLP-System", "description": "Large volume of data transferred to external IP"},
    {"title": "Unauthorized access to admin panel", "alert_type": "unauth_access", "severity": "high",
     "source": "WAF", "description": "Multiple 403 errors followed by successful admin login"},
    {"title": "DNS tunneling detected", "alert_type": "dns_tunnel", "severity": "medium",
     "source": "SIEM-Splunk", "description": "Unusual DNS query patterns suggesting data exfiltration"},
]

def random_ip():
    return f"{random.randint(1,254)}.{random.randint(0,254)}.{random.randint(0,254)}.{random.randint(1,254)}"

def generate_alert():
    template = random.choice(ALERT_TEMPLATES)
    alert = {
        **template,
        "source_ip": random_ip(),
        "dest_ip": f"10.0.{random.randint(1,10)}.{random.randint(1,254)}",
    }
    try:
        resp = requests.post(f"{API_URL}/api/alerts", json=alert, timeout=5)
        print(f"✅ Alert created: [{alert['severity'].upper()}] {alert['title']} (status: {resp.status_code})")
    except Exception as e:
        print(f"❌ Failed to create alert: {e}")

if __name__ == "__main__":
    interval = int(os.getenv("INTERVAL_SECONDS", "30"))
    print(f"🚨 Alert Simulator started. Generating alerts every {interval}s...")
    while True:
        generate_alert()
        time.sleep(interval)
```

### 3.2 Run it

```bash
cd simulator
pip install requests
python simulator.py
```

✅ **Checkpoint:** Simulator creates fake alerts every 30 seconds. Dashboard shows new alerts appearing.

---

## Step 4 — Dockerize Everything

### 4.1 Create `api/Dockerfile`

```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4.2 Create `app/Dockerfile`

```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 5000
CMD ["python", "app.py"]
```

### 4.3 Create `simulator/Dockerfile`

```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir requests
COPY simulator.py .
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser
CMD ["python", "simulator.py"]
```

### 4.4 Create `docker-compose.yml` (project root)

```yaml
version: '3.8'
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: socuser
      POSTGRES_PASSWORD: socpass123
      POSTGRES_DB: soc_db
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U socuser -d soc_db"]
      interval: 10s
      retries: 5

  api:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: "postgresql://socuser:socpass123@db:5432/soc_db"
    depends_on:
      db:
        condition: service_healthy

  dashboard:
    build: ./app
    ports:
      - "5000:5000"
    environment:
      API_URL: "http://api:8000"
    depends_on:
      - api

  simulator:
    build: ./simulator
    environment:
      API_URL: "http://api:8000"
      INTERVAL_SECONDS: "30"
    depends_on:
      - api

volumes:
  pgdata:
```

### 4.5 Build and run

```bash
# Build all images
docker-compose build

# Start everything
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f api

# Stop everything
docker-compose down
```

### 4.6 Push images to Docker Hub

```bash
# Login to Docker Hub
docker login

# Tag and push
docker tag soc-automation-platform-api:latest yourusername/soc-api:v1
docker tag soc-automation-platform-dashboard:latest yourusername/soc-dashboard:v1
docker tag soc-automation-platform-simulator:latest yourusername/soc-simulator:v1

docker push yourusername/soc-api:v1
docker push yourusername/soc-dashboard:v1
docker push yourusername/soc-simulator:v1
```

✅ **Checkpoint:** Everything runs with `docker-compose up`. Images pushed to Docker Hub.

---

## Step 5 — Push to GitHub

```bash
# Initialize repo
cd soc-automation-platform
git init
git branch -M main

# Create .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.pyo
.env
*.db
.pytest_cache/
venv/
.idea/
.vscode/
*.egg-info/
dist/
build/
terraform/.terraform/
terraform/*.tfstate*
EOF

# Add and commit
git add .
git commit -m "feat: initial SOC automation platform with Flask + FastAPI"

# Create GitHub repo and push
git remote add origin https://github.com/yourusername/soc-automation-platform.git
git push -u origin main

# Create dev branch
git checkout -b dev
git push -u origin dev
```

✅ **Checkpoint:** Code on GitHub with `main` and `dev` branches.

---

## Step 6 — Write Terraform Scripts

### 6.1 Create `terraform/main.tf`

```hcl
# For local Minikube, Terraform provisions a Docker-based environment.
# For cloud (AWS example), this would provision an EKS cluster.

terraform {
  required_version = ">= 1.0"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

# Pull PostgreSQL image
resource "docker_image" "postgres" {
  name         = "postgres:15-alpine"
  keep_locally = true
}

# Create Docker network
resource "docker_network" "soc_network" {
  name = "soc-network"
}

# Run PostgreSQL container
resource "docker_container" "postgres" {
  name  = "soc-postgres"
  image = docker_image.postgres.image_id

  env = [
    "POSTGRES_USER=${var.db_user}",
    "POSTGRES_PASSWORD=${var.db_password}",
    "POSTGRES_DB=${var.db_name}"
  ]

  ports {
    internal = 5432
    external = var.db_port
  }

  networks_advanced {
    name = docker_network.soc_network.name
  }

  volumes {
    volume_name    = docker_volume.pgdata.name
    container_path = "/var/lib/postgresql/data"
  }
}

resource "docker_volume" "pgdata" {
  name = "soc-pgdata"
}
```

### 6.2 Create `terraform/variables.tf`

```hcl
variable "db_user" {
  description = "PostgreSQL username"
  type        = string
  default     = "socuser"
}

variable "db_password" {
  description = "PostgreSQL password"
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "PostgreSQL database name"
  type        = string
  default     = "soc_db"
}

variable "db_port" {
  description = "PostgreSQL external port"
  type        = number
  default     = 5432
}
```

### 6.3 Create `terraform/outputs.tf`

```hcl
output "database_host" {
  value = docker_container.postgres.name
}

output "database_port" {
  value = var.db_port
}

output "network_name" {
  value = docker_network.soc_network.name
}
```

### 6.4 Create `terraform/terraform.tfvars`

```hcl
db_user     = "socuser"
db_password = "socpass123"
db_name     = "soc_db"
db_port     = 5432
```

### 6.5 Run Terraform

```bash
cd terraform
terraform init        # Download providers
terraform plan        # Preview changes
terraform apply       # Create infrastructure (type 'yes')
terraform show        # View current state
terraform destroy     # Tear down everything
```

✅ **Checkpoint:** Terraform provisions infrastructure. `terraform plan` shows changes before applying.

---

## Step 7 — Deploy on Kubernetes

### 7.1 Create Namespaces — `k8s/namespaces/namespaces.yaml`

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: soc-app
---
apiVersion: v1
kind: Namespace
metadata:
  name: monitoring
---
apiVersion: v1
kind: Namespace
metadata:
  name: logging
---
apiVersion: v1
kind: Namespace
metadata:
  name: vault
```

### 7.2 Create ConfigMap — `k8s/app/configmap.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: soc-app
data:
  API_URL: "http://fastapi-service:8000"
  FLASK_ENV: "production"
  LOG_LEVEL: "INFO"
```

### 7.3 Create Secrets — `k8s/app/secrets.yaml`

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
  namespace: soc-app
type: Opaque
stringData:
  DATABASE_URL: "postgresql://socuser:socpass123@postgres-service:5432/soc_db"
  FLASK_SECRET: "super-secret-key-change-me"
```

> ⚠️ In production, secrets should come from Vault. For initial setup, this is fine.

### 7.4 Create PostgreSQL — `k8s/database/postgres.yaml`

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: soc-app
spec:
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 5Gi
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgresql
  namespace: soc-app
spec:
  serviceName: postgres-service
  replicas: 1
  selector:
    matchLabels:
      app: postgresql
  template:
    metadata:
      labels:
        app: postgresql
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_USER
          value: "socuser"
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: FLASK_SECRET
        - name: POSTGRES_DB
          value: "soc_db"
        volumeMounts:
        - name: pgdata
          mountPath: /var/lib/postgresql/data
        resources:
          requests: { cpu: "250m", memory: "256Mi" }
          limits: { cpu: "500m", memory: "512Mi" }
      volumes:
      - name: pgdata
        persistentVolumeClaim:
          claimName: postgres-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
  namespace: soc-app
spec:
  selector:
    app: postgresql
  ports:
  - port: 5432
    targetPort: 5432
  clusterIP: None
```

### 7.5 Create FastAPI Deployment — `k8s/app/fastapi-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-backend
  namespace: soc-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: fastapi-backend
  template:
    metadata:
      labels:
        app: fastapi-backend
    spec:
      containers:
      - name: fastapi
        image: yourusername/soc-api:v1
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: DATABASE_URL
        livenessProbe:
          httpGet: { path: /api/health, port: 8000 }
          initialDelaySeconds: 15
          periodSeconds: 30
        readinessProbe:
          httpGet: { path: /api/ready, port: 8000 }
          initialDelaySeconds: 5
          periodSeconds: 10
        resources:
          requests: { cpu: "100m", memory: "128Mi" }
          limits: { cpu: "500m", memory: "256Mi" }
---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
  namespace: soc-app
spec:
  selector:
    app: fastapi-backend
  ports:
  - port: 8000
    targetPort: 8000
```

### 7.6 Create Flask Deployment — `k8s/app/flask-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-dashboard
  namespace: soc-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask-dashboard
  template:
    metadata:
      labels:
        app: flask-dashboard
    spec:
      containers:
      - name: flask
        image: yourusername/soc-dashboard:v1
        ports:
        - containerPort: 5000
        envFrom:
        - configMapRef:
            name: app-config
        env:
        - name: FLASK_SECRET
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: FLASK_SECRET
        resources:
          requests: { cpu: "100m", memory: "128Mi" }
          limits: { cpu: "500m", memory: "256Mi" }
---
apiVersion: v1
kind: Service
metadata:
  name: flask-service
  namespace: soc-app
spec:
  selector:
    app: flask-dashboard
  ports:
  - port: 5000
    targetPort: 5000
```

### 7.7 Create Ingress — `k8s/app/ingress.yaml`

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: soc-ingress
  namespace: soc-app
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: flask-service
            port:
              number: 5000
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: fastapi-service
            port:
              number: 8000
```

### 7.8 Create HPA — `k8s/app/hpa.yaml`

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: fastapi-hpa
  namespace: soc-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fastapi-backend
  minReplicas: 2
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### 7.9 Create Simulator CronJob — `k8s/simulator/cronjob.yaml`

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: alert-simulator
  namespace: soc-app
spec:
  schedule: "*/2 * * * *"   # Every 2 minutes
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: simulator
            image: yourusername/soc-simulator:v1
            env:
            - name: API_URL
              value: "http://fastapi-service:8000"
            - name: INTERVAL_SECONDS
              value: "5"
          restartPolicy: OnFailure
```

### 7.10 Deploy everything

```bash
# Make sure Minikube is running
minikube start --cpus=4 --memory=8192

# Enable ingress addon
minikube addons enable ingress
minikube addons enable metrics-server   # For HPA

# Apply everything in order
kubectl apply -f k8s/namespaces/
kubectl apply -f k8s/app/secrets.yaml
kubectl apply -f k8s/app/configmap.yaml
kubectl apply -f k8s/database/
kubectl apply -f k8s/app/
kubectl apply -f k8s/simulator/

# Wait for pods to be ready
kubectl get pods -n soc-app -w

# Get the URL to access the app
minikube service flask-service -n soc-app --url
```

✅ **Checkpoint:** All pods running in K8s. Dashboard accessible via Minikube URL.

---

## Step 8 — Set Up Jenkins CI/CD

### 8.1 Run Jenkins as a Docker container

```bash
docker run -d \
  --name jenkins \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts
```

### 8.2 Get initial admin password

```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Open `http://localhost:8080`, paste the password, install suggested plugins.

### 8.3 Install required Jenkins plugins

Go to **Manage Jenkins → Plugins → Available** and install:
- Docker Pipeline
- Kubernetes CLI
- Git
- Pipeline

### 8.4 Create the `Jenkinsfile` (project root)

```groovy
pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = 'yourusername'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/yourusername/soc-automation-platform.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r api/requirements.txt'
                sh 'pip install -r app/requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'cd api && python -m pytest tests/ -v --tb=short'
            }
        }

        stage('Code Lint') {
            steps {
                sh 'pip install flake8'
                sh 'flake8 api/ --max-line-length=120 --exclude=__pycache__ || true'
            }
        }

        stage('Security Scan') {
            steps {
                sh 'pip install bandit'
                sh 'bandit -r api/ -f json -o bandit-report.json || true'
                sh 'echo "Security scan complete"'
            }
        }

        stage('Docker Build & Push') {
            steps {
                sh "docker build -t ${DOCKER_HUB_USER}/soc-api:${IMAGE_TAG} ./api"
                sh "docker build -t ${DOCKER_HUB_USER}/soc-dashboard:${IMAGE_TAG} ./app"
                sh "docker push ${DOCKER_HUB_USER}/soc-api:${IMAGE_TAG}"
                sh "docker push ${DOCKER_HUB_USER}/soc-dashboard:${IMAGE_TAG}"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh """
                    kubectl set image deployment/fastapi-backend \
                        fastapi=${DOCKER_HUB_USER}/soc-api:${IMAGE_TAG} \
                        -n soc-app
                    kubectl set image deployment/flask-dashboard \
                        flask=${DOCKER_HUB_USER}/soc-dashboard:${IMAGE_TAG} \
                        -n soc-app
                    kubectl rollout status deployment/fastapi-backend -n soc-app
                    kubectl rollout status deployment/flask-dashboard -n soc-app
                """
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}
```

### 8.5 Create a Jenkins Pipeline Job

1. Jenkins Dashboard → **New Item** → "soc-pipeline" → **Pipeline**
2. Under Pipeline section → **Pipeline script from SCM**
3. SCM: Git, URL: your GitHub repo
4. Branch: `*/main`
5. Script Path: `Jenkinsfile`
6. Save and click **Build Now**

✅ **Checkpoint:** Jenkins pipeline runs all stages: Clone → Build → Test → Scan → Docker → Deploy.

---

## Step 9 — Set Up Prometheus & Grafana

### 9.1 Create `monitoring/prometheus/prometheus-config.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
      - job_name: 'fastapi'
        static_configs:
          - targets: ['fastapi-service.soc-app.svc.cluster.local:8000']
      - job_name: 'kubernetes-pods'
        kubernetes_sd_configs:
          - role: pod
```

### 9.2 Create `monitoring/prometheus/prometheus-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
  namespace: monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
      - name: prometheus
        image: prom/prometheus:latest
        ports:
        - containerPort: 9090
        volumeMounts:
        - name: config
          mountPath: /etc/prometheus/prometheus.yml
          subPath: prometheus.yml
      volumes:
      - name: config
        configMap:
          name: prometheus-config
---
apiVersion: v1
kind: Service
metadata:
  name: prometheus-service
  namespace: monitoring
spec:
  selector:
    app: prometheus
  ports:
  - port: 9090
    targetPort: 9090
  type: NodePort
```

### 9.3 Create `monitoring/grafana/grafana-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
  namespace: monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grafana
  template:
    metadata:
      labels:
        app: grafana
    spec:
      containers:
      - name: grafana
        image: grafana/grafana:latest
        ports:
        - containerPort: 3000
        env:
        - name: GF_SECURITY_ADMIN_PASSWORD
          value: "admin123"
---
apiVersion: v1
kind: Service
metadata:
  name: grafana-service
  namespace: monitoring
spec:
  selector:
    app: grafana
  ports:
  - port: 3000
    targetPort: 3000
  type: NodePort
```

### 9.4 Deploy and access

```bash
kubectl apply -f monitoring/

# Get URLs
minikube service prometheus-service -n monitoring --url
minikube service grafana-service -n monitoring --url
```

**Grafana setup:**
1. Login with `admin` / `admin123`
2. Add Data Source → Prometheus → URL: `http://prometheus-service:9090`
3. Create Dashboard → Add panels for request rate, error rate, latency

✅ **Checkpoint:** Prometheus scraping metrics. Grafana showing dashboards.

---

## Step 10 — Set Up ELK Stack

### 10.1 Create `logging/elasticsearch/elasticsearch-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: elasticsearch
  namespace: logging
spec:
  replicas: 1
  selector:
    matchLabels:
      app: elasticsearch
  template:
    metadata:
      labels:
        app: elasticsearch
    spec:
      containers:
      - name: elasticsearch
        image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
        ports:
        - containerPort: 9200
        env:
        - name: discovery.type
          value: "single-node"
        - name: xpack.security.enabled
          value: "false"
        - name: ES_JAVA_OPTS
          value: "-Xms512m -Xmx512m"
        resources:
          requests: { cpu: "500m", memory: "1Gi" }
          limits: { cpu: "1", memory: "2Gi" }
---
apiVersion: v1
kind: Service
metadata:
  name: elasticsearch-service
  namespace: logging
spec:
  selector:
    app: elasticsearch
  ports:
  - port: 9200
    targetPort: 9200
```

### 10.2 Create `logging/kibana/kibana-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kibana
  namespace: logging
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kibana
  template:
    metadata:
      labels:
        app: kibana
    spec:
      containers:
      - name: kibana
        image: docker.elastic.co/kibana/kibana:8.11.0
        ports:
        - containerPort: 5601
        env:
        - name: ELASTICSEARCH_HOSTS
          value: "http://elasticsearch-service:9200"
---
apiVersion: v1
kind: Service
metadata:
  name: kibana-service
  namespace: logging
spec:
  selector:
    app: kibana
  ports:
  - port: 5601
    targetPort: 5601
  type: NodePort
```

### 10.3 Deploy and access

```bash
kubectl apply -f logging/

# Wait for ES to be ready (takes 1-2 min)
kubectl get pods -n logging -w

# Access Kibana
minikube service kibana-service -n logging --url
```

✅ **Checkpoint:** Kibana accessible. Create index pattern to see application logs.

---

## Step 11 — Set Up HashiCorp Vault

### 11.1 Create `vault/vault-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vault
  namespace: vault
spec:
  replicas: 1
  selector:
    matchLabels:
      app: vault
  template:
    metadata:
      labels:
        app: vault
    spec:
      containers:
      - name: vault
        image: hashicorp/vault:latest
        ports:
        - containerPort: 8200
        env:
        - name: VAULT_DEV_ROOT_TOKEN_ID
          value: "root-token"
        - name: VAULT_DEV_LISTEN_ADDRESS
          value: "0.0.0.0:8200"
        command: ["vault", "server", "-dev"]
---
apiVersion: v1
kind: Service
metadata:
  name: vault-service
  namespace: vault
spec:
  selector:
    app: vault
  ports:
  - port: 8200
    targetPort: 8200
  type: NodePort
```

### 11.2 Create `vault/vault-setup.sh`

```bash
#!/bin/bash
# Store secrets in Vault
export VAULT_ADDR='http://localhost:8200'
export VAULT_TOKEN='root-token'

echo "📦 Storing SOC app secrets in Vault..."

vault kv put secret/soc-app \
    db_user="socuser" \
    db_password="socpass123" \
    db_name="soc_db" \
    jwt_secret="my-super-secret-jwt-key" \
    flask_secret="flask-production-secret"

echo "✅ Secrets stored. Verifying..."
vault kv get secret/soc-app

echo "🔑 Done! Secrets are now managed by Vault."
```

### 11.3 Deploy and configure

```bash
kubectl apply -f vault/

# Port-forward to access Vault locally
kubectl port-forward svc/vault-service 8200:8200 -n vault &

# Run setup script
chmod +x vault/vault-setup.sh
./vault/vault-setup.sh
```

✅ **Checkpoint:** Vault running, secrets stored. App can fetch secrets from Vault.

---

## Step 12 — Disaster Recovery Testing

Run these tests and take screenshots for D13:

### Test 1: Pod Self-Healing

```bash
# List pods
kubectl get pods -n soc-app

# Kill a pod (K8s will auto-restart it)
kubectl delete pod <fastapi-pod-name> -n soc-app

# Watch it come back
kubectl get pods -n soc-app -w
```

### Test 2: Rolling Update

```bash
# Deploy a new version (zero downtime)
kubectl set image deployment/fastapi-backend \
    fastapi=yourusername/soc-api:v2 -n soc-app

# Watch rollout
kubectl rollout status deployment/fastapi-backend -n soc-app

# Rollback if needed
kubectl rollout undo deployment/fastapi-backend -n soc-app
```

### Test 3: HPA Scaling

```bash
# Watch HPA
kubectl get hpa -n soc-app -w

# Generate load (from another terminal)
kubectl run -i --tty load-gen --rm --image=busybox --restart=Never -- \
    /bin/sh -c "while true; do wget -q -O- http://fastapi-service.soc-app:8000/api/health; done"
```

### Test 4: Database Backup & Restore

```bash
# Backup
kubectl exec postgresql-0 -n soc-app -- pg_dump -U socuser soc_db > backup.sql

# Restore (after data loss)
cat backup.sql | kubectl exec -i postgresql-0 -n soc-app -- psql -U socuser soc_db
```

✅ **Checkpoint:** All DR scenarios tested. Screenshots captured.

---

## Step 13 — Screenshots & Documentation

### Screenshots to capture (D13)

Take a screenshot of each and save to `docs/screenshots/`:

| # | What | How |
|---|------|-----|
| 1 | SOC Dashboard with alerts | Open Flask app in browser |
| 2 | Alert detail page | Click an alert |
| 3 | FastAPI Swagger docs | Open `/docs` endpoint |
| 4 | GitHub repo | Open your GitHub repo page |
| 5 | Docker Hub images | Open hub.docker.com |
| 6 | Jenkins pipeline (green) | Open Jenkins build |
| 7 | Jenkins stage view | Click on pipeline stages |
| 8 | `terraform apply` output | Run in terminal |
| 9 | `kubectl get pods -A` | Run in terminal |
| 10 | `kubectl get svc,ingress` | Run in terminal |
| 11 | HPA scaling event | Run `kubectl get hpa -w` |
| 12 | Grafana app dashboard | Open Grafana |
| 13 | Grafana infra dashboard | Open Grafana |
| 14 | Kibana log search | Open Kibana |
| 15 | Vault secrets | Run `vault kv get` |
| 16 | Pod self-healing | Delete pod, watch restart |
| 17 | Rolling update | `kubectl rollout status` |

---

## Cheat Sheet — Key Commands

### Docker
```bash
docker build -t name:tag .          # Build image
docker run -p 8000:8000 name:tag    # Run container
docker-compose up -d                # Start multi-container app
docker-compose down                 # Stop all
docker push user/image:tag          # Push to registry
```

### Kubernetes
```bash
kubectl apply -f file.yaml         # Create/update resources
kubectl get pods -n namespace       # List pods
kubectl describe pod name           # Debug pod
kubectl logs pod-name               # View logs
kubectl exec -it pod -- /bin/sh    # Shell into pod
kubectl rollout undo deployment/x   # Rollback
kubectl scale deploy x --replicas=3 # Scale manually
kubectl port-forward svc/x 8080:80  # Forward port locally
```

### Terraform
```bash
terraform init     # Initialize
terraform plan     # Preview
terraform apply    # Create
terraform destroy  # Delete
```

### Vault
```bash
vault kv put secret/path key=value  # Store secret
vault kv get secret/path            # Read secret
vault kv list secret/               # List paths
```

### Jenkins
```bash
# Run Jenkins in Docker
docker run -d -p 8080:8080 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

---

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `ImagePullBackOff` | K8s can't pull your Docker image | Check image name, run `docker push`, verify Docker Hub login |
| `CrashLoopBackOff` | Container keeps crashing | Run `kubectl logs <pod>` to see the error |
| `Connection refused` on API | FastAPI not running or wrong port | Check `kubectl get svc`, verify port mappings |
| `pending` PVC | No storage provisioner | Run `minikube addons enable storage-provisioner` |
| ELK eating all RAM | Elasticsearch is memory-hungry | Set `ES_JAVA_OPTS: "-Xms256m -Xmx256m"` |
| Jenkins can't run Docker | No Docker socket access | Mount `/var/run/docker.sock` when starting Jenkins |
| Vault `sealed` error | Vault not initialized | Use `vault server -dev` for dev mode (auto-unseals) |
| `terraform init` fails | Missing providers | Check internet connection, run `terraform init -upgrade` |
| `ModuleNotFoundError` | Missing Python dependency | Run `pip install -r requirements.txt` |
| HPA not scaling | Metrics server not installed | Run `minikube addons enable metrics-server` |

---

## Glossary

| Term | Definition |
|------|-----------|
| **CI/CD** | Continuous Integration / Continuous Deployment — automate build, test, deploy |
| **IaC** | Infrastructure as Code — define infra in config files, not manual clicks |
| **K8s** | Kubernetes — container orchestration platform |
| **HPA** | Horizontal Pod Autoscaler — auto-scales pods based on metrics |
| **PVC** | Persistent Volume Claim — request for storage in K8s |
| **StatefulSet** | K8s workload for stateful apps (like databases) |
| **Ingress** | K8s resource that routes external HTTP traffic to services |
| **ConfigMap** | K8s resource for non-sensitive configuration data |
| **Helm** | Package manager for K8s (like npm for JavaScript) |
| **GitOps** | Using Git as the source of truth for infrastructure |
| **SAST** | Static Application Security Testing — scan code for vulnerabilities |
| **SCA** | Software Composition Analysis — scan dependencies for known CVEs |
| **RTO** | Recovery Time Objective — max time to recover from failure |
| **RPO** | Recovery Point Objective — max data loss acceptable |
| **SOC** | Security Operations Center |
| **SIEM** | Security Information and Event Management |
| **EDR** | Endpoint Detection and Response |
| **SOAR** | Security Orchestration, Automation, and Response |
| **IOC** | Indicator of Compromise — evidence of a breach |
| **MITRE ATT&CK** | Framework of adversary tactics and techniques |

---

*End of Learning & Deployment Guide*
