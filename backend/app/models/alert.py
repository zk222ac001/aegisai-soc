from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Index
)
from datetime import datetime, timezone
from app.core.database import Base
class Alert(Base):
    __tablename__ = "alerts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Network Information
    source_ip = Column(
        String(45),   # Supports IPv4 + IPv6
        nullable=False,
        index=True
    )

    destination_ip = Column(
        String(45),
        nullable=False,
        index=True
    )

    source_port = Column(
        Integer,
        nullable=True,
        index=True
    )

    destination_port = Column(
        Integer,
        nullable=True,
        index=True
    )

    protocol = Column(
        String(10),
        nullable=False,
        index=True
    )

    # Threat Intelligence
    country = Column(
        String(2),    # ISO country code: US, DK, RU
        nullable=True,
        index=True
    )

    severity = Column(
        String(20),   # low, medium, high, critical
        nullable=False,
        index=True
    )

    risk_score = Column(
        Float,
        default=0.0,
        nullable=False,
        index=True
    )

    confidence = Column(
        Float,
        default=0.0,
        nullable=False
    )

    # Alert Details
    attack_type = Column(
        String(100),
        nullable=False,
        index=True
    )

    description = Column(
        String(500),
        nullable=False
    )

    status = Column(
        String(20),
        default="open",
        nullable=False,
        index=True
    )

    # Metadata
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True
    )

    # Database Optimization Indexes
    __table_args__ = (

        # Fast attack/severity filtering
        Index(
            "idx_attack_severity",
            "attack_type",
            "severity"
        ),

        # Fast IP traffic analysis
        Index(
            "idx_source_destination",
            "source_ip",
            "destination_ip"
        ),

        # Fast protocol + risk queries
        Index(
            "idx_protocol_risk",
            "protocol",
            "risk_score"
        ),

        # SOC dashboard queries
        Index(
            "idx_status_created",
            "status",
            "created_at"
        ),
    )