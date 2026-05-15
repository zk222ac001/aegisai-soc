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

# Get the running event loop once
main_loop = asyncio.get_event_loop()

async def process_packet(packet):
    try:        
        if detect_suspicious_ports(packet[IP].dport):
            severity = "high"
            attack_type = "Suspicious Port Access"  
        else:
            severity = "low"
            attack_type = "Network Traffic"
        # Ignore non-IP packets early
        if not packet.haslayer(IP):
            return

        ip_layer = packet[IP]

        # Detect protocol
        if packet.haslayer(TCP):
            protocol = "TCP"

        elif packet.haslayer(UDP):
            protocol = "UDP"

        else:
            protocol = "OTHER"

        if detect_port_scan(ip_layer.src, ip_layer.dport):
            severity = "high"
            attack_type = "Port Scan Detected"

        packet_count = track_flow(
               ip_layer.src,
               ip_layer.dst,
               packet[TCP].sport if packet.haslayer(TCP) else packet[UDP].sport,
               packet[TCP].dport if packet.haslayer(TCP) else packet[UDP].dport
        )
        features = extract_features(
            packet[IP].sport,
            packet[IP].dport,
            protocol,
            packet_count
            )
        
        ai_result = detector.predict(features)
        ai_anomaly = ai_result["anomaly"]
        ai_score = ai_result["score"]
        if ai_anomaly:
            severity = "critical"
            attack_type = "AI Anomaly Detected"
        
        alert = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source_ip": ip_layer.src,
            "destination_ip": ip_layer.dst,
            "protocol": protocol,
            "severity": severity,
            "attack_type": attack_type,
            "description": "Packet captured",
            "packet_count" : packet_count,
            "status": "open",
            "ai_score": ai_score,
            "ai_anomaly": ai_anomaly
        }

        print(alert)
        await manager.broadcast(alert)

    except Exception as e:
        print(f"Packet processing error: {e}")


def packet_callback(packet):
    """
    Schedule async task safely on the main loop
    without creating new event loops repeatedly.
    """
    asyncio.run_coroutine_threadsafe(
        process_packet(packet),
        main_loop
    )
def start_sniffing():
    print("[*] Starting packet capture...")
    sniff(
        prn=packet_callback,
        store=False,
        # Capture only IP packets for performance
        filter="ip"
    )