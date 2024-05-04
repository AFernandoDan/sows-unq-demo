import threading
import socket
import os

INTRO_MENSAJE = "Introduce un mensaje: "

class Cliente:
    def __init__(self, host='localhost', port=12345):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.mensajes = []

    def actualizar_consola(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpia la consola
        for mensaje in self.mensajes:
            print(mensaje)

    def enviar_mensaje(self, mensaje):
        self.sock.sendall(mensaje.encode() + b'\n')

    def recibir_mensaje(self):
        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            nuevo_mensaje = f"Anonimo: {data.decode()}"
            self.mensajes.append(nuevo_mensaje)
            self.actualizar_consola()
            print(INTRO_MENSAJE)

    def enviar_mensajes_desde_stdin(self):
        while True:
            mensaje = input("Introduce un mensaje: ")
            self.mensajes.append(f"Tu: {mensaje}\n")
            self.actualizar_consola()
            self.enviar_mensaje(mensaje)

    def iniciar(self):
        threading.Thread(target=self.recibir_mensaje).start()
        threading.Thread(target=self.enviar_mensajes_desde_stdin).start()

cliente = Cliente()
cliente.iniciar()