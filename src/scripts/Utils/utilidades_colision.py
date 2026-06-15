"""
Módulo de Utilidades de Colisión (utilidades_colision.py)

Acá separamos las funciones lógicas para calcular colisiones anticipadas en la grilla.
Sirve para preguntar "si me muevo para allá, ¿choco?" sin tener que mover 
realmente al personaje, manteniendo el código de movimiento mucho más limpio.
"""

import pygame

def es_pared_en_celda(centro_gxy, direccion_aplicar, escena, entidad=None):
    """
    Se fija si en la próxima celda a la que te querés mover hay una pared o una puerta.
    Tiene la lógica especial para que Pac-Man rebote en la puerta de la Ghost House, 
    pero los fantasmas puedan pasar si están muertos o recién salen.

    Args:
        centro_gxy (tuple): Tupla (x, y) con la celda actual en la grilla.
        direccion_aplicar (tuple): Tupla (x, y) con el vector de dirección (ej: (0, -1)).
        escena (EscenaBase): La escena actual, para poder acceder al grid_manager.
        entidad (Personaje, opcional): El personaje que se quiere mover. Lo usamos para saber si es Pac-Man o un fantasma.

    Returns:
        bool: True si hay un obstáculo que bloquea el paso, False si el camino está libre.
    """
    grilla = escena.game_manager.grid_manager
    
    #Calculamos cuál sería la próxima celda sumando la posición actual y la dirección
    siguiente_celda_pos = grilla.grid_to_world((
        centro_gxy[0] + direccion_aplicar[0],
        centro_gxy[1] + direccion_aplicar[1]
    ))
    
    #Buscamos qué objeto hay físicamente en esa celda
    siguiente_celda = grilla.get_cell_by_position(siguiente_celda_pos, escena.game_manager.entities)

    #Si por algún motivo nos salimos del mapa, no hay pared (los túneles)
    if siguiente_celda is None:
        return False

    #Choca contra paredes normales
    if hasattr(siguiente_celda, "is_wall") and siguiente_celda.is_wall:
        return True 

    #Lógica de la puerta de la Ghost House
    if hasattr(siguiente_celda, "es_puerta") and siguiente_celda.es_puerta:
        if entidad is None:
            return True  # sin contexto, bloqueamos por seguridad
        
        #Solo dejamos pasar a la entidad si NO es Pac-Man, y además el fantasma
        #está saliendo de casa o está volviendo muerto (en forma de ojos).
        puede_pasar = not entidad.es_jugador and (entidad.esta_en_casa or entidad.state == "muerto")
        
        #Invertimos el booleano: si NO puede pasar, devolvemos True (es decir, funciona como pared)
        return not puede_pasar

    return False

def es_target_en_celda(fantasma, target, escena):
    """
    Comprueba si el fantasma ya pisó la celda exacta que tenía como objetivo.
    Muy útil para la lógica de navegación (pathfinding).

    Args:
        fantasma (Enemigo): El objeto del fantasma que se está moviendo.
        target (tuple): Tupla (x, y) de la celda de la grilla a la que tiene que llegar.
        escena (EscenaBase): La escena actual para usar las herramientas de la grilla.

    Returns:
        bool: True si el fantasma ya llegó a la celda objetivo, False si le falta.
    """
    grilla = escena.game_manager.grid_manager
    
    #en que celda esta parado el fantasma? 
    celda_actual = grilla.world_to_grid(
        (fantasma.rect.centerx, fantasma.rect.centery)
    )

    if celda_actual==target:
        return True
    return False
