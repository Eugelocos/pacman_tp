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
        self.jugador = self._player()
        self.score = 0
        
    def _player(self):
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

        self.game_manager.entities.update(self.game_manager.ventana, delta_time, self, eventos=eventos)

        self.manejar_colisiones()


    def render(self):
        self.game_manager.ventana.fill(c.COLOR_BG)
        self.game_manager.entities.draw(self.game_manager.ventana)

        pass

        


    def manejar_colisiones(self):
        """Detecta y maneja las colisiones entre el jugador y las entidades del juego (paredes, pellets, enemigos)"""
        jugador = self._player()
        entidad = self.game_manager.grid_manager.check_collision((jugador.rect.x,jugador.rect.y), jugador.direction, self.game_manager.entities)
        if isinstance(entidad, Tile):
            if entidad.is_wall:
                jugador.direccion = (0, 0)
            elif entidad.contains_pellet:
                entidad.remove_pellet()
                self.score += 10
            elif entidad.contains_power_pellet:
                entidad.remove_power_pellet()
                self.score += 50
                jugador.powered_up = True
                jugador.power_up_timer = 5000 # en ms
                # LOGICA ASUSTADO MAS VELOCIDAD PACMAN