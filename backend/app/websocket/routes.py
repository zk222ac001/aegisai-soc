from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.manager import manager

router = APIRouter()

# Endpoint to retrieve alerts (placeholder implementation)
@router.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    # Accept the WebSocket connection and add it to the
    # manager's list of active connections
    await manager.connect(websocket)
    try:
        while True:
            # Receive and process messages from the client
            data = await websocket.receive_text()
            # Send a personal message back to the client acknowledging receipt of the message
            await manager.send_personal_message(
                f"Message received: {data}",
                websocket
            )

    except WebSocketDisconnect:
        manager.disconnect(websocket)