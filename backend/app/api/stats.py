from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.deps import get_db
from app.models.alert import Alert

router = APIRouter()

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    
    total_alerts = db.query(Alert).count()

    critical_alerts = db.query(Alert)\
        .filter(Alert.severity == "critical")\
        .count()

    anomalies = db.query(Alert)\
        .filter(Alert.ai_anomaly == True)\
        .count()

    return {
        "total_alerts": total_alerts,
        "critical_alerts": critical_alerts,
        "ai_anomalies": anomalies
    }