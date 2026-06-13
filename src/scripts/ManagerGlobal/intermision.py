import pygame
import os
import sys
import math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.funciones_aux import dibujar_texto

import constantes as c
from scripts.ManagerGlobal.escena import EscenaBase


class Intermision(EscenaBase):
    frames = None
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.nivel_siguiente = game_manager.nivel
        self.timer = 0
        self.duracion = 3  # seg
        self.alpha = 0  # fade(degrade)
        self.mostrar_puntos = True
        

        self.font_grande = pygame.font.Font(os.path.join("pacman_tp","assets", "fonts", "PressStart2P.ttf"), 48)
        self.font_mediana = pygame.font.Font(os.path.join("pacman_tp","assets", "fonts", "PressStart2P.ttf"), 32)
        self.font_pequena = pygame.font.Font(os.path.join("pacman_tp","assets", "fonts", "PressStart2P.ttf"), 20)
        
        self.frame_actual = 0
        self.frame_timer = 0
        self.frame_delay = 40
        self.x_pacman = -100

        if not Intermision.frames:
            Intermision.frames = [pygame.transform.scale(pygame.image.load(f"pacman_tp/assets/imagenes/characters/pacman/horizontal/pacman_{i}.png").convert_alpha(), (30, 30)) for i in range(4)]

        self.sonido = pygame.mixer.Sound(c.EFECTOS["jugar"])
        
    def on_enter(self):
        self.timer = 0
        self.alpha = 0
        
        self.game_manager.rutina_manager.pausar()
    
    def on_exit(self):
        self.sonido.play()
        
    def update(self, delta_time, eventos):
        delta_seg = delta_time / 1000.0
        self.timer += delta_seg
        self.x_pacman = self.game_manager.ventana.get_width() * (self.timer / self.duracion)
        self.actualizar_animacion(delta_time)

        if self.timer >= self.duracion:
            self.game_manager.rutina_manager.reiniciar()
            self.game_manager.rutina_manager.reanudar()
            self.game_manager.change_scene("game")
    
    def render(self):
        ventana = self.game_manager.ventana
        ancho = ventana.get_width()
        alto = ventana.get_height()
        
        ventana.fill(c.COLOR_BG)
        
        texto_nivel = f"NIVEL {self.nivel_siguiente}"
        x = ancho // 2
        y = alto // 3
        dibujar_texto(texto_nivel, ventana, self.font_grande, c.AMARILLO, x, y, True)
        
        texto_prepare = "PREPARESE"
        x = ancho // 2
        y = alto // 2
        dibujar_texto(texto_prepare, ventana, self.font_mediana, c.BLANCO, x, y, True)
        
        texto_score = f"PUNTAJE: {self.game_manager.score}"
        x = ancho // 2
        y = alto * 3 // 4
        dibujar_texto(texto_score, ventana, self.font_pequena, c.VERDE, x, y, True)

        pacman_y = alto // 2 + 50
        ventana.blit(Intermision.frames[self.frame_actual], (self.x_pacman, pacman_y))
    

    def actualizar_animacion(self, delta_time):
        self.frame_timer += delta_time
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.frame_actual = (self.frame_actual + 1) % len(Intermision.frames)
            self.image=Intermision.frames[self.frame_actual]
