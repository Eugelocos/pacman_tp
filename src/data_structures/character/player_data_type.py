import pygame
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.funciones_aux import cargar_con_transparencia
from data_structures.character.character_data_type import Personaje
class Jugador(Personaje):
    sprites_cache={}
    def __init__(self, position, visibility, nombre_jugador, direction, tile_size, lives=3):
        ruta_inicial = f"pacman_tp/assets/imagenes/characters/{nombre_jugador}/horizontal/{nombre_jugador}_0.png"
        super().__init__(position, visibility, direction, tile_size, ruta_inicial )
        self.lives=lives
        self.point=0
        self.nombre=nombre_jugador
        self.is_powered_up=False
        if direction not in Jugador.sprites_cache:
            self.cargar_frames()

    def cargar_frames(self):
        for direccion in ["arriba", "abajo", "derecha", "izquierda"]:
            for i in range(3):
                if direccion.lower() not in Jugador.sprites_cache:
                    Jugador.sprites_cache[direccion.lower()]=[]
                if direccion == "izquierda" or direccion == "derecha":
                    ruta=f"pacman_tp/assets/imagenes/characters/{self.nombre}/horizontal/{self.nombre}_{i}.png"
                    if direccion == "izquierda":
                        Jugador.sprites_cache[direccion.lower()].append(pygame.transform.scale(pygame.transform.flip(pygame.image.load(ruta).convert_alpha(), True, False), (self.tile_size, self.tile_size)))
                    else:
                        Jugador.sprites_cache[direccion.lower()].append(pygame.transform.scale(pygame.image.load(ruta).convert_alpha(), (self.tile_size, self.tile_size)))
                else:
                    ruta=f"pacman_tp/assets/imagenes/characters/{self.nombre}/vertical/{self.nombre}_{i}.png"
                    if direccion == "abajo":
                        Jugador.sprites_cache[direccion.lower()].append(pygame.transform.scale(pygame.transform.flip(cargar_con_transparencia(ruta), False, True), (self.tile_size, self.tile_size)))
                    else:
                        Jugador.sprites_cache[direccion.lower()].append(pygame.transform.scale(cargar_con_transparencia(ruta), (self.tile_size, self.tile_size)))

        self.cambiar_sprite_por_direccion()


    def cambiar_sprite_por_direccion(self):
        if self.direction[0]==0 and self.direction[1]==-1:
            self.frames=Jugador.sprites_cache["arriba"]
        elif self.direction[0]==0 and self.direction[1]==1:
            self.frames=Jugador.sprites_cache["abajo"]
        elif self.direction[0]==1 and self.direction[1]==0:
            self.frames=Jugador.sprites_cache["derecha"]
        elif self.direction[0]==-1 and self.direction[1]==0:
            self.frames=Jugador.sprites_cache["izquierda"]

        self.frame_actual=0
        self.image=self.frames[self.frame_actual]

    def update(self, ventana, delta_time, escena, eventos=None):
        self.leer_inputs(eventos)
        super().update(ventana, delta_time, escena, eventos)

    def leer_inputs(self, eventos=None):
        if eventos is None:
            eventos = pygame.event.get()
        for event in eventos:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.proxima_direccion=(0,-1)
                elif event.key == pygame.K_s:
                    self.proxima_direccion=(0,1)
                elif event.key == pygame.K_a:
                    self.proxima_direccion=(-1,0)
                elif event.key == pygame.K_d:
                    self.proxima_direccion=(1,0)

