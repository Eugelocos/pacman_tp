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
    if fantasma.state =="muerto":
        target = (15, 11)
    elif fantasma.esta_en_casa:
        target = (13, 11)
    else:
        if fantasma.state == "scatter":
            target = fantasma.pos_inicial
        elif fantasma.state =="chase":
            if fantasma.nombre_enemigo == "fantasma_rojo":
                target = celda_jugador
            elif fantasma.nombre_enemigo == "fantasma_amarillo":
                posicion_jugador = (jugador.rect.centerx, jugador.rect.centery)
                posicion_fantasma = (fantasma.rect.centerx, fantasma.rect.centery)
                distancia_a_jugador = round(distancia_euclideana(posicion_fantasma, posicion_jugador))

                if distancia_a_jugador < 8 * c.TAMAÑO_PARED:
                    target = fantasma.pos_inicial
                elif distancia_a_jugador >= 8 * c.TAMAÑO_PARED:
                    target = celda_jugador
            elif fantasma.nombre_enemigo == "fantasma_cian":
                fantasma_referencia = obtener_fantasma_por_tipo(escena, "fantasma_rojo")
                if not fantasma_referencia:
                    fantasmas_disponibles = [entity for entity in escena.game_manager.entities if hasattr(entity, 'nombre_enemigo')]
                    fantasma_referencia = random.choice(fantasmas_disponibles)
                
                posicion_fantasma_referencia = (fantasma_referencia.rect.centerx, fantasma_referencia.rect.centery)
                posicion_jugador = (jugador.rect.centerx, jugador.rect.centery)
                posicion_punto_referencia = (posicion_jugador[0] + jugador.direction[0]*2*c.TAMAÑO_PARED, posicion_jugador[1] + jugador.direction[1]*2*c.TAMAÑO_PARED)
                vector_punto_referencia = pygame.Vector2(posicion_punto_referencia)
                vector_fantasma_referencia = pygame.Vector2(posicion_fantasma_referencia)
                vector_diferencia = vector_punto_referencia - vector_fantasma_referencia
                posicion_objetivo = vector_fantasma_referencia + 2*vector_diferencia
                target = escena.game_manager.grid_manager.world_to_grid(posicion_objetivo)

            elif fantasma.nombre_enemigo == "fantasma_rosa":
                direccion_jugador = jugador.direction
                if direccion_jugador[1]==1:
                    target = celda_jugador[0]+4*direccion_jugador[0]-4, celda_jugador[1]+4*direccion_jugador[1]
                else:   
                    target = celda_jugador[0]+4*direccion_jugador[0], celda_jugador[1]+4*direccion_jugador[1]
            else:
                target = (4,11) # un target por defecto, no deberia pasar nunca que llegue aca
    return target

def decidir_direccion(fantasma, target, escena):
    direcciones_totales=[(0,-1), (0,1), (-1,0), (1,0)]
    direccion_opuesta=(fantasma.direction[0]*-1, fantasma.direction[1]*-1)
    centro_gxy=escena.game_manager.grid_manager.world_to_grid((fantasma.rect.centerx, fantasma.rect.centery))
    direccciones_posibles=[dir for dir in direcciones_totales if dir!=direccion_opuesta and not es_pared_en_celda(centro_gxy, dir, escena)]
    if not direccciones_posibles:
        return direccion_opuesta
    candidato=(direccciones_posibles[0],999999)
    for direccion_posible in direccciones_posibles:
        target_pxy=escena.game_manager.grid_manager.grid_to_world((target[0], target[1]))
        centro_nuevo=(fantasma.rect.centerx + c.TAMAÑO_PARED*direccion_posible[0], fantasma.rect.centery + c.TAMAÑO_PARED*direccion_posible[1])
        distancia = distancia_euclideana(centro_nuevo, target_pxy)
        celda_candidata = escena.game_manager.grid_manager.world_to_grid(centro_nuevo)

        if fantasma.state != "muerto":
            if 12 <= celda_candidata[1] <= 16 and 10 <= celda_candidata[0] <= 17:
                distancia *= 999

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
        
def obtener_fantasma_por_tipo(escena, tipo_buscado):
    for entity in escena.game_manager.entities:
        if hasattr(entity, 'nombre_enemigo') and entity.nombre_enemigo == tipo_buscado:
            return entity
    return None
    