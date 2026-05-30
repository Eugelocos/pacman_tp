import pygame
import os

#abrir el mapa 
ruta_mapa = os.path.join(os.path.dirname(__file__), "mapa.txt")
with open(ruta_mapa, "r") as mapa:
    matriz_mapa=[]
    caracteres_validos=["X",".","P","o"," ","G","-","T"]
    for linea in mapa:
        l=linea.strip()
        for letra in l:
            if letra not in caracteres_validos:
                print("mapa invalido")
                break    
        matriz_mapa.append(l)

