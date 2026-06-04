import pygame
import sys, os

ruta_actual = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ruta_actual)
import constantes as c
from scripts.ManagerGlobal.game_manager import GameManager


pygame.init()
# controlar FPS (framerate)
reloj=pygame.time.Clock()

game_manager = GameManager()


# MAIN LOOP


corriendo=True
while corriendo:
    delta_time = reloj.tick(c.FPS)

    eventos=pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            corriendo=False
            
    game_manager.update(delta_time, eventos)
    game_manager.render()
    
    

# EXIT
pygame.quit()
    
    