import asyncio
import websockets
import json

async def call_websocket():
    # Define the WebSocket URL and client ID
    client_id = "python-client-123"  # Unique client ID
    uri = f"ws://localhost:8000/websocket/ws?client_id={client_id}"  # Corrected URL

    try:
        async with websockets.connect(uri,) as websocket:  # Increased timeout
            print("WebSocket connected")

            # Send a JSON payload with tokens to subscribe
            payload = {
                "tokens": ["26000", "26009", "26037"]  # Replace with desired tokens
            }
            await websocket.send(json.dumps(payload))
            print(f"Sent subscription request: {payload}")

            # Receive messages from the server
            try:
                while True:
                    response = await websocket.recv()
                    data = json.loads(response)
                    print("Message from server:", data)
            except websockets.ConnectionClosed:
                print("WebSocket connection closed")
    except asyncio.TimeoutError:
        print("WebSocket connection timed out")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the WebSocket client
asyncio.run(call_websocket())