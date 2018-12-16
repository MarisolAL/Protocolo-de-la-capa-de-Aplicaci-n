#!/usr/bin/python           # This is server.py file

import socket  # Import socket module
from threading import *
import sys
from struct import *
import base_datos as bd
import random

class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def envia_mensaje(self, mensaje):
        MSGLEN = 1024
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(mensaje[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
            break

    def recibe_mensaje(self):
        MSGLEN = 1024
        # Esperamos la respuesta del cliente
        respuesta = False
        while not respuesta:
            chunk = self.sock.recv(min(MSGLEN - 0, 2048))
            if chunk != None:
                respuesta = True
        return chunk

    #Cierra la sesion solo si el codigo es 32
    def cierra_sesion(self,mensaje):
        codigo = mensaje[0]
        if codigo == 32:
            self.sock.close()
            print("Cerrando sesion del cliente: ",self.addr)
            exit()

    def run(self):
        chunk = self.recibe_mensaje()
        codigo1 = unpack('bi', chunk)
        codigo = codigo1[0]
        id_usr = codigo1[1]
        if not bd.valida_usuario(id_usr) or codigo != 10:
            # Usuario invalido
            mensaje = pack("b", 41)  # Mensaje de error
            self.envia_mensaje(mensaje)  # Enviamos el mensaje de error
            self.sock.close()

        id_pok, (nombre, ruta) = bd.obten_pokemon_random()
        # Creamos el struct para enviar el codigo y el mensaje con el nombre de pokemon
        mensaje_pok = nombre
        # Para este mensaje tenemos un byte para el codigo y un byte para la longitud del string
        # utilizando el tipo signed char, de esta manera mensaje_pok[0] es el codigo y
        # mensaje_pok[1] es la longitud del mensaje enviado
        mensaje_pok = pack("bb%ds" % len(mensaje_pok), 20, len(mensaje_pok), bytes(mensaje_pok, 'utf-8'))
        self.envia_mensaje(mensaje_pok)
        #En este punto necesitamos la respuesta del cliente
        recibido = self.recibe_mensaje()
        self.cierra_sesion(recibido) #Revisamos si tenemos que cerrar la sesion
        #En caso afirmativo esto ya no se va a ejecutar
        if not recibido[0] == 30:
            #Si no quiere capturarlo cerramos la sesion (aplica si recibimos un mensaje raro)
            self.cierra_sesion([32])
        intentos = 10 #Damos 10 intentos por default
        capturado = False
        while recibido[0] == 30 and intentos > 0 and  (not capturado):
            intentos -= 1
            capturado = random.choice([True, False])
            if capturado:
                #TODO Enviar imagen y codigo
                self.envia_mensaje(pack('b',22))
                #Agregamos a la pokedex del usuario
                bd.agrega_pokemon_a_pokedex(id_pok,id_usr)
                self.cierra_sesion([32])
            elif intentos == 0:
                self.envia_mensaje(pack('b', 23))
                self.cierra_sesion([32])
            else:
                #Enviamos el codigo 21 y los intentos restantes
                self.envia_mensaje(pack('bb', 21, intentos))
            recibido = self.recibe_mensaje()
        #Esta parte del codigo no deberia ejecutarse pero puede ocurrir un error raro
        mensaje = pack("b", 42)  # Mensaje de error
        self.envia_mensaje(mensaje)
        self.cierra_sesion([32])
###Main
if len(sys.argv) != 2:
    print("Uso:", sys.argv[0], "<host>")
    sys.exit(1)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host, port = sys.argv[1], 9999  # Siempre va a ser el 9999

print("Servidor inicializado!")
print("Escuchando en", (host, port))

s.bind((host, port))  # Bind to the port
s.listen(5)  # Now wait for client connection.

try:
    while True:
        c, addr = s.accept()  # Establecemos conexion con cliente
        print("Nuevo cliente! Su direccion es:", addr)
        client(c, addr)
except KeyboardInterrupt:
    print("Interrupcion de teclado \n Abortando...\n Abortando..\n Abortado X.X")
finally:
    s.close()
