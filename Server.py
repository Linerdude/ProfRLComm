import matplotlib.pyplot as plt
import numpy as np

# server.py
import asyncio
import websockets

connected_clients = set()  # Stores active client connections


async def handler(websocket, path):
    print("Client connected.")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received from client: {message}")
            # Echo back or broadcast
            await websocket.send(f"Server received: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected.")
    finally:
        connected_clients.remove(websocket)


async def send_to_all(message):
    if connected_clients:
        await asyncio.gather(*(client.send(message) for client in connected_clients))


async def periodic_server_message():
    while True:
        await asyncio.sleep(5)  # Send message every 5 seconds
        await send_to_all("Hello from the server!")


async def main():
    server = await websockets.serve(handler, "0.0.0.0", 8765)
    print("Server started on port 8765")
    await asyncio.gather(server.wait_closed(), periodic_server_message())


asyncio.run(main())
