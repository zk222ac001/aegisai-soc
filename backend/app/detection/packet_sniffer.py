from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP

from datetime import datetime, timezone
import asyncio

from app.websocket.manager import manager

# Get the running event loop once
main_loop = asyncio.get_event_loop()

async def process_packet(packet):
    try:
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

        alert = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source_ip": ip_layer.src,
            "destination_ip": ip_layer.dst,
            "protocol": protocol,
            "severity": "low",
            "attack_type": "Network Traffic",
            "description": "Packet captured"
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