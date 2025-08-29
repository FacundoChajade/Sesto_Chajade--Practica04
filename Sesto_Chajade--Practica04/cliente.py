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
            
            fecha_lanzamiento = input("Ingrese la fecha de lanzazmiento (DD-MM-YY): ")

            orbita = input("Ingrese la altura a la que orbita (min 160 KM): ")
            while True:
                try:
                    estado_opcion = int(input("Ingrese el estado: 1-Activo 2-Inactivo 3-En mantenimiento"))
                    if estado_opcion < 1 or estado_opcion > 3:
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
            
            while True:
                try:
                    sensor_radiacion = int(input("Desea agregar un piranometro? 1-Si 2-No "))
                    if sensor_radiacion < 1 or sensor_radiacion > 2:
                        raise ValueError("Ingrese un valor válido")
                    break
                except ValueError as ve:
                    print("Error: ",ve)
            if sensor_radiacion == 1:
                satelite.agregar_sensor(Sensor("Piranometro", "W/m²"))

            while True:
                try:
                    sensor_temperatura = int(input("Desea agregar un termometro? 1-Si 2-No "))
                    if sensor_temperatura < 1 or sensor_temperatura > 2:
                        raise ValueError("Ingrese un valor válido")
                    break
                except ValueError as ve:
                    print("Error: ",ve)
            if sensor_temperatura == 1:
                satelite.agregar_sensor(Sensor("Termometro", "°C"))

            while True:
                try:
                    sensor_presion = int(input("Desea agregar un barometro? 1-Si 2-No "))
                    if sensor_presion < 1 or sensor_presion > 2:
                        raise ValueError("Ingrese un valor válido")
                    break
                except ValueError as ve:
                    print("Error: ",ve)
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
            if isinstance(lista_satelites, dict) and "respuesta" in lista_satelites:
                print(lista_satelites["respuesta"])
                continue
            cantidad = 0
            for sat in lista_satelites:
                cantidad +=1
                print(f"{cantidad}-Nombre:{sat[1]}| Tipo: {sat[2]}| Fecha de lanzamiento: {sat[3]}| Orbita: {sat[4]}| Estado: {sat[5]}\n")
            if len(lista_satelites) == 0:
                print("Necesita tener un satelite creado")
                continue
            while True:
                try:
                    satelite = int(input("Seleccione el satelite que quiera asignar: "))
                    if satelite < 1 or satelite > len(lista_satelites):
                        raise ValueError("Ingrese un valor válido")
                    break
                except ValueError as ve:
                    print("Error: ",ve)
            objetivo = str(input("Ingrese el objetivo de la mision: "))
            zona = str(input("Ingrese la zona de observacion: "))
            duracion = input("Ingrese la duración de la mision (dias)")
            estado = str(input("En qué estado se encuentra: "))
            mision = Mision(nombre, satelite, objetivo, zona, duracion, estado)
            enviar = mision.devolver_json("registrar_mision")
            servidor.sendall(json.dumps(enviar).encode())
            respuesta = servidor.recv(3000).decode()
            respuesta = json.loads(respuesta)
            print(respuesta["respuesta"])
        
        
        elif opcion == 3:
            lista_misiones = recibir_datos("recibir_misiones")
            if isinstance(lista_misiones, dict) and "respuesta" in lista_misiones:
                print(lista_misiones["respuesta"])
                continue
            cantidad = 0
            for mis in lista_misiones:
                cantidad +=1
                print(f"{cantidad}-Nombre:{mis[1]}| ID del satelite: {mis[2]}| Objetivo: {mis[3]}| Zona de observación: {mis[4]}| Duracion: {mis[5]} días| Estado: {mis[6]}\n")
            while True:
                try:
                    mision_elegida = int(input("Seleccione el satelite que quiera asignar: "))
                    if mision_elegida < 1 or mision_elegida > len(lista_misiones):
                        raise ValueError("Ingrese un valor válido")
                    break
                except ValueError as ve:
                    print("Error: ",ve)
    
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
            misiones = recibir_datos("recibir_misiones")
            if isinstance(misiones, dict) and "respuesta" in misiones:
                print(misiones["respuesta"])
                misiones = []
            while True:
                try:
                    nombre = None
                    nombre_opcion = int(input("¿Aplicar filtro por nombre de mision?: 1-Si 2-No"))
                    if nombre_opcion < 1 or nombre_opcion > 2:
                        raise ValueError("El valor es inválido")
                    break
                except ValueError as ve:
                    print("Error: ",ve)
            if nombre_opcion == 1:
                nombre = str(input("¿Que nombre de mision desea filtrar?: "))
            while True:
                try:
                    sid = None
                    id_opcion = int(input("¿Aplicar filtro por id de satelite?: 1-Si 2-No"))
                    if id_opcion < 1 or id_opcion > 2:
                        raise ValueError("El valor es inválido")
                    break
                except ValueError as ve:
                    print("Error: ",ve)
            if id_opcion == 1:
                while True:
                    try:
                        sid = int(input("¿Que id de satelite desea filtrar?: "))
                        break
                    except Exception as e:
                        print("Error: ",e)
            misiones_filtradas = []
            for mision in misiones:
                if (str(mision[1]) == nombre or nombre == None) and (mision[2] == sid or sid == None):
                    misiones_filtradas.append(mision)
            if len(misiones_filtradas) == 0:
                print("No hay misiones con esos criterios")
            else:
                print("Misiones encontradas:")
                cantidad = 0
                for mis in misiones_filtradas:
                    cantidad+=1
                    print(f"{cantidad}-Nombre:{mis[1]}| ID del satelite: {mis[2]}| Objetivo: {mis[3]}| Zona de observación: {mis[4]}| Duracion: {mis[5]} días| Estado: {mis[6]}\n")
            



        elif opcion == 5:
            satelites = recibir_datos("recibir_satelites")
            if isinstance(satelites, dict) and "respuesta" in satelites:
                print(satelites["respuesta"])
                satelites = []
            while True:
                try:
                    tipo = None
                    tipo_opcion = int(input("¿Aplicar filtro por tipo de satelite?: 1-Si 2-No"))
                    if tipo_opcion < 1 or tipo_opcion > 2:
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
                    if sensor_opcion < 1 or sensor_opcion > 2:
                        raise ValueError("El valor es inválido")
                    break
                except ValueError as ve:
                    print("Error: ",ve)

            if sensor_opcion == 1:
                while True:
                    try:
                        sensor_elegir = int(input("¿Qué tipo de sensor desea filtrar? 1-Piranometro 2-Termometro 3-Barometro: "))
                        if sensor_elegir < 1 or sensor_elegir > 3:
                            raise ValueError("Ingrese un valor válido")
                        break
                    except ValueError as ve:
                        print("Error: ",ve)

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
                    if estado_opcion < 1 or estado_opcion > 2:
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
            for sat in satelites:
                if (sat[2] == tipo or tipo == None) and (sensor in sat[6] or sensor == None) and (sat[5] == estado or estado == None):
                    satelites_filtrados.append(sat)
            if len(satelites_filtrados) == 0:
                print("No hay satelites con esos criterios")
            else:
                print("Satelites encontrados:")
                cantidad = 0
                for sat in satelites_filtrados:
                    cantidad += 1
                    print(f"{cantidad}-Nombre:{sat[1]}| Tipo: {sat[2]}| Fecha de lanzamiento: {sat[3]}| Orbita: {sat[4]}| Estado: {sat[5]}\n")
        elif opcion == 6:
            lista_misiones = recibir_datos("recibir_misiones")
            if isinstance(lista_misiones, dict) and "respuesta" in lista_misiones:
                print(lista_misiones["respuesta"])
                lista_misiones = []
            cantidad = 0
            for mis in lista_misiones:
                cantidad +=1
                print(f"{cantidad}-Nombre:{mis[1]}| ID del satelite: {mis[2]}| Objetivo: {mis[3]}| Zona de observación: {mis[4]}| Duracion: {mis[5]} días| Estado: {mis[6]}\n")
            if len(lista_misiones) != 0:
                while True:
                    try:
                        mision_elegida = int(input("Elija la mision en la que quiera registrar un dato: "))
                        if mision_elegida < 1 or mision_elegida > len(lista_misiones):
                            raise ValueError("Ingrese un valor válido")
                        break
                    except ValueError as ve:
                        print("Error: ",ve)
                while True:
                    try:
                        accion = int(input("¿Que dato se recolectará? 1-Imagen 2-Sensor 3-Medicion Científica"))
                        if accion < 1 or accion > 3:
                            raise ValueError("Ingrese un valor válido")
                        break
                    except ValueError as ve:
                        print("Error: ",ve)
                if accion == 1:
                    descripcion = str(input("Describa el resultado de la medición científica "))
                    enviar = {
                        "accion": "registrar_datos",
                        "id_mision": mision_elegida,
                        "tipo": "imagen",
                        "valor": None,
                        "descripcion": descripcion
                    }
            
                elif accion == 2:
                    lista_satelites = recibir_datos("recibir_satelites")
                    if isinstance(lista_satelites, dict) and "respuesta" in lista_satelites:
                        print(lista_satelites["respuesta"])
                        lista_satelites = []
                    satelite_mision = None

                    for satelite in lista_satelites:
                        if satelite[0] == lista_misiones[mision_elegida-1][2]:
                            satelite_mision = satelite
                    if satelite_mision is None:
                        print("No se encontró el satélite asociado a la misión seleccionada.")
                        continue
                    sensores = satelite_mision[6]
                    if len(sensores) == 0:
                        print("La misión seleccionada no posee sensores asociados.")
                        continue
                    cantidad = 0
                    for sensor in sensores:
                        cantidad +=1
                        print(f"{cantidad}-{sensor}\n")
                    while True:
                        try:
                            sensor_elegido = int(input("Seleccione el sensor que registrá un dato: "))
                            if sensor_elegido < 1 or sensor_elegido > len(sensores):
                                raise ValueError("Ingrese un valor válido")
                            break
                        except ValueError as ve:
                            print("Error: ",ve)
                    sensor_registrar = sensores[sensor_elegido-1]
                    valor = int(input("Ingrese el valor a registrar: "))
                    enviar = {
                        "accion": "registrar_datos",
                        "id_mision": mision_elegida,
                        "tipo": sensor_registrar,
                        "valor": valor,
                        "descripcion": f"Dato registrado del sensor {sensor_registrar}"
                    }
                    
                           
                elif accion == 3:
                    descripcion = str(input("Describa el resultado de la medición científica "))
                    enviar = {
                        "accion": "registrar_datos",
                        "id_mision": mision_elegida,
                        "tipo": "imagen",
                        "valor": None,
                        "descripcion": descripcion
                    }
                
                servidor.sendall(json.dumps(enviar).encode())
                respuesta = servidor.recv(3000).decode()
                respuesta = json.loads(respuesta)
                print(respuesta["respuesta"])
            else:
                print("No hay misiones para registrar datos")
            
        elif opcion == 7:
            lista_datos = recibir_datos("recibir_datos")
            if isinstance(lista_datos, dict) and "respuesta" in lista_datos:
                print(lista_datos["respuesta"])
                lista_datos = []
            cantidad = 0
            for datos in lista_datos:
                cantidad +=1
                if datos[3] == None:
                    print(f"{cantidad}-ID de misión: {datos[1]}| Tipo de dato recolectado: {datos[2]}| Descripción: {datos[4]}\n")
                else:
                    print(f"{cantidad}-ID de misión: {datos[1]}| Tipo de dato recolectado: {datos[2]}| Valor registrado: {datos[3]}| Descripción: {datos[4]}\n")
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