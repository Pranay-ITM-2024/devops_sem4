"""
Unit tests for the FastAPI SOC API.
"""
import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


# ── Health checks ──────────────────────────────────────────

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_readiness_check():
    response = client.get("/api/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


# ── Alert CRUD ─────────────────────────────────────────────

def test_create_alert():
    payload = {
        "title": "Test brute force alert",
        "description": "Multiple failed SSH login attempts",
        "severity": "high",
        "source": "SIEM-Splunk",
        "source_ip": "203.0.113.50",
        "dest_ip": "10.0.1.42",
        "alert_type": "brute_force",
    }
    response = client.post("/api/alerts", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test brute force alert"
    assert data["severity"] == "high"
    assert data["status"] == "open"
    assert data["id"] > 0


def test_list_alerts():
    response = client.get("/api/alerts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_alerts_filter_severity():
    response = client.get("/api/alerts?severity=high")
    assert response.status_code == 200


def test_get_alert():
    # Create one first
    payload = {"title": "Get test alert", "severity": "low"}
    create_resp = client.post("/api/alerts", json=payload)
    alert_id = create_resp.json()["id"]

    response = client.get(f"/api/alerts/{alert_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Get test alert"


def test_get_alert_not_found():
    response = client.get("/api/alerts/99999")
    assert response.status_code == 404


def test_update_alert():
    # Create one first
    payload = {"title": "Update test alert", "severity": "medium"}
    create_resp = client.post("/api/alerts", json=payload)
    alert_id = create_resp.json()["id"]

    # Update status
    response = client.put(f"/api/alerts/{alert_id}", json={"status": "in_progress"})
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"


def test_close_alert():
    payload = {"title": "Close test alert", "severity": "low"}
    create_resp = client.post("/api/alerts", json=payload)
    alert_id = create_resp.json()["id"]

    response = client.put(f"/api/alerts/{alert_id}", json={"status": "closed"})
    assert response.status_code == 200
    assert response.json()["status"] == "closed"


def test_delete_alert():
    payload = {"title": "Delete test alert", "severity": "low"}
    create_resp = client.post("/api/alerts", json=payload)
    alert_id = create_resp.json()["id"]

    response = client.delete(f"/api/alerts/{alert_id}")
    assert response.status_code == 204

    # Verify gone
    response = client.get(f"/api/alerts/{alert_id}")
    assert response.status_code == 404


# ── Stats ──────────────────────────────────────────────────

def test_get_stats():
    response = client.get("/api/alerts/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_alerts" in data
    assert "open_alerts" in data
    assert "critical_count" in data


# ── Playbook ───────────────────────────────────────────────

def test_execute_playbook():
    # Create alert first
    payload = {
        "title": "Playbook test alert",
        "severity": "critical",
        "source_ip": "198.51.100.23",
        "dest_ip": "10.0.2.15",
    }
    create_resp = client.post("/api/alerts", json=payload)
    alert_id = create_resp.json()["id"]

    # Execute block_ip playbook
    response = client.post(f"/api/alerts/{alert_id}/respond", json={"action": "block_ip"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "Blocked" in data["result"]


def test_list_playbook_logs():
    response = client.get("/api/playbook-logs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ── Metrics ────────────────────────────────────────────────

def test_prometheus_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text
