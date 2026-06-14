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
from scripts.funciones_aux import dibujar_texto
from scripts.Utils.utilidades_colision import es_pared_en_celda


class GameScene(EscenaBase):
    muerte=None
    comer_fantasma=None
    sirena_normal=None
    sirena_power=None
    sirena_ojos=None
    waka_waka=None
    sonido_explosion=None
    sonido_pre_explosion=None
    
    
    def __init__(self, game_manager):
        super().__init__(game_manager)

        self.jugador = self._jugador()
        self.pellets_comidos = 0
        self.umbrales_salida = [0, 30, 60, 90]
        self.indice_siguiente_salida = 0
        self.lista_fantasmas = self._get_fantasmas_ordenados()
        self.game_manager.score = 0
        if GameScene.muerte is None:
            GameScene.muerte=pygame.mixer.Sound(c.EFECTOS["vida_perdida"])  
        if GameScene.comer_fantasma is None:
            GameScene.comer_fantasma=pygame.mixer.Sound(c.EFECTOS["fantasma_comido"])  
            GameScene.comer_fantasma.set_volume(0.5)
        if GameScene.sirena_normal is None:
            GameScene.sirena_normal = pygame.mixer.Sound(c.EFECTOS["mov_fantasmas"])
            GameScene.sirena_normal.set_volume(1.0)
        if GameScene.sirena_power is None:
            GameScene.sirena_power = pygame.mixer.Sound(c.EFECTOS["power_pellet"])
        if GameScene.sirena_ojos is None:
            GameScene.sirena_ojos = pygame.mixer.Sound(c.EFECTOS["ojos"])
            GameScene.sirena_ojos.set_volume(0.5)
        if GameScene.waka_waka is None:
            GameScene.waka_waka = pygame.mixer.Sound(c.EFECTOS["punto"])
            GameScene.waka_waka.set_volume(0.1)
        if GameScene.sonido_explosion is None: 
            GameScene.sonido_explosion=pygame.mixer.Sound(c.EFECTOS["explosion"])
        if GameScene.sonido_pre_explosion is None: 
            GameScene.sonido_pre_explosion=pygame.mixer.Sound(c.EFECTOS["pre_explosion"])
        
        
        self.canal_waka = pygame.mixer.Channel(1)
        pygame.mixer.set_reserved(1)     
        self.canal_waka = pygame.mixer.Channel(0)   
        self.frames_congelados = 0
        self.estado_sirena_actual = None
        
        self.power_up_timer=0
        self.power_up_duration=6000 #6 segs
        self.fantasmas_comidos_racha = 0 
        self.textos_puntajes = []
        ruta_fuente = os.path.join("pacman_tp","assets", "fonts", "PressStart2P.ttf")
        self.fuente_puntajes = pygame.font.Font(ruta_fuente, 8) 
        
    def _jugador(self):
        for entity in self.game_manager.entities:
            if isinstance(entity, Jugador):
                return entity
                
        
    def update(self, delta_time=0, eventos=None):
        if self.frames_congelados > 0:
            self.frames_congelados -= 1
            return
        if eventos is None:
            eventos = pygame.event.get()
            
        hay_ojos_activos = False 
        for entidad in self.game_manager.entities:
            if isinstance(entidad, Enemigo) and entidad.state == "muerto":
                hay_ojos_activos = True 
                break
        nuevo_estado_sirena = "normal"
        if hay_ojos_activos:
            nuevo_estado_sirena = "ojos"
        elif self.jugador and self.jugador.is_powered_up:
            nuevo_estado_sirena = "power"
        
        if nuevo_estado_sirena != self.estado_sirena_actual:
            GameScene.sirena_normal.stop()
            GameScene.sirena_power.stop()
            GameScene.sirena_ojos.stop()
        
            if nuevo_estado_sirena == "ojos":
                GameScene.sirena_ojos.play(loops=-1)
            elif nuevo_estado_sirena == "power":
                GameScene.sirena_power.play(loops=-1)
            elif nuevo_estado_sirena == "normal":
                GameScene.sirena_normal.play(loops=-1)
        
            self.estado_sirena_actual = nuevo_estado_sirena
        
        for texto in self.textos_puntajes[:]: 
            texto[3] -= delta_time 
            texto[2] -= 0.03 * delta_time
            if texto[3] <= 0:
                self.textos_puntajes.remove(texto)
            
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
                self.fantasmas_comidos_racha = 0

                for entidad in self.game_manager.entities:
                    if isinstance(entidad, Enemigo) and (entidad.state == "asustado" or entidad.state == "asustado_parpadeando"):
                        entidad.state = "scatter"  
                        entidad.velocidad = c.VELOCIDAD_BASE*0.75

        self._verificar_salida_fantasmas()
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
        
        for texto in self.textos_puntajes:
            superficie_texto = self.fuente_puntajes.render(texto[0], True, (0, 255, 255))
            rect_texto = superficie_texto.get_rect(center=(texto[1], texto[2]))
            self.game_manager.ventana.blit(superficie_texto, rect_texto)

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
                    self.pellets_comidos += 1
                    self.canal_waka.play(GameScene.waka_waka)  # siempre, sin get_busy
                    self.frames_congelados = 1
                    
                        
                elif entidad_colisionada.contains_power_pellet:
                    entidad_colisionada.remove_power_pellet()
                    self.game_manager.score += 50
                    self.pellets_comidos += 1
                    self.frames_congelados=3
                    jugador.is_powered_up = True
                    jugador.velocidad=c.VELOCIDAD_BASE*0.90
                    self.power_up_timer=0
                    
                    for entidad in self.game_manager.entities:
                        if isinstance(entidad,Enemigo):
                            if entidad.state != "muerto" and not entidad.esta_en_casa:
                                entidad.state = "asustado"
                                entidad.velocidad = c.VELOCIDAD_BASE * 0.5
                                entidad.direction = (entidad.direction[0] * -1, entidad.direction[1] * -1) 
                                entidad.proxima_direccion = entidad.direction

                                centro_x, centro_y = entidad.rect.centerx, entidad.rect.centery
                                centro_gxy = self.game_manager.grid_manager.world_to_grid((centro_x, centro_y))
                                
                                direccion_invertida = (-entidad.direction[0], -entidad.direction[1])
                                if not es_pared_en_celda(centro_gxy, direccion_invertida, self,entidad):
                                    entidad.proxima_direccion = direccion_invertida
                                    entidad.direction = direccion_invertida
                                else:
                                    direcciones = [(1,0), (-1,0), (0,1), (0,-1)]
                                    for nueva_dir in direcciones:
                                        if nueva_dir == entidad.direction or nueva_dir == direccion_invertida:
                                            continue
                                        if not es_pared_en_celda(centro_gxy, nueva_dir, self,entidad):
                                            entidad.proxima_direccion = nueva_dir
                                            entidad.direction = nueva_dir
                                            break
                                entidad.cambiar_sprite_por_direccion()

                                centro_celda = self.game_manager.grid_manager.grid_to_world(centro_gxy)
                                entidad.rect.center = centro_celda

            elif isinstance(entidad_colisionada, Enemigo):
                estados_susto=["asustado", "asustado_parpadeando"]
                estados=["asustado", "asustado_parpadeando","muerto", "explotando"]
                
                if jugador.is_powered_up and (entidad_colisionada.state in estados_susto):
                    entidad_colisionada.state="muerto"
                    entidad_colisionada.cambiar_sprite_por_direccion()
                    if GameScene.comer_fantasma is not None:
                        GameScene.comer_fantasma.play()
                    entidad_colisionada.velocidad=c.VELOCIDAD_BASE*1.5
                    puntos_ganados = 200 * (2 ** self.fantasmas_comidos_racha)
                    self.game_manager.score += puntos_ganados
                    self.fantasmas_comidos_racha += 1
                    self.textos_puntajes.append([
                        str(puntos_ganados), 
                        entidad_colisionada.rect.centerx, 
                        entidad_colisionada.rect.centery, 
                        1000
                    ])
                elif entidad_colisionada.state not in estados:
                    GameScene.muerte.play()
                    GameScene.sirena_normal.stop()
                    GameScene.sirena_power.stop()
                    GameScene.sirena_ojos.stop()
                    jugador.lives -= 1
                    self._reiniciar_tras_muerte()
                    

    def check_pellets(self):
        for entidad in self.game_manager.entities:
            if isinstance(entidad, Tile):
                if entidad.contains_pellet or entidad.contains_power_pellet:
                    return True
        return False
    
    def reiniciar(self):
        self.game_manager.resetear_grilla()
        self.jugador=self._jugador()
        self.pellets_comidos = 0
        self.indice_siguiente_salida = 0
        self.lista_fantasmas = self._get_fantasmas_ordenados()

    def avanzar_nivel(self):
        self.reiniciar()
        self.game_manager.nivel += 1
        self.game_manager.rutina_manager.rutina =self.game_manager.rutina_manager.inicializar_rutinas()
        self.game_manager.rutina_manager.reiniciar()
        self.game_manager.scenes['intermision'] = Intermision(self.game_manager)
        self.game_manager.change_scene("intermision")

    def on_enter(self):
        self.game_manager.rutina_manager.reanudar()
        self.game_manager.pausado = False

    def on_exit(self):
        self.game_manager.rutina_manager.pausar()
        self.game_manager.pausado = False
        
    def _get_fantasmas_ordenados(self):
        fantasmas = [e for e in self.game_manager.entities if isinstance(e, Enemigo)]
        orden_oficial = [f[0] for f in c.FANTASMAS]
        fantasmas.sort(key=lambda x: orden_oficial.index(x.nombre_enemigo) if x.nombre_enemigo in orden_oficial else 99)
        return fantasmas

    def _verificar_salida_fantasmas(self):
        if not self.lista_fantasmas:
            self.lista_fantasmas = self._get_fantasmas_ordenados()
            if not self.lista_fantasmas:
                return 
        while (self.indice_siguiente_salida < len(self.umbrales_salida) and 
               self.indice_siguiente_salida < len(self.lista_fantasmas) and
               self.pellets_comidos >= self.umbrales_salida[self.indice_siguiente_salida]):
            fantasma = self.lista_fantasmas[self.indice_siguiente_salida]
            fantasma.esta_esperando = False   
            self.indice_siguiente_salida += 1
            
    def _reiniciar_tras_muerte(self):
        self.lista_fantasmas = self._get_fantasmas_ordenados()
        
        for i, fantasma in enumerate(self.lista_fantasmas):
            fantasma.esta_en_casa = True
            fantasma.state = "scatter"
            fantasma.velocidad = c.VELOCIDAD_BASE * 0.75 * c.MULTIPLICADOR_VELOCIDAD_ENEMIGOS[fantasma.nombre_enemigo]
            fantasma.esta_esperando = (i >= self.indice_siguiente_salida)
            centro_celda = self.game_manager.grid_manager.grid_to_world(fantasma.pos_inicial)
            fantasma.rect.center = centro_celda