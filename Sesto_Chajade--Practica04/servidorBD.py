import socket

registros = {}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("localhost", 6001))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print(f"Se estableció la conexión con {addr}")


       