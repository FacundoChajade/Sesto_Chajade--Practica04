import socket
import threading
def consultar_servidor_db(nombre):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 6001))
        s.sendall(nombre.encode())
        return s.recv(1024).decode()

def registrar_servidor_db(datos):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 6001))
        s.sendall(datos.encode())
        return s.recv(1024).decode()

def gestionar_clientes(conn, addr):
    pass

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind("localhost", 6000)
    s.listen(5)

    while True:
        conn, addr = s.accept()
        threading.Thread(target=gestionar_clientes, args=(conn, addr)).start()