from app.models.alert import Alert

def save_alert(db, alert_data):
    
    alert = Alert(
        source_ip=alert_data.get("source_ip"),
        destination_ip=alert_data.get("destination_ip"),
        source_port=alert_data.get("source_port"),
        destination_port=alert_data.get("destination_port"),
        protocol=alert_data.get("protocol"),
        severity=alert_data.get("severity"),
        attack_type=alert_data.get("attack_type"),
        description=alert_data.get("description"),
        ai_anomaly=alert_data.get("ai_anomaly"),
        ai_score=alert_data.get("ai_score"),
        risk_score=alert_data.get("risk_score"),
        flow_packets=alert_data.get("flow_packets"),
        country=alert_data.get("country"),
        raw_data=str(alert_data)
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert