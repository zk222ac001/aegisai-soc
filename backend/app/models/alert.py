from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.core.database import Base
class Alert(Base):
    __tablename__ = "alerts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    source_ip: Mapped[str] = mapped_column(String, nullable=True)
    destination_ip: Mapped[str] = mapped_column(String, nullable=True)
    source_port: Mapped[int] = mapped_column(Integer, nullable=True)
    destination_port: Mapped[int] = mapped_column(Integer, nullable=True)
    protocol: Mapped[str] = mapped_column(String, nullable=True)
    severity: Mapped[str] = mapped_column(String, nullable=True)
    attack_type: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    ai_anomaly: Mapped[bool] = mapped_column(Boolean, default=False)
    ai_score: Mapped[float] = mapped_column(Float, default=0.0)
    risk_score: Mapped[int] = mapped_column(Integer, default=0)
    flow_packets: Mapped[int] = mapped_column(Integer, default=0)
    country: Mapped[str] = mapped_column(String, nullable=True)
    raw_data: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)