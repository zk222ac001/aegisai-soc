from collections import defaultdict
from datetime import datetime, timedelta

scan_tracker = defaultdict(list)

PORT_SCAN_THRESHOLD = 10
TIME_WINDOW = 10

def detect_port_scan(src_ip, dst_port):
    now = datetime.utcnow()
    scan_tracker[src_ip].append(
        (dst_port, now)
    )
    recent_attempts = [
        port for port, ts in scan_tracker[src_ip]
        if now - ts < timedelta(seconds=TIME_WINDOW)
    ]
    unique_ports = set(recent_attempts)
    if len(unique_ports) > PORT_SCAN_THRESHOLD:
        return True

    return False