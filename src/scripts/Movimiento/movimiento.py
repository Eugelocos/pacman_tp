import pygame
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import constantes as c
from scripts.Utils.utilidades_colision import es_pared_en_celda
def manejar_movimiento(entidad, escena, delta_time=1):
    grilla = escena.game_manager.grid_manager
    delta_time = min(delta_time, 50)
    centro_x, centro_y = entidad.rect.centerx, entidad.rect.centery
    centro_gxy = grilla.world_to_grid((centro_x, centro_y))
    centro_celda_gxy = grilla.grid_to_world(centro_gxy)
    

    velocidad=round(entidad.velocidad * delta_time / 1000)

    direccion_aplicar=entidad.direction



    
    es_pared_siguiente_dir=es_pared_en_celda(centro_gxy, entidad.proxima_direccion, escena)
    if not es_pared_siguiente_dir:
        alineado=False
        if entidad.proxima_direccion[0]!=0:
            alineado=abs(centro_y-centro_celda_gxy[1])<velocidad+2
        else:
            alineado=abs(centro_x-centro_celda_gxy[0])<velocidad+2 

  
        if alineado:     
            direccion_aplicar=entidad.proxima_direccion
            if entidad.proxima_direccion[0]!=0:
                entidad.rect.centery=int(centro_celda_gxy[1])
            else:
                entidad.rect.centerx=int(centro_celda_gxy[0]) 
            
            centro_x, centro_y = entidad.rect.centerx, entidad.rect.centery
            centro_gxy = grilla.world_to_grid((centro_x, centro_y))
            centro_celda_gxy = grilla.grid_to_world(centro_gxy)



    es_pared = es_pared_en_celda(centro_gxy, direccion_aplicar, escena)
    if es_pared:
        alineado = False
        if direccion_aplicar[0]!=0:
            if abs(centro_x - centro_celda_gxy[0]) < velocidad + 2:
                alineado=True
        else:
            if abs(centro_y - centro_celda_gxy[1]) < velocidad + 2:
                alineado=True

        if alineado:
            entidad.rect.centery = centro_celda_gxy[1]
            entidad.rect.centerx = centro_celda_gxy[0]
            if entidad.es_jugador:
                entidad.direction = (0, 0)
            
            return
        
        if direccion_aplicar[0] > 0:
            entidad.rect.centerx = min(entidad.rect.centerx + velocidad, centro_celda_gxy[0])
        elif direccion_aplicar[0] < 0:
            entidad.rect.centerx = max(entidad.rect.centerx - velocidad, centro_celda_gxy[0])
        elif direccion_aplicar[1] > 0:
            entidad.rect.centery = min(entidad.rect.centery + velocidad, centro_celda_gxy[1])
        elif direccion_aplicar[1] < 0:
            entidad.rect.centery = max(entidad.rect.centery - velocidad, centro_celda_gxy[1])
        
        if entidad.direction != direccion_aplicar:
            entidad.direction = direccion_aplicar
            entidad.cambiar_sprite_por_direccion()
        return
    

    if entidad.direction != direccion_aplicar:
        entidad.direction = direccion_aplicar
        entidad.cambiar_sprite_por_direccion()

    x_previa, y_previa = entidad.rect.left, entidad.rect.top
    entidad.rect.top += velocidad * direccion_aplicar[1]
    if _choco_con_pared(entidad, grilla):
        entidad.rect.top = y_previa

    entidad.rect.x += velocidad * direccion_aplicar[0]
    if _choco_con_pared(entidad, grilla):
        entidad.rect.left = x_previa

    
    





def _choco_con_pared(entidad, grilla):
    for celda in grilla.grid:
        if hasattr(celda, "is_wall") and celda.is_wall:
            if entidad.rect.colliderect(celda.rect):
                return True
    return False

