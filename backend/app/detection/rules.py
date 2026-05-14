SUSPICIOUS_PORTS = [
    22,
    23,
    3389,
    445,
    1433
]

def detect_suspicious_ports(dst_port):
    if dst_port in SUSPICIOUS_PORTS:
        return True

    return False