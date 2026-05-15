def calculate_risk_score(
    ai_score,
    suspicious_port,
    port_scan
):
    risk = 0
    
    if suspicious_port:
        risk += 30

    if port_scan:
        risk += 40

    if ai_score < 0:
        risk += 30

    return min(risk, 100)