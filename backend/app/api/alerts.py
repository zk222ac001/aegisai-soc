from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from typing import Optional

from app.core.deps import get_db
from app.models.alert import Alert

router = APIRouter()
@router.get("/alerts")

def get_alerts(
    severity: Optional[str] = None,
    attack_type: Optional[str] = None,
    db: Session = Depends(get_db)
):

    query = db.query(Alert)
    
    if severity:
        query = query.filter(Alert.severity == severity)

    if attack_type:
        query = query.filter(Alert.attack_type == attack_type)

    alerts = query.order_by(Alert.timestamp.desc()).limit(100).all()

    return alerts