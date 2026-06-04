import pygame
import constantes as c

class GameOver():
    def __init__(self, game_manager):
        self.game_manager=game_manager
        self.milisegundos=c.PARPADEO
        self.high_score=0 #luego hay que implementar la logica de lectura de archivo donde esta el high score real 
        self.texto=True
        self.tiempo=0
        self.fuente_titulo = pygame.font.SysFont("Courier", 70)
        self.fuente_normal = pygame.font.SysFont("Courier", 30)
    
       
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
        self.game_manager.ventana.fill(c.COLOR_BG)
     
        x = c.ANCHO_VENTANA // 2 - 150
        y = c.ALTO_VENTANA // 2 
        dibujar_texto("GAME OVER",self.game_manager.ventana,self.fuente_titulo, c.AMARILLO, x,y)
        
        x = c.ANCHO_VENTANA // 2 - 150
        y = c.ALTO_VENTANA // 2 + 100
        dibujar_texto("Presiona ENTER para reiniciar",self.game_manager.ventana,self.fuente_normal, c.BLANCO, x,y) 
        
        x = c.ANCHO_VENTANA // 2 - 150
        y = c.ALTO_VENTANA // 2 + 200
        dibujar_texto("Presiona ESC para ir al menu",self.game_manager.ventana,self.fuente_normal, c.BLANCO, x,y)


            

def dibujar_texto(texto, ventana , fuente, color, x, y):
    img=fuente.render(texto, True, color)
    ventana.blit(img, (x, y))
        
        
    