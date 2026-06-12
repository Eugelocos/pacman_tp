import pygame
import os
import sys
import constantes as c
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.funciones_aux import dibujar_texto


ruta_fuente = os.path.join("pacman_tp","assets", "fonts", "PressStart2P.ttf")

class GameOver():
    def __init__(self, game_manager):
        self.game_manager=game_manager
        self.milisegundos=c.PARPADEO
        self.high_score=0 #luego hay que implementar la logica de lectura de archivo donde esta el high score real 
        self.texto=True
        self.tiempo=0
        self.fuente_titulo = pygame.font.Font(ruta_fuente, 20)
        self.fuente_normal = pygame.font.Font(ruta_fuente, 10)    
       
    def update(self,delta_time=0, eventos=None):
        for event in eventos:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    self.game_manager.change_scene("game")
                if event.key==pygame.K_ESCAPE:
                    self.game_manager.change_scene("welcome")
                   
        self.tiempo+=delta_time
        if self.tiempo>=self.milisegundos:
            self.tiempo=0
            self.texto=not self.texto
                                
    def render(self):
        ancho_actual, alto_actual = self.game_manager.ventana.get_size()
        self.game_manager.ventana.fill(c.COLOR_BG)
     
        x = ancho_actual // 2
        y = alto_actual *  3 // 16
        dibujar_texto("GAME OVER",self.game_manager.ventana,self.fuente_titulo, c.AMARILLO, x,y,True)
        
        x = ancho_actual // 2
        y = alto_actual *  7 // 16
        dibujar_texto("Presiona ENTER para reiniciar",self.game_manager.ventana,self.fuente_normal, c.BLANCO, x,y, True) 
        
        x = ancho_actual // 2
        y = alto_actual *  9 // 16
        dibujar_texto("Presiona ESC para ir al menu",self.game_manager.ventana,self.fuente_normal, c.BLANCO, x,y, True)



        
        
    