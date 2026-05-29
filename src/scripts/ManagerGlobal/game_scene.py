import pygame

class GameScene():
    def __init__(self, game_manager):
        self.game_manager=game_manager
        
    def get_player(self):
        """Busca y devuelve el jugador dentro de las entidades del juego.
    
        Returns:
        Player: El jugador si existe, o None si no se encontró.
    """
        for entity in self.game_manager.entities:
            if isinstance(entity, Player):
                return entity
                
        
    def update(self):
        jugador = self.get_player()
        entidad = self.game_manager.grid_manager.check_collision(jugador.pos, jugador.direccion, self.game_manager.entities)
        if isinstance(entidad, Tile) and entidad.es_pared:
            # detener al jugador
            ...

    def render(self, screen):
        pass
