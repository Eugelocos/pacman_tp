import pygame
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import constantes as c
from data_structures.character.enemy_data_type import Enemigo
from data_structures.map.tile_data_type import Tile
from data_structures.character.player_data_type import Jugador
from scripts.Movimiento.movimiento import manejar_movimiento
from scripts.ManagerGlobal.intermision import Intermision
from scripts.ManagerGlobal.escena import EscenaBase


class GameScene(EscenaBase):
    muerte=None
    def __init__(self, game_manager):
        super().__init__(game_manager)

        self.jugador = self._jugador()
        self.game_manager.score = 0
        if GameScene.muerte is None:
            GameScene.muerte=pygame.mixer.Sound(c.EFECTOS["vida_perdida"])  
        self.power_up_timer=0
        self.power_up_duration=6000 #6 segs
        
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
            
        if self.jugador and self.jugador.is_powered_up:
            self.power_up_timer += delta_time          
            
            if self.power_up_timer >= 4000 and self.power_up_timer < self.power_up_duration:
                for entidad in self.game_manager.entities:
                    if isinstance(entidad, Enemigo) and entidad.state == "asustado":
                        entidad.state = "asustado_parpadeando" 
            
            if self.power_up_timer >= self.power_up_duration: 
                self.jugador.is_powered_up = False     
                self.jugador.velocidad = c.VELOCIDAD_BASE * 0.80
                self.power_up_timer = 0                

                for entidad in self.game_manager.entities:
                    if isinstance(entidad, Enemigo) and (entidad.state == "asustado" or entidad.state == "asustado_parpadeando"):
                        entidad.state = "scatter"  #los fantasmas vuelven a su patrón de movimiento normal
                        entidad.velocidad = c.VELOCIDAD_BASE*0.75  #recuperan su velocidad


        self.game_manager.entities.update(self.game_manager.ventana, delta_time, self, eventos=eventos)
        self.manejar_colisiones()
        
        if self.jugador.lives <= 0:    
            self.game_manager.resetear_grilla()
            self.game_manager.nivel=0
            self.game_manager.scenes["game"] = GameScene(self.game_manager)
            self.game_manager.change_scene("game_over")
            return
        if not self.check_pellets():
            self.avanzar_nivel()
        



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
                    self.game_manager.score += 10
                elif entidad_colisionada.contains_power_pellet:
                    entidad_colisionada.remove_power_pellet()
                    self.game_manager.score += 50
                    jugador.is_powered_up = True
                    jugador.velocidad=c.VELOCIDAD_BASE*0.90
                    self.power_up_timer=0
                    
                    for entidad in self.game_manager.entities:
                        if isinstance(entidad,Enemigo):
                            if entidad.state != "muerto" and not entidad.esta_en_casa:
                                entidad.state = "asustado"
                                entidad.velocidad = c.VELOCIDAD_BASE * 0.5  # Velocidad a la mitad
                                entidad.direction = (entidad.direction[0] * -1, entidad.direction[1] * -1) #invertir direccion
                                entidad.proxima_direccion = entidad.direction
            elif isinstance(entidad_colisionada, Enemigo):
                estados_susto=["asustado", "asustado_parpadeando"]
                estados=["asustado", "asustado_parpadeando","muerto"]
                if jugador.is_powered_up and (entidad_colisionada.state in estados_susto):
                    entidad_colisionada.state="muerto"
                    entidad_colisionada.velocidad=c.VELOCIDAD_BASE*1.5
                    self.game_manager.score += 200
                elif entidad_colisionada.state not in estados:
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

    def avanzar_nivel(self):
        self.reiniciar()
        self.game_manager.nivel += 1
        self.game_manager.rutina_manager.rutina =self.game_manager.rutina_manager.inicializar_rutinas()
        print("rutinas", self.game_manager.rutina_manager.rutina)
        self.game_manager.rutina_manager.reiniciar()
        self.game_manager.scenes['intermision'] = Intermision(self.game_manager)
        self.game_manager.change_scene("intermision")

    def on_enter(self):
        print("Entrango a Juego")
        self.game_manager.rutina_manager.reanudar()
        self.game_manager.pausado = False

    def on_exit(self):
        self.game_manager.rutina_manager.pausar()
        self.game_manager.pausado = False
    
