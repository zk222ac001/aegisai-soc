from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from contextlib import asynccontextmanager

import asyncio
import threading

from app.api.alerts import router as alert_router
from app.websocket.routes import router as websocket_router

from app.services.alert_generator import generate_alerts
from app.detection.packet_sniffer import start_sniffing

from app.ai.anomaly_detector import detector

# For stats endpoint
from app.api.stats import router as stats_router

# For timeline endpoint
from app.api.timeline import router as timeline_router

from app.core.database import Base, engine
from app.models.alert import Alert  # important: register model

# Create database tables
Base.metadata.create_all(bind=engine)

# Load or train the anomaly detection model at startup
detector.load_model()

# Store background task references
background_tasks = []

# Store sniffing thread reference
sniff_thread = None

# Note: In production, consider using a more robust task management system (e.g., Celery) and proper thread management for the sniffer.
@asynccontextmanager
async def lifespan(app: FastAPI):

    print("[*] Starting AI SOC Platform...")
    
    # Start async background task
    alert_task = asyncio.create_task(generate_alerts())
    background_tasks.append(alert_task)
    
    # Start packet sniffer thread
    global sniff_thread
    
    sniff_thread = threading.Thread(
        target=start_sniffing,
        daemon=True
    )
    sniff_thread.start()
    yield
    print("[*] Shutting down AI SOC Platform...")
    # Cancel async tasks gracefully
    for task in background_tasks:
        task.cancel()
    await asyncio.gather(*background_tasks, return_exceptions=True)


app = FastAPI(
    title="AI SOC Platform",
    lifespan=lifespan
)



# Better production CORS config
app.add_middleware(
    CORSMiddleware,

    # Replace with frontend URL in production
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(alert_router)
app.include_router(websocket_router)
app.include_router(stats_router)
app.include_router(timeline_router)
@app.get("/")
async def root():
    return {
        "status": "running",
        "platform": "AI SOC Dashboard"
    }   