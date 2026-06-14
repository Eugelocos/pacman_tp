import sys
import os
import pygame
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from data_structures.entity import Entity

class Tile(Entity):
    def __init__(self, pos, activo, sprite, is_wall, tile_size):
        super().__init__(pos, activo, tile_size, sprite)
        self.is_wall = is_wall
        self.es_puerta = False
        self.contains_pellet = False
        self.contains_power_pellet = False
        self.is_tunnel = False
        
    def place_pellet(self):
        self.contains_pellet = True
    def place_power_pellet(self):
        self.contains_power_pellet = True
    def remove_pellet(self):
        self.contains_pellet = False
        
    def remove_power_pellet(self):
        self.contains_power_pellet = False
        
    def draw(self, ventana):
        if self.contains_pellet or self.contains_power_pellet or self.is_wall or self.es_puerta:
            super().draw(ventana)
