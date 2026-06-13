import pygame
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import constantes as c
from scripts.ManagerGlobal.escena import EscenaBase


class Intermision(EscenaBase):
    def __init__(self, game_manager, duracion=800):
        super().__init__(game_manager)
        self.tiempo_inicio = pygame.time.get_ticks()
        self.duracion = duracion  # ms
        
    def update(self, delta_time, eventos):

        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_inicio >= self.duracion:
            self.game_manager.change_scene('game')  
    
    def render(self):
        self.game_manager.ventana.fill(c.COLOR_BG)

    def on_enter(self):

        self.game_manager.rutina_manager.pausar()
        

    def on_exit(self):
        
        self.game_manager.rutina_manager.reanudar()


