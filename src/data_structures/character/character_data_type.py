
from entity import Entity

class Character(Entity):
    def __init__(self, pos, activo, speed, tipo_movimiento):
        super().__init__(pos, activo)
        self.speed=speed
        self.tipo_movimiento=tipo_movimiento