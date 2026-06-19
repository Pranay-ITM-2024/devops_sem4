from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ── Alert Schemas ──────────────────────────────────────────

class AlertCreate(BaseModel):
    """Schema for creating a new alert."""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    severity: str = Field(default="medium", pattern="^(critical|high|medium|low)$")
    source: Optional[str] = None
    source_ip: Optional[str] = None
    dest_ip: Optional[str] = None
    alert_type: Optional[str] = None


class AlertUpdate(BaseModel):
    """Schema for updating an existing alert (triage actions)."""
    status: Optional[str] = Field(default=None, pattern="^(open|in_progress|closed)$")
    assigned_to: Optional[str] = None


class AlertResponse(BaseModel):
    """Schema returned when reading an alert."""
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
    updated_at: Optional[datetime]
    closed_at: Optional[datetime]

    class Config:
        from_attributes = True


# ── Playbook Schemas ───────────────────────────────────────

class PlaybookRequest(BaseModel):
    """Schema for triggering a mock playbook action."""
    action: str = Field(..., pattern="^(block_ip|isolate_host|notify_team)$")


class PlaybookLogResponse(BaseModel):
    """Schema returned when reading a playbook log entry."""
    id: int
    alert_id: int
    action: str
    status: str
    details: Optional[str]
    executed_at: datetime

    class Config:
        from_attributes = True


# ── Stats Schema ───────────────────────────────────────────

class StatsResponse(BaseModel):
    """Dashboard summary statistics."""
    total_alerts: int
    open_alerts: int
    in_progress_alerts: int
    closed_alerts: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int


# ── Auth Schemas ───────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
