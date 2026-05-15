from app.core.database import engine, Base

from app.models.alert import Alert
from app.models.flow import NetworkFlow

Base.metadata.create_all(bind=engine)

print(" Alerts [DB] Tables created.")