from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.alert import Alert

# Create tables once at startup
Base.metadata.create_all(bind=engine)


def save_alert(alert: dict):    
   #  Save SOC/IDS alert into database safely 
    db: Session = SessionLocal()  # ✅ real DB session
    try:
        alert_obj = Alert(
            source_ip=str(alert.get("source_ip")),
            destination_ip=str(alert.get("destination_ip")),
            source_port=int(alert.get("source_port", 0))
            if alert.get("source_port") else None,
            destination_port=int(alert.get("destination_port", 0))
            if alert.get("destination_port") else None,
            protocol=str(alert.get("protocol")),
            severity=str(alert.get("severity")),
            attack_type=str(alert.get("attack_type")),
            description=str(alert.get("description")),
            ai_anomaly=bool(alert.get("ai_anomaly")),
            ai_score=float(alert.get("ai_score", 0.0)),
            risk_score=int(alert.get("risk_score", 0)),
            flow_packets=int(alert.get("flow_packets", 0)),
            country=str(alert.get("country")) if alert.get("country") else None,
            raw_data=str(alert)
        )
        db.add(alert_obj)
        db.commit()
        db.refresh(alert_obj)

        return alert_obj

    except Exception as e:
        db.rollback()
        print(f"[DB ERROR] {e}")
        return None

    finally:
        db.close()