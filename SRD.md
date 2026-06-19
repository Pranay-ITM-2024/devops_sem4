# Software Requirements Document (SRD)

## SOC Automation Platform — DevOps Exam Project

| Field               | Details                                      |
|---------------------|----------------------------------------------|
| **Project Name**    | SOC Automation Platform                      |
| **Industry**        | Cybersecurity                                |
| **Type**            | DevOps Exam Project                          |
| **Version**         | 2.0                                          |
| **Date**            | 2026-06-16                                   |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Project Scope & Deliverables](#2-project-scope--deliverables)
3. [Application Requirements](#3-application-requirements)
4. [System Architecture](#4-system-architecture)
5. [DevOps Lifecycle Requirements](#5-devops-lifecycle-requirements)
6. [Non-Functional Requirements](#6-non-functional-requirements)
7. [Technology Stack](#7-technology-stack)
8. [Deliverable-to-Requirement Mapping](#8-deliverable-to-requirement-mapping)
9. [Disaster Recovery Plan](#9-disaster-recovery-plan)
10. [Acceptance Criteria](#10-acceptance-criteria)

---

## 1. Introduction

### 1.1 Purpose

This SRD defines the requirements for a **small but functional SOC (Security Operations Center) web application** and the **complete DevOps lifecycle** implemented around it — covering automated build, test, deploy, monitor, log, recover, and secure workflows.

### 1.2 Problem Statement

A global cybersecurity provider monitors 25,000+ enterprise environments. Security analysts face:

- **Alert fatigue** — millions of daily alerts, most are noise
- **Manual response workflows** — slow, error-prone human processes
- **Infrastructure scalability issues** — can't handle spikes
- **Delayed threat remediation** — hours/days instead of minutes
- **Inconsistent deployments** — no standardization across environments

### 1.3 Our Approach

> **"Build a small but functional business application first. Then demonstrate how DevOps tools automate deployment, scaling, monitoring, recovery, and security of that application."**

We will build a **simplified SOC Dashboard** that demonstrates core cybersecurity operations functionality, then wrap it with a complete DevOps toolchain to show how the application would be deployed, scaled, monitored, and secured in a real environment.

---

## 2. Project Scope & Deliverables

### 2.1 What We ARE Building

A **working SOC web application** with:
- A dashboard to view, filter, and triage security alerts
- A REST API for alert management (CRUD + bulk actions)
- Simulated alert ingestion (fake alert generator)
- Basic automated response (mock playbook execution)
- Simple authentication

Then a **full DevOps pipeline** around it:
- Containerization, CI/CD, IaC, orchestration, monitoring, logging, and secrets management

### 2.2 What We Are NOT Building

- A production-grade system for 25,000 tenants
- Real SIEM/EDR integrations
- ML-based threat detection
- Multi-region HA deployment
- Real-time Kafka streaming at scale

### 2.3 Required Deliverables Checklist

| #  | Deliverable                                       | Description                                                |
|----|---------------------------------------------------|------------------------------------------------------------|
| D1 | **Working Application**                           | Flask dashboard + FastAPI backend for SOC alert management |
| D2 | **Source Code Repository (GitHub)**                | Organized monorepo with README, branching strategy         |
| D3 | **Dockerfile and Docker Images**                  | Multi-stage Dockerfiles for Flask app and FastAPI API      |
| D4 | **Jenkins CI/CD Pipeline**                        | Jenkinsfile with build, test, scan, deploy stages          |
| D5 | **Terraform Infrastructure Scripts**              | IaC to provision cloud/local infra (VMs, networking, K8s)  |
| D6 | **Kubernetes Deployment Files**                   | Deployments, Services, Ingress, ConfigMaps, HPA            |
| D7 | **Monitoring (Prometheus + Grafana)**             | Metrics collection, custom dashboards, alerting rules      |
| D8 | **Logging (ELK Stack)**                           | Elasticsearch + Logstash + Kibana for centralized logging  |
| D9 | **Secret Management (Vault)**                     | HashiCorp Vault for DB credentials, API keys, secrets      |
| D10| **Architecture Diagram**                          | High-level system architecture showing all components      |
| D11| **Deployment Diagram**                            | How the app is deployed across K8s cluster                 |
| D12| **Disaster Recovery Plan**                        | Documented DR strategy with RTO/RPO targets                |
| D13| **Demonstration Screenshots**                     | Screenshots of every deliverable in action                 |
| D14| **Project Documentation**                         | SRD, handover doc, README, setup guides                    |

---

## 3. Application Requirements

### 3.1 Application Overview

The SOC Automation Platform consists of two backend services and a web frontend:

```
┌──────────────────────────────────────────────────┐
│                SOC AUTOMATION PLATFORM            │
│                                                    │
│  ┌─────────────────┐    ┌──────────────────────┐  │
│  │  Flask Web App   │    │  FastAPI Backend API  │  │
│  │  (Dashboard UI)  │◄──►│  (Alert CRUD + Logic) │  │
│  │                  │    │                       │  │
│  │  - Alert List    │    │  - GET /api/alerts    │  │
│  │  - Alert Detail  │    │  - POST /api/alerts   │  │
│  │  - Triage View   │    │  - PUT /api/alerts/id │  │
│  │  - Playbook Logs │    │  - POST /api/respond  │  │
│  │  - Login Page    │    │  - GET /api/metrics   │  │
│  └─────────────────┘    └──────────┬───────────┘  │
│                                     │              │
│                          ┌──────────▼───────────┐  │
│                          │   PostgreSQL / SQLite │  │
│                          │   (Alert Database)    │  │
│                          └──────────────────────┘  │
│                                                    │
│  ┌─────────────────────────────────────────────┐  │
│  │  Alert Simulator (Python Script / Cron Job)  │  │
│  │  Generates fake security alerts every N sec  │  │
│  └─────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
```

### 3.2 Functional Requirements — Flask Web Dashboard (FR-100)

| ID     | Requirement                                                              | Priority |
|--------|--------------------------------------------------------------------------|----------|
| FR-101 | Dashboard SHALL display a list of security alerts with severity badges   | Critical |
| FR-102 | Dashboard SHALL allow filtering alerts by severity (Critical/High/Med/Low)| Critical |
| FR-103 | Dashboard SHALL allow filtering alerts by status (Open/In Progress/Closed)| Critical |
| FR-104 | Dashboard SHALL show alert detail view with full event information        | High     |
| FR-105 | Dashboard SHALL provide one-click triage actions (Acknowledge, Escalate, Close) | High |
| FR-106 | Dashboard SHALL display summary statistics (total alerts, open count, MTTR) | High  |
| FR-107 | Dashboard SHALL have a simple login page with username/password auth      | Medium   |
| FR-108 | Dashboard SHALL show playbook execution logs                             | Medium   |
| FR-109 | Dashboard SHALL have a dark-themed UI suitable for SOC analyst work      | Medium   |

### 3.3 Functional Requirements — FastAPI Backend API (FR-200)

| ID     | Requirement                                                              | Priority |
|--------|--------------------------------------------------------------------------|----------|
| FR-201 | API SHALL expose `GET /api/alerts` to list all alerts with pagination    | Critical |
| FR-202 | API SHALL expose `GET /api/alerts/{id}` to get alert details             | Critical |
| FR-203 | API SHALL expose `POST /api/alerts` to create new alerts                 | Critical |
| FR-204 | API SHALL expose `PUT /api/alerts/{id}` to update alert status           | Critical |
| FR-205 | API SHALL expose `DELETE /api/alerts/{id}` to delete alerts              | High     |
| FR-206 | API SHALL expose `POST /api/alerts/{id}/respond` to trigger mock playbook| High     |
| FR-207 | API SHALL expose `GET /api/alerts/stats` for dashboard statistics        | High     |
| FR-208 | API SHALL expose `GET /api/health` for health check (K8s liveness probe) | Critical |
| FR-209 | API SHALL expose `GET /api/ready` for readiness check (K8s readiness)    | Critical |
| FR-210 | API SHALL expose `GET /metrics` in Prometheus format                     | Critical |
| FR-211 | API SHALL validate all inputs and return proper HTTP status codes         | High     |
| FR-212 | API SHALL generate auto-documentation via Swagger/OpenAPI at `/docs`     | Medium   |

### 3.4 Functional Requirements — Alert Simulator (FR-300)

| ID     | Requirement                                                              | Priority |
|--------|--------------------------------------------------------------------------|----------|
| FR-301 | Simulator SHALL generate realistic fake alerts at a configurable interval| High     |
| FR-302 | Simulator SHALL produce alerts of varying severity (Critical/High/Med/Low)| High    |
| FR-303 | Simulator SHALL simulate different alert types (brute force, malware, phishing, port scan) | High |
| FR-304 | Simulator SHALL post alerts to the FastAPI backend via REST API          | High     |

### 3.5 Functional Requirements — Mock Playbook Engine (FR-400)

| ID     | Requirement                                                              | Priority |
|--------|--------------------------------------------------------------------------|----------|
| FR-401 | System SHALL support a "Block IP" mock response action                   | High     |
| FR-402 | System SHALL support an "Isolate Host" mock response action              | High     |
| FR-403 | System SHALL support a "Notify Team" mock response action (log output)   | Medium   |
| FR-404 | System SHALL log all playbook executions with timestamp and result        | High     |

### 3.6 Data Model

```
┌───────────────────────────────────────┐
│              alerts                    │
├───────────────────────────────────────┤
│ id           INTEGER  PK AUTO_INCR    │
│ title        VARCHAR(255) NOT NULL     │
│ description  TEXT                      │
│ severity     ENUM(critical,high,       │
│              medium,low)               │
│ status       ENUM(open,in_progress,    │
│              closed)                   │
│ source       VARCHAR(100)              │
│ source_ip    VARCHAR(45)               │
│ dest_ip      VARCHAR(45)               │
│ alert_type   VARCHAR(50)               │
│ assigned_to  VARCHAR(100)              │
│ created_at   TIMESTAMP                 │
│ updated_at   TIMESTAMP                 │
│ closed_at    TIMESTAMP NULL            │
└───────────────────────────────────────┘

┌───────────────────────────────────────┐
│         playbook_logs                  │
├───────────────────────────────────────┤
│ id           INTEGER  PK AUTO_INCR    │
│ alert_id     INTEGER  FK → alerts.id  │
│ action       VARCHAR(50)              │
│ status       ENUM(success,failed)     │
│ details      TEXT                      │
│ executed_at  TIMESTAMP                 │
└───────────────────────────────────────┘

┌───────────────────────────────────────┐
│              users                     │
├───────────────────────────────────────┤
│ id           INTEGER  PK AUTO_INCR    │
│ username     VARCHAR(50) UNIQUE        │
│ password_hash VARCHAR(255)             │
│ role         ENUM(analyst,admin)       │
│ created_at   TIMESTAMP                 │
└───────────────────────────────────────┘
```

### 3.7 API Endpoints Summary

| Method | Endpoint                    | Description                     | Auth Required |
|--------|-----------------------------|---------------------------------|---------------|
| POST   | `/api/auth/login`           | Login, get JWT token            | No            |
| GET    | `/api/alerts`               | List alerts (paginated)         | Yes           |
| GET    | `/api/alerts/{id}`          | Get single alert                | Yes           |
| POST   | `/api/alerts`               | Create alert                    | Yes           |
| PUT    | `/api/alerts/{id}`          | Update alert (triage)           | Yes           |
| DELETE | `/api/alerts/{id}`          | Delete alert                    | Yes (Admin)   |
| POST   | `/api/alerts/{id}/respond`  | Execute mock playbook           | Yes           |
| GET    | `/api/alerts/stats`         | Dashboard statistics            | Yes           |
| GET    | `/api/playbook-logs`        | List playbook execution logs    | Yes           |
| GET    | `/api/health`               | Liveness probe                  | No            |
| GET    | `/api/ready`                | Readiness probe                 | No            |
| GET    | `/metrics`                  | Prometheus metrics              | No            |
| GET    | `/docs`                     | Swagger UI (FastAPI auto-gen)   | No            |

---

## 4. System Architecture

### 4.1 Architecture Diagram (D10)

```
                        ┌─────────────────┐
                        │   GitHub Repo    │
                        │  (Source Code)   │
                        └────────┬────────┘
                                 │ webhook
                                 ▼
                        ┌─────────────────┐
                        │    Jenkins CI/CD │
                        │   ┌───────────┐ │
                        │   │ Build     │ │
                        │   │ Test      │ │
                        │   │ Scan      │ │
                        │   │ Push Image│ │
                        │   │ Deploy    │ │
                        │   └───────────┘ │
                        └────────┬────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
    │  Docker Hub  │   │  Terraform   │   │  Vault       │
    │  (Images)    │   │  (Infra IaC) │   │  (Secrets)   │
    └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
           │                  │                  │
           └──────────────────┼──────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │      Kubernetes Cluster       │
              │                               │
              │  ┌─────────┐  ┌────────────┐  │
              │  │ Flask   │  │ FastAPI    │  │
              │  │ Web App │  │ Backend    │  │
              │  │ (2 pods)│  │ (2 pods)   │  │
              │  └────┬────┘  └─────┬──────┘  │
              │       │             │          │
              │       └──────┬──────┘          │
              │              ▼                 │
              │  ┌────────────────────┐        │
              │  │    PostgreSQL      │        │
              │  │    (1 pod + PVC)   │        │
              │  └────────────────────┘        │
              │                               │
              │  ┌─────────┐  ┌────────────┐  │
              │  │Prometheus│  │ ELK Stack  │  │
              │  │+ Grafana │  │ (Logging)  │  │
              │  └─────────┘  └────────────┘  │
              └───────────────────────────────┘
```

### 4.2 Deployment Diagram (D11)

```
┌─────────────────────────────────────────────────────────┐
│                  Kubernetes Cluster                      │
│                                                         │
│  ┌─── Namespace: soc-app ─────────────────────────────┐ │
│  │                                                     │ │
│  │  ┌─────────────────────┐  ┌──────────────────────┐ │ │
│  │  │ Deployment:         │  │ Deployment:          │ │ │
│  │  │ flask-dashboard     │  │ fastapi-backend      │ │ │
│  │  │ replicas: 2         │  │ replicas: 2          │ │ │
│  │  │ image: soc-flask:v1 │  │ image: soc-api:v1    │ │ │
│  │  │ port: 5000          │  │ port: 8000           │ │ │
│  │  └────────┬────────────┘  └──────────┬───────────┘ │ │
│  │           │                          │             │ │
│  │  ┌────────▼──────────────────────────▼───────────┐ │ │
│  │  │  Service: flask-svc    Service: api-svc       │ │ │
│  │  │  (ClusterIP:5000)      (ClusterIP:8000)       │ │ │
│  │  └───────────────────────┬───────────────────────┘ │ │
│  │                          │                         │ │
│  │  ┌───────────────────────▼───────────────────────┐ │ │
│  │  │  Ingress Controller (nginx)                    │ │ │
│  │  │  / → flask-svc:5000                           │ │ │
│  │  │  /api → api-svc:8000                          │ │ │
│  │  └───────────────────────────────────────────────┘ │ │
│  │                                                     │ │
│  │  ┌───────────────────┐  ┌──────────────────────┐   │ │
│  │  │ StatefulSet:      │  │ CronJob:             │   │ │
│  │  │ postgresql        │  │ alert-simulator      │   │ │
│  │  │ PVC: 5Gi          │  │ schedule: */2 * * * *│   │ │
│  │  └───────────────────┘  └──────────────────────┘   │ │
│  │                                                     │ │
│  │  ┌──────────────────────────────────────────────┐   │ │
│  │  │ ConfigMap: app-config                        │   │ │
│  │  │ Secret: db-credentials (from Vault)          │   │ │
│  │  │ HPA: min=2, max=5, cpu-target=70%            │   │ │
│  │  └──────────────────────────────────────────────┘   │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                         │
│  ┌─── Namespace: monitoring ──────────────────────────┐ │
│  │  Prometheus │ Grafana │ AlertManager                │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                         │
│  ┌─── Namespace: logging ─────────────────────────────┐ │
│  │  Elasticsearch │ Logstash │ Kibana                  │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                         │
│  ┌─── Namespace: vault ───────────────────────────────┐ │
│  │  HashiCorp Vault (dev mode)                        │ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 5. DevOps Lifecycle Requirements

### 5.1 Source Code & Version Control (D2)

| ID     | Requirement                                                              | Priority |
|--------|--------------------------------------------------------------------------|----------|
| DO-101 | Code SHALL be hosted on a GitHub repository (public or private)          | Critical |
| DO-102 | Repository SHALL follow a branching strategy (main, dev, feature/*)      | Critical |
| DO-103 | Repository SHALL include a comprehensive README.md                      | Critical |
| DO-104 | Repository SHALL include a `.gitignore` for Python, Docker, and IDE files| High     |
| DO-105 | Repository SHALL use meaningful commit messages                          | High     |

### 5.2 Containerization — Docker (D3)

| ID     | Requirement                                                              | Priority |
|--------|--------------------------------------------------------------------------|----------|
| DO-201 | Flask app SHALL have a Dockerfile (multi-stage build)                    | Critical |
| DO-202 | FastAPI app SHALL have a Dockerfile (multi-stage build)                  | Critical |
| DO-203 | Alert simulator SHALL have a Dockerfile                                  | High     |
| DO-204 | A `docker-compose.yml` SHALL be provided for local development           | High     |
| DO-205 | Docker images SHALL be pushed to Docker Hub or a container registry       | Critical |
| DO-206 | Images SHALL use non-root users for security                             | High     |
| DO-207 | Images SHALL include health check instructions                           | Medium   |

### 5.3 CI/CD Pipeline — Jenkins (D4)

| ID     | Requirement                                                              | Priority |
|--------|--------------------------------------------------------------------------|----------|
| DO-301 | A `Jenkinsfile` SHALL define the complete pipeline                       | Critical |
| DO-302 | Pipeline SHALL have a **Build** stage (install deps, compile)            | Critical |
| DO-303 | Pipeline SHALL have a **Test** stage (run pytest unit tests)             | Critical |
| DO-304 | Pipeline SHALL have a **Code Quality** stage (linting with flake8/pylint)| High     |
| DO-305 | Pipeline SHALL have a **Security Scan** stage (Trivy or Bandit)          | High     |
| DO-306 | Pipeline SHALL have a **Docker Build & Push** stage                      | Critical |
| DO-307 | Pipeline SHALL have a **Deploy to K8s** stage (kubectl apply)            | Critical |
| DO-308 | Pipeline SHALL trigger on push to `main` branch (webhook or polling)     | High     |
| DO-309 | Pipeline SHALL display build status badge in README                      | Medium   |
| DO-310 | Pipeline SHALL fail fast on test/scan failures                           | High     |

**Pipeline Flow:**

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  Clone   │──▶│  Build   │──▶│  Test    │──▶│  Scan    │──▶│  Docker  │──▶│  Deploy  │
│  Repo    │   │  (pip)   │   │ (pytest) │   │ (Trivy/  │   │  Build & │   │  to K8s  │
│          │   │          │   │          │   │  Bandit)  │   │  Push    │   │          │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
```

### 5.4 Infrastructure as Code — Terraform (D5)

| ID     | Requirement                                                              | Priority |
|--------|--------------------------------------------------------------------------|----------|
| DO-401 | Terraform SHALL provision the Kubernetes cluster (or VM infrastructure)   | Critical |
| DO-402 | Terraform SHALL provision networking (VPC, subnets, security groups)      | Critical |
| DO-403 | Terraform SHALL provision any required cloud resources (RDS, S3, etc.)    | High     |
| DO-404 | Terraform state SHALL be managed (local or remote backend)               | High     |
| DO-405 | Terraform code SHALL use modules for reusability                         | High     |
| DO-406 | Terraform SHALL support `terraform plan` for change preview              | High     |
| DO-407 | Variables SHALL be externalized via `variables.tf` and `terraform.tfvars`| High     |

### 5.5 Container Orchestration — Kubernetes (D6)

| ID     | Requirement                                                              | Priority |
|--------|--------------------------------------------------------------------------|----------|
| DO-501 | Flask app SHALL be deployed as a K8s Deployment with 2 replicas          | Critical |
| DO-502 | FastAPI app SHALL be deployed as a K8s Deployment with 2 replicas        | Critical |
| DO-503 | PostgreSQL SHALL be deployed as a StatefulSet with PersistentVolumeClaim | Critical |
| DO-504 | Alert simulator SHALL run as a K8s CronJob                               | High     |
| DO-505 | Services SHALL be exposed via ClusterIP Services                         | Critical |
| DO-506 | An Ingress resource SHALL route external traffic to the services         | Critical |
| DO-507 | ConfigMaps SHALL be used for application configuration                   | High     |
| DO-508 | Secrets SHALL be used for sensitive data (sourced from Vault)            | Critical |
| DO-509 | HPA SHALL auto-scale Flask and FastAPI pods based on CPU (70% target)    | High     |
| DO-510 | Liveness and readiness probes SHALL be configured for all app pods       | Critical |
| DO-511 | Resource limits (CPU/memory) SHALL be set for all pods                   | High     |
| DO-512 | All resources SHALL be deployed in a dedicated namespace `soc-app`       | High     |

### 5.6 Monitoring — Prometheus & Grafana (D7)

| ID     | Requirement                                                              | Priority |
|--------|--------------------------------------------------------------------------|----------|
| DO-601 | Prometheus SHALL scrape metrics from FastAPI `/metrics` endpoint         | Critical |
| DO-602 | Prometheus SHALL scrape K8s node and pod metrics (kube-state-metrics)    | High     |
| DO-603 | Grafana SHALL have a dashboard showing: request rate, latency, error rate| Critical |
| DO-604 | Grafana SHALL have a dashboard showing: pod CPU, memory, restart count  | High     |
| DO-605 | Grafana SHALL have a custom SOC dashboard: alert counts by severity      | High     |
| DO-606 | AlertManager SHALL send alerts on: pod crash, high error rate, high CPU  | Medium   |
| DO-607 | Prometheus and Grafana SHALL run in a `monitoring` namespace             | High     |

### 5.7 Logging — ELK Stack (D8)

| ID     | Requirement                                                              | Priority |
|--------|--------------------------------------------------------------------------|----------|
| DO-701 | Application logs SHALL be output to stdout/stderr in JSON format         | Critical |
| DO-702 | Logstash (or Filebeat) SHALL collect logs from all application pods      | Critical |
| DO-703 | Elasticsearch SHALL store and index all collected logs                   | Critical |
| DO-704 | Kibana SHALL provide a dashboard for log search and visualization        | Critical |
| DO-705 | Logs SHALL include: timestamp, level, service name, request ID           | High     |
| DO-706 | ELK stack SHALL run in a `logging` namespace                             | High     |
| DO-707 | Log retention SHALL be configured (e.g., 7 days for demo purposes)       | Medium   |

### 5.8 Secret Management — Vault (D9)

| ID     | Requirement                                                              | Priority |
|--------|--------------------------------------------------------------------------|----------|
| DO-801 | HashiCorp Vault SHALL be deployed in K8s (dev mode is acceptable)        | Critical |
| DO-802 | Database credentials SHALL be stored in Vault, not in plain text         | Critical |
| DO-803 | API JWT secret key SHALL be stored in Vault                              | High     |
| DO-804 | Application pods SHALL fetch secrets from Vault at startup               | Critical |
| DO-805 | Vault SHALL run in a `vault` namespace                                   | High     |
| DO-806 | A demo walkthrough of storing/retrieving a secret SHALL be documented    | High     |

---

## 6. Non-Functional Requirements

### 6.1 Performance (Exam-Scoped)

| ID      | Requirement                                           | Target           |
|---------|-------------------------------------------------------|------------------|
| NFR-101 | API response time                                     | < 500ms (p95)    |
| NFR-102 | Dashboard page load time                              | < 3 seconds      |
| NFR-103 | Concurrent users supported                            | ≥ 10             |
| NFR-104 | Alert simulator throughput                            | 1 alert / 30 sec |

### 6.2 Availability

| ID      | Requirement                                           | Target           |
|---------|-------------------------------------------------------|------------------|
| NFR-201 | Application uptime during demo                        | 99%              |
| NFR-202 | Pod auto-restart on crash (K8s self-healing)          | < 30 seconds     |
| NFR-203 | Rolling updates with zero downtime                    | Required         |

### 6.3 Security

| ID      | Requirement                                           | Target           |
|---------|-------------------------------------------------------|------------------|
| NFR-301 | No hardcoded secrets in source code                   | Required         |
| NFR-302 | Docker images run as non-root                         | Required         |
| NFR-303 | API endpoints require JWT authentication              | Required         |
| NFR-304 | Input validation on all API endpoints                 | Required         |

---

## 7. Technology Stack

| Layer                | Technology                             | Purpose                           |
|----------------------|----------------------------------------|-----------------------------------|
| **Frontend/Dashboard** | Python Flask + Jinja2 + Bootstrap    | SOC analyst web dashboard         |
| **Backend API**       | Python FastAPI + Uvicorn              | REST API, Swagger docs, metrics   |
| **Database**          | PostgreSQL (or SQLite for simplicity) | Alert and user data storage       |
| **Alert Simulator**   | Python script                         | Generate fake security alerts     |
| **Containerization**  | Docker (multi-stage builds)           | Package apps as containers        |
| **CI/CD**             | Jenkins (Jenkinsfile)                 | Automated build-test-deploy       |
| **IaC**               | Terraform                             | Provision infrastructure          |
| **Orchestration**     | Kubernetes (Minikube or cloud K8s)    | Deploy and scale containers       |
| **Monitoring**        | Prometheus + Grafana                  | Metrics, dashboards, alerting     |
| **Logging**           | Elasticsearch + Logstash + Kibana     | Centralized log management        |
| **Secrets**           | HashiCorp Vault                       | Secure secret storage             |
| **Version Control**   | Git + GitHub                          | Source code management            |
| **Python Deps**       | pip + requirements.txt                | Dependency management             |
| **Testing**           | pytest + coverage                     | Unit and integration testing      |
| **Linting**           | flake8 / pylint                       | Code quality                      |
| **Security Scan**     | Bandit (SAST) + Trivy (container)     | Vulnerability scanning            |

---

## 8. Deliverable-to-Requirement Mapping

This matrix shows which requirements map to each exam deliverable:

| Deliverable                  | Requirements Covered                     | Key Files / Artifacts                  |
|------------------------------|------------------------------------------|----------------------------------------|
| D1: Working Application      | FR-101 to FR-404                        | `app/`, `api/`, `simulator/`           |
| D2: GitHub Repository        | DO-101 to DO-105                        | `.git`, `README.md`, `.gitignore`      |
| D3: Docker                   | DO-201 to DO-207                        | `Dockerfile`, `docker-compose.yml`     |
| D4: Jenkins Pipeline         | DO-301 to DO-310                        | `Jenkinsfile`                          |
| D5: Terraform                | DO-401 to DO-407                        | `terraform/`                           |
| D6: Kubernetes               | DO-501 to DO-512                        | `k8s/`                                 |
| D7: Prometheus + Grafana     | DO-601 to DO-607                        | `monitoring/`                          |
| D8: ELK Stack                | DO-701 to DO-707                        | `logging/`                             |
| D9: Vault                    | DO-801 to DO-806                        | `vault/`                               |
| D10: Architecture Diagram    | § 4.1                                   | `docs/architecture-diagram.png`        |
| D11: Deployment Diagram      | § 4.2                                   | `docs/deployment-diagram.png`          |
| D12: Disaster Recovery Plan  | § 9                                     | `docs/disaster-recovery.md`            |
| D13: Screenshots             | All                                     | `docs/screenshots/`                    |
| D14: Documentation           | This SRD + README + Handover            | `docs/`, `README.md`                   |

---

## 9. Disaster Recovery Plan

### 9.1 Overview

| Parameter | Target                                                    |
|-----------|-----------------------------------------------------------|
| **RTO**   | < 30 minutes (Recovery Time Objective)                     |
| **RPO**   | < 1 hour (Recovery Point Objective — last backup)          |

### 9.2 Failure Scenarios & Recovery Actions

| Scenario                        | Detection Method               | Recovery Action                                    |
|---------------------------------|--------------------------------|----------------------------------------------------|
| **Pod crash**                   | K8s liveness probe fails       | Auto-restart by K8s (immediate, < 30 sec)          |
| **Node failure**                | K8s node status = NotReady     | Pods rescheduled to healthy nodes (< 5 min)        |
| **Database data loss**          | Application errors / monitoring| Restore from latest PostgreSQL backup (PVC snapshot)|
| **Docker image corruption**     | Pull failure in K8s            | Rollback to previous image tag (`kubectl rollout undo`) |
| **Full cluster failure**        | Monitoring alerts              | Re-provision via Terraform + redeploy via Jenkins  |
| **Secret compromise**           | Audit logs / Vault alerts      | Rotate secrets in Vault, restart affected pods     |
| **CI/CD pipeline failure**      | Jenkins build status           | Manual rollback + fix pipeline + re-trigger        |

### 9.3 Backup Strategy

| Component    | Backup Method                      | Frequency    | Retention |
|--------------|------------------------------------|--------------|-----------|
| Database     | `pg_dump` via CronJob to PVC/S3    | Every 6 hours| 7 days    |
| Vault secrets| Vault snapshot                     | Daily        | 30 days   |
| K8s manifests| Stored in Git (source of truth)    | Every commit | Permanent |
| Docker images| Stored in Docker Hub with tags     | Every build  | 10 latest |

### 9.4 Recovery Procedures

**Scenario: Full Cluster Rebuild**

```bash
# Step 1: Re-provision infrastructure
cd terraform/
terraform init
terraform apply -auto-approve

# Step 2: Deploy all K8s resources
kubectl apply -f k8s/namespaces/
kubectl apply -f k8s/vault/
kubectl apply -f k8s/database/
kubectl apply -f k8s/app/
kubectl apply -f k8s/monitoring/
kubectl apply -f k8s/logging/

# Step 3: Restore database from backup
kubectl exec -it postgresql-0 -- pg_restore -d soc_db /backups/latest.dump

# Step 4: Verify all pods are running
kubectl get pods -A

# Step 5: Run smoke tests
curl http://<ingress-ip>/api/health
curl http://<ingress-ip>/api/ready
```

---

## 10. Acceptance Criteria

### 10.1 Application Acceptance

| Test                                         | Pass Criteria                              |
|----------------------------------------------|--------------------------------------------|
| Dashboard loads and shows alerts             | Page loads < 3 sec, alerts visible          |
| Create alert via API                         | `POST /api/alerts` returns 201             |
| Triage alert (change status)                 | Status updates reflected in dashboard       |
| Execute mock playbook                        | Log entry created in playbook_logs table    |
| Simulator generates alerts                   | New alerts appear automatically             |

### 10.2 DevOps Pipeline Acceptance

| Test                                         | Pass Criteria                              |
|----------------------------------------------|--------------------------------------------|
| Push to GitHub triggers Jenkins build        | Build starts within 2 minutes              |
| Jenkins pipeline completes all stages        | Green build with test + scan passing        |
| Docker images pushed to registry             | Image pullable from Docker Hub              |
| `terraform apply` provisions infra           | Resources created without errors            |
| `kubectl apply` deploys all manifests        | All pods in Running state                   |
| HPA scales pods under load                   | Pod count increases when CPU > 70%          |
| Prometheus scrapes application metrics       | Metrics visible in Prometheus targets       |
| Grafana dashboards display data              | Request rate and pod metrics visible        |
| Kibana shows application logs                | Logs searchable by service name             |
| Vault stores and serves secrets              | App reads DB password from Vault            |
| Pod killed → auto-restart                    | K8s restarts pod within 30 seconds          |
| Rollback deployment                          | `kubectl rollout undo` restores previous    |

### 10.3 Documentation Acceptance

| Test                                         | Pass Criteria                              |
|----------------------------------------------|--------------------------------------------|
| Architecture diagram complete                | Shows all components and data flow          |
| Deployment diagram complete                  | Shows K8s resources and namespaces          |
| DR plan documented                           | Covers scenarios, RTO/RPO, procedures       |
| Screenshots captured for all deliverables    | ≥ 15 screenshots covering all components    |
| README has setup instructions                | New developer can run locally in < 30 min   |

---

## Appendix: Required Screenshots List (D13)

| #  | Screenshot                                         | Shows                                        |
|----|----------------------------------------------------|----------------------------------------------|
| 1  | SOC Dashboard — Alert List                         | Working application with alert data           |
| 2  | SOC Dashboard — Alert Detail / Triage              | Alert details with triage actions             |
| 3  | FastAPI Swagger Docs (`/docs`)                     | Auto-generated API documentation              |
| 4  | GitHub Repository                                  | Repo structure, README, branches              |
| 5  | Docker Hub — Pushed Images                         | Container images with tags                    |
| 6  | Jenkins Pipeline — Successful Build                | All stages green                              |
| 7  | Jenkins Pipeline — Stage View                      | Individual stage execution logs               |
| 8  | Terraform Apply — Output                           | Infrastructure provisioning output            |
| 9  | Kubernetes — `kubectl get pods`                    | All pods running in correct namespaces        |
| 10 | Kubernetes — `kubectl get svc,ingress`             | Services and ingress configured               |
| 11 | Kubernetes — HPA in Action                         | Pod scaling event                             |
| 12 | Grafana — Application Dashboard                    | Request rate, latency, errors                 |
| 13 | Grafana — Infrastructure Dashboard                 | Pod CPU/memory metrics                        |
| 14 | Kibana — Log Search                                | Application logs queried by filter            |
| 15 | Vault — Secret Storage                             | Secret stored and accessible                  |
| 16 | Self-Healing — Pod Restart                         | Pod killed and auto-restarted by K8s          |
| 17 | Rolling Update — Zero Downtime                     | New version deployed while old runs           |

---

## Appendix: Repository Structure

```
soc-automation-platform/
├── README.md                           # Project overview + setup guide
├── SRD.md                              # This document
├── ProjectHandover.md                  # Handover document
│
├── app/                                # Flask Web Dashboard (D1)
│   ├── Dockerfile                      # (D3)
│   ├── requirements.txt
│   ├── app.py                          # Flask application entry
│   ├── templates/                      # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── alert_detail.html
│   │   └── playbook_logs.html
│   ├── static/                         # CSS, JS assets
│   │   ├── css/style.css
│   │   └── js/main.js
│   └── tests/
│       └── test_app.py
│
├── api/                                # FastAPI Backend API (D1)
│   ├── Dockerfile                      # (D3)
│   ├── requirements.txt
│   ├── main.py                         # FastAPI application entry
│   ├── models.py                       # SQLAlchemy models
│   ├── schemas.py                      # Pydantic schemas
│   ├── database.py                     # DB connection
│   ├── routes/
│   │   ├── alerts.py
│   │   ├── auth.py
│   │   ├── playbooks.py
│   │   └── health.py
│   ├── services/
│   │   ├── alert_service.py
│   │   └── playbook_service.py
│   └── tests/
│       ├── test_alerts.py
│       └── test_health.py
│
├── simulator/                          # Alert Simulator (D1)
│   ├── Dockerfile                      # (D3)
│   ├── requirements.txt
│   └── simulator.py
│
├── docker-compose.yml                  # Local dev environment (D3)
│
├── Jenkinsfile                         # CI/CD Pipeline (D4)
│
├── terraform/                          # Infrastructure as Code (D5)
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── terraform.tfvars
│   ├── modules/
│   │   ├── network/
│   │   ├── compute/
│   │   └── kubernetes/
│   └── backend.tf
│
├── k8s/                                # Kubernetes Manifests (D6)
│   ├── namespaces/
│   │   └── namespaces.yaml
│   ├── app/
│   │   ├── flask-deployment.yaml
│   │   ├── flask-service.yaml
│   │   ├── fastapi-deployment.yaml
│   │   ├── fastapi-service.yaml
│   │   ├── ingress.yaml
│   │   ├── hpa.yaml
│   │   └── configmap.yaml
│   ├── database/
│   │   ├── postgres-statefulset.yaml
│   │   ├── postgres-service.yaml
│   │   └── postgres-pvc.yaml
│   ├── simulator/
│   │   └── simulator-cronjob.yaml
│   └── secrets/
│       └── vault-injected-secrets.yaml
│
├── monitoring/                         # Prometheus + Grafana (D7)
│   ├── prometheus/
│   │   ├── prometheus-config.yaml
│   │   ├── prometheus-deployment.yaml
│   │   └── alert-rules.yaml
│   └── grafana/
│       ├── grafana-deployment.yaml
│       ├── grafana-service.yaml
│       └── dashboards/
│           ├── soc-app-dashboard.json
│           └── infra-dashboard.json
│
├── logging/                            # ELK Stack (D8)
│   ├── elasticsearch/
│   │   └── elasticsearch-deployment.yaml
│   ├── logstash/
│   │   ├── logstash-deployment.yaml
│   │   └── logstash.conf
│   └── kibana/
│       └── kibana-deployment.yaml
│
├── vault/                              # Secret Management (D9)
│   ├── vault-deployment.yaml
│   ├── vault-policy.hcl
│   └── vault-setup.sh
│
└── docs/                               # Documentation (D10-D14)
    ├── architecture-diagram.png        # (D10)
    ├── deployment-diagram.png          # (D11)
    ├── disaster-recovery.md            # (D12)
    └── screenshots/                    # (D13)
        ├── 01-dashboard.png
        ├── 02-alert-detail.png
        ├── ...
        └── 17-rolling-update.png
```

---

*End of Software Requirements Document*
