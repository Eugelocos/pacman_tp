"""
Módulo de Escenas de Menú (menu_scene.py)

Acá se definen todas las pantallas previas al juego real:
1. WelcomeScene: La pantalla de inicio clásica de Pac-Man.
2. SelectFantasmas: Menú interactivo para elegir qué 4 fantasmas van a aparecer.
3. SelectEsquinas: Menú para asignarle a cada fantasma elegido su esquina de "Scatter".
"""

import pygame
import constantes as c 
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.funciones_aux import dibujar_texto,dibujar_fantasma,dibujar_selec_esquinas
from scripts.ManagerGlobal.game_scene import GameScene
from scripts.ManagerGlobal.escena import EscenaBase

#ruta para fuente retro
ruta_fuente = os.path.join("pacman_tp","assets", "fonts", "PressStart2P.ttf")

class WelcomeScene(EscenaBase): 
    """
    Pantalla principal del juego. Muestra el título, el High Score y 
    un texto parpadeante que invita a presionar ENTER.
    """
    click = None
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.milisegundos=c.PARPADEO #intervalo de titileo del texto
        self.texto=True #variable para saber si se dibuja el texto o se lo oculta
        self.tiempo=0
        
        #se carga el sonido una sola vez para no saturar la memoria
        if WelcomeScene.click is None:
            WelcomeScene.click = pygame.mixer.Sound(c.EFECTOS["click"])  

    def update(self,delta_time=0, eventos=None):
        """Maneja los inputs y el temporizador del parpadeo."""
        for event in eventos:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    WelcomeScene.click.play()
                    # Pasamos a la siguiente pantalla
                    self.game_manager.change_scene("select_fantasmas")
                    
        #Lógica del parpadeo del texto "Presiona ENTER"
        self.tiempo+=delta_time
        if self.tiempo>=self.milisegundos:
            self.tiempo=0
            self.texto=not self.texto # Invierte el estado (Visible <-> Invisible)
                                
    def render(self):
        """Dibuja todos los textos de la pantalla de bienvenida."""
        
        ancho_actual, alto_actual = self.game_manager.ventana.get_size()
        self.fuente_titulo = pygame.font.Font(ruta_fuente, 48)
        self.fuente_normal = pygame.font.Font(ruta_fuente, 15)

        self.game_manager.ventana.fill(c.COLOR_BG)
        
        # High Score - Título
        x = ancho_actual // 2
        y = alto_actual *  3 // 16
        dibujar_texto("HIGH SCORE:", self.game_manager.ventana, self.fuente_normal, c.BLANCO, x, y, True)

        # High Score - Numero
        x = ancho_actual // 2
        y = alto_actual *  4 // 16       
        dibujar_texto(str(self.game_manager.high_score),self.game_manager.ventana,self.fuente_normal, c.VERDE, x,y, True)

        # Título principal del juego
        x = ancho_actual // 2
        y = alto_actual *  8 // 16        
        dibujar_texto("PAC-MAN",self.game_manager.ventana,self.fuente_titulo, c.AMARILLO, x,y, True)

        # Texto parpadeante
        if self.texto: 
            x = ancho_actual // 2
            y = alto_actual * 11 // 16            
            dibujar_texto("Presiona ENTER para jugar",self.game_manager.ventana,self.fuente_normal, c.BLANCO, x,y, True)

        
    def on_enter(self):
        """Se ejecuta al entrar a esta escena. Resetea el parpadeo."""
        self.tiempo = 0
        self.texto = True
        self.game_manager.pausado = False


