"""
Módulo de Creación del Mapa (crear_mapa.py)

Acá agarramos la matriz de texto cruda (las letritas que leímos del .txt) 
y la transformamos en objetos reales de Pygame. Básicamente instanciamos 
las paredes, los pellets, el Pac-Man y los fantasmas en sus coordenadas exactas.
"""

import pygame
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import constantes as c
from data_structures.character.enemy_data_type import Enemigo 
from data_structures.character.player_data_type import Jugador 
from data_structures.map.tile_data_type import Tile

def crear_mapa(matriz, ventana, tipos_enemigos: list[tuple[str, tuple[int, int]]]):
    """
    Recorre la matriz del mapa casillero por casillero y genera el objeto 
    correspondiente según la letra que encuentre ('X' para pared, 'P' para jugador, etc.).

    Args:
        matriz (list[str]): La lista de strings que representa el mapa (ej: ["XXXX", "X..X"]).
        ventana (pygame.Surface): La superficie donde se va a dibujar (actualmente sin uso directo acá, pero útil para escalados futuros).
        tipos_enemigos (list): Lista de tuplas con los fantasmas que eligió el jugador 
                               y las coordenadas de sus esquinas (target_inicial).

    Returns:
        tuple: Devuelve dos cosas. 
               1. Una lista gigante con TODOS los sprites (entidades y personajes) listos para el Group.
               2. Una lista de tuplas con las coordenadas (x,y) de todas las celdas que son pasillo 
                  (súper necesario para el kamikaze).
    """
    lista_entidades=[]
    lista_personajes=[]
    celdas_pasillo=[] #lista para pasarle al kamikaze asi sabe donde puede explotar
    # Coordenadas fijas en la grilla donde aparecen los fantasmas (Adentro de la Ghost House)
    posiciones_iniciales_fantasmas=[(12, 13), (12, 15), (15, 13), (15,15)]
    indice_enemigo=0
    
    # Recorremos fila por fila (i) y columna por columna (j)
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
    
            #j*c.TAMAÑO_PARED nos da el borde superior izquierdo de la celda.
            #Le sumamos la mitad (c.TAMAÑO_PARED // 2) para clavar el objeto justo en el centro.
            
            if matriz[i][j]=="X": #pared solida 
                pared=Tile((j*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2,i*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2),True,"pacman_tp/assets/imagenes/items/pared.png",True, c.TAMAÑO_PARED)
                lista_entidades.append(pared)
            elif matriz[i][j]=="-": #puerta de la ghost house que altera comportamiento segun entidad
                puerta=Tile((j*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2,i*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2),True,"pacman_tp/assets/imagenes/items/puerta.png",False, c.TAMAÑO_PARED)
                puerta.es_puerta = True
                lista_entidades.append(puerta)
            else: #si no es pared ni puerta, es un lugar donde el kamikaze puede ir a explotar
                celdas_pasillo.append((j, i))
                if matriz[i][j]==".": #puntito
                    pallet=Tile((j*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2,i*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2),True,"pacman_tp/assets/imagenes/items/pellet_pequeño.png",False, c.TAMAÑO_PARED//5)
                    pallet.place_pellet()
                    lista_entidades.append(pallet)
                elif matriz[i][j]=="o": #power pellet
                    power_pellet=Tile((j*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2,i*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2),True,"pacman_tp/assets/imagenes/items/pellet_grande.png",False, c.TAMAÑO_PARED//2)
                    power_pellet.place_power_pellet()
                    lista_entidades.append(power_pellet)
                elif matriz[i][j]=="P": #pac man 
                    jugador=Jugador((j*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2,i*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2), True, "pacman", "idle", c.TAMAÑO_PARED)
                    lista_personajes.append(jugador)
                elif matriz[i][j]=="T": #celda tunel para teletransportar
                    transportador=Tile((j*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2,i*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2),True,"pacman_tp/assets/imagenes/items/pasillo.png",False, c.TAMAÑO_PARED)
                    lista_entidades.append(transportador)
                    transportador.is_tunnel = True
                elif matriz[i][j]=="G" and indice_enemigo < len(tipos_enemigos): 
                    # Spawneamos un fantasma. 
                    # Extraemos a qué esquina le toca ir según lo que eligió el jugador en el menú
                    target_inicial = tipos_enemigos[indice_enemigo][1]
                    # Le asignamos una de las 4 posiciones fijas de la Ghost House
                    x_ghost = posiciones_iniciales_fantasmas[indice_enemigo][0] * c.TAMAÑO_PARED + c.TAMAÑO_PARED // 2
                    y_ghost = posiciones_iniciales_fantasmas[indice_enemigo][1] * c.TAMAÑO_PARED + c.TAMAÑO_PARED // 2
                    pos = (x_ghost, y_ghost)
                    
                    enemigo=Enemigo(pos,True,tipos_enemigos[indice_enemigo][0],c.TAMAÑO_PARED, "idle", pos_inicial=target_inicial, state="scatter")
                    lista_personajes.append(enemigo)
                    indice_enemigo+=1
                
                else:
                    # Si es un espacio vacío (' '), le ponemos el tile de pasillo negro de fondo
                    pared=Tile((j*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2,i*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2),True,"pacman_tp/assets/imagenes/items/pasillo.png",False, c.TAMAÑO_PARED)
                    lista_entidades.append(pared)

# Devolvemos todos los sprites juntos en una sola lista, más la lista de celdas caminables para el kamikaze
    return lista_entidades+lista_personajes,celdas_pasillo