import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from data_structures.entity import Entity
from scripts.Movimiento.movimiento import manejar_movimiento
import constantes as c

class Personaje(Entity):
    DIRECTIONS={"arriba":(0,-1),"abajo":(0,1),"derecha":(1, 0),"izquierda":(-1,0)}
    def __init__(self,position, visibility, direction, tile_size, sprite):
        super().__init__(position, visibility, tile_size, sprite)

        self.velocidad=c.VELOCIDAD_BASE
        self.direction=self.DIRECTIONS[direction]
        self.proxima_direccion=self.direction
        self.frames = [self.image]
        self.frame_actual = 0
        self.frame_timer = 0
        self.frame_delay = 100


    def cambiar_direccion(self, new_dir):
        self.direction=self.DIRECTIONS[new_dir]
        if hasattr(self, 'cambiar_sprite_por_direccion'):
            self.cambiar_sprite_por_direccion()
            self.frame_timer=0
            self.frame_actual=0
    def actualizar_animacion(self, delta_time):
        self.frame_timer += delta_time
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)
            self.image=self.frames[self.frame_actual]
    
    def update(self, ventana, delta_time, escena=None, eventos=None):
        manejar_movimiento(self, escena, self.direction, delta_time)
        super().update(ventana, delta_time, escena, eventos)


