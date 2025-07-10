import asyncio
import websockets
import os

connected = set()

async def handler(websocket):
    connected.add(websocket)
    print(f"[Server] Client kết nối. Tổng client: {len(connected)}")
    try:
        async for message in websocket:
            print(f"[Server] Nhận: {message}")
            # Echo lại client gửi
            await websocket.send(f"Echo: {message}")
    except websockets.ConnectionClosedOK:
        print("[Server] Client đóng kết nối bình thường.")
    except websockets.ConnectionClosedError:
        print("[Server] Client đóng kết nối bất thường.")
    finally:
        connected.remove(websocket)
        print(f"[Server] Client ngắt kết nối. Tổng client còn lại: {len(connected)}")

async def broadcast(message):
    if not connected:
        print("[Server] Không có client để gửi broadcast.")
        return
    dead = set()
    for ws in connected:
        try:
            await ws.send(message)
        except Exception as e:
            print(f"[Server] Lỗi gửi broadcast: {e}")
            dead.add(ws)
    connected.difference_update(dead)

async def main():
    port = int(os.environ.get("PORT", 3000))
    async with websockets.serve(handler, "0.0.0.0", port):
        print(f"[Server] Đang chạy trên port {port}")
        await asyncio.Future()  # chạy mãi mãi

if __name__ == "__main__":
    asyncio.run(main())
