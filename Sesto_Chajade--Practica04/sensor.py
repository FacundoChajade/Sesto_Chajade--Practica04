import random
class Sensor():
    def __init__(self,nombre,tipo_unidad):
        self.nombre = nombre
        self.tipo_unidad = tipo_unidad

    def registrar_datos(self):
        if self.nombre == "piranometro":
            valor = f"{random.randint(0, 1400)} {self.tipo_unidad}"
        elif self.nombre == "termometro":
            valor = f"{random.randint(-50, 50)} {self.tipo_unidad}"
        elif self.nombre == "barometro":
            valor = f"{random.randint(300, 1100)} {self.tipo_unidad}"
        return valor