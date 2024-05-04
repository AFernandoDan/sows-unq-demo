import asyncio
import websockets

async def repetir_mensaje(websocket):
    i = 1
    while True:
        await websocket.send(f"Mensaje {i}")
        i += 1
        await asyncio.sleep(1)

async def esperarMensajes(websocket):
    async for message in websocket:
        print(f"Mensaje recibido: {message}")
        asyncio.create_task(websocket.send(f"Mensaje recibido: {message}"))

async def handler(websocket, path):
    try :
        tareas = [
            repetir_mensaje(websocket),
            esperarMensajes(websocket)
        ]
        await asyncio.gather(*tareas)
    except websockets.exceptions.ConnectionClosed:
        print('La conexión con el cliente se ha cerrado')
    await asyncio.wait(asyncio.all_tasks())

start_server = websockets.serve(handler, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()