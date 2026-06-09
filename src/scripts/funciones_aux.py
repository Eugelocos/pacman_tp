import os
import sys
import pygame
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import constantes as c

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


def cargar_con_transparencia(ruta):
    img = pygame.image.load(ruta).convert()  
    img.set_colorkey((0, 0, 0))             
    return img.convert_alpha()       


#dibujar texto
def dibujar_texto(texto, ventana , fuente, color, x, y):
    img=fuente.render(texto, True, color)
    ventana.blit(img, (x, y)) 
    return img

#dibujar fantasma
def dibujar_fantasma(fantasma,i,ventana,seleccionados):
    fuente= pygame.font.SysFont("Courier", 30)
    fuente_pequeña= pygame.font.SysFont("Courier", 20)
    x_circulo = 180
    x_numero = 210
    x_nombre = 240
    x_rectangulo=100
    espaciado = 100
    y = 100 + i * espaciado
    pygame.draw.circle(ventana, fantasma[3], (x_circulo, y+20), 20, 0)
    dibujar_texto(f"{i+1}", ventana,fuente,c.BLANCO,x_numero,y)
    dibujar_texto(f"{fantasma[1]}",ventana,fuente,fantasma[3],x_nombre,y)
    dibujar_texto(f"{fantasma[2]}",ventana,fuente_pequeña,c.BLANCO,x_nombre,y+30)
    #dibujar rectangulo que indica que el fantasma se selecciono
    if fantasma in seleccionados:
        pygame.draw.rect(ventana, c.BLANCO, (x_rectangulo, y-20, 700, 80),1)
        
#seleccionar esquinas
def dibujar_selec_esquinas(ventana,seleccionado,i,esquinas):
    fuente= pygame.font.SysFont("Courier", 30)
    fuente_pequeña= pygame.font.SysFont("Courier", 25)
    x=100
    y=20
    nombre=seleccionado[1]
    color=seleccionado[3]
    dibujar_texto(f"Asigná una esquina a {nombre} ({i}/4):",ventana,fuente,color,x,y)
    opciones = [(0,0), (28,0), (0,31), (28,31)]
    nombres_esquinas = ["Superior izquierda", "Superior derecha", "Inferior izquierda", "Inferior derecha"]
    for n, (esquina, nombre_esquina) in enumerate(zip(opciones, nombres_esquinas), 1):
        if esquina in esquinas:
            color_numero = c.GRIS
        else:
            color_numero = c.BLANCO
        dibujar_texto(f"{n}. {nombre_esquina}", ventana, fuente_pequeña, color_numero, x+150, y+50+(n*100))
    
        
    
    
          