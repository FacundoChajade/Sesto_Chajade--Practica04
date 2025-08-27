class Mision:
    def __init__(self, nombre, satelite, objetivo, zona, duracion, estado):
        self.nombre = nombre
        self.satelite = satelite
        self.objetivo = objetivo
        self.zona = zona
        self.duracion = duracion
        self.estado = estado

    def modificar_estado(self, estado):
        self.estado = estado
    
    def devolver_json(self, accion):
        return {
            "accion":accion,
            "nombre":self.nombre,
            "satelite":self.satelite,
            "objetivo":self.objetivo,
            "zona":self.zona,
            "duracion":self.duracion,
            "estado":self.estado      
        }
        