import socket
from threading import *
import sys
from struct import *
import base_datos as bd
import random


class client(Thread):
    '''
    Clase que modela clientes usando Threads
    '''
    def __init__(self, socket, address):
        '''
        Constructor de la clase cliente
        :param socket: socket creado para el cliente
        :param address: Direccion del cliente (ip,puerto)
        '''
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def envia_mensaje(self, mensaje, MSGLEN=1024):
        '''
        Funcion que envia un mensaje
        :param mensaje: Mensaje que vamos a enviar
        :param MSGLEN: Tama;o del buffer para enviar el mensaje
        :return: void
        :raise :RuntimeError en caso de que la conexion con el socket se pierda
        '''
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(mensaje[totalsent:])
            if sent == 0:
                raise RuntimeError("Se ha roto la conexion con el socket")
            break

    def recibe_mensaje(self):
        '''
        Funcion que se encarga de recibir un mensaje del
        socket del cliente
        :return: str
            mensaje recibido y codificado
        '''
        MSGLEN = 1024
        return self.sock.recv(min(MSGLEN - 0, 2048))


    def cierra_sesion(self, mensaje):
        '''
        Funcion que se encarga de cerrar la sesion si y solo si
        mensaje[0] es 32 (el codigo para cerrar sesion)
        Si se cierra la sesion el socket se cierra y se mata el hilo.
        :param mensaje: Mensaje codificado
        :return: void
        '''
        codigo = mensaje[0]
        if codigo == 32:
            self.sock.close()
            print("Cerrando sesion del cliente: ", self.addr)
            exit()

    def enviar_imagen(self, ruta):
        '''
        Funcion que se encarga de obtener la imagen de
        la ruta descrita en la base de datos para posteriormente
        estructurar el mensaje
        :param ruta: str
            String que nos dice donde esta la imagen solicitada
        :return: void
        '''
        imagen = open(ruta, 'rb')
        imagen_en_bytes = imagen.read()
        long = len(imagen_en_bytes)
        # Enviamos el mensaje con un byte que representa el codigo 22
        # 4 bytes que representan el tama;o de la imagen
        # y el codigo de la imagen
        mensaje = pack('bI%ds' % long, 22, long, imagen_en_bytes)
        self.envia_mensaje(mensaje, long)

    def run(self):
        '''
        Esta funcion se ejecuta por cada cliente, se encarga de manejar toda la interaccion con
        el servidor
        :return: void
        '''
        mensaje = self.recibe_mensaje()
        mensaje = unpack('bb', mensaje)
        codigo = mensaje[0]
        id_usr = mensaje[1]
        if not bd.valida_usuario(id_usr):
            # Usuario invalido
            mensaje = pack("b", 41)  # Mensaje de error
            self.envia_mensaje(mensaje)  # Enviamos el mensaje de error
            self.sock.close()
        if codigo == 43:
            #Pedimos pokedex
            pokedex = bd.obten_pokedex(id_usr)
            #Enviamos mensaje con pokedex
            self.envia_mensaje(pack("bb%ds" % len(pokedex), 44, len(pokedex), bytes(pokedex, 'utf-8')))
            self.cierra_sesion([32])
        if codigo != 10:
            mensaje = pack("b", 42)  # Mensaje de error
            self.envia_mensaje(mensaje)  # Enviamos el mensaje de error
            self.cierra_sesion([32])
        id_pok, (nombre, ruta) = bd.obten_pokemon_random()
        # Creamos el struct para enviar el codigo y el mensaje con el nombre de pokemon
        mensaje_pok = nombre
        # Para este mensaje tenemos un byte para el codigo y un byte para la longitud del string
        # utilizando el tipo signed char, de esta manera mensaje_pok[0] es el codigo y
        # mensaje_pok[1] es la longitud del mensaje enviado
        mensaje_pok = pack("bb%ds" % len(mensaje_pok), 20, len(mensaje_pok), bytes(mensaje_pok, 'utf-8'))
        self.envia_mensaje(mensaje_pok)
        # En este punto necesitamos la respuesta del cliente
        recibido = self.recibe_mensaje()
        self.cierra_sesion(recibido)  # Revisamos si tenemos que cerrar la sesion
        # En caso afirmativo esto ya no se va a ejecutar
        if not recibido[0] == 30:
            # Si no quiere capturarlo cerramos la sesion (aplica si recibimos un mensaje raro)
            self.cierra_sesion([32])
        intentos = 10  # Damos 10 intentos por default
        capturado = False
        while recibido[0] == 30 and intentos > 0 and (not capturado):
            intentos -= 1
            capturado = random.choice([True, False])
            if capturado:
                self.enviar_imagen(ruta)
                # Agregamos a la pokedex del usuario
                bd.agrega_pokemon_a_pokedex(id_pok, id_usr)
                self.cierra_sesion([32])
            elif intentos == 0:
                self.envia_mensaje(pack('b', 23))
                self.cierra_sesion([32])
            else:
                # Enviamos el codigo 21 y los intentos restantes
                self.envia_mensaje(pack('bb', 21, intentos))
            recibido = self.recibe_mensaje()
        # Esta parte del codigo no deberia ejecutarse pero puede ocurrir un error raro
        mensaje = pack("b", 42)  # Mensaje de error
        self.envia_mensaje(mensaje)
        self.cierra_sesion([32])


###Main
if len(sys.argv) != 3:
    print("Uso:", sys.argv[0], "<host> <puerto>")
    sys.exit(1)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host, port = sys.argv[1], int(sys.argv[2])  # Siempre va a ser el 9999

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
