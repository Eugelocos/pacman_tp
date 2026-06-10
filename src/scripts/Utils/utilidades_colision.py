




def es_pared_en_celda(centro_gxy, direccion_aplicar, escena):
    grilla=escena.game_manager.grid_manager
    siguiente_celda_pos = grilla.grid_to_world((
        centro_gxy[0] + direccion_aplicar[0],
        centro_gxy[1] + direccion_aplicar[1]
    ))    
    siguiente_celda=grilla.get_cell_by_position(siguiente_celda_pos, escena.game_manager.entities)

    return siguiente_celda and hasattr(siguiente_celda, "is_wall") and siguiente_celda.is_wall
