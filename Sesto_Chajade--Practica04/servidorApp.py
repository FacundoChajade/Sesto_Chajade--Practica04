import socket
import threading
import json
from datetime import datetime


def acceder_servidor_db(datos):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 6001))
        s.sendall(datos.encode())
        return s.recv(3000).decode()

def validar_satelite(data):
    try:
        if not data.get("nombre") or not isinstance(data.get("nombre"), str):
            raise ValueError("Nombre inválido")
        tipos = ["Monolitico","Modular","Nanosatelital"]
        if data.get("tipo") not in tipos:
            raise ValueError("Tipo inválido")
        try:
            datetime.strptime(data.get("fecha_lanzamiento"), "%d-%m-%y")
        except Exception:
            raise ValueError("Fecha inválida. Formato esperado DD-MM-YY")
        try:
            orbita = int(data.get("orbita"))
        except Exception:
            raise ValueError("Órbita inválida")
        if orbita < 160:
            raise ValueError("Órbita fuera de rango")
        estados = ["Activo","Inactivo","En mantenimiento"]
        if data.get("estado") not in estados:
            raise ValueError("Estado inválido")
        sensores = data.get("sensores", [])
        if not isinstance(sensores, list):
            raise ValueError("Sensores inválidos")
        for s in sensores:
            if not s.get("nombre") or not s.get("tipo_unidad"):
                raise ValueError("Sensor inválido")
        return None
    except Exception as e:
        return str(e)

def validar_mision(data):
    try:
        if not data.get("nombre") or not isinstance(data.get("nombre"), str):
            raise ValueError("Nombre inválido")
        try:
            satelite_id = int(data.get("satelite"))
        except Exception:
            raise ValueError("Satelite inválido")
        if not data.get("objetivo") or not isinstance(data.get("objetivo"), str):
            raise ValueError("Objetivo inválido")
        if not data.get("zona") or not isinstance(data.get("zona"), str):
            raise ValueError("Zona inválida")
        try:
            duracion = int(data.get("duracion"))
        except Exception:
            raise ValueError("Duración inválida")
        if duracion < 1:
            raise ValueError("Duración fuera de rango")
        if not data.get("estado") or not isinstance(data.get("estado"), str):
            raise ValueError("Estado inválido")
        consulta = {"accion":"recibir_satelites"}
        r = acceder_servidor_db(json.dumps(consulta))
        lista = json.loads(r)
        ids = [fila[0] for fila in lista]
        if satelite_id not in ids:
            raise ValueError("Satelite inexistente")
        return None
    except Exception as e:
        return str(e)

def validar_modificar_mision(data):
    try:
        try:
            mid = int(data.get("id"))
        except Exception:
            raise ValueError("ID inválido")
        if not data.get("estado") or not isinstance(data.get("estado"), str):
            raise ValueError("Estado inválido")
        consulta = {"accion":"recibir_misiones"}
        r = acceder_servidor_db(json.dumps(consulta))
        lista = json.loads(r)
        ids = [fila[0] for fila in lista]
        if mid not in ids:
            raise ValueError("Misión inexistente")
        return None
    except Exception as e:
        return str(e)

def validar_registro_datos(data):
    try:
        try:
            mid = int(data.get("id_mision"))
        except Exception:
            raise ValueError("ID de misión inválido")
        consulta = {"accion":"recibir_misiones"}
        r = acceder_servidor_db(json.dumps(consulta))
        lista = json.loads(r)
        ids = [fila[0] for fila in lista]
        if mid not in ids:
            raise ValueError("Misión inexistente")
        tipo = data.get("tipo")
        if not isinstance(tipo, str) or len(tipo) == 0:
            raise ValueError("Tipo inválido")
        if tipo != "imagen":
            try:
                int(data.get("valor"))
            except Exception:
                raise ValueError("Valor inválido")
        if data.get("descripcion") is None or not isinstance(data.get("descripcion"), str):
            raise ValueError("Descripción inválida")
        return None
    except Exception as e:
        return str(e)

def gestionar_clientes(conn, addr):
    print("Conectando con puerto 6000...")
    #while True:
    with conn:
        while True:
            print(f"Conexión de cliente {addr}")
            data = conn.recv(3000).decode()
            data = json.loads(data)
            if data["accion"] == "salir":
                break
            else:
                if data["accion"] == "registrar_satelite":
                    error = validar_satelite(data)
                    if error:
                        respuesta = json.dumps({"respuesta": f"Error: {error}"})
                    else:
                        respuesta = acceder_servidor_db(json.dumps(data))
                elif data["accion"] == "registrar_mision":
                    error = validar_mision(data)
                    if error:
                        respuesta = json.dumps({"respuesta": f"Error: {error}"})
                    else:
                        respuesta = acceder_servidor_db(json.dumps(data))
                elif data["accion"] == "modificar_mision":
                    error = validar_modificar_mision(data)
                    if error:
                        respuesta = json.dumps({"respuesta": f"Error: {error}"})
                    else:
                        respuesta = acceder_servidor_db(json.dumps(data))
                elif data["accion"] == "registrar_datos":
                    error = validar_registro_datos(data)
                    if error:
                        respuesta = json.dumps({"respuesta": f"Error: {error}"})
                    else:
                        respuesta = acceder_servidor_db(json.dumps(data))
                elif data["accion"] == "recibir_satelites":
                    r = acceder_servidor_db(json.dumps(data))
                    try:
                        lista = json.loads(r)
                        if isinstance(lista, list) and len(lista) == 0:
                            respuesta = json.dumps({"respuesta":"No existen satélites registrados."})
                        else:
                            respuesta = r
                    except Exception:
                        respuesta = r
                elif data["accion"] == "recibir_misiones":
                    r = acceder_servidor_db(json.dumps(data))
                    try:
                        lista = json.loads(r)
                        if isinstance(lista, list) and len(lista) == 0:
                            respuesta = json.dumps({"respuesta":"No existen misiones registradas."})
                        else:
                            respuesta = r
                    except Exception:
                        respuesta = r
                elif data["accion"] == "recibir_datos":
                    r = acceder_servidor_db(json.dumps(data))
                    try:
                        lista = json.loads(r)
                        if isinstance(lista, list) and len(lista) == 0:
                            respuesta = json.dumps({"respuesta":"No existen datos registrados."})
                        else:
                            respuesta = r
                    except Exception:
                        respuesta = r
                else:
                    respuesta = acceder_servidor_db(json.dumps(data))
            conn.sendall(respuesta.encode())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("localhost", 6000))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        threading.Thread(target=gestionar_clientes, args=(conn, addr)).start()