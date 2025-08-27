import socket
import threading as th

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

def manejar_cliente(conn,addr):
    print("Conectando con puerto 6000...")
    while True:
        with conn:
            while True:
                print(f"Conexión de cliente {addr}")
                data = conn.recv(1024).decode()
                if not data:
                    continue
                if data == "salir":
                    break
                if "," in data:
                    nombre, nota = data.split(",")
                    try:
                        nota = int(nota)
                    except Exception as e:
                        print("Error: ",e)
                    if not isinstance(nota, int) or nota < 1 or nota > 10:
                        mensaje = "ERROR: Debe enviar una nota válida"
                    else:
                        mensaje = "Los datos recibidos son válidos"
                        mensaje += f"\n{registrar_servidor_db(data)}"
                else:
                    mensaje = consultar_servidor_db(data)

                conn.sendall(str(mensaje).encode())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("localhost", 6000))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        th.Thread(target=manejar_cliente,args=(conn,addr)).start()
        