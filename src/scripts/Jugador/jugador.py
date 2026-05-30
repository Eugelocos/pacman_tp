import pygame
from funciones_aux import escalar_img
import pacman_tp.src.constantes as c   

#skin del pj
animaciones=[]
for i in range(4):
    img=pygame.image.load(f"assets//images//characters//player//player_{i}.PNG")
    img=escalar_img(img,c.ESCALA_JUGADOR)
    animaciones.append(img)
    
