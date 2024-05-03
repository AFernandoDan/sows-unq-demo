import asyncio
import websockets
import json

async def cargarPrograma(programa, message_queue):
    path = programa["path"]
    priority = programa["priority"]
    await asyncio.sleep(1)  # Simular una operación de lectura/escritura
    msg = 'Programa cargado: ' + path + ' con prioridad: ' + str(priority)
    print(msg)
    message_queue.put_nowait(msg)
    await simularEjecucion(programa, message_queue)

async def simularEjecucion(programa, message_queue):
    instructions = programa["instructions"]
    for instruction in instructions:
        await asyncio.sleep(1)  # Simular una operación de lectura/escritura
        msg = 'Operación completada: ' + instruction
        print(msg)
        message_queue.put_nowait(msg)
    await asyncio.sleep(1)  # Simular una operación de lectura/escritura
    message_queue.put_nowait('Programa ejecutado con éxito')

async def send_messages(websocket, message_queue):
    while True:
        print('Esperando mensaje en cola')
        message = await message_queue.get()
        await websocket.send(message)
        

async def handle_message(websocket, path):
    message_queue = asyncio.Queue()
    asyncio.create_task(send_messages(websocket, message_queue))
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
            await cargarPrograma(programa, message_queue)
            # send no async msg
            
        except websockets.exceptions.ConnectionClosed:
            print('La conexión con el cliente se ha cerrado')
            break

start_server = websockets.serve(handle_message, 'localhost', 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class Server(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/json':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 - No encontrado')

def run(server_class=HTTPServer, handler_class=Server):
    server_address = ('', 8001)
    httpd = server_class(server_address, handler_class)
    print('Servidor HTTP corriendo en el puerto 8001...')
    httpd.serve_forever()

run()