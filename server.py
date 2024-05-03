import asyncio
import websockets
import json


apiIsOnline = False
logSocketList = []
logMessageQueue = asyncio.Queue()

def crearTareaSendLog(): 
    async def send_log_messages():
        while True:
            for logSocket in logSocketList:
                    message = await logMessageQueue.get()
                    await logSocket.send(message)

    asyncio.create_task(send_log_messages())

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

def mandarMensajeCadaSegundo():
    print("Mandando mensaje cada segundo")
    async def asyncFunc():
        while True:
            logMessageQueue.put_nowait("server vivo")
            await asyncio.sleep(1)
            print(logMessageQueue)
    asyncio.create_task(asyncFunc())

async def recibirProgramas(websocket):
        async for message in websocket:
            print("cabeceras websocket", websocket.request_headers)
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

async def esperarParaSiempre(websocket):
    async for message in websocket:
        pass

async def handle_message(websocket, path):
    global apiIsOnline
    if not apiIsOnline:
        mandarMensajeCadaSegundo()
        crearTareaSendLog()
        apiIsOnline = True
    await websocket.send('Bienvenido al Sistema Operativo remoto, carga tus programas')
    try:
        if websocket.request_headers["Method"] == "LOG":
            logSocketList.append(websocket)
            print("Se ha conectado un socket de log")

        elif websocket.request_headers["Method"] == "POST":
            await recibirProgramas(websocket)

        await esperarParaSiempre(websocket)
    except websockets.exceptions.ConnectionClosed:
        print('La conexión con el cliente se ha cerrado')
        # quitar de la lista de sockets de log
        if websocket in logSocketList:
            logSocketList.remove(websocket)

start_server = websockets.serve(handle_message, 'localhost', 8000)



asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()