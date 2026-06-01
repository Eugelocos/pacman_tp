import pygame
import sys, os

ruta_actual = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ruta_actual)
import constantes as c
from scripts.funciones_aux import *
from scripts.Mapa.map import *
from scripts.ManagerGlobal.game_manager import GameManager


pygame.init()


#controlar el framerate
reloj=pygame.time.Clock()

corriendo=True

game_manager = GameManager()

while corriendo:
    
    reloj.tick(c.FPS)
    
    delta_time = reloj.get_time()

    eventos=pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            corriendo=False

    game_manager.update(delta_time, eventos)
    game_manager.render()
    
    

            
    
pygame.quit()
    
    