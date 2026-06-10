import pygame
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import constantes as c
from scripts.Utils.utilidades_colision import es_pared_en_celda, es_target_en_celda

def decidir_movimiento(jugador, fantasma, game_manager):
    # Lógica para decidir la dirección del fantasma

    # se llamaria a:
    # self.cambiar_direccion(nueva_direccion)
    # donde nueva_direccion es una de las siguientes: "arriba", "abajo", "izquierda", "derecha"
    # la logica de decision dependera del tipo de fantasma ( self.nombre_enemigo ) y del estado del juego ( self.state )
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
        target = decidir_target(jugador, fantasma, escena)

        if es_target_en_celda(fantasma, target, escena):
            print(f"🎯 {fantasma.nombre_enemigo} llegó a {target}")
            manejar_llegada_al_target(fantasma, escena)
        return decidir_direccion(fantasma, target, escena)

    return fantasma.direction

def decidir_target(jugador, fantasma, escena):
    target=None
    if fantasma.esta_en_casa:
        target=(13, 11)
    else:
        if fantasma.state=="scatter":
            target=fantasma.pos_inicial
        elif fantasma.state=="chase":
            if fantasma.name=="fantasma_rojo":
                target=escena.game_manager.grid_manager.world_to_grid((jugador.rect.centerx, jugador.rect.centery))
            else:
                target=(13, 11)
        elif fantasma.state=="muerto":
            target=(13, 11)
            

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
        centro_target=pygame.Vector2((target[0], target[1]))
        distancia=centro__nuevo_fantasma.distance_to(centro_target)

        if distancia<candidato[1]:
            candidato=(direccion_posible, distancia)
    
    return candidato[0]



def manejar_llegada_al_target(fantasma, escena):
    if fantasma.esta_en_casa:
        fantasma.esta_en_casa=False
    # else:
    #   otros tipos de casos