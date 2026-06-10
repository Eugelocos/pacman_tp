import pygame
import os
import constantes as c 
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.funciones_aux import dibujar_texto,dibujar_fantasma,dibujar_selec_esquinas
from scripts.ManagerGlobal.game_scene import GameScene

ruta_fuente = os.path.join("pacman_tp","assets", "fonts", "PressStart2P.ttf")

class WelcomeScene(): 
    def __init__(self, game_manager):
        self.game_manager=game_manager
        self.milisegundos=c.PARPADEO
        self.high_score=0 #luego hay que implementar la logica de lectura de archivo donde esta el high score real 
        self.texto=True
        self.tiempo=0

       
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
        ancho_actual, alto_actual = self.game_manager.ventana.get_size()
        self.fuente_titulo = pygame.font.Font(ruta_fuente, 50)
        self.fuente_normal = pygame.font.Font(ruta_fuente, 30)
        margen=20
        self.game_manager.ventana.fill(c.COLOR_BG)
        x = ancho_actual // 2
        y = alto_actual *  3 // 16
        dibujar_texto("HIGH SCORE:", self.game_manager.ventana, self.fuente_normal, c.BLANCO, x, y, True)
     
        x = ancho_actual // 2
        y = alto_actual *  4 // 16       
        dibujar_texto(str(self.high_score),self.game_manager.ventana,self.fuente_normal, c.VERDE, x,y, True)

        x = ancho_actual // 2
        y = alto_actual *  8 // 16        
        dibujar_texto("PAC-MAN",self.game_manager.ventana,self.fuente_titulo, c.AMARILLO, x,y, True)

        if self.texto: 
            x = ancho_actual // 2
            y = alto_actual * 11 // 16            
            dibujar_texto("Presiona ENTER para jugar",self.game_manager.ventana,self.fuente_normal, c.BLANCO, x,y, True)
            
class SelectFantasmas():

    def __init__(self,game_manager):
        self.game_manager=game_manager
        self.seleccionados=[]
        self.fuente_titulos=pygame.font.Font(ruta_fuente, 30)

    def update(self,delta_time=0,eventos=None):
        for event in eventos:
            if event.type==pygame.KEYDOWN:
                tecla_indice = {
                    pygame.K_1: 0,
                    pygame.K_2: 1,
                    pygame.K_3: 2,
                    pygame.K_4: 3,
                    pygame.K_5: 4,
                    pygame.K_6: 5,
                }
                if event.key in tecla_indice:
                    indice = tecla_indice[event.key]
                    fantasma = c.FANTASMAS[indice]
                    if fantasma not in self.seleccionados:
                        if len(self.seleccionados)<4:
                            self.seleccionados.append(fantasma)
                        elif len(self.seleccionados)==4:
                            self.seleccionados.pop(0)
                            self.seleccionados.append(fantasma)
                    elif fantasma in self.seleccionados:
                        self.seleccionados.remove(fantasma)
                if event.key==pygame.K_RETURN and len(self.seleccionados)==4:
                    self.game_manager.scenes["select_esquinas"]=SelectEsquinas(self.game_manager,self.seleccionados)
                    self.game_manager.change_scene("select_esquinas")

    def render(self):
        ancho_actual, alto_actual = self.game_manager.ventana.get_size()
        self.game_manager.ventana.fill(c.COLOR_BG)
        x = ancho_actual // 2
        y = alto_actual *  2 // 16
        f=len(self.seleccionados) # variable que cambia el numero de fantasmas seleccionados
        dibujar_texto(f"Elegi 4 fantasmas [{f}/4]",self.game_manager.ventana,self.fuente_titulos, c.AMARILLO, x,y, True)
        for i in range(6):
            dibujar_fantasma(i,self.game_manager.ventana,self.seleccionados, ruta_fuente)

class SelectEsquinas():
    def __init__(self,game_manager, lista_fantasmas):    
        self.game_manager=game_manager
        self.fantasmas=lista_fantasmas
        self.esquinas=[]
        self.fuente_titulos=pygame.font.Font(ruta_fuente, 35)
        self.fuente_subtitulos=pygame.font.Font(ruta_fuente, 20)
        self.fuente_normal=pygame.font.Font(ruta_fuente, 10)
    
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
                    lista_enemigos = [(fantasma[0], esquina) for fantasma, esquina in zip(self.fantasmas, self.esquinas)]

                    
                    self.game_manager.actualizar_enemigos(lista_enemigos)
                    self.game_manager.scenes["game"] = GameScene(self.game_manager)
                    self.game_manager.change_scene("game")
        
    
    def render(self):
        
        self.game_manager.ventana.fill(c.COLOR_BG)
        f=len(self.esquinas)
        if f<4:
            dibujar_selec_esquinas(self.game_manager.ventana,self.fantasmas[f],len(self.esquinas)+1,self.esquinas, ruta_fuente)
    
        
    
    
          
            


        
                
        
        


        
        
    
    
    
    