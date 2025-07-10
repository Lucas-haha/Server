import asyncio
import websockets

connected = set()

async def handler(websocket):
    connected.add(websocket)
    try:
        async for message in websocket:
            print(f"Received: {message}")
            await websocket.send(f"Echo: {message}")
    finally:
        connected.remove(websocket)

async def main():
    port = int(os.environ.get("PORT", 3000))  # Lấy port từ biến môi trường Railway cấp
    async with websockets.serve(handler, "0.0.0.0", port):
        print(f"Server đang chạy trên port {port}")
        await asyncio.Future()  # chạy mãi mãi

if __name__ == "__main__":
    import os
    asyncio.run(main())
