import asyncio
import websockets
import json

async def cargarPrograma(programa, websocket):
    path = programa["path"]
    priority = programa["priority"]
    await asyncio.sleep(1)  # Simular una operación de lectura/escritura
    msg = 'Programa cargado: ' + path + ' con prioridad: ' + str(priority)
    print(msg)
    await websocket.send(msg)
    await simularEjecucion(programa, websocket)

async def simularEjecucion(programa, websocket):
    instructions = programa["instructions"]
    for instruction in instructions:
        await asyncio.sleep(1)  # Simular una operación de lectura/escritura
        msg = 'Operación completada: ' + instruction
        print(msg)
        await websocket.send(msg)
    await websocket.send('Programa ejecutado con éxito')

async def handle_message(websocket, path):
    await websocket.send('Bienvenido al Sistema Operativo remoto, carga tus programas')
    while True:
        try:
            message = await websocket.recv()
            data = json.loads(message)
            run_data = data.get('run', {})
            instructions = run_data.get('instructions', [])
            priority = run_data.get('priority')
            path = run_data.get('path')
            programa = {
                "instructions": instructions,
                "priority": priority,
                "path": path
            }
            await cargarPrograma(programa, websocket)
        except websockets.exceptions.ConnectionClosed:
            print('La conexión con el cliente se ha cerrado')
            break

start_server = websockets.serve(handle_message, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()