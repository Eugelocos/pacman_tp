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
def dibujar_texto(texto, ventana, fuente, color, x, y, centrado=False):
    img = fuente.render(texto, True, color)
    rect = img.get_rect()
    
    if centrado:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    
    ventana.blit(img, rect)
    return img

#dibujar fantasma
def dibujar_fantasma(i,ventana,seleccionados, ruta_fuente):
    ancho_actual, alto_actual = ventana.get_size()
    fuente= pygame.font.Font(ruta_fuente, 18)
    fuente_pequeña= pygame.font.Font(ruta_fuente, 12)
    fantasma = c.FANTASMAS[i]

    espaciado_y = alto_actual * 2 // 16          # <<< MARGEN entre cartas

    ancho_carta = 430
    
    bloque_x = (ancho_actual - ancho_carta) // 2

    
    
    x_circulo = bloque_x + 40
    x_numero = bloque_x + 80
    x_nombre = bloque_x + 120
    x_rectangulo = bloque_x


    y = alto_actual * 4 // 16 + i * espaciado_y  # <<< POSICION INICIAL de la primera carta 25% de alto_actual

    pygame.draw.circle(ventana, fantasma[3], (x_circulo, y+20), 20, 0)
    dibujar_texto(f"{i+1}", ventana,fuente,c.BLANCO,x_numero,y)
    dibujar_texto(f"{fantasma[1]}",ventana,fuente,fantasma[3],x_nombre,y)
    dibujar_texto(f"{fantasma[2]}",ventana,fuente_pequeña,c.BLANCO,x_nombre,y+30)
    #dibujar rectangulo que indica que el fantasma se selecciono
    if fantasma in seleccionados:
        pygame.draw.rect(ventana, c.BLANCO, (x_rectangulo, y-20, ancho_carta, alto_actual * 2 // 16),1)
        
#seleccionar esquinas
def dibujar_selec_esquinas(ventana,seleccionado,i,esquinas, ruta_fuente):
    fuente= pygame.font.Font(ruta_fuente, 18)
    fuente_pequeña= pygame.font.Font(ruta_fuente, 12)
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
    
        
    
    
          