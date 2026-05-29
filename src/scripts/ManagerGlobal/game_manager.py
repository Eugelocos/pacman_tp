
import pygame
from .game_scene import GameScene
from .menu_scene import MenuScene
from Mapa.map import matriz_mapa
from Mapa.grid_manager import GridManager

class GameManager():
    def __init__(self):
        self.entities=pygame.sprite.Group()
        self.scenes={}
        self.pantalla=pygame.display.set_mode((800,600))
        self.scenes={"menu": MenuScene(self), "game": GameScene(self), "game_over": GameScene(self)}
        self.current_scene="menu"
        self.grid_manager = GridManager(matriz_mapa)
        

    def add_entity(self, entity):
        self.entities.add(entity)
    
    def remove_entity(self, entity):
        self.entities.remove(entity)
    
    def change_scene(self, new_scene):
        if new_scene in self.scenes:
            self.current_scene=new_scene

    def render(self, screen):
        self.scenes.get(self.current_scene).render(screen)
    def update(self):
        self.scenes.get(self.current_scene).update()



