import pygame
import constantes as c 
from funciones_aux import dibujar_texto

class WelcomeScene(): 
    def __init__(self, game_manager):
        self.game_manager=game_manager
        self.milisegundos=c.PARPADEO
        self.high_score=0 #luego hay que implementar la logica de lectura de archivo donde esta el high score real 
        self.texto=True
        self.tiempo=0
        self.fuente_titulo = pygame.font.SysFont("comicsans", 70)
        self.fuente_normal = pygame.font.SysFont("comicsans", 30)
       
    def update(self,delta_time=0, eventos=None):
        for event in eventos:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    self.game_manager.change_scene("game")
        self.tiempo+=delta_time
        if self.tiempo>=self.milisegundos:
            self.tiempo=0
            self.texto=not self.texto
                                
    def render(self):
        self.game_manager.ventana.fill(c.COLOR_BG)
        x = c.ANCHO_VENTANA // 2 - 100
        y = c.ALTO_VENTANA // 2 - 300
        dibujar_texto("HIGH SCORE:",self.game_manager.ventana,self.fuente_normal, c.BLANCO, x,y)
     
        y = c.ALTO_VENTANA // 2 - 250
        dibujar_texto(str(self.high_score),self.game_manager.ventana,self.fuente_normal, c.VERDE, x,y)
        x = c.ANCHO_VENTANA // 2 - 150
        y = c.ALTO_VENTANA // 2 
        dibujar_texto("PAC-MAN",self.game_manager.ventana,self.fuente_titulo, c.AMARILLO, x,y)
        
        if self.texto: 
            x = c.ANCHO_VENTANA // 2 - 170
            y = c.ALTO_VENTANA // 2 + 100
            dibujar_texto("Presiona ENTER para jugar",self.game_manager.ventana,self.fuente_normal, c.BLANCO, x,y)
            
        
        
        
        
        

#dibujar texto
def dibujar_texto(texto, ventana , fuente, color, x, y):
    img=fuente.render(texto, True, color)
    ventana.blit(img, (x, y))
        
        
    
    