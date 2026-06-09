import pygame
import constantes as c 
from funciones_aux import dibujar_texto,dibujar_fantasma,dibujar_selec_esquinas

class WelcomeScene(): 
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
                    self.game_manager.change_scene("select_fantasmas")
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
            
class SelectFantasmas():
    def __init__(self,game_manager):
        self.game_manager=game_manager
        self.seleccionados=[]
        self.fuente_titulos=pygame.font.SysFont("Courier", 35)

    def update(self,delta_time=0,eventos=None):
        for event in eventos:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_1:
                    if c.FANTASMAS[0] not in self.seleccionados:
                        if len(self.seleccionados)<4:
                            self.seleccionados.append(c.FANTASMAS[0])
                        elif len(self.seleccionados)==4:
                            self.seleccionados.remove(self.seleccionados[0])
                            self.seleccionados.append(c.FANTASMAS[0])
                    elif c.FANTASMAS[0] in self.seleccionados:
                        self.seleccionados.remove(c.FANTASMAS[0])
                if event.key==pygame.K_2:
                    if c.FANTASMAS[1] not in self.seleccionados:
                        if len(self.seleccionados)<4:
                            self.seleccionados.append(c.FANTASMAS[1])
                        elif len(self.seleccionados)==4:
                            self.seleccionados.remove(self.seleccionados[0])
                            self.seleccionados.append(c.FANTASMAS[1])
                    elif c.FANTASMAS[1] in self.seleccionados:
                        self.seleccionados.remove(c.FANTASMAS[1])
                if event.key==pygame.K_3:
                    if c.FANTASMAS[2] not in self.seleccionados:
                        if len(self.seleccionados)<4:
                            self.seleccionados.append(c.FANTASMAS[2])
                        elif len(self.seleccionados)==4:
                            self.seleccionados.remove(self.seleccionados[0])
                            self.seleccionados.append(c.FANTASMAS[2])
                    elif c.FANTASMAS[2] in self.seleccionados:
                        self.seleccionados.remove(c.FANTASMAS[2])
                if event.key==pygame.K_4:
                    if c.FANTASMAS[3] not in self.seleccionados:
                        if len(self.seleccionados)<4:
                            self.seleccionados.append(c.FANTASMAS[3])
                        elif len(self.seleccionados)==4:
                            self.seleccionados.remove(self.seleccionados[0])
                            self.seleccionados.append(c.FANTASMAS[3])
                    elif c.FANTASMAS[3] in self.seleccionados:
                        self.seleccionados.remove(c.FANTASMAS[3])
                if event.key==pygame.K_5:
                    if c.FANTASMAS[4] not in self.seleccionados:
                        if len(self.seleccionados)<4:
                            self.seleccionados.append(c.FANTASMAS[4])
                        elif len(self.seleccionados)==4:
                            self.seleccionados.remove(self.seleccionados[0])
                            self.seleccionados.append(c.FANTASMAS[4])
                    elif c.FANTASMAS[4] in self.seleccionados:
                        self.seleccionados.remove(c.FANTASMAS[4])
                if event.key==pygame.K_6:
                    if c.FANTASMAS[5] not in self.seleccionados:
                        if len(self.seleccionados)<4:
                            self.seleccionados.append(c.FANTASMAS[5])
                        elif len(self.seleccionados)==4:
                            self.seleccionados.remove(self.seleccionados[0])
                            self.seleccionados.append(c.FANTASMAS[5])
                    elif c.FANTASMAS[5] in self.seleccionados:
                        self.seleccionados.remove(c.FANTASMAS[5])
                if event.key==pygame.K_RETURN and len(self.seleccionados)==4:
                        self.game_manager.scenes["select_esquinas"]=SelectEsquinas(self.game_manager,self.seleccionados)
                        self.game_manager.change_scene("select_esquinas")
                    
                    
    def render(self):
        self.game_manager.ventana.fill(c.COLOR_BG)
        x = c.ANCHO_VENTANA // 2 - 250
        y = c.ALTO_VENTANA // 2 - 350
        f=len(self.seleccionados) #variable que cambia el numero de fantasmas seleccionados
        dibujar_texto(f"Elegi 4 fantasmas [{f}/4]",self.game_manager.ventana,self.fuente_titulos, c.AMARILLO, x,y)
        for i in range(6):
            fantasma=c.FANTASMAS[i]
            dibujar_fantasma(fantasma,i,self.game_manager.ventana,self.seleccionados)

class SelectEsquinas():
    def __init__(self,game_manager, lista_fantasmas):    
        self.game_manager=game_manager
        self.fantasmas=lista_fantasmas
        self.esquinas=[]
        self.fuente_titulos=pygame.font.SysFont("Courier", 35)
        self.fuente_subtitulos=pygame.font.SysFont("Courier", 20)
        self.fuente_normal=pygame.font.SysFont("Courier", 10)
    
    def update(self,delta_time=0,eventos=None):
        sup_izq=(0,0)
        sup_der=(28,0)
        inf_izq=(0,31)
        inf_der=(28,31)
        for event in eventos:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_1:
                    if sup_izq not in self.esquinas and len(self.esquinas)<4:
                        self.esquinas.append(sup_izq)
                if event.key==pygame.K_2:
                    if sup_der not in self.esquinas and len(self.esquinas)<4:
                        self.esquinas.append(sup_der)
                if event.key==pygame.K_3:
                    if inf_izq not in self.esquinas and len(self.esquinas)<4:
                        self.esquinas.append(inf_izq)
                if event.key==pygame.K_4:
                    if inf_der not in self.esquinas and len(self.esquinas)<4:
                        self.esquinas.append(inf_der)  
                if len(self.esquinas)==4:
                    self.game_manager.change_scene("game")
        
    
    def render(self):
        
        self.game_manager.ventana.fill(c.COLOR_BG)
        f=len(self.esquinas)
        if f<4:
            dibujar_selec_esquinas(self.game_manager.ventana,self.fantasmas[f],len(self.esquinas)+1,self.esquinas)
    
        
    
    
          
            


        
                
        
        


        
        
    
    
    
    