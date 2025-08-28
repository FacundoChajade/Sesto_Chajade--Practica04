import socket
import os
import json
from datetime import datetime
from mision import Mision
from satelite import Satelite
from sensor import Sensor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.connect(("localhost", 6000))

def recibir_datos(consulta):
    enviar = {
        "accion": f"{consulta}"
    }
    servidor.sendall(json.dumps(enviar).encode())
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
                    tipo_opcion = int(input("Ingrese el tipo de satelite: 1-Monolitico 2-Modular 3-Nanosatelital"))
                    if tipo_opcion < 1 or tipo_opcion > 3:
                        raise ValueError("Ingrese un valor válido")
                    break
                except ValueError as ve:
                    print("Error: ",ve)
            if tipo_opcion == 1:
                tipo = "Monolitico"
            elif tipo_opcion == 2:
                tipo = "Modular"
            elif tipo_opcion == 3:
                tipo = "Nanosatelital"
            
            while True:
                fecha_lanzamiento = input("Ingrese la fecha de lanzazmiento (DD-MM-YY): ")
                try:
                    fecha_obj = datetime.strptime(fecha_lanzamiento, "%d-%m-%y")
                    fecha = fecha_obj.strftime("%d-%m-%y")
                    break
                except Exception as e:
                    print("Error: ",e)

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
                    break
                except ValueError as ve:
                    print("Error: ",ve)
            
            if estado_opcion == 1:
                estado = "Activo"
            elif estado_opcion == 2:
                estado = "Inactivo"
            elif estado_opcion == 3:
                estado = "En mantenimiento"
            satelite = Satelite(nombre,tipo,fecha_lanzamiento, orbita,estado)
            cantidad = 0
            
            sensor_radiacion = int(input("Desea agregar un piranometro? 1-Si 2-No "))
            if sensor_radiacion == 1:
                satelite.agregar_sensor(Sensor("Piranometro", "W/m²"))

            sensor_temperatura = int(input("Desea agregar un termometro? 1-Si 2-No "))
            if sensor_temperatura == 1:
                satelite.agregar_sensor(Sensor("Termometro", "°C"))

            sensor_presion = int(input("Desea agregar un barometro? 1-Si 2-No "))
            if sensor_presion == 1:
                satelite.agregar_sensor(Sensor("Barometro", "hPa"))

            enviar = satelite.devolver_json("registrar_satelite")
            servidor.sendall(json.dumps(enviar).encode())
            respuesta = servidor.recv(3000).decode()
            respuesta = json.loads(respuesta)
            print(respuesta["respuesta"])
        

        elif opcion == 2:
            nombre = str(input("Ingrese el nombre de la mision: "))
            lista_satelites = recibir_datos("recibir_satelites")
            cantidad = 0
            for sat in lista_satelites:
                cantidad +=1
                print(f"{cantidad}-{sat}\n")
            if len(lista_satelites) == 0:
                print("Necesita tener un satelite creado")
                continue
            while True:
                try:
                    satelite = int(input("Seleccione el satelite que quiera asignar: "))
                    if satelite > len(lista_satelites):
                        raise ValueError("Ingrese un valor valido")
                    break
                except Exception as e:
                    print("Error: ",e)
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
            mision = Mision(nombre, satelite, objetivo, zona, duracion, estado)
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
                    if mision_elegida > len(lista_misiones):
                        raise ValueError("Ingrese un valor valido")
                    break
                except Exception as e:
                    print("Error: ",e)
    
            estado_nuevo = str(input("Ingrese el nuevo estado de la mision: "))
            enviar = {
                "accion": "modificar_mision",
                "id": mision_elegida,
                "estado": estado_nuevo
            }
            servidor.sendall(json.dumps(enviar).encode())
            respuesta = servidor.recv(3000).decode()
            respuesta = json.loads(respuesta)
            print(respuesta["respuesta"])
        
        elif opcion == 4:
            #filtrar por nombre de satelite, por nombre de mision
            misiones = recibir_datos("recibir_misiones")
            
            while True:
                try:
                    nombre = None
                    nombre_opcion = int(input("¿Aplicar filtro por nombre de mision?: 1-Si 2-No"))
                    if nombre_opcion != 1 and nombre_opcion != 2:
                        raise ValueError("El valor es inválido")
                    break
                except ValueError as ve:
                    print("Error: ",ve)
            if nombre_opcion == 1:
                    nombre = str(input("¿Que nombre de mision desea filtrar?: "))
            while True:
                try:
                    id = None
                    id_opcion = int(input("¿Aplicar filtro por id de satelite?: 1-Si 2-No"))
                    if id_opcion != 1 and id_opcion != 2:
                        raise ValueError("El valor es inválido")
                    break
                except ValueError as ve:
                    print("Error: ",ve)
            if id_opcion == 1:
                while True:
                    try:
                        id = int(input("¿Que id de satelite desea filtrar?: "))
                        break
                    except Exception as e:
                        print("Error: ",e)
            misiones_filtradas = []
            for mision in misiones:
                print(mision[1])
                if (str(mision[1]) == nombre or nombre == None) and (mision[2] == id or id == None):
                    misiones_filtradas.append(mision)
            if len(misiones_filtradas) == 0:
                print("No hay misiones con esos criterios")
            else:
                print("Misiones encontradas:")
                for mision in misiones_filtradas:
                    print(mision)
            



        elif opcion == 5:
            #filtrar por tipo de satelite, tipo de sensor y por estado

            satelites = recibir_datos("recibir_satelites")
            
            while True:
                try:
                    tipo = None
                    tipo_opcion = int(input("¿Aplicar filtro por tipo de satelite?: 1-Si 2-No"))
                    if tipo_opcion != 1 and tipo_opcion != 2:
                        raise ValueError("El valor es inválido")
                    break
                except ValueError as ve:
                    print("Error: ",ve)
            if tipo_opcion == 1:
                while True:
                    try:
                        tipo_elegido = int(input("¿Qué tipo de satelite desea filtrar? 1-Monolitico 2-Modular 3-Nanosatelital: "))
                        if tipo_elegido < 1 or tipo_elegido > 3:
                            raise ValueError("Ingrese un valor válido")
                        break
                    except ValueError as ve:
                        print("Error: ",ve)
                if tipo_elegido == 1:
                    tipo = "Monolitico"
                elif tipo_elegido == 2:
                    tipo = "Modular"
                elif tipo_elegido == 3:
                    tipo = "Nanosatelital"    
            while True:
                try:
                    sensor = None
                    sensor_opcion = int(input("¿Aplicar filtro por tipo de sensor?: 1-Si 2-No"))
                    if sensor_opcion != 1 and sensor_opcion != 2:
                        raise ValueError("El valor es inválido")
                    break
                except ValueError as ve:
                    print("Error: ",ve)

            if sensor_opcion == 1:
                sensor_elegir = int(input("¿Qué tipo de sensor desea filtrar? 1-Piranometro 2-Termometro 3-Barometro): "))
                if sensor_elegir == 1:
                    sensor = "Piranometro"
                elif sensor_elegir == 2:
                    sensor = "Termometro"
                elif sensor_elegir == 3:
                    sensor = "Barometro"
            while True:
                try:
                    estado = None
                    estado_opcion = int(input("¿Aplicar filtro por estado?: 1-Si 2-No"))
                    if estado_opcion != 1 and estado_opcion != 2:
                        raise ValueError("El valor es inválido")
                    break
                except ValueError as ve:
                    print("Error: ",ve)
            if estado_opcion == 1:
                while True:
                    try:
                        estado_opcion2 = int(input("Ingrese el estado: 1-Activo 2-Inactivo 3-En mantenimiento"))
                        if estado_opcion2 < 1 or estado_opcion2 > 3:
                            raise ValueError("Ingrese un valor válido")
                        if estado_opcion2 == 1:
                            estado = "Activo"
                        elif estado_opcion2 == 2:
                            estado = "Inactivo"
                        elif estado_opcion2 == 3:
                            estado = "En mantenimiento"
                        break
                    except ValueError as ve:
                        print("Error: ",ve)

            satelites_filtrados = []
            for satelite in satelites:
                if (satelite[2] == tipo or tipo == None) and (sensor in satelite[6] or sensor == None) and (satelite[5] == estado or estado == None):
                    satelites_filtrados.append(satelite)
            if len(satelites_filtrados) == 0:
                print("No hay satelites con esos criterios")
            else:
                print("Satelites encontrados:")
                for sat in satelites_filtrados:
                    print(sat)
        elif opcion == 6:
            pass
        elif opcion == 7:
            lista_datos = recibir_datos("recibir_datos")
            cantidad = 0
            for datos in lista_datos:
                cantidad +=1
                print(f"{cantidad}-{datos}\n")
        elif opcion == 8:
            mensaje = {
                "accion":"salir"
            }
            servidor.sendall(json.dumps(mensaje).encode())
            break
        
    except Exception as e:
        print("error: ",e)

servidor.close()

print("Se cerró la conexión con el servidor")
os.system("pause")    