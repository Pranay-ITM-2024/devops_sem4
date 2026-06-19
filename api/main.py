"""
SOC Automation Platform — FastAPI Backend
==========================================
Main application entry point. Registers all routes and configures
Prometheus metrics instrumentation.
"""
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import logging
import sys

from database import engine, Base
from routes.alerts import router as alerts_router
from routes.playbooks import router as playbooks_router
from routes.health import router as health_router

# ── Structured logging ────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s","level":"%(levelname)s","service":"soc-api","msg":"%(message)s"}',
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("soc-api")

# ── Create database tables ────────────────────────────────
Base.metadata.create_all(bind=engine)

# ── FastAPI application ───────────────────────────────────
app = FastAPI(
    title="SOC Automation API",
    description="Security Operations Center — Alert Management & Automated Response API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── Register routers ──────────────────────────────────────
app.include_router(alerts_router)
app.include_router(playbooks_router)
app.include_router(health_router)

# ── Prometheus metrics ────────────────────────────────────
Instrumentator().instrument(app).expose(app)

# ── Startup log ───────────────────────────────────────────
logger.info("SOC Automation API started successfully")
