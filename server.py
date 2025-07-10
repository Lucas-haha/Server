import asyncio
from aiohttp import web
import os


connected = set()

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    connected.add(ws)
    print(f"[Server] Client kết nối. Tổng client: {len(connected)}")
    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                print(f"[Server] Nhận: {msg.data}")

                # Gửi broadcast tới tất cả client, không chỉ client gửi
                await broadcast(msg.data)

            elif msg.type == web.WSMsgType.ERROR:
                print(f"[Server] Lỗi WebSocket: {ws.exception()}")
    finally:
        connected.remove(ws)
        print(f"[Server] Client ngắt kết nối. Tổng client còn lại: {len(connected)}")
    return ws

async def health_check(request):
    return web.Response(text="OK")

async def broadcast(message):
    if not connected:
        print("[Server] Không có client để gửi broadcast.")
        return
    dead = set()
    for ws in connected:
        try:
            await ws.send_str(message)
        except Exception as e:
            print(f"[Server] Lỗi gửi broadcast: {e}")
            dead.add(ws)
    connected.difference_update(dead)

app = web.Application()
app.router.add_get('/ws', websocket_handler)   # websocket chạy ở /ws
app.router.add_get('/health', health_check)    # health check /health  # health check HEAD /health

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    web.run_app(app, host='0.0.0.0', port=port)
