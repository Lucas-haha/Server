import asyncio
import websockets
import os

connected = set()

async def handler(websocket):
    # Thêm client mới vào tập connected
    connected.add(websocket)
    print(f"[Server] Client kết nối. Tổng: {len(connected)}")
    try:
        async for message in websocket:
            print(f"[Server] Nhận được: {message}")
            # Ví dụ echo lại cho client gửi
            await websocket.send(f"Echo: {message}")
    except websockets.ConnectionClosedOK:
        print("[Server] Client đóng kết nối bình thường.")
    except websockets.ConnectionClosedError:
        print("[Server] Client đóng kết nối bất thường.")
    finally:
        connected.remove(websocket)
        print(f"[Server] Client ngắt kết nối. Tổng còn lại: {len(connected)}")

async def main():
    port = int(os.environ.get("PORT", 3000))
    async with websockets.serve(handler, "0.0.0.0", port):
        print(f"[Server] Đang chạy trên port {port}")
        await asyncio.Future()  # giữ server chạy mãi

if __name__ == "__main__":
    asyncio.run(main())
