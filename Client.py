# client.py
import asyncio
import websockets


async def listen_to_server():
    uri = "ws://192.168.50.195:8765"  # Replace with your server's local IP
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello from client!")
        while True:
            message = await websocket.recv()
            print(f"Server says: {message}")


asyncio.run(listen_to_server())
