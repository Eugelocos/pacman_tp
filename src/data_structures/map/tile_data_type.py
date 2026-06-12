import sys
import os
import pygame
import constantes as c
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from data_structures.entity import Entity

class Tile(Entity):
    waka_waka=None
    power_pellet=None
    tiempo_reproduccion = 0
    duracion_maxima = 90
    def __init__(self, pos, activo, sprite, is_wall, tile_size):
        super().__init__(pos, activo, tile_size, sprite)
        self.is_wall = is_wall
        self.contains_pellet = False
        self.contains_power_pellet = False
        self.is_tunnel = False
        if Tile.waka_waka is None:
            Tile.waka_waka = pygame.mixer.Sound(c.EFECTOS["punto"])
        if Tile.power_pellet is None: 
            Tile.power_pellet = pygame.mixer.Sound(c.EFECTOS["power_pellet"])
    def place_pellet(self):
        self.contains_pellet = True
    def place_power_pellet(self):
        self.contains_power_pellet = True
    def remove_pellet(self):
        self.contains_pellet = False
        Tile.waka_waka.stop()
        Tile.waka_waka.play()
        Tile.tiempo_reproduccion = pygame.time.get_ticks()
    def remove_power_pellet(self):
        self.contains_power_pellet = False
        Tile.power_pellet.play()
    def draw(self, ventana):
        if Tile.tiempo_reproduccion > 0:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - Tile.tiempo_reproduccion >= Tile.duracion_maxima:
                Tile.waka_waka.stop()
                Tile.tiempo_reproduccion = 0 
        if self.contains_pellet or self.contains_power_pellet or self.is_wall:
            super().draw(ventana)
