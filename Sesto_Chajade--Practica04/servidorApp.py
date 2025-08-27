import socket
import threading
import json


def acceder_servidor_db(datos):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 6001))
        s.sendall(datos.encode())
        return s.recv(3000).decode()

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
                respuesta = acceder_servidor_db(json.dumps(data))
            conn.sendall(respuesta.encode())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("localhost", 6000))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        threading.Thread(target=gestionar_clientes, args=(conn, addr)).start()