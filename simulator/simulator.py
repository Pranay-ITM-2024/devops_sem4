"""
SOC Alert Simulator
====================
Generates realistic fake security alerts and posts them to the
FastAPI backend at a configurable interval. Used to populate the
dashboard with demo data.
"""
import requests
import random
import time
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("alert-simulator")

API_URL = os.getenv("API_URL", "http://localhost:8000")

# ── Alert templates ───────────────────────────────────────
ALERT_TEMPLATES = [
    {
        "title": "Brute force SSH login attempt",
        "alert_type": "brute_force",
        "severity": "high",
        "source": "SIEM-Splunk",
        "description": "Over 50 failed SSH login attempts in 5 minutes from a single IP address.",
    },
    {
        "title": "Ransomware signature detected on endpoint",
        "alert_type": "malware",
        "severity": "critical",
        "source": "EDR-CrowdStrike",
        "description": "Known WannaCry ransomware hash matched on workstation process.",
    },
    {
        "title": "Phishing email with malicious attachment",
        "alert_type": "phishing",
        "severity": "medium",
        "source": "Email-Gateway",
        "description": "User reported email containing a .docm file with suspicious macros.",
    },
    {
        "title": "External port scan detected",
        "alert_type": "port_scan",
        "severity": "low",
        "source": "SIEM-QRadar",
        "description": "Sequential TCP SYN scan across ports 1-1024 from external IP.",
    },
    {
        "title": "Privilege escalation via sudo abuse",
        "alert_type": "priv_escalation",
        "severity": "critical",
        "source": "EDR-SentinelOne",
        "description": "Unauthorized user ran sudo command to gain root access on prod server.",
    },
    {
        "title": "Suspected data exfiltration via HTTPS",
        "alert_type": "data_exfil",
        "severity": "high",
        "source": "DLP-System",
        "description": "Unusual 2.5GB data transfer to external cloud storage IP detected.",
    },
    {
        "title": "Admin panel unauthorized access attempt",
        "alert_type": "unauth_access",
        "severity": "high",
        "source": "WAF",
        "description": "Multiple 403 errors followed by a successful login on /admin endpoint.",
    },
    {
        "title": "DNS tunneling activity detected",
        "alert_type": "dns_tunnel",
        "severity": "medium",
        "source": "SIEM-Splunk",
        "description": "Encoded DNS TXT queries to suspicious domain suggesting C2 channel.",
    },
    {
        "title": "Lateral movement via PsExec",
        "alert_type": "lateral_movement",
        "severity": "critical",
        "source": "EDR-CrowdStrike",
        "description": "PsExec used to remotely execute commands on 3 internal servers.",
    },
    {
        "title": "Cryptominer process detected",
        "alert_type": "cryptominer",
        "severity": "medium",
        "source": "EDR-SentinelOne",
        "description": "XMRig mining process consuming 95% CPU on web server.",
    },
]


def random_ip():
    """Generate a random public-ish IP address."""
    return f"{random.randint(1, 254)}.{random.randint(0, 254)}.{random.randint(0, 254)}.{random.randint(1, 254)}"


def random_internal_ip():
    """Generate a random internal IP address."""
    return f"10.0.{random.randint(1, 20)}.{random.randint(1, 254)}"


def generate_alert():
    """Pick a random template, add random IPs, and POST to the API."""
    template = random.choice(ALERT_TEMPLATES)
    alert = {
        **template,
        "source_ip": random_ip(),
        "dest_ip": random_internal_ip(),
    }
    try:
        resp = requests.post(f"{API_URL}/api/alerts", json=alert, timeout=5)
        severity_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵"}
        icon = severity_icon.get(alert["severity"], "⚪")
        logger.info(
            "%s [%s] %s → %s  (HTTP %d)",
            icon, alert["severity"].upper(), alert["title"], alert["source_ip"], resp.status_code,
        )
    except requests.exceptions.ConnectionError:
        logger.error("❌ Cannot connect to API at %s", API_URL)
    except Exception as e:
        logger.error("❌ Failed to create alert: %s", e)


def main():
    interval = int(os.getenv("INTERVAL_SECONDS", "30"))
    logger.info("🚨 Alert Simulator started")
    logger.info("   API URL: %s", API_URL)
    logger.info("   Interval: %d seconds", interval)
    logger.info("   Templates: %d alert types", len(ALERT_TEMPLATES))
    logger.info("─" * 50)

    while True:
        generate_alert()
        time.sleep(interval)


if __name__ == "__main__":
    main()
