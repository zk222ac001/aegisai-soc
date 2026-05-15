from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.models.alert import Alert

router = APIRouter()

@router.get("/timeline")
def get_timeline(db: Session = Depends(get_db)):
    
    alerts = db.query(Alert)\
        .order_by(Alert.timestamp.desc())\
        .limit(50)\
        .all()

    return [{
            "time": a.timestamp,
            "event": a.attack_type,
            "severity": a.severity
             }
        for a in alerts
    ]