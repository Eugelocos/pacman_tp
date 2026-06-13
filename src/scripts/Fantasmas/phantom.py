import pygame
import sys
import os
import random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import constantes as c
from scripts.Utils.utilidades_colision import es_pared_en_celda, es_target_en_celda

def decidir_movimiento(jugador, fantasma, game_manager):
    
    grilla=game_manager.grid_manager
    escena=game_manager.scenes[game_manager.current_scene]
    centro = (fantasma.rect.centerx, fantasma.rect.centery)
    

    celda = grilla.world_to_grid(centro)
    centro_celda = grilla.grid_to_world(celda)

    centrado = (
        abs(centro_celda[0] - centro[0]) <= 2 and
        abs(centro_celda[1] - centro[1]) <= 2
    )

    if centrado:
        posibles_estados=["asustado","asustado_parpadeando"]
        if fantasma.state in posibles_estados:
            direcciones_totales = [(0,-1), (0,1), (-1,0), (1,0)]
            direccion_opuesta = (fantasma.direction[0] * -1, fantasma.direction[1] * -1)
            direcciones_posibles=[]
            for d in direcciones_totales:
                if d!=direccion_opuesta and not es_pared_en_celda(celda,d,escena):
                    direcciones_posibles.append(d)
                    
            if direcciones_posibles:
                return random.choice(direcciones_posibles)
            else:
                return direccion_opuesta
            
        target = decidir_target(jugador, fantasma, escena)
        fantasma.target = target
        if es_target_en_celda(fantasma, target, escena):
            manejar_llegada_al_target(fantasma, escena)
        return decidir_direccion(fantasma, target, escena)

    return fantasma.direction

def decidir_target(jugador, fantasma, escena: object):
    target = None
    celda_jugador = escena.game_manager.grid_manager.world_to_grid((jugador.rect.centerx, jugador.rect.centery))
    if fantasma.esta_en_casa:
        target = (13, 11)
    else:
        if fantasma.state=="scatter":
            target=fantasma.pos_inicial
        elif fantasma.state=="chase":
            if fantasma.nombre_enemigo=="fantasma_rojo":
                target=escena.game_manager.grid_manager.world_to_grid((jugador.rect.centerx, jugador.rect.centery))
            else:
                target = (4,11)

        elif fantasma.state =="muerto":
            target = (13, 11)
            

    return target

def decidir_direccion(fantasma, target, escena):
    direcciones_totales=[(0,-1), (0,1), (-1,0), (1,0)]
    direccion_opuesta=(fantasma.direction[0]*-1, fantasma.direction[1]*-1)
    centro_gxy=escena.game_manager.grid_manager.world_to_grid((fantasma.rect.centerx, fantasma.rect.centery))
    direccciones_posibles=[dir for dir in direcciones_totales if dir!=direccion_opuesta and not es_pared_en_celda(centro_gxy, dir, escena)]
    
    candidato=(direccciones_posibles[0],999999)
    for direccion_posible in direccciones_posibles:
        target_pxy=escena.game_manager.grid_manager.grid_to_world((target[0], target[1]))
        centro_nuevo=(fantasma.rect.centerx + c.TAMAÑO_PARED*direccion_posible[0], fantasma.rect.centery + c.TAMAÑO_PARED*direccion_posible[1])
        centro__nuevo_fantasma=pygame.Vector2(centro_nuevo)
        centro_target=pygame.Vector2(target_pxy)
        distancia=centro__nuevo_fantasma.distance_to(centro_target)

        if distancia<candidato[1]:
            candidato=(direccion_posible, distancia)
    
    return candidato[0]



def manejar_llegada_al_target(fantasma, escena):
    if fantasma.esta_en_casa:
        fantasma.esta_en_casa=False
    elif fantasma.state=="muerto":
        fantasma.state="scatter"
        fantasma.velocidad=c.VELOCIDAD_BASE*0.75
        fantasma.esta_en_casa=True
    