class SelectFantasmas(EscenaBase):
    """
    Pantalla donde el jugador elige 4 fantasmas distintos de una lista usando 
    las teclas del 1 al 6.
    """
    click = None
    error = None
    def __init__(self,game_manager):
        super().__init__(game_manager)
        
        self.seleccionados=[] # Lista que guarda los fantasmas elegidos
        self.fuente_titulos=pygame.font.Font(ruta_fuente, 15)
        
        if SelectFantasmas.click is None:
            SelectFantasmas.click = pygame.mixer.Sound(c.EFECTOS["click"])  

        if SelectFantasmas.error is None:
            SelectFantasmas.error = pygame.mixer.Sound(c.EFECTOS["error"])  

    def update(self,delta_time=0,eventos=None):
        """Maneja la selección de fantasmas con el teclado numérico."""
        for event in eventos:
            if event.type==pygame.KEYDOWN:
                # Diccionario para mapear teclas (1-6) a índices de la lista de fantasmas
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
                    
                    #logica de seleccion/deseleccion
                    if fantasma not in self.seleccionados:
                        if len(self.seleccionados)<4:
                            self.seleccionados.append(fantasma)
                        elif len(self.seleccionados)==4:
                            # Si ya hay 4, sacamos al primero más viejo (FIFO) y metemos el nuevo
                            self.seleccionados.pop(0)
                            self.seleccionados.append(fantasma)
                    elif fantasma in self.seleccionados:
                        # Si tocas uno que ya está, lo deseleccionás
                        self.seleccionados.remove(fantasma)
                if event.key==pygame.K_RETURN:
                    # Validamos que sí o sí haya 4 antes de continuar
                    if len(self.seleccionados)==4:
                        SelectFantasmas.click.play()
                        # Instanciamos la siguiente escena pasándole los fantasmas elegidos
                        self.game_manager.scenes["select_esquinas"]=SelectEsquinas(self.game_manager,self.seleccionados)
                        self.game_manager.change_scene("select_esquinas")
                    else:
                        SelectFantasmas.error.play() # Suena error si faltan fantasmas


    def render(self):
        """Dibuja la UI de selección y el contador."""
        ancho_actual, alto_actual = self.game_manager.ventana.get_size()
        self.game_manager.ventana.fill(c.COLOR_BG)
        x = ancho_actual // 2
        y = alto_actual *  2 // 16
        f=len(self.seleccionados) # variable que cambia el numero de fantasmas seleccionados
        
        #Título dinámico que avisa cuántos vas eligiendo
        dibujar_texto(f"Elegi 4 fantasmas [{f}/4]",self.game_manager.ventana,self.fuente_titulos, c.AMARILLO, x,y, True)
        
        #dibuja los 6 fantasmas en pantalla (con funcion auxiliar dibujar_fantasma)
        for i in range(6):
            dibujar_fantasma(i,self.game_manager.ventana,self.seleccionados, ruta_fuente)

    def on_enter(self):
        """Limpia la selección al entrar por si venimos de un "Volver" o reinicio."""
        self.seleccionados=[]

    def on_exit(self):
        pass

class SelectEsquinas(EscenaBase):
    """
    Pantalla para asignarle a cada fantasma previamente elegido su esquina destino 
    (su Target Tile durante el modo SCATTER).
    """
    efecto_jugar=None
    def __init__(self,game_manager, lista_fantasmas): 
        super().__init__(game_manager)   
        self.game_manager=game_manager
        self.fantasmas=lista_fantasmas # Recibe los 4 seleccionados de la escena anterior
        self.esquinas=[]
        self.fuente_titulos=pygame.font.Font(ruta_fuente, 20)
        self.fuente_subtitulos=pygame.font.Font(ruta_fuente, 10)
        self.fuente_normal=pygame.font.Font(ruta_fuente, 15)
 
        if SelectEsquinas.efecto_jugar is None:
            SelectEsquinas.efecto_jugar=pygame.mixer.Sound(c.EFECTOS["jugar"])  
    
    def update(self,delta_time=0,eventos=None):
        """Mapea las 4 esquinas del tablero a cada fantasma."""
        # Coordenadas grid fijas (X, Y) de las 4 esquinas del mapa
        sup_izq=(0,0)
        sup_der=(28,0)
        inf_izq=(0,31)
        inf_der=(28,31)
        for event in eventos:
            if event.type==pygame.KEYDOWN:
                # Asignamos esquinas sin permitir repetirla
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
                        
                # Cuando ya asignamos las 4 esquinas, arranca el juego!
                if len(self.esquinas)==4:
                    # Emparejamos cada fantasma con la esquina que le tocó en orden
                    lista_enemigos = [(fantasma[0], esquina) for fantasma, esquina in zip(self.fantasmas, self.esquinas)]

                    
                    self.game_manager.actualizar_enemigos(lista_enemigos)
                    # Creamos la escena principal del juego recién ahora con toda la data
                    self.game_manager.scenes["game"] = GameScene(self.game_manager)
                    self.game_manager.nivel=1
                    self.game_manager.change_scene("game")
        
    
    def render(self):
        """Muestra el progreso de asignación de esquinas."""
        self.game_manager.ventana.fill(c.COLOR_BG)
        f=len(self.esquinas)
        # Mientras falten esquinas por asignar, seguimos dibujando el menú
        if f<4:
            # Dibuja el fantasma actual y las esquinas disponibles
            dibujar_selec_esquinas(self.game_manager.ventana,self.fantasmas[f],len(self.esquinas)+1,self.esquinas, ruta_fuente)

    def on_enter(self):
        """Limpia las esquinas si volvemos a entrar a la escena."""
        self.esquinas=[]

    def on_exit(self):
        """Suena el ruidito justo antes de saltar a GameScene."""
        SelectEsquinas.efecto_jugar.play()
        pass
        
    
    
          
            


        
                
        
        


        
        
    
    
    
    