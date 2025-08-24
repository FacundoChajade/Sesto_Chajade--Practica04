class Satelite:
    def __init__(self, nombre, tipo, fecha_lanzamiento, orbita, estado):
        self.nombre = nombre
        self.tipo = tipo
        self.sensores = []
        self.fecha_lanzamiento = fecha_lanzamiento
        self.orbita = orbita
        self.estado = estado

    def agregar_sensor(self,sensor):
        self.sensores.append(sensor)
        
    
    def devolver_json(self, accion):
        return {
            "accion":accion,
            "nombre":self.nombre,
            "tipo":self.tipo,
            "sensores":[sensor.devolver_json() for sensor in self.sensores],
            "fecha_lanzamiento":self.fecha_lanzamiento,
            "orbita":self.orbita,
            "estado":self.estado  
        }