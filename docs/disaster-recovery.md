# Disaster Recovery (DR) Plan

## 1. Overview
This document outlines the Disaster Recovery strategy for the SOC Automation Platform, ensuring that security alerts and dashboard availability are maintained in the event of infrastructure failure.

### Target Metrics
* **Recovery Time Objective (RTO):** 30 minutes (Time to restore services).
* **Recovery Point Objective (RPO):** 1 hour (Maximum acceptable data loss).

## 2. Architecture Resilience (High Availability)
The application is designed for resilience using Kubernetes:
* **Stateless Apps:** Flask and FastAPI run as standard Deployments with `replicas: 2`. If a node dies, pods are rescheduled automatically.
* **Auto-scaling:** Horizontal Pod Autoscaler (HPA) monitors CPU. If load spikes above 70%, K8s scales the FastAPI pods up to 5 replicas.
* **Self-Healing:** Liveness and readiness probes check `/api/health`. If an app freezes, K8s kills and restarts the container.

## 3. Failure Scenarios and Recovery Procedures

### Scenario 1: Pod Crash (Application Bug / OOM)
**Detection:** Kubernetes Liveness probe fails.
**Action:** No human intervention required. Kubernetes `ReplicaSet` controller automatically kills the failed pod and provisions a new one within seconds.

### Scenario 2: Traffic Spike (DDoS or Alert Storm)
**Detection:** Prometheus alerts on high CPU usage or HTTP 500 errors.
**Action:** HPA automatically scales the `fastapi-backend` deployment from 2 to 5 pods. Once traffic subsides, it scales back down.

### Scenario 3: Database Corruption or Failure
**Detection:** App logs show "Connection refused" or SQL errors.
**Action:** 
1. If the `postgresql` pod crashes, the K8s `StatefulSet` restarts it and reattaches the Persistent Volume Claim (PVC). Data is retained.
2. If the volume data is corrupted, DBA must restore from the latest SQL dump:
   ```bash
   cat backup.sql | kubectl exec -i postgresql-0 -n soc-app -- psql -U socuser soc_db
   ```

### Scenario 4: Bad Deployment (Buggy Code Released)
**Detection:** Jenkins pipeline succeeds, but post-deploy health checks fail, or Grafana shows high error rates.
**Action:** Zero-downtime rollback using K8s native rollout history:
```bash
kubectl rollout undo deployment/fastapi-backend -n soc-app
```

## 4. Backups
In a production environment:
1. **Database:** A Kubernetes `CronJob` runs `pg_dump` every hour and pushes the encrypted `.sql` file to an AWS S3 bucket.
2. **Infrastructure:** Terraform state (`terraform.tfstate`) is stored remotely in an S3 bucket with versioning enabled.

## 5. DR Testing Runbook
To verify this DR plan during the exam demonstration, perform the following live tests:

1. **Kill a pod manually:**
   `kubectl delete pod -l app=fastapi-backend -n soc-app`
   *Expected:* A new pod enters `ContainerCreating` status immediately.

2. **Trigger Auto-scaling:**
   Run a load generator loop against the API.
   *Expected:* `kubectl get hpa -n soc-app` shows replicas increasing from 2 to max 5.

3. **Simulate a bad release:**
   `kubectl set image deployment/flask-dashboard flask=nginx:latest -n soc-app`
   *Expected:* Application breaks. 
   Run `kubectl rollout undo deployment/flask-dashboard -n soc-app` to instantly restore functionality.
