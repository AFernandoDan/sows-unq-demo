import asyncio

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
        self.writer.close()

    def dar_bienvenida(self):
        self.writer.write("Bienvenido a chat TCP\n".encode())

class SalaChat:
    def __init__(self, host='127.0.0.1', port=12345):
        self.participantes = []
        self.host = host
        self.port = port

        asyncio.run(self.iniciar())

    def ingresar(self, participante):
        self.participantes.append(participante)

    def borrar(self, participante):
        self.participantes.remove(participante)

    def dar_bienvenida(self, participante):
        participante.dar_bienvenida()

    async def esperar_mensajes(self, participante):
        while True:
            data = await participante.reader.read(100)
            if data:
                message = data.decode()
                participante.enviar_mensaje(message)
                await participante.writer.drain()

    async def atender(self, cliente):
        try :
            self.ingresar(cliente)
            self.dar_bienvenida(cliente)
            await self.esperar_mensajes(cliente)
        except ConnectionResetError:
            print(f"Conexión perdida con {cliente.writer.get_extra_info('peername')}")
            self.borrar(cliente)

    async def recibir_clientes(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Conexión aceptada de {addr}")

        cliente = Participante(self, writer, reader)
        await self.atender(cliente)

    async def iniciar(self):
        print(f'Iniciando sala de chat...')
        server = await asyncio.start_server(
            self.recibir_clientes,
            self.host,
            self.port)

        addr = server.sockets[0].getsockname()
        print(f'Servidor escuchando en {addr}')

        async with server:
            await server.serve_forever()

SalaChat()