import pygame
import pacman_tp.src.scripts.constantes as c
from ...data_structures.character.enemy_data_type import Enemy 
from ...data_structures.character.player_data_type import Player 
from ...data_structures.map.tile_data_type import Tile

pelleto_pequeño=pygame.image.load("pacman_tp/assets/Items/pellet_pequeño.png").convert_alpha()
pellet_grande=pygame.image.load("pacman_tp/assets/Items/pellet_grande.png").convert_alpha()


def crear_mapa(matriz, ventana, tipos_enemigos: list[str]):
    lista_entidades=[]
    for x in range(len(matriz[0])):
        for y in range(len(matriz)):
            if matriz[x][y]=="X":
                pared=Tile((y*c.TAMAÑO_PARED,x*c.TAMAÑO_PARED),True,"pacman_tp/assets/images/items/pared.png",True)
                lista_entidades.append(pared)
                #pared=pygame.Rect(y*c.TAMAÑO_PARED,x*c.TAMAÑO_PARED,c.TAMAÑO_PARED,c.TAMAÑO_PARED)
                #pygame.draw.rect(ventana,c.AZUL,pared)
            elif matriz[x][y]==".":
                #pun_peq=Item(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,1,[punto_pequeño])
                #grupo_items.add(pun_peq)
                pallet=Tile((y*c.TAMAÑO_PARED,x*c.TAMAÑO_PARED),True,"pacman_tp/assets/images/items/pared.png",False)
                pallet.place_pellet()
                lista_entidades.append(pallet)
            elif matriz[x][y]=="o":
                power_pellet=Tile((y*c.TAMAÑO_PARED,x*c.TAMAÑO_PARED),True,"pacman_tp/assets/images/items/pared.png",False)
                power_pellet.place_power_pellet()
                lista_entidades.append(power_pellet)
                #pun_gran=Item(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,2,[punto_grande])
                #grupo_items.add(pun_gran)
            elif matriz[x][y]=="P":
                jugador=Player((y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2), True, "pacman_tp/assets/images/items/pared.png", "UP", 3)
                #jugador=Personaje(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,c.COLOR_PERSONAJE,animaciones) 
                lista_entidades.append(jugador)
            elif matriz[x][y]=="G":
                #crear lista de enemigos
                enemigos=[Enemy((y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2),True,f"pacman_tp/assets/images/{tipos_enemigos[i]}/{tipos_enemigos[i]}_1.png",tipos_enemigos[i], "IDLE", None) for i in range(4)]
                for enemigo in enemigos:
                    lista_entidades.append(enemigo)
        

    return lista_entidades