"""
Módulo de Carga del Mapa (map.py)

Este script se encarga de leer el archivo de texto (mapa.txt) que usamos como 
plantilla para dibujar el nivel. Lo procesa renglón por renglón, valida que los 
caracteres sean los permitidos, y arma una lista (matriz) que después usa el 
GridManager para instanciar las paredes, pastillas y túneles.
"""

import pygame
import os


# LECTURA Y VALIDACIÓN DEL MAPA
#Armamos la ruta relativa/absoluta al archivo mapa.txt para que no tire error 
#si ejecutamos el juego desde otra carpeta.

ruta_mapa = os.path.join(os.path.dirname(__file__), "mapa.txt")
caracteres_validos=["X",".","P","o"," ","G","-","T"]
matriz_mapa=[]
try:
    with open(ruta_mapa, "r") as mapa:
        lineas = mapa.readlines()

        if not lineas:
            raise ValueError("El archivo esta vacio")
        
        largo_esperado = len(lineas[0].strip())
        for i, linea in enumerate(lineas):
            if len(linea.strip()) != largo_esperado:
                raise ValueError(f"La fila {i+1} tiene largo {len(linea.strip())}, se esperaba {largo_esperado}")
            
        tiene_casa = False
        tiene_pacman = False

        #recorremos el archivo de texto renglon por renglon
        for linea in lineas:
            l=linea.strip() #le sacamos los \n
            #revisa letra por letra para verificar que no haya caracteres raros
            for letra in l:
                if letra == "P":
                    if tiene_pacman:
                        raise ValueError("El archivo contiene multiples posiciones para PacMan")
                    else:
                        tiene_pacman = True
                if letra == "G":
                    tiene_casa = True
                if letra not in caracteres_validos:
                    raise ValueError("El archivo de texto contiene caracteres invalidos")    
            #se guarda el renglon limpio     
            matriz_mapa.append(l)
        if not tiene_pacman:
            raise ValueError("El mapa no contiene la posicion de PacMan (P)")
        if not tiene_casa:
            raise ValueError("El mapa no contiene la Ghost House (G)")
except FileNotFoundError:
    raise FileNotFoundError(f"No se encontro el archivo mapa.txt en {ruta_mapa}")
except Exception as e:
    print(f"Error al cargar el mapa: {e}")
    raise


