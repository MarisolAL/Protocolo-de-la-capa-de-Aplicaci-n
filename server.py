#!/usr/bin/env python3

import sys
import socket
from threading import *


class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def run(self):
        while 1:
            print('Client sent:', self.sock.recv(1024).decode())
            self.sock.send(b'Me enviaste algo')


def on_new_client(clientsocket):
    while True:
        msg = clientsocket.sock.recv(1024)
        print(clientsocket.addr, ' >> ', msg)
        # hacer cosas aqui
        clientsocket.send(msg)
    clientsocket.close()


# Parte del main
if len(sys.argv) != 2:  # Necesitamos el puerto
    print("Uso:", sys.argv[0], "<host>")
    sys.exit(1)

host, port = sys.argv[1], 9999  # Siempre va a ser el 9999
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Servidor inicializado!")
print("Escuchando en", (host, port))
lsock.bind((host, port))
lsock.listen(1)
lsock.setblocking(False)
try:
    while True:
        print("Nueva conexion!")
        clientsocket, address = lsock.accept()
        print(address)
        client(clientsocket, address)
        on_new_client(client)
except KeyboardInterrupt:
    print("Interrupcion de teclado \n Abortando...\n Abortando..\n Abortado X.X")
finally:
    lsock.close()
