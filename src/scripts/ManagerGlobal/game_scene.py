import pygame
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import constantes as c
from data_structures.character.enemy_data_type import Enemigo
from data_structures.map.tile_data_type import Tile
from data_structures.character.player_data_type import Jugador
from scripts.Movimiento.movimiento import manejar_movimiento


class GameScene():
    def __init__(self, game_manager):
        self.game_manager=game_manager
        self.jugador = self._jugador()
        self.score = 0
        
    def _jugador(self):
        """Busca y devuelve el jugador dentro de las entidades del juego.
    
        Returns:
            Jugador: la instancia jugador, si existe, o None si no se encontró.
        """
        for entity in self.game_manager.entities:
            if isinstance(entity, Jugador):
                return entity
                
        
    def update(self, delta_time=0, eventos=None):
        if eventos is None:
            eventos = pygame.event.get()
        
        
        self.manejar_colisiones()

        self.game_manager.entities.update(self.game_manager.ventana, delta_time, self, eventos=eventos)



    def render(self):
        self.game_manager.ventana.fill(c.COLOR_BG)
        self.game_manager.entities.draw(self.game_manager.ventana)

        pass

    def manejar_colisiones(self):
        jugador = self.jugador
        if jugador is None:
            return
        
        entidad = self.game_manager.grid_manager.check_collision(
            (jugador.rect.x, jugador.rect.y), 
            jugador.direction, 
            self.game_manager.entities,
            ignorar=jugador
        )
        
        if isinstance(entidad, Tile):
            if entidad.contains_pellet:
                entidad.remove_pellet()
                self.score += 10
            elif entidad.contains_power_pellet:
                entidad.remove_power_pellet()
                self.score += 50
                jugador.is_powered_up = True
        elif isinstance(entidad, Enemigo):
            if jugador.is_powered_up:
                entidad.kill()
                self.score += 200
            else:
                jugador.lives -= 1