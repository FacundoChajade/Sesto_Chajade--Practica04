import socket

registros = {}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("localhost", 6001))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print(f"Se estableció la conexión con {addr}")
        data = conn.recv(1024).decode()

        if "," in data:
            nombre, nota = data.split(",")
            if nombre in registros:
                mensaje = "El alumno ya se encuentra registrado"
            else:
                registros[nombre] = nota
                mensaje = f"Se registró a {nombre} con la nota {nota}"
        else:
            if data not in registros:
                mensaje = f"El alumno no se encuentra en la base de datos"
            else:
                mensaje = f"La nota de {data} es: {registros[data]}"
        conn.sendall(mensaje.encode())