
import os
import sys
import pygame
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import constantes as c
from scripts.ManagerGlobal.game_scene import GameScene
from scripts.ManagerGlobal.menu_scene import MenuScene
from Mapa.map import matriz_mapa
from Mapa.grid_manager import GridManager

class GameManager():
    def __init__(self):
        self.entities=pygame.sprite.Group()
        self.scenes={}
        self.ventana=pygame.display.set_mode((c.ANCHO_VENTANA, c.ALTO_VENTANA))
        self.scenes={"menu": MenuScene(self), "game": GameScene(self), "game_over": GameScene(self)}
        self.current_scene="game"
        self.grid_manager = GridManager(matriz_mapa)
        for tile in self.grid_manager.grid:
            self.add_entity(tile)
        

    def add_entity(self, entity):
        self.entities.add(entity)
    
    def remove_entity(self, entity):
        self.entities.remove(entity)
    
    def change_scene(self, new_scene):
        if new_scene in self.scenes:
            self.current_scene=new_scene

    def render(self):
        self.scenes.get(self.current_scene).render()
    def update(self, delta_time=0, eventos=None):
        if eventos is None:
            eventos = pygame.event.get()
        
        self.scenes.get(self.current_scene).update(delta_time, eventos)
        pygame.display.update()


