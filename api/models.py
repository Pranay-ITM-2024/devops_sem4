from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base


class Alert(Base):
    """Security alert raised by SIEM, EDR, or threat intelligence sources."""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String(20), default="medium")       # critical, high, medium, low
    status = Column(String(20), default="open")            # open, in_progress, closed
    source = Column(String(100), nullable=True)            # e.g. "SIEM-Splunk", "EDR-CrowdStrike"
    source_ip = Column(String(45), nullable=True)
    dest_ip = Column(String(45), nullable=True)
    alert_type = Column(String(50), nullable=True)         # brute_force, malware, phishing, etc.
    assigned_to = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    closed_at = Column(DateTime, nullable=True)


class PlaybookLog(Base):
    """Log entry for every automated playbook execution."""
    __tablename__ = "playbook_logs"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"))
    action = Column(String(50))                            # block_ip, isolate_host, notify_team
    status = Column(String(20), default="success")         # success, failed
    details = Column(Text, nullable=True)
    executed_at = Column(DateTime, server_default=func.now())


class User(Base):
    """SOC analyst / admin user account."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="analyst")           # analyst, admin
    created_at = Column(DateTime, server_default=func.now())
