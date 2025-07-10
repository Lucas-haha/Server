import asyncio
import websockets
import json

connected = set()
server_ready = asyncio.Event()  # <-- Đánh dấu khi server đã sẵn sàng


async def websocket_server():
    async def handler(websocket):
        print("[Server] Unity đã kết nối.")
        connected.add(websocket)
        try:
            async for _ in websocket:
                pass
        except websockets.exceptions.ConnectionClosedOK:
            pass
        except Exception as e:
            print(f"[Server] Lỗi kết nối: {e}")
        finally:
            connected.discard(websocket)
            print("[Server] Unity đã ngắt kết nối.")

    print("[Server] Đang lắng nghe tại ws://localhost:3000 ...", flush=True)
    server_ready.set()  # <-- Đánh dấu server đã sẵn sàng
    async with websockets.serve(handler, "127.0.0.1", 3000):
        await asyncio.Future()  # Để server chạy mãi mãi # Giữ server chạy mãi mãi

async def send_expression(expression):
    msg = json.dumps({
        "type": "expression",     # <-- thêm dòng này
        "expression": expression
    })
    dead = set()
    for ws in connected:
        try:
            await ws.send(msg)
            print(f"[Server] Đã gửi biểu cảm: {expression}")
        except Exception as e:
            print(f"[Server] Lỗi gửi tới client: {e}")
            dead.add(ws)
    connected.difference_update(dead)


async def send_lipsync(phenomes, duration=1.0):
    msg = json.dumps({
        "type": "lip_sync",
        "expression": phenomes,
        "duration": duration
    })
    dead = set()
    for ws in connected:
        try:
            await ws.send(msg)
            print(f"[Server] Đã gửi biểu cảm: {phenomes} (duration: {duration}s)")
        except Exception as e:
            print(f"[Server] Lỗi gửi tới client: {e}")
            dead.add(ws)
    connected.difference_update(dead)



#def start_server_in_background():
    #def run():
        #loop = asyncio.new_event_loop()
        #asyncio.set_event_loop(loop)
        #loop.run_until_complete(websocket_server())

    #thread = threading.Thread(target=run, daemon=True)
    #thread.start()
    #print("[Server] Đã khởi động trong nền.")

