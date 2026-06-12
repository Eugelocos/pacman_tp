
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

        ANCHO_RETRO, ALTO_RETRO = 224, 288
        self.ventana = pygame.Surface((ANCHO_RETRO, ALTO_RETRO))

        self.ventana_real = pygame.display.set_mode(
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

        self.current_scene = "welcome"
        

    def add_entity(self, entity):
        self.entities.add(entity)
    
    def remove_entity(self, entity):
        self.entities.remove(entity)
    
    def change_scene(self, new_scene):
        if new_scene in self.scenes:
            self.current_scene=new_scene

    def render(self):
        ancho_actual, alto_actual = self.ventana_real.get_size()
        self.scenes.get(self.current_scene).render()

        escala = min(ancho_actual / c.ANCHO_VENTANA, alto_actual / c.ALTO_VENTANA)
        ancho_escalado = int(c.ANCHO_VENTANA * escala)
        alto_escalado = int(c.ALTO_VENTANA * escala)

        superficie_escalada = pygame.transform.scale(self.ventana, (ancho_escalado, alto_escalado))

        pos_x = (ancho_actual - ancho_escalado) // 2
        pos_y = (alto_actual - alto_escalado) // 2

        self.ventana_real.fill((0, 0, 0)) 
        self.ventana_real.blit(superficie_escalada, (pos_x, pos_y))
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