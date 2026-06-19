"""
Health & readiness check routes — used by Kubernetes probes.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from database import get_db

router = APIRouter(tags=["Health"])


@router.get("/api/health")
def health_check():
    """Liveness probe — is the process alive?"""
    return {"status": "healthy", "service": "soc-api"}


@router.get("/api/ready")
def readiness_check(db: Session = Depends(get_db)):
    """Readiness probe — can we serve traffic (DB reachable)?"""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception as e:
        return {"status": "not_ready", "database": str(e)}
