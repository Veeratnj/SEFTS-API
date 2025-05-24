import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.services.stock_services import get_live_stock_prices
from typing import List
import asyncio

router = APIRouter()

@router.websocket("/ws/stocks1")
async def websocket_endpoint1(websocket: WebSocket):
    print("WebSocket connection established")
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            tokens = data.get("tokens", [])
            print(f"Received tokens: {tokens}")
            live_prices = await get_live_stock_prices(tokens)
            logging.debug(f"Sending live prices: {live_prices}")
            await websocket.send_json({"live_prices": live_prices})
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("WebSocket disconnected")


@router.websocket("/ws/stocks")
async def websocket_endpoint(websocket: WebSocket):
    print("WebSocket connection established")
    await websocket.accept()
    try:
        # Receive the initial message with client_id and tokens
        initial_data = await websocket.receive_json()
        client_id = initial_data.get("client_id")
        tokens = initial_data.get("tokens", [])
        print(f"Client ID: {client_id}, Tokens: {tokens}")

        while True:
            # Fetch live stock prices for the tokens
            live_prices = await get_live_stock_prices(tokens)
            # Convert the dictionary to a list of values
            live_prices_list = list(live_prices.values())
            logging.debug(f"Sending live prices to client {client_id}: {live_prices_list}")
            await websocket.send_json({"client_id": client_id, "live_prices": live_prices_list})
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print(f"WebSocket disconnected")