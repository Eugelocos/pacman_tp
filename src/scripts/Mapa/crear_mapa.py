import pygame
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import constantes as c
from data_structures.character.enemy_data_type import Enemigo 
from data_structures.character.player_data_type import Jugador 
from data_structures.map.tile_data_type import Tile

def crear_mapa(matriz, ventana, tipos_enemigos: list[str]):
    lista_entidades=[]
    lista_personajes=[]
    indice_enemigo=0
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j]=="X":
                pared=Tile((j*c.TAMAÑO_PARED,i*c.TAMAÑO_PARED),True,"pacman_tp/assets/imagenes/items/pared.png",True, c.TAMAÑO_PARED)
                lista_entidades.append(pared)
            elif matriz[i][j]==".":
                #pun_peq=Item(j*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,i*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,1,[punto_pequeño])
                #grupo_items.add(pun_peq)
                pallet=Tile((j*c.TAMAÑO_PARED,i*c.TAMAÑO_PARED),True,"pacman_tp/assets/imagenes/items/pellet_pequeño.png",False, c.TAMAÑO_PARED//10)
                pallet.place_pellet()
                lista_entidades.append(pallet)
            elif matriz[i][j]=="o":
                power_pellet=Tile((j*c.TAMAÑO_PARED,i*c.TAMAÑO_PARED),True,"pacman_tp/assets/imagenes/items/pellet_grande.png",False, c.TAMAÑO_PARED//2)
                power_pellet.place_power_pellet()
                lista_entidades.append(power_pellet)
                #pun_gran=Item(j*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,i*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,2,[punto_grande])
                #grupo_items.add(pun_gran)
            elif matriz[i][j]=="P":
                jugador=Jugador((j*c.TAMAÑO_PARED,i*c.TAMAÑO_PARED), True, "pacman", "derecha", c.TAMAÑO_PARED)
                lista_personajes.append(jugador)
            elif matriz[i][j]=="G":

                #se debe implementar logica de maximos fantasmas y spawnear en pos_inicial
                enemigo=Enemigo((j*c.TAMAÑO_PARED,i*c.TAMAÑO_PARED),True,tipos_enemigos[indice_enemigo],c.TAMAÑO_PARED, "derecha")
                lista_personajes.append(enemigo)
                indice_enemigo+=1
                if indice_enemigo>=len(tipos_enemigos):
                    indice_enemigo=0

    return lista_entidades+lista_personajes