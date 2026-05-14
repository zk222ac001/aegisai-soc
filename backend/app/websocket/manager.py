from fastapi import WebSocket
from typing import List
import json

# WebSocket connection manager for real-time communication with clients
class ConnectionManager:
    # Initialize the connection manager with an empty list of active connections
    def __init__(self):
        # List to store active WebSocket connections
        self.active_connections: List[WebSocket] = []
    
    # Accept a new WebSocket connection and add it to the list     # of active connections
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    # Remove a WebSocket connection from the list of active connections
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    # Send a personal message to a specific WebSocket connection
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    # Broadcast a message to all active WebSocket connections
    async def broadcast(self, data: dict):
        message = json.dumps(data)

        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()