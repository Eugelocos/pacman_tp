import pygame
from funciones import escalar_img
import constantes as c   

#skin del pj
animaciones=[]
for i in range(4):
    img=pygame.image.load(f"assets//images//characters//player//player_{i}.PNG")
    img=escalar_img(img,c.ESCALA_JUGADOR)
    animaciones.append(img)
    
