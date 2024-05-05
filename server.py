import asyncio
import websockets
import json


apiIsOnline = False
logSocketList = []
logMessageQueue = asyncio.Queue(maxsize=5)

async def send_log_messages():
    while True:
        message = await logMessageQueue.get()
        for logSocket in logSocketList:
            try :
                await logSocket.send(message)
            except websockets.exceptions.ConnectionClosed:
                print('La conexión con el cliente se ha cerrado')
                # quitar de la lista de sockets de log
                if logSocket in logSocketList:
                    logSocketList.remove(logSocket)
        logMessageQueue.task_done()
            
async def cargarPrograma(programa):
    path = programa["path"]
    priority = programa["priority"]
    await asyncio.sleep(1)  # Simular una operación de lectura/escritura
    msg = 'Programa cargado: ' + path + ' con prioridad: ' + str(priority)
    print(msg)
    logMessageQueue.put_nowait(msg)
    await simularEjecucion(programa)

async def simularEjecucion(programa):
    instructions = programa["instructions"]
    for instruction in instructions:
        await asyncio.sleep(1)  # Simular una operación de lectura/escritura
        msg = 'Operación completada: ' + instruction
        print(msg)
        logMessageQueue.put_nowait(msg)
    await asyncio.sleep(1)  # Simular una operación de lectura/escritura
    logMessageQueue.put_nowait('Programa ejecutado con éxito')

async def mandarMensajeCadaSegundo():
    print("Mandando mensaje cada segundo")
    while True:
        logMessageQueue.put_nowait("server vivo")
        await asyncio.sleep(0.1)
        print(logMessageQueue)

async def recibirProgramas(websocket):
        logSocketList.append(websocket)
        async for message in websocket:
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
            await cargarPrograma(programa)

async def handle_message(websocket, path):
    try:
        global apiIsOnline
        if not apiIsOnline:
            # asyncio.create_task(mandarMensajeCadaSegundo())
            asyncio.create_task(send_log_messages())
            apiIsOnline = True
        await websocket.send('Bienvenido al Sistema Operativo remoto, carga tus programas')
        await recibirProgramas(websocket)
    except websockets.exceptions.ConnectionClosed:
        print('La conexión con el cliente se ha cerrado')
        # quitar de la lista de sockets de log
        if websocket in logSocketList:
            logSocketList.remove(websocket)

start_server = websockets.serve(handle_message, 'localhost', 8000)



asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()