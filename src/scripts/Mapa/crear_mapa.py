import pygame
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import constantes as c
from data_structures.character.enemy_data_type import Enemigo 
from data_structures.character.player_data_type import Jugador 
from data_structures.map.tile_data_type import Tile

def crear_mapa(matriz, ventana, tipos_enemigos: list[tuple[str, tuple[int, int]]]):
    lista_entidades=[]
    lista_personajes=[]
    posiciones_iniciales_fantasmas=[(12, 13), (12, 15), (15, 13), (15,15)]
    indice_enemigo=0
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j]=="X":
                pared=Tile((j*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2,i*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2),True,"pacman_tp/assets/imagenes/items/pared.png",True, c.TAMAÑO_PARED)
                lista_entidades.append(pared)
            elif matriz[i][j]==".":
                pallet=Tile((j*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2,i*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2),True,"pacman_tp/assets/imagenes/items/pellet_pequeño.png",False, c.TAMAÑO_PARED//5)
                pallet.place_pellet()
                lista_entidades.append(pallet)
            elif matriz[i][j]=="o":
                power_pellet=Tile((j*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2,i*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2),True,"pacman_tp/assets/imagenes/items/pellet_grande.png",False, c.TAMAÑO_PARED//2)
                power_pellet.place_power_pellet()
                lista_entidades.append(power_pellet)
            elif matriz[i][j]=="P":
                jugador=Jugador((j*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2,i*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2), True, "pacman", "derecha", c.TAMAÑO_PARED)
                lista_personajes.append(jugador)
            elif matriz[i][j]=="G" and indice_enemigo < len(tipos_enemigos):

                target_inicial=(tipos_enemigos[indice_enemigo][1][0]*c.TAMAÑO_PARED + c.TAMAÑO_PARED//2,tipos_enemigos[indice_enemigo][1][1]*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2)
                pos=(posiciones_iniciales_fantasmas[indice_enemigo][0]*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2, posiciones_iniciales_fantasmas[indice_enemigo][1]*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2)
                # ATENCION! => se debe implementar logica de maximos fantasmas y spawnear en pos_inicial     <<< cambio importante
                enemigo=Enemigo(pos,True,tipos_enemigos[indice_enemigo][0],c.TAMAÑO_PARED, "idle", pos_inicial=target_inicial, state="reaparicion")
                lista_personajes.append(enemigo)
                indice_enemigo+=1

            else:
                pared=Tile((j*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2,i*c.TAMAÑO_PARED+ c.TAMAÑO_PARED//2),True,"pacman_tp/assets/imagenes/items/pasillo.png",False, c.TAMAÑO_PARED)
                lista_entidades.append(pared)


    return lista_entidades+lista_personajes