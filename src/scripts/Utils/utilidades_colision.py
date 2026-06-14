import pygame




def es_pared_en_celda(centro_gxy, direccion_aplicar, escena, entidad=None):
    grilla = escena.game_manager.grid_manager
    siguiente_celda_pos = grilla.grid_to_world((
        centro_gxy[0] + direccion_aplicar[0],
        centro_gxy[1] + direccion_aplicar[1]
    ))
    siguiente_celda = grilla.get_cell_by_position(siguiente_celda_pos, escena.game_manager.entities)

    if siguiente_celda is None:
        return False

    if hasattr(siguiente_celda, "is_wall") and siguiente_celda.is_wall:
        return True

    if hasattr(siguiente_celda, "es_puerta") and siguiente_celda.es_puerta:
        if entidad is None:
            return True  # sin contexto, bloqueamos por seguridad
        puede_pasar = not entidad.es_jugador and (entidad.esta_en_casa or entidad.state == "muerto")
        return not puede_pasar

    return False

def es_target_en_celda(fantasma, target, escena):
    grilla = escena.game_manager.grid_manager
    celda_actual = grilla.world_to_grid(
        (fantasma.rect.centerx, fantasma.rect.centery)
    )

    if celda_actual==target:
        return True
    return False
