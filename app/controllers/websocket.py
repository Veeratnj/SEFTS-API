from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from SmartApi import SmartConnect
from smartWebSocketV2 import SmartWebSocketV2
import pyotp
import creds  # Placeholder — later to be fetched from DB
from logzero import logger
import asyncio
from app.db.meta_data import token_map

router = APIRouter()

# ----------------------------
# WebSocket Connection Manager
# ----------------------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.client_subscriptions: dict[str, set] = {}
        self.smart_clients: dict[str, SmartWebSocketV2] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.client_subscriptions[client_id] = set()

    def disconnect(self, client_id: str):
        self.active_connections.pop(client_id, None)
        self.client_subscriptions.pop(client_id, None)

        # Close the user's websocket
        sws = self.smart_clients.pop(client_id, None)
        if sws:
            sws.close_connection()

    async def send_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)


manager = ConnectionManager()

# ----------------------------
# WebSocket Callbacks
# ----------------------------
def make_callbacks(client_id: str):
    def on_open(wsapp):
        logger.info(f"[{client_id}] WebSocket opened.")

    def on_data(wsapp, message):
        try:
            ticks = message.get("data", [])
            for tick in ticks:
                token = tick.get("token")
                ltp = tick.get("ltp") / 100.0

                stock_name = next((name for name, details in token_map.items() if token in details["tokens"]), None)
                if stock_name and stock_name in manager.client_subscriptions.get(client_id, set()):
                    msg = f"{stock_name} LTP: {ltp}"
                    asyncio.create_task(manager.send_message(msg, client_id))
        except Exception as e:
            logger.error(f"[{client_id}] Tick error: {e}")

    def on_error(wsapp, error):
        logger.error(f"[{client_id}] WebSocket error: {error}")

    def on_close(wsapp):
        logger.info(f"[{client_id}] WebSocket closed")

    return on_open, on_data, on_error, on_close

# ----------------------------
# WebSocket Endpoint
# ----------------------------
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)

    try:
        # Get user-specific creds (can later be replaced with DB lookup)
        api_key = creds.api_key
        username = creds.username
        pwd = creds.pwd
        token = creds.token

        # Generate TOTP and session
        totp = pyotp.TOTP(token).now()
        smartApi = SmartConnect(api_key)
        data = smartApi.generateSession(username, pwd, totp)

        # Start individual WebSocket
        smw = SmartWebSocketV2(
            client_code=data['data']['clientcode'],
            auth_token=data['data']['jwtToken'],
            feed_token=data['data']['feedToken'],
            api_key=api_key,
        )

        # Set callbacks for this user's socket
        on_open, on_data, on_error, on_close = make_callbacks(client_id)
        smw.on_open = on_open
        smw.on_data = on_data
        smw.on_error = on_error
        smw.on_close = on_close

        # Store the user-specific WebSocket
        manager.smart_clients[client_id] = smw

        # Start the socket connection
        smw.connect()

        while True:
            data = await websocket.receive_text()
            if data in token_map:
                # Subscribe to token
                subscription_data = token_map[data]
                manager.client_subscriptions[client_id].add(data)
                smw.subscribe("corr_id_" + client_id, 1, [subscription_data])
                await manager.send_message(f"Subscribed to {data}", client_id)

    except WebSocketDisconnect:
        manager.disconnect(client_id)
        logger.info(f"[{client_id}] Disconnected")

    except Exception as e:
        logger.error(f"[{client_id}] Error: {e}")
        manager.disconnect(client_id)
        await websocket.close()
