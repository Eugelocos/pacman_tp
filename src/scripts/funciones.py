import os
import pygame
from scripts import constantes as c

def nombres_carpetas(directorio):
    return os.listdir(directorio)

#escalar imagen
def escalar_img(imagen, escala):
    w=imagen.get_width()
    h=imagen.get_height()
    nueva_imagen=pygame.transform.scale(imagen,(w*escala,h*escala))
    return nueva_imagen

#funcion para contar elementos
def contar_elementos(directorio):
    return len(os.listdir(directorio))


#dibujar paredes
def dibujar_paredes(matriz, ventana):
    """
    FIX 1: esta función solo dibuja las paredes, sin crear items ni personajes.
    Es la que se llama DENTRO del game loop en cada frame.
    """
    for x in range(len(matriz)):
        for y in range(len(matriz[x])):
            if matriz[x][y] == "X":
                pared = pygame.Rect(y*c.TAMAÑO_PARED, x*c.TAMAÑO_PARED, c.TAMAÑO_PARED, c.TAMAÑO_PARED)
                pygame.draw.rect(ventana, c.AZUL, pared)