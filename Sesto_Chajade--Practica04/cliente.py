import socket
import os
import json
from mision import Mision
from satelite import Satelite
from sensor import Sensor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.connect(("localhost", 6000))

def recibir_datos(consulta):
    enviar = {
        "accion": f"{consulta}"
    }
    servidor.sendall(json.dumps(enviar).encode)
    respuesta = servidor.recv(3000).decode()
    return json.loads(respuesta)

while True:
    while True:
        try:
            opcion = int(input("¿Que desea realizar?\n1-Registrar satélite\n2-Registrar Mision\n3-Actualizar Mision\n4-Informacion sobre Misiones\n5-Informacion sobre Satelites\n6-Registrar Datos Recolectados\n7-Consultar Datos Recolectados\n8-Salir\n"))
            if opcion < 1 or opcion > 8:
                raise ValueError("Ingrese un valor válido")
            break
        except ValueError as ve:
            print("Error: ",ve)
    try:
        if opcion == 1:
            nombre = str(input("Ingrese el nombre del satelite: "))
            while True:
                try:
                    tipo = int(input("Ingrese el tipo de satelite: 1-Monolitico 2-Modular 3-Nanosatelital"))
                    if opcion < 1 or opcion > 3:
                        raise ValueError("Ingrese un valor válido")
                    break
                except ValueError as ve:
                    print("Error: ",ve)
            
            
            fecha_lanzamiento = str("Ingrese la fecha de lanzazmiento (DD-MM-YY): ")
            while True:
                try:
                    orbita = int(input("Ingrese la altura a la que orbita (KM): "))
                    if orbita < 160:
                        raise ValueError("Ingrese un valor válido")
                    break
                except ValueError as ve:
                    print("Error: ",ve)
            while True:
                try:
                    estado_opcion = int(input("Ingrese el estado de la mision: 1-Activo 2-Inactivo 3-En mantenimiento"))
                    if estado_opcion < 1 or estado_opcion >3:
                        raise ValueError("Ingrese un valor válido")
                    if estado_opcion == 1:
                        estado = "Activo"
                    elif estado_opcion == 2:
                        estado = "Inactivo"
                    elif estado_opcion == 3:
                        estado = "En mantenimiento"
                    break
                except ValueError as ve:
                    print("Error: ",ve)
                
            satelite = Satelite(nombre,tipo,fecha_lanzamiento, orbita,estado)
            cantidad = 0
            
            sensor_radiacion = int(input("Desea agregar un piranometro? 1-Si 2-No "))
            if sensor_radiacion == 1:
                satelite.agregar_sensor(Sensor("piranometro", "W/m²"))

            sensor_temperatura = int(input("Desea agregar un termometro? 1-Si 2-No "))
            if sensor_temperatura == 1:
                satelite.agregar_sensor(Sensor("termometro", "°C"))

            sensor_presion = int(input("Desea agregar un barometro? 1-Si 2-No "))
            if sensor_presion == 1:
                satelite.agregar_sensor(Sensor("barometro", "hPa"))

            enviar = satelite.devolver_json("registrar_satelite")
            servidor.sendall(json.dumps(enviar).encode())

        elif opcion == 2:
            nombre = str(input("Ingrese el nombre de la mision: "))
            lista_satelites = recibir_datos("recibir_satelites")
            cantidad = 0
            for sat in lista_satelites:
                cantidad +=1
                print(f"{cantidad}-{sat}\n")
            while True:
                try:
                    satelite_elegido = int(input("Seleccione el satelite que quiera asignar: "))
                    if satelite_elegido > (len(lista_satelites)+1):
                        raise ValueError("Ingrese un valor valido")
                    break
                except Exception as e:
                    print("Error: ",e)
            satelite = lista_satelites[satelite_elegido-1]
            objetivo = str(input("Ingrese el objetivo de la mision: "))
            zona = str(input("Ingrese la zona de observacion: "))
            while True:
                duracion = input("Ingrese la duración de la mision (dias)")
                try:
                    duracion = int(duracion)
                except Exception as e:
                    print("Error: ",e)
                if not isinstance(duracion, int):
                    raise ValueError("Ingrese un valor válido")
                break
            estado = str(input("En qué estado se encuentra: "))
            mision = Mision(satelite, objetivo, zona, duracion, estado)
            enviar = mision.devolver_json("registrar_mision")
            servidor.sendall(json.dumps(enviar).encode())
        
        elif opcion == 3:
            lista_misiones = recibir_datos("recibir_misiones")
            cantidad = 0
            for mis in lista_misiones:
                cantidad +=1
                print(f"{cantidad}-{mis}\n")
            while True:
                try:
                    mision_elegida = int(input("Seleccione el satelite que quiera asignar: "))
                    if mision_elegida > (len(lista_misiones)+1):
                        raise ValueError("Ingrese un valor valido")
                    break
                except Exception as e:
                    print("Error: ",e)
            mision = lista_misiones[mision_elegida-1]
            estado_nuevo = str(input("Ingrese el nuevo estado de la mision: "))
            mision.modificar_estado(estado_nuevo)
            enviar = mision.devolver_json("modificar_mision")
            servidor.sendall(json.dumps(enviar).encode())
        
        elif opcion == 4:
            pass
        elif opcion == 5:
            pass
        elif opcion == 6:
            pass
        elif opcion == 7:
            pass
        elif opcion == 8:
            servidor.sendall("salir".encode())
            break
        
    except Exception as e:
        print("error: ",e)

servidor.close()

print("Se cerró la conexión con el servidor")
os.system("pause")    