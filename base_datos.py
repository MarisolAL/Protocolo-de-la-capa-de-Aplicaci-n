import sqlite3

conn = sqlite3.connect('pokemon.db')
c = conn.cursor()


# Funcion que dado un id de usuario verifica si esta registrado en la base
def valida_usuario(id):
    consulta = "Select * from usuarios where id = %d" % id
    c.execute(consulta)
    if c.fetchone() == None:
        print("Id invalido, intente con otro porfavor")
        return -1
    else:
        return 1


# Funcion que dado el id del pokemon obtiene la ruta de la imagen y su nombre
def get_nombre_y_ruta(id):
    consulta = "Select nombre,imagen from pokemon where id = %d" % id
    print(consulta)
    c.execute(consulta)
    if c.fetchone() == None:
        print("Oh, ha ocurrido un error D:")
        return -1
    else:
        for row in c.execute("Select nombre,imagen from pokemon where id = %d" % id):
            nombre = row[0]
            ruta = row[1]
        return nombre, ruta


# Funcion que dado un id de pokemon y el usuario que lo capturo
# guarda el registro en la base
def agrega_pokemon_a_pokedex(pokemon, usuario):
    c.execute("INSERT INTO tiene_pok VALUES (" + str(usuario) + "," + str(pokemon) + ")")


conn.commit()  # Guardar los cambios
conn.close()  # Cerramos la conexion
