import asyncio
import websockets
import json

# Manejador para el evento de conexión
async def handle_connection(websocket, path):
    print("Cliente conectado")

    asyncio.create_task(websocket.send("Conexión exitosa"))
# Manejador para el evento de desconexión
async def handle_disconnection(websocket):
    print("Cliente desconectado")
    # Aquí puedes realizar tareas de limpieza o notificar a otros clientes

# Manejador para el evento personalizado "evento1"
async def handle_evento1(websocket, data):
    print(f"Evento personalizado 'evento1' recibido: {data}")
    # Aquí puedes definir acciones específicas para el evento1
    await websocket.send("Evento personalizado 'evento1' recibido")

# Manejador para el evento personalizado "evento2"
async def handle_evento2(websocket, data):
    print(f"Evento personalizado 'evento2' recibido: {data}")
    message = "Evento personalizado 'evento2' recibido"
    if data:
        await websocket.send(message + f" con datos: {data}")
    else:
        await websocket.send(message + " sin datos")

# Asigna el manejador "handle_evento1" al evento "evento1"
event_handlers = {
    "evento1": handle_evento1,
    "evento2": handle_evento2
}

async def try_parse_and_use_handler(message, websocket, path):
    try:
        await asyncio.sleep(3)
        data = json.loads(message) # Implementa tu lógica para analizar el mensaje
        event_of_message = data.get("event")
        if event_handlers.get(event_of_message) is not None:
            asyncio.create_task(event_handlers[event_of_message](websocket, data.get("data")))
        else:
            print(f"Evento desconocido: {event_of_message}")
            asyncio.create_task(websocket.send(f"Evento desconocido: {event_of_message}"))
    except Exception as e:
        print(f"Error al procesar el mensaje: {e}")
        asyncio.create_task(websocket.send(f"Error al procesar el mensaje: {e}"))


# Manejador general para todos los eventos
async def handle_events(websocket, path):
    try:
        asyncio.create_task(handle_connection(websocket, path))
        async for message in websocket:
            asyncio.create_task(try_parse_and_use_handler(message, websocket, path))
    except websockets.ConnectionClosed:
        print("La conexión con el cliente " + str(websocket.remote_address) + " se ha cerrado")
        asyncio.create_task(handle_disconnection(websocket))
    except json.JSONDecodeError:
        print("Error al decodificar el mensaje JSON")
        asyncio.create_task(websocket.send("Error al decodificar el mensaje JSON"))

# Crea un servidor WebSocket en el puerto 8765
start_server = websockets.serve(handle_events, "localhost", 8765)

# Ejecuta el servidor de manera indefinida
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()