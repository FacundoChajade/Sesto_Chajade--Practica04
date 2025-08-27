import socket
import json
from conexion import Conexion
registros = {}
conexion = Conexion()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("localhost", 6001))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print(f"Se estableció la conexión con {addr}")
        data = s.recv(3000).decode()
        data = json.loads(data)
        if data["accion"] == "registrar_satelite":
            conexion.conectar()
            cursor = conexion.conn.cursor()
            cursor.execute("INSERT INTO Satelite(nombre, tipo, fecha_lanzamiento, orbita, estado) VALUES(%s,%s,%s,%s,%s)",(data["nombre"],data["tipo"],data["fecha_lanzamiento"],data["orbita"],data["estado"]))
            conexion.conn.commit()
            conexion.desconectar()
            conn.sendall("Se registró correctamente el satélite")
        elif data["accion"] == "registrar_mision":
            conexion.conectar()
            cursor = conexion.conn.cursor()
            cursor.execute("INSERT INTO Mision(nombre, satelite_id, objetivo, zona, duracion, estado) VALUES(%s,%s,%s,%s,%s,%s)",(data["nombre"],data["satelite_id"],data["objetivo"],data["zona"],data["duracion"],data["estado"]))
            conexion.conn.commit()
            conexion.desconectar()
            conn.sendall("Se registró correctamente el satélite")
        elif data["accion"] == "recibir_satelites":
            conexion.conectar()
            cursor = conexion.conn.cursor()
            cursor.execute("SELECT * FROM Satelite")
            filas = cursor.fetchall()
            conexion.desconectar()
            conn.sendall(json.dumps(filas).encode())