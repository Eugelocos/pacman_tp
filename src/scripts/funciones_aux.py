"""
Módulo de Funciones Auxiliares (funciones_aux.py)

Este archivo contiene herramientas y funciones genéricas reutilizables en todos los codigos.
Incluye utilidades para manipulación de archivos, procesamiento de imágenes (escalado y transparencias),
y funciones de renderizado para textos y menús de la interfaz de usuario (UI).
"""

import os
import sys
import pygame
#Asegura que el directorio raíz del proyecto esté en el path para importar módulos correctamente
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import constantes as c

def nombres_carpetas(directorio):
    """
    Obtiene una lista con los nombres de todos los elementos dentro de una carpeta.

    Args:
        directorio (str): La ruta relativa o absoluta del directorio a inspeccionar.

    Returns:
        list: Lista de strings con los nombres de archivos y subcarpetas.
    """
    return os.listdir(directorio)

#escalar imagen
def escalar_img(imagen, escala):
    """
    Modifica el tamaño de una imagen multiplicando sus dimensiones por un factor de escala.

    Args:
        imagen (pygame.Surface): La imagen original de Pygame a escalar.
        escala (int | float): El multiplicador de tamaño (ej. 2 duplica el tamaño).

    Returns:
        pygame.Surface: La nueva imagen escalada.
    """
    w=imagen.get_width()
    h=imagen.get_height()
    nueva_imagen=pygame.transform.scale(imagen,(w*escala,h*escala))
    return nueva_imagen

#funcion para contar elementos
def contar_elementos(directorio):
    """
    Cuenta la cantidad total de archivos y/o carpetas dentro de un directorio.

    Args:
        directorio (str): La ruta del directorio a contar.

    Returns:
        int: Número total de elementos en el directorio.
    """
    return len(os.listdir(directorio))


def cargar_con_transparencia(ruta):
    """
    Carga una imagen desde el disco y convierte los píxeles de color negro puro (0,0,0)
    en píxeles totalmente transparentes. Ideal para cargar sprites con fondos negros.

    Args:
        ruta (str): La ruta hacia el archivo de imagen.

    Returns:
        pygame.Surface: La imagen optimizada para Pygame con canal Alpha (transparencia).
    """
    img = pygame.image.load(ruta).convert()  
    img.set_colorkey((0, 0, 0))             
    return img.convert_alpha()       


#dibujar texto
def dibujar_texto(texto, ventana, fuente, color, x, y, centrado=False):
    """
    Renderiza y dibuja una cadena de texto en la pantalla en las coordenadas indicadas.

    Args:
        texto (str): El string de texto que se desea mostrar en pantalla.
        ventana (pygame.Surface): La superficie/pantalla donde se dibujará el texto.
        fuente (pygame.font.Font): Objeto de fuente tipográfica de Pygame.
        color (tuple): Tupla RGB con el color del texto.
        x (int): Coordenada X donde se ubicará el texto.
        y (int): Coordenada Y donde se ubicará el texto.
        centrado (bool, optional): Si es True, (x,y) será el centro del texto. 
                                   Si es False, (x,y) será la esquina superior izquierda. Por defecto es False.

    Returns:
        pygame.Surface: La superficie generada que contiene únicamente el texto renderizado.
    """
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
    """
    Dibuja una "carta" o bloque de interfaz para seleccionar a un fantasma 
    en la pantalla de selección del menú (WelcomeScene / SelectFantasmas).

    Args:
        i (int): El índice numérico del fantasma dentro de la lista global c.FANTASMAS.
        ventana (pygame.Surface): La pantalla donde se renderiza la UI.
        seleccionados (list): Lista de tuplas con los datos de los fantasmas ya seleccionados por el jugador.
        ruta_fuente (str): Ruta al archivo de fuente .ttf para los textos.
    """
    ancho_actual, alto_actual = ventana.get_size()
    fuente= pygame.font.Font(ruta_fuente, 15)
    fuente_pequeña= pygame.font.Font(ruta_fuente, 10)
    fantasma = c.FANTASMAS[i]

    #Cálculos dinámicos de posición según el tamaño de la ventana
    espaciado_y = alto_actual * 1.5 // 16 #MARGEN 
    ancho_carta = 400
    bloque_x = (ancho_actual - ancho_carta) // 2

    x_circulo = bloque_x + 30
    x_numero = bloque_x + 60
    x_nombre = bloque_x + 120
    x_rectangulo = bloque_x

    #Posición Y inicial de la primera carta (25% del alto actual)
    y = alto_actual * 4 // 16 + i * espaciado_y  

    #Dibuja el círculo indicador de color, número, nombre y descripción
    pygame.draw.circle(ventana, fantasma[3], (x_circulo, y+7), 5, 0)
    dibujar_texto(f"{i+1}.", ventana,fuente,c.BLANCO,x_numero,y)
    dibujar_texto(f"{fantasma[1]}",ventana,fuente,fantasma[3],x_nombre,y)
    dibujar_texto(f"{fantasma[2]}",ventana,fuente_pequeña,c.BLANCO,x_nombre,y+17)
    
    #dibuja rectangulo que indica que el fantasma se selecciono
    if fantasma in seleccionados:
        pygame.draw.rect(ventana, c.BLANCO, (x_rectangulo, y, ancho_carta, alto_actual * 1.5 // 16),1)
        
#seleccionar esquinas
def dibujar_selec_esquinas(ventana,seleccionado,i,esquinas, ruta_fuente):
    """
    Dibuja el menú de interfaz para asignar una esquina inicial (pos_inicial)
    a un fantasma previamente seleccionado.

    Args:
        ventana (pygame.Surface): La pantalla principal donde se renderiza la UI.
        seleccionado (tuple): La metadata del fantasma actual al que se le está asignando esquina.
        i (int): El número de turno del fantasma (1 al 4) para mostrar en el título.
        esquinas (list): Lista de las coordenadas de las esquinas que ya fueron ocupadas.
        ruta_fuente (str): Ruta al archivo de fuente .ttf para los textos.
    """
    ancho_actual, alto_actual = ventana.get_size()
    fuente= pygame.font.Font(ruta_fuente, 10)
    fuente_pequeña= pygame.font.Font(ruta_fuente, 10)

    #Cálculos dinámicos de espaciado
    espaciado_y = alto_actual * 2 // 16          
    ancho_carta = 150
    bloque_x = (ancho_actual - ancho_carta) // 2


    nombre=seleccionado[1]
    color=seleccionado[3]
    
    #Título principal del menú
    dibujar_texto(f"Asigná una esquina a {nombre} ({i}/4):", ventana, fuente, color, ancho_actual//2, espaciado_y * 1, True)
    
    #Opciones de esquinas (coordenadas lógicas de grilla)
    opciones = [(0,0), (28,0), (0,31), (28,31)]
    nombres_esquinas = ["Superior izquierda", "Superior derecha", "Inferior izquierda", "Inferior derecha"]
    
    #Iteracion sobre cada opcion para dibujarla
    for n, (esquina, nombre_esquina) in enumerate(zip(opciones, nombres_esquinas), 1):
        #Si la esquina ya fue ocupada por otro fantasma, se muestra en gris (deshabilitada visualmente)
        if esquina in esquinas:
            color_numero = c.GRIS
        else:
            color_numero = c.BLANCO
        y = alto_actual * 4 // 16 + n * espaciado_y
        dibujar_texto(f"{n}. {nombre_esquina}", ventana, fuente_pequeña, color_numero, bloque_x-30, y-30)
    
        
    
    
          