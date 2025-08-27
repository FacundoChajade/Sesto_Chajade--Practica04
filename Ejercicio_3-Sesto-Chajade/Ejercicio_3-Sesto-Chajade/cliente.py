import socket
import os


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.connect(("localhost", 6000))
print("Se abrió la conexión con el servidor")

while True:
    while True:
        try:
            opcion = int(input("¿Que desea realizar? 1-Registrar datos 2-Consultar nota 3-Salir "))
            if opcion < 1 or opcion > 3:
                raise ValueError("Ingrese un valor válido")
            break
        except ValueError as ve:
            print("Error: ",ve)
    try:
        if opcion == 1:
            nombre = str(input("Ingrese el nombre del alumno: "))
            nota = input("Ingrese la nota del alumno: ")
            servidor.sendall(f"{nombre},{nota}".encode())
            respuesta = servidor.recv(1024).decode()
            print(respuesta)
        elif opcion == 2:
            nombre = str(input("Ingrese el nombre del alumno: "))
            servidor.sendall(nombre.encode())
            respuesta = servidor.recv(1024).decode()
            print(respuesta)
        elif opcion == 3:
            servidor.sendall("salir".encode())
            break
    except Exception as e:
        print("error: ",e)

servidor.close()

print("Se cerró la conexión con el servidor")
os.system("pause")    