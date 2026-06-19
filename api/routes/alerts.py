"""
Alert routes — CRUD operations for security alerts.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import logging

from database import get_db
from models import Alert
from schemas import AlertCreate, AlertUpdate, AlertResponse, StatsResponse

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])
logger = logging.getLogger("soc-api")


@router.get("", response_model=List[AlertResponse])
def list_alerts(
    severity: Optional[str] = None,
    status: Optional[str] = None,
    alert_type: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all alerts with optional filters and pagination."""
    query = db.query(Alert)
    if severity:
        query = query.filter(Alert.severity == severity)
    if status:
        query = query.filter(Alert.status == status)
    if alert_type:
        query = query.filter(Alert.alert_type == alert_type)
    alerts = query.order_by(Alert.created_at.desc()).offset(skip).limit(limit).all()
    logger.info("Listed %d alerts (severity=%s, status=%s)", len(alerts), severity, status)
    return alerts


@router.get("/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    """Return dashboard summary statistics."""
    return StatsResponse(
        total_alerts=db.query(Alert).count(),
        open_alerts=db.query(Alert).filter(Alert.status == "open").count(),
        in_progress_alerts=db.query(Alert).filter(Alert.status == "in_progress").count(),
        closed_alerts=db.query(Alert).filter(Alert.status == "closed").count(),
        critical_count=db.query(Alert).filter(Alert.severity == "critical").count(),
        high_count=db.query(Alert).filter(Alert.severity == "high").count(),
        medium_count=db.query(Alert).filter(Alert.severity == "medium").count(),
        low_count=db.query(Alert).filter(Alert.severity == "low").count(),
    )


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    """Get a single alert by ID."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.post("", response_model=AlertResponse, status_code=201)
def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    """Create a new security alert."""
    db_alert = Alert(**alert.model_dump())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    logger.info("Created alert #%d: %s [%s]", db_alert.id, db_alert.title, db_alert.severity)
    return db_alert


@router.put("/{alert_id}", response_model=AlertResponse)
def update_alert(alert_id: int, alert: AlertUpdate, db: Session = Depends(get_db)):
    """Update an alert's status or assignment (triage action)."""
    db_alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    if alert.status:
        db_alert.status = alert.status
        if alert.status == "closed":
            db_alert.closed_at = datetime.utcnow()
    if alert.assigned_to:
        db_alert.assigned_to = alert.assigned_to
    db.commit()
    db.refresh(db_alert)
    logger.info("Updated alert #%d: status=%s", alert_id, db_alert.status)
    return db_alert


@router.delete("/{alert_id}", status_code=204)
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    """Delete an alert."""
    db_alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    db.delete(db_alert)
    db.commit()
    logger.info("Deleted alert #%d", alert_id)
