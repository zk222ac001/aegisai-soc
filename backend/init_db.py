from app.core.database import engine
from app.models.alert import Alert

Alert.metadata.create_all(bind=engine)

print("Database initialized.")