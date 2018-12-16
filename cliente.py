#!/usr/bin/env python3

import sys
import socket
from struct import *

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

def envia_mensaje(sock, mensaje):
    MSGLEN = 1024
    totalsent = 0
    while totalsent < MSGLEN:
        sent = sock.send(mensaje[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent
        break

def recibe_mensaje(sock):
    # Esperamos la respuesta del servidor
    while True:
        chunk = sock.recv(min(MSGLEN - 0, 2048))
        return chunk
        break

def termina_sesion(sock):
    envia_mensaje(sock, pack('b', 32))  # Enviamos mensaje de termino de sesion
    sock.close()
    exit()


server_addr = (host, int(port))
print("Inicializando la conexion en ", server_addr)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect_ex(server_addr)
try:
    MSGLEN = 1024
    totalsent = 0
    #Comenzamos con el mensaje inicial con el codigo 10 y el id
    msg = pack('hi',10,id_usuario)
    envia_mensaje(sock,msg)
    chunk = recibe_mensaje(sock)
    codigo = chunk[0]
    #En este punto el codigo puede ser 11 o 20
    if codigo == 11:
        print("El ID ingresado es invalido, intente con otro please")
        termina_sesion(sock)
    if not codigo == 20:
        print("Ha ocurrido un error! Intenta de nuevo por favor :(")
        termina_sesion(sock)
    #Nos regreso un string con pokemon con el codigo 20
    longitud_string = chunk[1]
    #Decodificamos el mensaje que recibimos donde esta el nombre del pokemon
    # y pasamos los bytes decodificados a un string para imprimir el mensaje al cliente
    nombre_pokemon = unpack('%ds'%longitud_string ,chunk[2:])[0].decode("utf-8")
    print("Gusta capturar al pokemon %s?"%nombre_pokemon)
    text = input("[si/No]")
    if text != "si":
        print("Terminando sesion")
        termina_sesion(sock)
    print("Tienes 10 intentos")

except KeyboardInterrupt:
    print("Interrupcion de teclado \n Abortando...\n Abortando..\n Abortado X.X")
finally:
    sock.close()