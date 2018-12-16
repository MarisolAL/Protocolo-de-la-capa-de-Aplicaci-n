#!/usr/bin/env python3

import sys
import socket
import types

messages = [b"Message 1 from client.", b"Message 2 from client."]

def es_entero(s):
    try:
        int(s)
        return True
    except ValueError:
        return False





if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <puerto> <Id de usuario>")
    sys.exit(1)
if not es_entero(sys.argv[3]):
    print("El id debe ser un entero")
    sys.exit(1)
if not es_entero(sys.argv[2]):
    print("El puerto debe ser un entero")
    sys.exit(1)
host, port, id_usuario = sys.argv[1:4]
id_usuario = int(id_usuario)

server_addr = (host, int(port))
print("Inicializando la conexion en ", server_addr)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setblocking(False)
sock.connect_ex(server_addr)
try:
    while True:
        MSGLEN = 1024
        totalsent = 0
        msg = b'%d'%id_usuario
        while totalsent < MSGLEN:
            sent = sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
            break
except KeyboardInterrupt:
    print("Interrupcion de teclado \n Abortando...\n Abortando..\n Abortado X.X")
finally:
    sock.close()