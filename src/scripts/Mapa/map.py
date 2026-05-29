import pygame


#abrir el mapa 

with open("pacman_tp\src\scripts\Mapa\mapa.txt","r") as mapa:
    matriz_mapa=[]
    caracteres_validos=["X",".","P","o"," ","G","-","T"]
    for linea in mapa:
        l=linea.strip()
        for letra in l:
            if letra not in caracteres_validos:
                print("mapa invalido")
                break    
        matriz_mapa.append(l)

