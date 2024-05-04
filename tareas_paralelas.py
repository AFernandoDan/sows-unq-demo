import asyncio
import websockets

websockets_list = []

def borrar_cerrados():
    for ws in websockets_list:
        if ws.closed:
            websockets_list.remove(ws)

def enviar_mensaje(websocket, message):
    asyncio.create_task(websocket.send(message))

async def repetir_mensaje_para_todos():
    i = 1
    while True:
        borrar_cerrados()
        for ws in websockets_list:
                enviar_mensaje(ws, f"Mensaje {i}")
        i += 1
        await asyncio.sleep(1)

async def esperarMensajes(websocket):
    async for message in websocket:
        print(f"Mensaje recibido: {message}")
        enviar_mensaje(websocket, f"Recibido: {message}")

async def handler(websocket, path):
    try :
        websockets_list.append(websocket)
        tareas = [
            esperarMensajes(websocket)
        ]
        await asyncio.gather(*tareas)
    except websockets.exceptions.ConnectionClosed:
        print('La conexión con el cliente se ha cerrado')
        websockets_list.remove(websocket)
    await asyncio.wait(asyncio.all_tasks())

start_server = websockets.serve(handler, "localhost", 8000)

asyncio.get_event_loop().create_task(repetir_mensaje_para_todos())
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()