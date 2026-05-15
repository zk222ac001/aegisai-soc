from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    Text,
    Index
)

from datetime import datetime, timezone
from app.core.database import Base


class Alert(Base):

    __tablename__ = "alerts"

    # 1) id - /Primary Key
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    # 2) Timestamp
    timestamp = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True
    )
    # 3)  source ip
    source_ip = Column(
        String(45),      # IPv4 + IPv6 support
        nullable=False,
        index=True
    )
    # 4) destination ip
    destination_ip = Column(
        String(45),
        nullable=False,
        index=True
    )
    # 5) Source Ports
    source_port = Column(
        Integer,
        nullable=True,
        index=True
    )
    # 6) Destination Ports
    destination_port = Column(
        Integer,
        nullable=True,
        index=True
    )
    # 7) Protocol
    protocol = Column(
        String(10),      # TCP / UDP / ICMP
        nullable=False,
        index=True
    )
    # 8) Severity & Attack Type
    severity = Column(
        String(20),      # low / medium / high / critical
        nullable=False,
        index=True
    )
    # 9) Attack Type
    attack_type = Column(
        String(100),
        nullable=False,
        index=True
    )
    # 10) Description
    description = Column(
        String(500),
        nullable=False
    )
    # 11) AI Anomaly Detection
    ai_anomaly = Column(
        Boolean,
        default=False,
        nullable=False,
        index=True
    )
    # 12) AI Score
    ai_score = Column(
        Float,
        default=0.0,
        nullable=False,
        index=True
    )
    # 13) Risk Scoring
    risk_score = Column(
        Integer,         # Recommended 0–100
        default=0,
        nullable=False,
        index=True
    )
    # 14) Flow packet
    flow_packets = Column(
        Integer,
        default=0,
        nullable=False
    )   
       
    #  15) Country (GeoIP)
    country = Column(
        String(2),       # ISO country code: US, DK, RU
        nullable=True,
        index=True
    )
    # 16) Raw Packet / JSON Payload
    raw_data = Column(
        Text,
        nullable=True
    )
    # Optimized Composite Indexes
    __table_args__ = (

        # Common SOC dashboard queries
        Index(
            "idx_attack_severity",
            "attack_type",
            "severity"
        ),

        # Traffic correlation
        Index(
            "idx_source_destination",
            "source_ip",
            "destination_ip"
        ),

        # AI analysis queries
        Index(
            "idx_ai_risk",
            "ai_anomaly",
            "risk_score"
        ),

        # Protocol analytics
        Index(
            "idx_protocol_country",
            "protocol",
            "country"
        ),
    )