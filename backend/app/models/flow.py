from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime
from datetime import datetime

from app.core.database import Base
class NetworkFlow(Base):
    __tablename__ = "network_flows"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source_ip = Column(String)
    destination_ip = Column(String)
    source_port = Column(Integer)
    destination_port = Column(Integer)
    protocol = Column(String)
    packet_count = Column(Integer)