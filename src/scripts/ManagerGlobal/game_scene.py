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
    
    def __init__(self, game_manager):
        super().__init__(game_manager)

        self.jugador = self._jugador()
        self.game_manager.score = 0
        if GameScene.muerte is None:
            GameScene.muerte=pygame.mixer.Sound(c.EFECTOS["vida_perdida"])  
        if GameScene.comer_fantasma is None:
            GameScene.comer_fantasma=pygame.mixer.Sound(c.EFECTOS["fantasma_comido"])  
        if GameScene.sirena_normal is None:
            GameScene.sirena_normal = pygame.mixer.Sound(c.EFECTOS["mov_fantasmas"])
        if GameScene.sirena_power is None:
            GameScene.sirena_power = pygame.mixer.Sound(c.EFECTOS["power_pellet"])
        if GameScene.sirena_ojos is None:
            GameScene.sirena_ojos = pygame.mixer.Sound(c.EFECTOS["ojos"])
        if GameScene.waka_waka is None:
            GameScene.waka_waka = pygame.mixer.Sound(c.EFECTOS["punto"])
        
        self.ultimo_waka = 0
        self.intervalo_waka = 150 
        self.estado_sirena_actual = None
            
        
        self.power_up_timer=0
        self.power_up_duration=6000 # 6 segs
        self.fantasmas_comidos_racha = 0 
        self.textos_puntajes = []
        ruta=f"pacman_tp/assets/imagenes/characters/pacman/horizontal/pacman_1.png"
        self.imagen_vida = pygame.transform.scale(pygame.image.load(ruta).convert_alpha(), (c.TAMAÑO_PARED, c.TAMAÑO_PARED))
        ruta_fuente = os.path.join("pacman_tp","assets", "fonts", "PressStart2P.ttf")
        self.fuente_puntajes = pygame.font.Font(ruta_fuente, 8)
        self.fuente_info = pygame.font.Font(ruta_fuente, 10)
        self.fuente_data = pygame.font.Font(ruta_fuente, 15)
        
    def _jugador(self):
        for entity in self.game_manager.entities:
            if isinstance(entity, Jugador):
                return entity
                
        
    def update(self, delta_time=0, eventos=None):
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
        ventana = self.game_manager.ventana
        self.game_manager.ventana.fill(c.COLOR_BG)   
        ancho_actual, alto_actual = self.game_manager.ventana.get_size()

            
        hud_alto = alto_actual * 0.08  # 8% del alto
        hud_rect = pygame.Rect(0, 0, ancho_actual, hud_alto)
        pygame.draw.rect(self.game_manager.ventana, (10, 10, 30), hud_rect)
        pygame.draw.line(self.game_manager.ventana, (255, 255, 100), (0, hud_alto), (ancho_actual, hud_alto), 2)
        y_info = hud_alto * 1//3 
        y_data = hud_alto * 2//3 

        x_score = ancho_actual * 0.15

        

        dibujar_texto(f"Score:",self.game_manager.ventana,self.fuente_info, c.NARANJA, x_score ,y_info, True)
        dibujar_texto(
            f"{self.game_manager.score:06d}", 
            ventana, 
            self.fuente_data,
            (255, 215, 0), 
            x_score,
            y_data, 
            True
        )

        x_high_score = ancho_actual * 0.5

    
        dibujar_texto(f"High Score:",self.game_manager.ventana,self.fuente_info, c.ROJO, x_high_score ,y_info, True)
        dibujar_texto(
            f"{self.game_manager.score:06d}", 
            ventana, 
            self.fuente_data,
            c.ROJO, 
            x_high_score,
            y_data, 
            True)


        x_nivel = ancho_actual * 0.85

        dibujar_texto(f"Nivel:",self.game_manager.ventana,self.fuente_info, c.ROSA, x_nivel, y_info, True)
        dibujar_texto(f"{self.game_manager.nivel}",self.game_manager.ventana,self.fuente_info, c.AMARILLO, x_nivel,y_data, True)


        y_footer = alto_actual * 15.5 // 16
        x_vidas = ancho_actual * 0.5
        x_espaciado = ancho_actual * 0.06

        for i in range(self.jugador.lives):
            x = x_vidas + (i-1) * x_espaciado
            ventana.blit(self.imagen_vida, (x, y_footer))


        OFFSET_Y = hud_alto
        for entity in self.game_manager.entities:
            y_original = entity.rect.y
            entity.rect.y += OFFSET_Y

            entity.draw(self.game_manager.ventana)
            entity.rect.y = y_original
        for texto in self.textos_puntajes:
            dibujar_texto(
                texto=texto[0],
                ventana=self.game_manager.ventana,
                fuente=self.fuente_puntajes,
                color=(0, 255, 255),
                x=texto[1],
                y=texto[2],
                centrado=True
            )
        

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
                    tiempo_actual = pygame.time.get_ticks()
                    if tiempo_actual - self.ultimo_waka >= self.intervalo_waka:
                        GameScene.waka_waka.play()
                        self.ultimo_waka = tiempo_actual
                        
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
                                entidad.velocidad = c.VELOCIDAD_BASE * 0.5

                                centro_x, centro_y = entidad.rect.centerx, entidad.rect.centery
                                centro_gxy = self.game_manager.grid_manager.world_to_grid((centro_x, centro_y))
                                
                                direccion_invertida = (-entidad.direction[0], -entidad.direction[1])
                                if not es_pared_en_celda(centro_gxy, direccion_invertida, self):
                                    entidad.proxima_direccion = direccion_invertida
                                    entidad.direction = direccion_invertida
                                else:
                                    direcciones = [(1,0), (-1,0), (0,1), (0,-1)]
                                    for nueva_dir in direcciones:
                                        if nueva_dir == entidad.direction or nueva_dir == direccion_invertida:
                                            continue
                                        if not es_pared_en_celda(centro_gxy, nueva_dir, self):
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
                    
    def check_pellets(self):
        for entidad in self.game_manager.entities:
            if isinstance(entidad, Tile):
                if entidad.contains_pellet or entidad.contains_power_pellet:
                    return True
        return False
    
    def reiniciar(self):
        self.game_manager.resetear_grilla()
        self.jugador=self._jugador()

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
        GameScene.muerte.stop()
        GameScene.sirena_normal.stop()
        GameScene.sirena_power.stop()
        GameScene.sirena_ojos.stop()
        GameScene.waka_waka.stop()

    
