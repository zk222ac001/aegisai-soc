import asyncio
import random
from datetime import datetime

from app.websocket.manager import manager

ATTACK_TYPES = [
    "Port Scan",
    "SQL Injection",
    "Brute Force",
    "Malware Traffic",
    "DNS Tunneling",
    "Ransomware Activity",
    "Suspicious Login",
]

SEVERITIES = [
    "low",
    "medium",
    "high",
    "critical"
]

SOURCE_IPS = [
    "192.168.1.10",
    "10.0.0.5",
    "172.16.1.20",
    "8.8.8.8",
    "45.33.32.156"
]

async def generate_alerts():
    while True:
        alert = {
             "id": random.randint(1000, 9999),
             "timestamp": str(datetime.utcnow()),
             "source_ip": random.choice(SOURCE_IPS),
             "destination_ip": "192.168.1.100",
             "severity": random.choice(SEVERITIES),
             "attack_type": random.choice(ATTACK_TYPES),
             "protocol": random.choice(["TCP", "UDP", "HTTP"]),
             "country": random.choice(["US", "CN", "RU", "DE"]),
             "risk_score": random.randint(1, 100),
             "description": "Suspicious activity detected",
             "created_at": str(datetime.utcnow())
        }
        print(f"[ALERT] {alert}")
        await manager.broadcast(alert)
        await asyncio.sleep(3)