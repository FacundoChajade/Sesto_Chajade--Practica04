import socket
import json
import os
from datetime import datetime
from conexion import Conexion
registros = {}
conexion = Conexion()
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 6001))
        s.listen(5)

        while True:
            conn, addr = s.accept()
            print(f"Se estableció la conexión con {addr}")
            data = conn.recv(3000).decode()
            data = json.loads(data)
            if data["accion"] == "registrar_satelite":
                conexion.conectar()
                cursor = conexion.conn.cursor()
                cursor.execute("INSERT INTO Satelite(nombre, tipo, fecha_lanzamiento, orbita, estado) VALUES(%s,%s,%s,%s,%s)",(data["nombre"],data["tipo"],datetime.strptime(data["fecha_lanzamiento"], "%d-%m-%y"),data["orbita"],data["estado"]))
                
                conexion.conn.commit()
                nuevo_id = cursor.lastrowid
                cursor2 = conexion.conn.cursor()
                for i in data["sensores"]:
                    cursor2.execute("INSERT INTO Sensor(nombre,tipo_unidad, satelite_id) VALUES (%s,%s,%s)",(i["nombre"],i["tipo_unidad"],nuevo_id))
                conexion.conn.commit()
                conexion.desconectar()
                conn.sendall(json.dumps({"respuesta":"Se registró correctamente el satélite"}).encode())
            elif data["accion"] == "registrar_mision":
                conexion.conectar()
                cursor = conexion.conn.cursor()
                cursor.execute("INSERT INTO Mision(nombre, satelite_id, objetivo, zona, duracion, estado) VALUES(%s,%s,%s,%s,%s,%s)",(data["nombre"],data["satelite"],data["objetivo"],data["zona"],data["duracion"],data["estado"]))
                conexion.conn.commit()
                conexion.desconectar()
                conn.sendall(json.dumps({"respuesta":"Se registró correctamente la mision"}).encode())
            elif data["accion"] == "recibir_satelites":
                conexion.conectar()
                cursor = conexion.conn.cursor()
                cursor.execute("SELECT * FROM Satelite")
                filas = cursor.fetchall()
                satelites=[]
                for fila in filas:
                    cursor2 = conexion.conn.cursor()
                    cursor2.execute("SELECT nombre FROM Sensor WHERE satelite_id = %s",(fila[0],))
                    fila_sensores = cursor2.fetchall()
                    sensores = [s[0] for s in fila_sensores]
                    satelites.append((fila[0], fila[1],fila[2],str(fila[3]),fila[4],fila[5],sensores))
                conexion.desconectar()
                conn.sendall(json.dumps(satelites).encode())
            elif data["accion"] == "recibir_misiones":
                conexion.conectar()
                cursor = conexion.conn.cursor()
                cursor.execute("SELECT * FROM Mision")
                filas = cursor.fetchall()
                misiones=[]
                for fila in filas:
                    misiones.append(fila)
                conexion.desconectar()
                conn.sendall(json.dumps(misiones).encode())
            elif data["accion"] == "modificar_mision":
                conexion.conectar()
                cursor = conexion.conn.cursor()
                cursor.execute("UPDATE Mision SET estado = %s WHERE id = %s",(data["estado"], data["id"]))
                conexion.conn.commit()
                conn.sendall(json.dumps({"respuesta":"Se actualizó correctamente la misión."}).encode())
                conexion.desconectar()
            elif data["accion"] == "recibir_datos":
                conexion.conectar()
                cursor = conexion.conn.cursor()
                cursor.execute("SELECT * FROM datos_mision")
                filas = cursor.fetchall()
                datos=[]
                for fila in filas:
                    datos.append(fila)
                conexion.desconectar()
                conn.sendall(json.dumps(datos).encode())
            elif data["accion"] == "registrar_datos":
                conexion.conectar()
                cursor = conexion.conn.cursor()
                
                cursor.execute("INSERT INTO datos_mision(id_mision, tipo, valor, descripcion) VALUES(%s,%s,%s,%s)",(data["id_mision"],data["tipo"],data["valor"],data["descripcion"]))
                conexion.conn.commit()
                conexion.desconectar()
                conn.sendall(json.dumps({"respuesta":"Se registraron los datos correctamente."}).encode())
except Exception as e:
    print("Error: ",e)
os.system("pause")