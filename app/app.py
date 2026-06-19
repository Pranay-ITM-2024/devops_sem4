"""
SOC Automation Platform — Flask Web Dashboard
===============================================
Server-rendered dashboard for SOC analysts to view,
filter, triage, and respond to security alerts.
"""
from flask import Flask, render_template, request, redirect, url_for, flash
import requests as http_requests
import os
import logging

# ── Config ────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "dev-secret-key-change-me")
API_URL = os.getenv("API_URL", "http://localhost:8000")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("soc-dashboard")


def api_get(path, params=None):
    """Helper to call the FastAPI backend with error handling."""
    try:
        resp = http_requests.get(f"{API_URL}{path}", params=params, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logger.error("API call failed: %s %s — %s", path, params, e)
        return None


# ── Routes ────────────────────────────────────────────────

@app.route("/")
def dashboard():
    """Main dashboard — alert list with filters and summary stats."""
    severity = request.args.get("severity", "")
    status = request.args.get("status", "")

    params = {}
    if severity:
        params["severity"] = severity
    if status:
        params["status"] = status

    alerts = api_get("/api/alerts", params) or []
    stats = api_get("/api/alerts/stats") or {
        "total_alerts": 0, "open_alerts": 0, "in_progress_alerts": 0,
        "closed_alerts": 0, "critical_count": 0, "high_count": 0,
        "medium_count": 0, "low_count": 0,
    }

    if not alerts and not params:
        flash("⚠️ No alerts found or cannot connect to API backend.", "warning")

    return render_template(
        "dashboard.html",
        alerts=alerts,
        stats=stats,
        current_severity=severity,
        current_status=status,
    )


@app.route("/alert/<int:alert_id>")
def alert_detail(alert_id):
    """Alert detail view with triage actions and playbook triggers."""
    alert = api_get(f"/api/alerts/{alert_id}")
    if not alert:
        flash("❌ Alert not found.", "error")
        return redirect(url_for("dashboard"))
    return render_template("alert_detail.html", alert=alert)


@app.route("/alert/<int:alert_id>/triage", methods=["POST"])
def triage_alert(alert_id):
    """Handle triage button clicks (Acknowledge, Escalate, Close)."""
    action = request.form.get("action")
    status_map = {
        "acknowledge": "in_progress",
        "escalate": "in_progress",
        "close": "closed",
    }
    new_status = status_map.get(action)
    if new_status:
        try:
            http_requests.put(
                f"{API_URL}/api/alerts/{alert_id}",
                json={"status": new_status},
                timeout=5,
            )
            flash(f"✅ Alert #{alert_id} → {action.title()}", "success")
        except Exception as e:
            flash(f"❌ Triage failed: {e}", "error")
    return redirect(url_for("dashboard"))


@app.route("/alert/<int:alert_id>/respond", methods=["POST"])
def respond_to_alert(alert_id):
    """Trigger a mock playbook action against an alert."""
    playbook_action = request.form.get("playbook_action")
    try:
        result = http_requests.post(
            f"{API_URL}/api/alerts/{alert_id}/respond",
            json={"action": playbook_action},
            timeout=5,
        ).json()
        flash(f"✅ {result['result']}", "success")
    except Exception as e:
        flash(f"❌ Playbook failed: {e}", "error")
    return redirect(url_for("alert_detail", alert_id=alert_id))


@app.route("/playbook-logs")
def playbook_logs():
    """View recent playbook execution logs."""
    logs = api_get("/api/playbook-logs") or []
    return render_template("playbook_logs.html", logs=logs)


@app.route("/health")
def health():
    """Health check for K8s liveness probe."""
    return {"status": "healthy", "service": "soc-dashboard"}


# ── Run ───────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
