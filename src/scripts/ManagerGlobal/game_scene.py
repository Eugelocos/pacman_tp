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
    muerte=None
    def __init__(self, game_manager):
        self.game_manager=game_manager
        self.jugador = self._jugador()
        self.score = 0
        if GameScene.muerte is None:
            GameScene.muerte=pygame.mixer.Sound(c.EFECTOS["vida_perdida"])  
        
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
        
        

        self.game_manager.entities.update(self.game_manager.ventana, delta_time, self, eventos=eventos)
        self.manejar_colisiones()
        
        if self.jugador.lives <= 0:    
            self.game_manager.resetear_grilla()
            self.game_manager.scenes["game"] = GameScene(self.game_manager)
            self.game_manager.change_scene("game_over")
            return
        if not self.check_pellets():
            self.reiniciar()
        



    def render(self):
        self.game_manager.ventana.fill(c.COLOR_BG)    

        for entity in self.game_manager.entities:
            entity.draw(self.game_manager.ventana)

        pass

    def manejar_colisiones(self):
        jugador = self.jugador
        if jugador is None:
            return
        
        entidades_colisionadas = pygame.sprite.spritecollide(jugador, self.game_manager.entities, False)
        for entidad_colisionada in entidades_colisionadas:
            if isinstance(entidad_colisionada, Tile):
                if entidad_colisionada.contains_pellet:
                    entidad_colisionada.remove_pellet()
                    self.score += 10
                elif entidad_colisionada.contains_power_pellet:
                    entidad_colisionada.remove_power_pellet()
                    self.score += 50
                    #jugador.is_powered_up = True
            elif isinstance(entidad_colisionada, Enemigo):
                if jugador.is_powered_up:
                    entidad_colisionada.kill()
                    self.score += 200
                else:
                    GameScene.muerte.play()
                    jugador.lives -= 1
                    

    def check_pellets(self):
        for entidad in self.game_manager.entities:
            if isinstance(entidad, Tile):
                if entidad.contains_pellet or entidad.contains_power_pellet:
                    return True


        return False
    
    def reiniciar(self):
        self.game_manager.resetear_grilla()
        self.jugador=self._jugador()
        pass