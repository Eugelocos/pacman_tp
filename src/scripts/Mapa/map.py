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
with open(ruta_mapa, "r") as mapa:
    matriz_mapa=[]
    #unicos caracteres validos
    caracteres_validos=["X",".","P","o"," ","G","-","T"]
    #recorremos el archivo de texto renglon por renglon
    for linea in mapa:
        l=linea.strip() #le sacamos los \n
        #revisa letra por letra para verificar que no haya caracteres raros
        for letra in l:
            if letra not in caracteres_validos:
                print("mapa invalido")
                break    
        #se guarda el renglon limpio     
        matriz_mapa.append(l)

