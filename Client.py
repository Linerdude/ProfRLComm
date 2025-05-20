# client.py
import asyncio
import websockets
import threading
from GUI import GUI
import matplotlib.pyplot as plt

gui = GUI()


async def listen_to_server():
    uri = "ws://10.55.10.212:8765"  # Replace with your server's local IP
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello from client!")
        while True:
            message = await websocket.recv()
            print(f"Server says: {message}")
            # Parse and update GUI here if message is a block
            # Example message: "green triangle"
            try:
                color, shape = message.strip().split(",")
                gui.add_their_block(color, shape)
            except Exception as e:
                print(f"Invalid message or GUI error: {e}")

async def update_gui():
    while True:
        plt.pause(0.05)  # Allow GUI to update
        await asyncio.sleep(0.05)

async def main():
    task1 = asyncio.create_task(listen_to_server())
    task2 = asyncio.create_task(update_gui())
    await asyncio.gather(task1, task2)

if __name__ == "__main__":
    gui.main(init_only=True)  # Only initialize GUI, don’t block with plt.show()
    asyncio.run(main())