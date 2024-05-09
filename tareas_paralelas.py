import asyncio
import websockets

websockets_list = []
message_queue = asyncio.Queue()

def borrar_cerrados():
    for ws in websockets_list:
        if ws.closed:
            websockets_list.remove(ws)

def enviar_mensaje(websocket, message):
    try:
        asyncio.create_task(websocket.send(message))
    except websockets.exceptions.ConnectionClosed:
        print('La conexión con el cliente se ha cerrado')
        websockets_list.remove(websocket)

async def cargar_mensaje_a_la_cola():
    while True:
        # carga mensajes a la message_list
        message_queue.put_nowait("Mensaje de la cola")
        await asyncio.sleep(0.5)

async def enviar_mensajes_de_la_lista():
    while True:
        # toma la message_list y enviarla a todos los websockets
        message = await message_queue.get()
        borrar_cerrados()
        print(f"Enviando mensaje: {message}")

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

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().create_task(cargar_mensaje_a_la_cola())
asyncio.get_event_loop().create_task(enviar_mensajes_de_la_lista())
asyncio.get_event_loop().run_forever()