#!/usr/bin/env python3

import sys
import socket
from struct import *
from PIL import Image
import io

def es_entero(s):
    '''
    Funcion de verificacion que nos dice si s es un
    entero al hacer el cast
    :param s: str
        String que queremos verificar
    :return: True si en efecto se trata de un entero, False en otro caso
    '''
    try:
        int(s)
        return True
    except ValueError:
        return False

def envia_mensaje(sock, mensaje):
    '''
    Funcion que se encarga de enviar el mensaje a traves del socket
    :param sock: Socket a traves del cual mandaremos el mensaje
    :param mensaje: Mensaje que queremos mandar ya codificado
    :return: void
    '''
    MSGLEN = 1024
    totalsent = 0
    while totalsent < MSGLEN:
        sent = sock.send(mensaje[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent
        break

def recibe_mensaje(sock,MSGLEN = 1024):
    '''
    Funcion que se encarga de la recepcion de mensajes
    :param sock: socket que recibira el mensaje
    :param MSGLEN: Tama;o del buffer sobre el que leeremps
    :return: El mensaje obtenido del socket
    '''
    return sock.recv(MSGLEN)


def termina_sesion(sock):
    '''
    Funcion que se encarga de enviar un mensaje de fin de sesion al
    servidor y posteriormente terminar con la ejecucion del programa
    :param sock: Socket que enviara el mensaje y que terminara su sesion
    :return: void
    '''
    print("Terminando sesion")
    envia_mensaje(sock, pack('b', 32))  # Enviamos mensaje de termino de sesion
    sock.close()
    exit()

def lee_imagen(mensaje):
    '''
    Funcion que se encarga de decodificar una imagen
    recibida en un mensaje codificado y posteriormente desplegar
    la imagen
    :param mensaje: Mensaje a decodificar
    :return: void
    '''
    (i,), mensaje = unpack("I", mensaje[:4]), mensaje[4:]
    (i,), imagen = unpack("I", mensaje[:4]), mensaje[4:]
    image = Image.open(io.BytesIO(imagen))
    image.show()


if len(sys.argv) < 4:
    print("usage:", sys.argv[0], "<host> <puerto> <Id de usuario> <'pokedex'> \n El ultimo argumento es por si se desea consultar la pokedex actual del usuario")
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
sock.connect_ex(server_addr)
if len(sys.argv) ==  5:
    if sys.argv[4].lower()== "pokedex":
        #Queremos la pokedex
        envia_mensaje(sock, pack('bb', 43, id_usuario)) #Codigo que pide la pokedex
        mensaje = recibe_mensaje(sock)
        if mensaje[0] == 44:
            longitud_string = mensaje[1]
            pokedex = unpack('%ds'%longitud_string ,mensaje[2:])[0].decode("utf-8")
            print("Tu pokedex es la siguiente: ")
            print(pokedex)
        exit()

try:
    #Comenzamos con el mensaje inicial con el codigo 10 y el id
    msg = pack('bb',10,id_usuario)
    envia_mensaje(sock,msg)
    chunk = recibe_mensaje(sock)
    codigo = chunk[0]
    #En este punto el codigo puede ser 11 o 20
    if codigo == 41:
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
        termina_sesion(sock)

    puedo_intentar = True
    envia_mensaje(sock, pack('b', 30))  # Enviamos que si queremos intentar capturarlo
    mensaje = recibe_mensaje(sock,100000) #Aumentamos el tama;o del buffer porque puede haber una imagen
    while puedo_intentar:
        if mensaje[0] == 21:
            #No lo atrapamos por lo que imprimimos los intentos restantes
            intentos_restantes = mensaje[1]
            print("¿Intentar captura de nuevo? Quedan %d intentos."%intentos_restantes)
            text = input("[si/No]")
            if text != "si":
                termina_sesion(sock)
            envia_mensaje(sock, pack('b', 30)) #Enviamos que queremos intentar nuevamente
        elif mensaje[0] == 22:
            print("Felicidades, has atrapado a %s"%nombre_pokemon)
            lee_imagen(mensaje)
            puedo_intentar = False
            termina_sesion(sock)
        elif mensaje[0] == 23:
            print("Se han terminado tus intentos :/")
            termina_sesion(sock)
        elif mensaje[0] == 42:
            print("Ha ocurrido un error u.u intenta de nuevo")
            termina_sesion(sock)
        else:
             puedo_intentar = False
             print("Ha ocurrido un error, intenta de nuevo por favor")
             termina_sesion(sock)
        mensaje = recibe_mensaje(sock, 100000)


except KeyboardInterrupt:
    print("Interrupcion de teclado \n Abortando...\n Abortando..\n Abortado X.X")
finally:
    sock.close()