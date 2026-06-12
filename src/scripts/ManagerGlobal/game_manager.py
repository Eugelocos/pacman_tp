
import os
import sys
import pygame
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import constantes as c
from scripts.ManagerGlobal.game_scene import GameScene
from scripts.ManagerGlobal.menu_scene import WelcomeScene, SelectFantasmas
from scripts.ManagerGlobal.game_over import GameOver
from Mapa.map import matriz_mapa
from Mapa.grid_manager import GridManager

class GameManager():
    def __init__(self):
        self.entities = pygame.sprite.Group()

        self.ventana = pygame.display.set_mode(
            (c.ANCHO_VENTANA, c.ALTO_VENTANA), 
            pygame.RESIZABLE
        )
        self.tipos_enemigos=[] # [("fantasma_... ,  (esquina)"), ... ]
        self.grid_manager = GridManager(matriz_mapa)

        for entity in self.grid_manager.grid:
            self.add_entity(entity)

        self.scenes = {
            "welcome": WelcomeScene(self),
            "select_fantasmas": SelectFantasmas(self),
            "game": GameScene(self),
            "game_over": GameOver(self)
        }
        
        self.change_scene("welcome")
        

    def add_entity(self, entity):
        self.entities.add(entity)
    
    def remove_entity(self, entity):
        self.entities.remove(entity)
    
    def change_scene(self, new_scene):
        if new_scene in self.scenes:
            self.current_scene=new_scene
        if new_scene in c.MUSICA:
            pygame.mixer.music.load(c.MUSICA[new_scene])
            pygame.mixer.music.play(loops=-1)
        elif new_scene not in c.MUSICA:
            pygame.mixer.music.stop()

    def render(self):
        self.scenes.get(self.current_scene).render()
        pygame.display.flip()
    
    def update(self, delta_time=0, eventos=None):
        if eventos is None:
            eventos = pygame.event.get()
        
        self.scenes.get(self.current_scene).update(delta_time, eventos)

    def resetear_grilla(self):
        self.entities.empty()

        self.grid_manager = GridManager(matriz_mapa, tipos_enemigos=self.tipos_enemigos)

        for entity in self.grid_manager.grid:
            self.add_entity(entity)

    def actualizar_enemigos(self, nuevos_enemigos):
        self.tipos_enemigos=nuevos_enemigos
        self.resetear_grilla()