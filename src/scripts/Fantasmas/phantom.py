import pygame
import sys
import os
import random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import constantes as c
from scripts.Utils.utilidades_colision import es_pared_en_celda, es_target_en_celda


def decidir_movimiento(jugador, fantasma, game_manager) -> tuple[int, int]:
    """Decide la siguiente direccion de movimiento del fantasma.

    Si el fantasma esta centrado en una celda y cambio de celda, calcula 
    la nueva direccion segun su estado (asustado o normal). En estado 
    asustado elige una direccion aleatoria sin retroceder. En estado 
    normal calcula el target y la direccion hacia el.

    Args:
        jugador (Jugador): Referencia al jugador (PacMan).
        fantasma (Enemigo): El fantasma que se esta moviendo.
        game_manager (GameManager): Referencia al administrador del juego.

    Returns:
        tuple[int, int]: La siguiente direccion de movimiento (dx, dy). 
                         (0, -1) arriba, (0, 1) abajo, (-1, 0) izquierda, 
                         (1, 0) derecha. Si no hay cambio, retorna la 
                         direccion actual.
    """
    grilla=game_manager.grid_manager
    escena=game_manager.scenes[game_manager.current_scene]
    centro = (fantasma.rect.centerx, fantasma.rect.centery)
    

    celda = grilla.world_to_grid(centro)
    centro_celda = grilla.grid_to_world(celda)

    centrado = (
        abs(centro_celda[0] - centro[0]) <= 2 and
        abs(centro_celda[1] - centro[1]) <= 2
    )

    if centrado  and celda != fantasma.ultima_celda:

        fantasma.ultima_celda = celda

        # logica de decision random
        posibles_estados=["asustado","asustado_parpadeando"]
        if fantasma.state in posibles_estados:
            direcciones_totales = [(0,-1), (0,1), (-1,0), (1,0)]
            direccion_opuesta = (fantasma.direction[0] * -1, fantasma.direction[1] * -1)
            direcciones_posibles=[]
            for d in direcciones_totales:
                if d!=direccion_opuesta and not es_pared_en_celda(celda,d,escena,fantasma):
                    direcciones_posibles.append(d)
                    
            if direcciones_posibles:
                return random.choice(direcciones_posibles)
            else:
                return direccion_opuesta
        
        # logica de decision no random 
        target = decidir_target(jugador, fantasma, escena)
        fantasma.target = target
        if es_target_en_celda(fantasma, target, escena):
            manejar_llegada_al_target(fantasma, escena)
        return decidir_direccion(fantasma, target, escena)

    return fantasma.direction

def decidir_target(jugador, fantasma, escena: object) -> tuple[int, int]:
    """Determina la celda objetivo (target) hacia donde el fantasma debe dirigirse.

    El target varia segun el estado del fantasma (muerto, en casa, scatter, chase)
    y su tipo (rojo, rosa, cyan, naranja, violeta, verde). Cada fantasma tiene
    un comportamiento unico:
    - Rojo: Apunta directamente al jugador.
    - Rosa: Apunta 4 celdas por delante del jugador.
    - Cyan: Usa un punto de referencia a 2 celdas del jugador y duplica 
            la distancia desde el fantasma rojo.
    - Naranja: Cambia entre ir al jugador o a su esquina segun la distancia.
    - Verde: Elige aleatoriamente a otro fantasma como victima y lo persigue en modo Chase, en modo Scatter persigue al jugador.
    - Violeta: Se mueve a una posicion kamikaze aleatoria fuera de la zona segura.

    Args:
        jugador (Jugador): Referencia al jugador (PacMan).
        fantasma (Enemigo): El fantasma que se esta moviendo.
        escena (object): Referencia a la escena actual (GameScene).

    Returns:
        tuple[int, int]: Representa el target en posicion discretizada (en grilla, no en pixeles).
                            Valores posibles: 
                                - (13, 11): Si esta en la ghost house, se utiliza para que puedan salir de la ghost house.
                                - (13, 14): Casa de fantasma (estado muerto).
                                - pos_inicial: Esquina del fantasma (modo Scatter).
                                - celda_jugador: Posicion del jugador
                                - Coordenada calculada segun la logica de cada fantasma
    """
    target = None
    celda_jugador = escena.game_manager.grid_manager.world_to_grid((jugador.rect.centerx, jugador.rect.centery))
    if fantasma.state =="muerto":
        target = (13, 14)
    elif fantasma.esta_en_casa:
        target = (13, 11)
    elif fantasma.nombre_enemigo=="fantasma_violeta":
                if not hasattr(fantasma, 'destino_kamikaze'):
                    celldas_validas = escena.game_manager.celdas_pasillo
                    celdas_seguras = []
                    for celda in celldas_validas:
                        if not (12 <= celda[1] <= 16 and 10 <= celda[0] <= 17):
                            celdas_seguras.append(celda)
                    
                    if celdas_seguras:
                        fantasma.destino_kamikaze = random.choice(celdas_seguras)
                    else:
                        fantasma.destino_kamikaze = celda_jugador 

                target = fantasma.destino_kamikaze
    else:

        if fantasma.state == "scatter":
            if fantasma.nombre_enemigo == "fantasma_verde":
                target = celda_jugador
            else:
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
            elif fantasma.nombre_enemigo == "fantasma_verde":
                tiempo_actual = pygame.time.get_ticks()
                
                if not hasattr(fantasma, 'victima') or not hasattr(fantasma, 'tiempo_cambio_victima') or (tiempo_actual - fantasma.tiempo_cambio_victima > 8000):
                                        
                    fantasmas_disponibles=[]
                    for entity in escena.game_manager.entities:
                        if hasattr(entity, 'nombre_enemigo') and entity != fantasma:
                            fantasmas_disponibles.append(entity)
                        
                    if fantasmas_disponibles:
                        fantasma.victima = random.choice(fantasmas_disponibles)
                        fantasma.tiempo_cambio_victima = tiempo_actual  
                    else:
                        fantasma.victima = None

                if hasattr(fantasma, 'victima') and fantasma.victima is not None:
                    centro_victima = (fantasma.victima.rect.centerx, fantasma.victima.rect.centery)
                    target = escena.game_manager.grid_manager.world_to_grid(centro_victima)
                else:
                    target = celda_jugador
            elif fantasma.nombre_enemigo == "fantasma_violeta":
                        if not hasattr(fantasma, 'destino_kamikaze'):
                            celdas_validas = escena.game_manager.celdas_pasillo
                            celdas_seguras = []
                            for celda in celdas_validas:
                                if not (12 <= celda[1] <= 16 and 10 <= celda[0] <= 17):
                                    celdas_seguras.append(celda)
                            
                            if celdas_seguras:
                                fantasma.destino_kamikaze = random.choice(celdas_seguras)
                            else:
                                fantasma.destino_kamikaze = celda_jugador

                        target = fantasma.destino_kamikaze
        else:
            target = (4,11) 
    return target

