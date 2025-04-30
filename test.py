import asyncio
import websockets
import json

async def listen():
    uri = "ws://13.127.115.72:8000/websocket/ws/stocks"
    async with websockets.connect(uri) as websocket:
        # Send initial payload
        await websocket.send(json.dumps({
            "client_id": "test_client",
            "tokens": ["RELIANCE", "TCS", "INFY"]
        }))

        while True:
            response = await websocket.recv()
            data = json.loads(response)
            print("Received:", data)

asyncio.run(listen())
