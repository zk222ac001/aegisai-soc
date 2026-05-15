from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP

from app.detection.rules import detect_suspicious_ports
from app.detection.port_scan import detect_port_scan
from app.detection.flow_tracker import track_flow

from app.ai.feature_extractor import extract_features
from app.ai.anomaly_detector import detector

from datetime import datetime, timezone
import asyncio

from app.websocket.manager import manager

from app.core.database import SessionLocal
from app.services.alert_service import save_alert


# =========================================================
# Event Loop (safe reuse)
# =========================================================
main_loop = asyncio.get_event_loop()
# =========================================================
# Packet Processing
# =========================================================

async def process_packet(packet):
    try:
        # -------------------------------------------------
        # Step 1: Filter non-IP packets
        # -------------------------------------------------
        if not packet.haslayer(IP):
            return

        ip_layer = packet[IP]

        severity = "low"
        attack_type = "Normal Traffic"

        # -------------------------------------------------
        # Step 2: Protocol detection + safe ports
        # -------------------------------------------------
        if packet.haslayer(TCP):
            protocol = "TCP"
            sport = packet[TCP].sport
            dport = packet[TCP].dport

        elif packet.haslayer(UDP):
            protocol = "UDP"
            sport = packet[UDP].sport
            dport = packet[UDP].dport

        else:
            protocol = "OTHER"
            sport = 0
            dport = 0
        # -------------------------------------------------
        # Step 3: Rule-based detection
        # -------------------------------------------------
        if detect_suspicious_ports(dport):
            severity = "high"
            attack_type = "Suspicious Port Access"

        if detect_port_scan(ip_layer.src, dport):
            severity = "high"
            attack_type = "Port Scan Detected"
        # -------------------------------------------------
        # Step 4: Flow tracking
        # -------------------------------------------------
        packet_count = track_flow(
            ip_layer.src,
            ip_layer.dst,
            sport,
            dport
        )
        # -------------------------------------------------
        # Step 5: Feature extraction (ML input)
        # -------------------------------------------------
        features = extract_features(
            sport,
            dport,
            protocol,
            packet_count,
            byte_count=len(packet),
            duration=0
        )
        # -------------------------------------------------
        # Step 6: AI prediction
        # -------------------------------------------------
        ai_result = detector.predict(features)

        ai_anomaly = ai_result.get("anomaly", False)
        ai_score = ai_result.get("ai_score", 0.0)
        risk_score = ai_result.get("risk_score", 0)

        # Override severity if AI detects anomaly
        if ai_anomaly:
            severity = "critical"
            attack_type = "AI Anomaly Detected"
        # -------------------------------------------------
        # Step 7: Alert creation
        # -------------------------------------------------
        alert = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source_ip": ip_layer.src,
            "destination_ip": ip_layer.dst,
            "protocol": protocol,
            "severity": severity,
            "attack_type": attack_type,
            "description": "Packet captured and analyzed",
            "flow_packets": packet_count,
            "ai_score": ai_score,
            "ai_anomaly": ai_anomaly,
            "risk_score": risk_score
        }

        # -------------------------------------------------
        # Step 8: Logging + DB
        # -------------------------------------------------
        print(alert)

        db = SessionLocal()
        save_alert(db, alert)
        db.close()

        # -------------------------------------------------
        # Step 9: WebSocket broadcast
        # -------------------------------------------------
        await manager.broadcast(alert)

    except Exception as e:
        print(f"Packet processing error: {e}")


# =========================================================
# Safe Scapy callback wrapper
# =========================================================

def packet_callback(packet):
    asyncio.run_coroutine_threadsafe(
        process_packet(packet),
        main_loop
    )


# =========================================================
# Start Sniffing
# =========================================================

def start_sniffing():
    print("[*] Starting packet capture...")

    sniff(
        prn=packet_callback,
        store=False,
        filter="ip"
    )