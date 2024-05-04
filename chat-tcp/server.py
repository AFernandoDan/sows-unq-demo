import asyncio

class SalaDeChat:
    def __init__(self):
        self.participantes = set()

    def ingresar(self, participante):
        self.participantes.add(participante)

class Participante:
    def __init__(self, sala, writer, reader):
        self.sala = sala
        self.writer = writer
        self.reader = reader

    def recibir_mensaje(self, mensaje):
        self.writer.write(mensaje.encode())

    def enviar_mensaje(self, mensaje):
        for participante in self.sala.participantes:
            if participante != self:
                participante.recibir_mensaje(mensaje)

    def borrar(self):
        self.sala.participantes.remove(self)

    def dar_bienvenida(self):
        self.writer.write("Bienvenido a chat TCP\n".encode())

sala = SalaDeChat()

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Conexión aceptada de {addr}")

    cliente = Participante(sala, writer, reader)
    sala.ingresar(cliente)

    cliente.dar_bienvenida()

    while True:
        data = await reader.read(100)
        if data:
            message = data.decode()
            # enviar mensaje a todos los participantes
            cliente.enviar_mensaje(message)
            await writer.drain()
        else:
            print("Cerrando la conexión")
            writer.close()
            cliente.borrar()
            break

async def main():
    server = await asyncio.start_server(
        handle_client,
        '127.0.0.1',
        12345)

    addr = server.sockets[0].getsockname()
    print(f'Servidor escuchando en {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())