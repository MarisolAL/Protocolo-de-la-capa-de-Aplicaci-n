import sqlite3
import random


# Funcion que dado un id de usuario verifica si esta registrado en la base
def valida_usuario(id):
    conn = sqlite3.connect('pokemon.db')
    c = conn.cursor()
    consulta = "Select * from usuarios where id = %d" % id
    c.execute(consulta)
    if c.fetchone() == None:
        print("Id invalido, intente con otro porfavor")
        conn.close()  # Cerramos la conexion
        return False
    else:
        conn.close()  # Cerramos la conexion
        return True


# Funcion que dado el id del pokemon obtiene la ruta de la imagen y su nombre
def get_nombre_y_ruta(id):
    conn = sqlite3.connect('pokemon.db')
    c = conn.cursor()
    consulta = "Select nombre,imagen from pokemon where id = %d" % id
    c.execute(consulta)
    if c.fetchone() == None:
        print("Oh, ha ocurrido un error D:")
        conn.close()  # Cerramos la conexion
        return -1
    else:
        for row in c.execute("Select nombre,imagen from pokemon where id = %d" % id):
            nombre = row[0]
            ruta = row[1]
        conn.close()  # Cerramos la conexion
        return nombre, ruta


# Funcion que dado un id de pokemon y el usuario que lo capturo
# guarda el registro en la base
def agrega_pokemon_a_pokedex(pokemon, usuario):
    conn = sqlite3.connect('pokemon.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO tiene_pok VALUES (" + str(usuario) + "," + str(pokemon) + ")")
    except sqlite3.Error as e:
        #Si el usuario ya tenia ese pokemon hacemos como que lo agregamos
        print("Este usuario ya tenia ese pokemon")
    finally:
        conn.commit()  # Guardar los cambios
        conn.close()  # Cerramos la conexion


# Funcion que obtiene el nombre y ruta de un pokemon aleatorio
def obten_pokemon_random():
    conn = sqlite3.connect('pokemon.db')
    c = conn.cursor()
    consulta = "Select count(id) from pokemon"
    c.execute(consulta)
    if c.fetchone() == None:
        print("Oh, ha ocurrido un error D:")
        conn.close()  # Cerramos la conexion
        return None
    for row in c.execute("Select count(id) from pokemon"):
        total = int(row[0])
    conn.close()  # Cerramos la conexion
    id = random.randint(0, total)
    return id, get_nombre_y_ruta(id)

def obten_pokedex(id_usuario):
    conn = sqlite3.connect('pokemon.db')
    c = conn.cursor()
    lista_pok = "\n"
    for row in c.execute("select nombre from pokemon inner join tiene_pok on id_pokemon = id where id_usuario = " + str(id_usuario)):
        lista_pok += str(row[0]) + "\n"
    conn.close()  # Cerramos la conexion
    return lista_pok