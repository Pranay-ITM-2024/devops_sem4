"""
Playbook routes — mock automated response actions.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from database import get_db
from models import Alert, PlaybookLog
from schemas import PlaybookRequest, PlaybookLogResponse

router = APIRouter(prefix="/api", tags=["Playbooks"])
logger = logging.getLogger("soc-api")


@router.post("/alerts/{alert_id}/respond")
def execute_playbook(alert_id: int, request: PlaybookRequest, db: Session = Depends(get_db)):
    """Execute a mock playbook action against an alert."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    # Simulate playbook actions (these would call real APIs in production)
    action_results = {
        "block_ip": f"🚫 Blocked source IP {alert.source_ip or 'N/A'} on perimeter firewall",
        "isolate_host": f"🔒 Isolated destination host {alert.dest_ip or 'N/A'} from corporate network",
        "notify_team": f"📢 Sent alert notification to SOC team (Slack #soc-alerts) for alert #{alert_id}",
    }
    result = action_results.get(request.action, f"Unknown action: {request.action}")

    # Log the execution
    log_entry = PlaybookLog(
        alert_id=alert_id,
        action=request.action,
        status="success",
        details=result,
    )
    db.add(log_entry)

    # Update alert status to in_progress
    if alert.status == "open":
        alert.status = "in_progress"

    db.commit()
    logger.info("Playbook '%s' executed for alert #%d", request.action, alert_id)

    return {
        "alert_id": alert_id,
        "action": request.action,
        "result": result,
        "status": "success",
    }


@router.get("/playbook-logs", response_model=List[PlaybookLogResponse])
def list_playbook_logs(
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """List recent playbook execution logs."""
    logs = db.query(PlaybookLog).order_by(PlaybookLog.executed_at.desc()).limit(limit).all()
    return logs
