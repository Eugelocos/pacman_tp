import pygame
import sys, os

ruta_actual = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ruta_actual)
import constantes as c
from scripts.funciones_aux import *
from scripts.Mapa.map import *



pygame.init()

#crear y mostrar la ventana
ventana = pygame.display.set_mode((c.ANCHO_VENTANA,c.ALTO_VENTANA))
pygame.display.set_caption("PACMAN")


#controlar el framerate
reloj=pygame.time.Clock()

corriendo=True

while corriendo:
    
    reloj.tick(c.FPS)
    ventana.fill(c.COLOR_BG)
    
    dibujar_paredes(matriz_mapa, ventana)
    
    
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo=False
            
    pygame.display.update()
    
pygame.quit()
    
    