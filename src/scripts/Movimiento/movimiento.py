import pygame
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import constantes as c

def manejar_movimiento(entidad, escena, direccion, delta_time=1):
    x, y = getattr(entidad, 'rect').x, getattr(entidad, 'rect').y
    proxima_direccion = getattr(entidad, 'proxima_direccion', None)
    colision = escena.game_manager.grid_manager.check_collision((x, y), proxima_direccion, escena.game_manager.entities)
    es_pared = colision is not None and hasattr(colision, 'is_wall') and colision.is_wall
    
    if not es_pared:
        entidad.rect.x = int(x + direccion[0] * entidad.velocidad * delta_time / 1000)
        entidad.rect.y = int(y + direccion[1] * entidad.velocidad * delta_time / 1000)
    else:
        entidad.direccion=(0,0)
        entidad.proxima_direccion=(0,0)

