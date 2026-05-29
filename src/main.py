import sys
import os

# Esto busca la carpeta del archivo main.py y le dice a Python que busque ahí dentro
ruta_actual = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ruta_actual)

import pygame
from scripts import constantes as c
from scripts.funciones import *
from scripts.Mapa.map import *



pygame.init()

#crear y mostrar la ventana
ventana = pygame.display.set_mode((c.ANCHO_VENTANA,c.ALTO_VENTANA))
pygame.display.set_caption("PACMAN")


#controlar el framerate
reloj=pygame.time.Clock()

run=True

while run:
    
    reloj.tick(c.FPS)
    ventana.fill(c.COLOR_BG)
    
    dibujar_paredes(matriz_mapa, ventana)
    
    
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            run=False
            
    pygame.display.update()
    
pygame.quit()
    
    