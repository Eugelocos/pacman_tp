from funciones import nombres_carpetas,escalar_img,contar_elementos
import constantes as c 
import pygame

#cargar imagenes fantasmas

directorio_enemigos="pacman_tp//assets//images//characters//enemies"
tipo_enemigos=nombres_carpetas(directorio_enemigos)
animaciones_enemigos=[]
for eni in tipo_enemigos:
    lista_temp=[]
    ruta_temp=f"assets//images//characters//enemies//{eni}"
    num_animaciones=contar_elementos(ruta_temp)
    for i in range(num_animaciones):
        img_enemigo=pygame.image.load(f"{ruta_temp}//{eni}_{i+1}.png").convert_alpha()
        img_enemigo=escalar_img(img_enemigo,c.ESCALA_ENEMIGOS)
        lista_temp.append(img_enemigo)
    animaciones_enemigos.append(lista_temp)