def decidir_direccion(fantasma, target: tuple[int, int], escena: object) -> tuple[int, int]:
    """Decide la mejor direccion para el fantasma hacia el target.

    Calcula la direccion que minimiza la distancia al target, evitando
    la direccion opuesta a la actual y evitando paredes. Penaliza movimientos
    que entran en la casa de fantasmas.

    Args:
        fantasma: El fantasma que se esta moviendo.
        target: Tupla (x, y) con la posicion objetivo en coordenadas de grilla.
        escena: Referencia a la escena actual (GameScene).

    Returns:
        tuple[int, int]: La siguiente direccion de movimiento (dx, dy). 
                         (0, -1) arriba, (0, 1) abajo, (-1, 0) izquierda, 
                         (1, 0) derecha. Si no hay cambio, retorna la 
                         direccion actual.
    """
    direcciones_totales=[(0,-1), (0,1), (-1,0), (1,0)]
    direccion_opuesta=(fantasma.direction[0]*-1, fantasma.direction[1]*-1)
    centro_gxy=escena.game_manager.grid_manager.world_to_grid((fantasma.rect.centerx, fantasma.rect.centery))
    direccciones_posibles=[dir for dir in direcciones_totales if dir!=direccion_opuesta and not es_pared_en_celda(centro_gxy, dir, escena,fantasma)]
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
                distancia *= 999    # numero arbitrario para penalizar el camino si es por dentro de la ghost house

        if distancia<candidato[1]:
            candidato=(direccion_posible, distancia)
    
    return candidato[0]



def manejar_llegada_al_target(fantasma, escena: object):
    """Ejecuta logica especial cuando un fantasma llega a su target.

    Casos especiales:
    - Si el fantasma estaba en casa: sale de ella.
    - Si el fantasma estaba muerto: revive y vuelve a casa.
    - Si es el fantasma violeta y no esta explotando: activa carga de explosion.

    Args:
        fantasma: El fantasma que se esta llego al target.
        escena: Referencia a la escena actual (GameScene).
    """
    tiempo=pygame.time.get_ticks()
    if fantasma.esta_en_casa:
        fantasma.esta_en_casa=False
    elif fantasma.state=="muerto":
        fantasma.state="scatter"
        fantasma.velocidad=c.VELOCIDAD_BASE*0.75*c.MULTIPLICADOR_VELOCIDAD_ENEMIGOS[fantasma.nombre_enemigo]
        fantasma.esta_en_casa=True
    elif fantasma.nombre_enemigo == "fantasma_violeta" and fantasma.state != "explotando":
        fantasma.state = "cargando_explosion" 
        fantasma.velocidad = 0
        fantasma.tiempo_inicio_carga = pygame.time.get_ticks()
        escena.sonido_pre_explosion.play()
        
        
def obtener_fantasma_por_tipo(escena: object, tipo_buscado: str) -> object|None:
    """Helper que obtiene la instancia de la clase Enemigo con el atributo nombre_enemigo especificado

    Args:
        escena (object): Referencia a la escena actual (GameScene).
        tipo_buscado (str): Nombre del enemigo del cual se requiere su Instancia.

    Returns:
        Enemigo|None: La instancia del enemigo que coincide con el tipo buscado, si no existe None
    """
    for entity in escena.game_manager.entities:
        if hasattr(entity, 'nombre_enemigo') and entity.nombre_enemigo == tipo_buscado:
            return entity
    return None
    
def distancia_euclideana(pos_a: tuple[int, int], pos_b: tuple[int, int]) -> int|float:
    """Obtiene la distancia euclideana entre A y B (sqrt((pos_a[0] - pos_b[0])^2 + (pos_a[1] - pos_b[1])^2))

    Args:
        pos_a (tuple[int, int]): Posicion de A en pixeles, no grilla
        pos_b (tuple[int, int]): Posicion de B en pixeles, no grilla

    Returns:
        int|float: La distancia euclideana entre A y B
    """
    pos_a_vector=pygame.Vector2(pos_a)
    pos_b_vector=pygame.Vector2(pos_b)
    distancia=pos_a_vector.distance_to(pos_b_vector)

    return distancia