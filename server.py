#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
from threading import *
import sys

class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def run(self):
        while 1:
            print('Cliente enviar:', self.sock.recv(1024).decode())
            self.sock.send(b'Me enviaste algo')

def on_new_client(cliente):
    while True:
        msg = cliente.sock.recv(1024)
        #verificaciones aqui
        print(cliente.addr, ' >> ', msg)
        #hacer aqui
        cliente.sock.send(msg)
    clientsocket.close()

if len(sys.argv) != 2:
    print("Uso:", sys.argv[0], "<host>")
    sys.exit(1)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host, port = sys.argv[1], 9999  # Siempre va a ser el 9999

print("Servidor inicializado!")
print("Escuchando en", (host, port))

s.bind((host, port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.

try:
    while True:
       c, addr = s.accept()     # Establecemos conexion con cliente
       print("Nuevo cliente! Su direccion es:", addr)
       client(c, addr)
except KeyboardInterrupt:
    print("Interrupcion de teclado \n Abortando...\n Abortando..\n Abortado X.X")
finally:
    s.close()
