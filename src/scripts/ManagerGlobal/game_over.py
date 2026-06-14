import pygame
import os
import sys
import constantes as c
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.funciones_aux import dibujar_texto
from scripts.ManagerGlobal.escena import EscenaBase


ruta_fuente = os.path.join("pacman_tp","assets", "fonts", "PressStart2P.ttf")

class GameOver(EscenaBase):
    def __init__(self, game_manager):
        super().__init__(game_manager)

        self.milisegundos=c.PARPADEO
        self.high_score=0 #luego hay que implementar la logica de lectura de archivo donde esta el high score real 
        self.texto=True
        self.tiempo=0
        self.fuente_titulo = pygame.font.Font(ruta_fuente, 48)
        self.fuente_normal = pygame.font.Font(ruta_fuente, 15)    
        self.musica_game_over = pygame.mixer.music.load(c.MUSICA["game_over"])
        pygame.mixer.music.play(-1)
       
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
        self.game_manager.ventana.fill((0,0,0))
     
        x = ancho_actual // 2
        y = alto_actual *  5 // 16
        dibujar_texto("GAME OVER",self.game_manager.ventana,self.fuente_titulo, c.AMARILLO, x,y,True)
        
        x = ancho_actual // 2
        y = alto_actual *  10 // 16
        dibujar_texto("Presiona ENTER para reiniciar",self.game_manager.ventana,self.fuente_normal, c.BLANCO, x,y, True) 
        
        x = ancho_actual // 2
        y = alto_actual *  12 // 16
        dibujar_texto("Presiona ESC para ir al menu",self.game_manager.ventana,self.fuente_normal, c.BLANCO, x,y, True)

    def on_exit(self):
        self.game_manager.rutina_manager.reiniciar()
        pygame.mixer.music.stop()
    


        
        
    