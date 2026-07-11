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
    """Escena principal del juego. Maneja toda la logica de la partida.

    Controla el jugador, los fantasmas, las colisiones, los power-ups,
    los niveles, las vidas, los sonidos y la logica de juego en general.
    Implementa el comportamiento clasico de PacMan con variantes propias.

    Comportamientos implementados:
        - Fantasmas con logica individual (rojo, rosa, cyan, naranja, verde, violeta)
        - Power-ups que asustan fantasmas y dan puntaje multiplicador
        - Rutinas scatter/chase que alternan segun el nivel
        - Salida progresiva de fantasmas de la casa (0, 30, 60, 90 puntos comidos)
        - Animacion de muerte con circulo expansivo
        - Puntajes flotantes al comer fantasmas
        - Sonidos ambientales segun el estado (normal, power, ojos)

    Attributes:
        muerte: Sonido de muerte del jugador (variable de clase).
        comer_fantasma: Sonido al comer un fantasma (variable de clase).
        sirena_normal: Musica base del juego (variable de clase).
        sirena_power: Musica durante power-up (variable de clase).
        sirena_ojos: Musica cuando los fantasmas vuelven a casa (variable de clase).
        waka_waka: Sonido de comer puntos (variable de clase).
        sonido_explosion: Sonido de explosion del violeta (variable de clase).
        sonido_pre_explosion: Sonido previo a la explosion (variable de clase).

        jugador: Referencia al jugador (PacMan).
        pellets_comidos: Cantidad de puntos comidos en el nivel actual.
        umbrales_salida: Puntos necesarios para que salga cada fantasma de la casa.
        indice_siguiente_salida: Proximo fantasma que debe salir.
        lista_fantasmas: Fantasmas ordenados para salida progresiva.
        estado_sirena_actual: Sirena que esta sonando actualmente.

        power_up_timer: Timer del efecto power-up.
        power_up_duration: Duracion total del power-up (6000ms).
        muerte_timer: Timer de la animacion de muerte.
        estado_muerto: True si el jugador esta en animacion de muerte.
        escala_circulo: Tamaño del circulo de muerte.
        circulo_creciendo: True si el circulo esta creciendo, False si decrece.

        textos_puntajes: Lista de textos flotantes (puntajes al comer fantasma).
        imagen_vida: Icono de vida que se muestra en el HUD.
        fuentes: Diferentes tamaños de fuente para el HUD.
    """

    muerte=None
    comer_fantasma=None
    sirena_normal=None
    sirena_power=None
    sirena_ojos=None
    waka_waka=None
    sonido_explosion=None
    sonido_pre_explosion=None
    
    
    def __init__(self, game_manager):
        """Inicializa la escena del juego.

        Carga sonidos, fuentes, imagenes y configura el estado inicial
        del nivel (timer, puntajes, fantasmas, etc.)

        Args:
            game_manager: Referencia al administrador principal del juego.
        """
        super().__init__(game_manager)

        self.jugador = self._jugador()
        self.pellets_comidos = 0
        self.umbrales_salida = [0, 30, 60, 90]
        self.indice_siguiente_salida = 0
        self.lista_fantasmas = self._get_fantasmas_ordenados()
        self.game_manager.score = 0
        self.sumar_vida=False
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
        self.power_up_duration=6000 # 6 segs

        self.cortina_timer = 1500
        self.cortina_rect = pygame.Rect(0, 0, self.game_manager.ventana.get_width(), self.game_manager.ventana.get_height())
        self.is_cortina = True

        self.muerte_timer = 1500
        self.estado_muerto = False

        self.fantasmas_comidos_racha = 0 
        self.textos_puntajes = []
        ruta=f"pacman_tp/assets/imagenes/characters/pacman/horizontal/pacman_1.png"
        self.imagen_vida = pygame.transform.scale(pygame.image.load(ruta).convert_alpha(), (c.TAMAÑO_PARED, c.TAMAÑO_PARED))
        ruta_fuente = os.path.join("pacman_tp","assets", "fonts", "PressStart2P.ttf")
        self.fuente_puntajes = pygame.font.Font(ruta_fuente, 8)
        self.fuente_info = pygame.font.Font(ruta_fuente, 10)
        self.fuente_data = pygame.font.Font(ruta_fuente, 15)
        self.escala_circulo = 0
        self.circulo_creciendo = True


    def _jugador(self) -> Jugador|None:
        """Busca y devuelve la instancia de Jugador en el grupo de entidades

        Returns:
            Jugador|None: La instancia de Jugador, o None si no se encuentra.
        """
        for entity in self.game_manager.entities:
            if isinstance(entity, Jugador):
                return entity
                
        
    def update(self, delta_time: int|float, eventos=None):
        
  
            
        """Actualiza toda la logica del juego cada frame.

        Maneja en orde:
            0. Manejo de vida extra
            1. Congelacion de frames (efecto de impacto al comer)
            2. Animacion de muerte y estado de muerte (game over)
            3. Cambio de sirenas segun estado del juego
            4. Actualizacion de textos flotantes
            5. Power up y parpadeo de fantasmas
            6. Logica de salida de fantasmas en orden dependiendo de pellets comidos
            7. Actualizacion de logica individual de entidades
            8. Manejo de colisiones
            9. Verificacion de nivel superado

        Args:
            delta_time (int | float): Tiempo transcurrido desde el ultimo frame (en ms).
            eventos (_type_, optional): Lista de eventos de pygame. Defaults to None.

        """

        if self.is_cortina:
            self.cortina_timer -= delta_time
            if self.cortina_timer <= 0:
                self.is_cortina = False

            progreso = 1 - (self.cortina_timer / 1500)
            salto_actual = int(progreso * 36)

            altura_maxima = self.game_manager.ventana.get_height()
            self.altura_actual = altura_maxima - (salto_actual * (altura_maxima / 36))

            self.cortina_rect.height = int(self.altura_actual)
            return
        
        if self.game_manager.score>10000 and self.jugador.lives<4 and (not self.sumar_vida):
            self.jugador.lives+=1
            self.sumar_vida=True

        if self.frames_congelados>0:
            self.frames_congelados-=1
            return
        if eventos is None:
            eventos = pygame.event.get()

        for event in eventos:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.avanzar_nivel()

        if self.estado_muerto:
            self.muerte_timer -= delta_time
            if self.circulo_creciendo:
                self.escala_circulo += delta_time

                if self.escala_circulo >= self.game_manager.ventana.get_height() and self.jugador.lives > 0:
                    self.circulo_creciendo = False

            else:
                self.escala_circulo -= delta_time
                self.reiniciar_posiciones()
                if self.escala_circulo <= 0:
                    self.escala_circulo = 0
                    self.circulo_creciendo = True
                    self.muerte_timer = 0


            if self.muerte_timer <= 0:
                self.estado_muerto = False
                if self.jugador.lives <= 0:
                    with open("pacman_tp//assets//high_score","w") as nuevo:
                        nuevo.write(str(self.game_manager.high_score))
                    self.game_manager.resetear_grilla()
                    self.game_manager.nivel = 1
                    self.game_manager.scenes["game"] = GameScene(self.game_manager)
                    self.game_manager.change_scene("game_over")
                    return
                else:
                    GameScene.sirena_normal.play(loops=-1)
                    self.estado_sirena_actual = "normal"
            return

        if self.jugador.lives <= 0:
            self.game_manager.resetear_grilla()
            self.game_manager.nivel = 1
            self.game_manager.scenes["game"] = GameScene(self.game_manager)
            self.game_manager.change_scene("game_over")
            return
        
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
        

        if not self.check_pellets():
            self.avanzar_nivel()
        
        

    def render(self):
        """Dibuja todos los elementos del juego en pantalla.

        Orden de dibujo:
            1. Fondo
            2. Entidades
            3. Texto puntajes
            4. Circulo animacion muerte
            5. HUD (score, high score, nivel, vidas)

        """

        ventana = self.game_manager.ventana
        self.game_manager.ventana.fill(c.COLOR_BG)   
        ancho_actual, alto_actual = self.game_manager.ventana.get_size()
        hud_alto = alto_actual * 0.08  # 8% del alto
        hud_rect = pygame.Rect(0, 0, ancho_actual, hud_alto)

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

        if self.estado_muerto:
            x_jugador = self.jugador.rect.centerx
            y_jugador = self.jugador.rect.centery

            pygame.draw.circle(ventana, c.COLOR_BG, (x_jugador, y_jugador), self.escala_circulo)


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
            f"{self.game_manager.high_score:06d}", 
            ventana, 
            self.fuente_data,
            c.ROJO, 
            x_high_score,
            y_data, 
            True)


        x_nivel = ancho_actual * 0.85

        dibujar_texto(f"Level:",self.game_manager.ventana,self.fuente_info, c.ROSA, x_nivel, y_info, True)
        dibujar_texto(f"{self.game_manager.nivel}",self.game_manager.ventana,self.fuente_info, c.AMARILLO, x_nivel,y_data, True)


        y_footer = alto_actual * 15.5 // 16
        x_vidas = ancho_actual * 0.5
        x_espaciado = ancho_actual * 0.06

        for i in range(self.jugador.lives):
            x = x_vidas + (i-1) * x_espaciado
            ventana.blit(self.imagen_vida, (x, y_footer))

        pygame.draw.rect(self.game_manager.ventana, c.COLOR_BG, self.cortina_rect)


    def manejar_colisiones(self):
        """Procesa las colisiones del Jugador con Tiles y Enemigos.

        - Si es Tile y es pellet +10pts, si es power pellet +50pts con logica de power up.
        - Si es Enemigo y el Jugador tiene power up, come al fantasma (200*2^n pts), si no pierde vida
        """
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
                    self.perder_vida()
    

            if self.game_manager.score>self.game_manager.high_score:
                        self.game_manager.high_score=self.game_manager.score
                
    def check_pellets(self) -> bool:
        """Helper que verifica si quedan pellets o power pellets en el mapa sin comer

        Returns:
            bool: True si quedan, False si no queda ninguna
        """
        for entidad in self.game_manager.entities:
            if isinstance(entidad, Tile):
                if entidad.contains_pellet or entidad.contains_power_pellet:
                    return True
        return False
    
    def reiniciar(self):
        """Reiniciar el estado del nivel (grilla, referencias, pellets, contadores).
        """
        self.game_manager.resetear_grilla()
        self.jugador=self._jugador()
        self.pellets_comidos = 0
        self.indice_siguiente_salida = 0
        self.lista_fantasmas = self._get_fantasmas_ordenados()

    def avanzar_nivel(self):
        """Avanza al siguiente nivel

        Reincia el estado, aumenta el nivel, limpia la rutinas, y cambia a la escena Intermision
        """
        self.reiniciar()
        self.game_manager.nivel += 1
        self.game_manager.rutina_manager.rutina =self.game_manager.rutina_manager.inicializar_rutinas()
        self.game_manager.rutina_manager.reiniciar()
        self.game_manager.scenes['intermision'] = Intermision(self.game_manager)
        self.game_manager.change_scene("intermision")

    def perder_vida(self):
        """Maneja la perdida de una vida

        Reproduce sonido, resta vida, detiene sirenas, resetea power ups, contadores/rachas 
        y la animacion de muerte, establece estado muerto en True
        """
        if self.estado_muerto:
            return
        
        self.circulo_creciendo = True
        GameScene.muerte.play()
        self.jugador.lives -= 1
        self.game_manager.vidas = self.jugador.lives

        

        GameScene.sirena_normal.stop()
        GameScene.sirena_power.stop()
        GameScene.sirena_ojos.stop()
        

        self.jugador.is_powered_up = False
        self.power_up_timer = 0
        self.fantasmas_comidos_racha = 0

        self.escala_circulo = 0
        self.muerte_timer = 2000

        self.estado_muerto = True

    def reiniciar_posiciones(self):
        """Reinicia posiciones y estados de los peronajes de la escena

        Reinicia posicion del jugador, y por cada enemigo reinicia su posicion y estados, y restablece su velocidad.
        """
        self.jugador.rect.centerx = self.jugador.pos_aparicion[0]
        self.jugador.rect.centery = self.jugador.pos_aparicion[1]

        enemigos = [entidad for entidad in self.game_manager.entities if isinstance(entidad, Enemigo)]
        for i,enemigo in enumerate(enemigos):
            enemigo.rect.centerx = enemigo.pos_aparicion[0]
            enemigo.rect.centery = enemigo.pos_aparicion[1]
            enemigo.velocidad = c.VELOCIDAD_BASE * 0.75 * c.MULTIPLICADOR_VELOCIDAD_ENEMIGOS[enemigo.nombre_enemigo]
            enemigo.esta_en_casa = True
            enemigo.state = "scatter"
            enemigo.esta_esperando = (i >= self.indice_siguiente_salida)

    def on_enter(self):
        """Se ejecuta al entrar a la escena. Reanuda rutinas y desactiva la pausa.
        """
        self.game_manager.rutina_manager.reanudar()
        self.game_manager.pausado = False
        print(f"Restaurando vidas: {self.game_manager.vidas}")
        self.jugador.lives = self.game_manager.vidas

    def on_exit(self):
        """Se ejecuta al salir de la escena. Pausa rutinas y desactiva la pausa."""
        self.game_manager.rutina_manager.pausar()
        self.game_manager.pausado = False
        GameScene.sirena_normal.stop()
        GameScene.sirena_power.stop()
        GameScene.sirena_ojos.stop()
        self.jugador.is_powered_up = False
        self.power_up_timer = 0
        self.fantasmas_comidos_racha = 0
        self.is_cortina = True
        self.cortina_timer = 1500
        self.cortina_rect.height = self.game_manager.ventana.get_height()

    def _get_fantasmas_ordenados(self) -> list[Enemigo]:
        """Obtiene los fantasmas ordenados segun el orden oficial.

        Returns:
            list[Enemigo]: Lista de fantasmas ordenada por su tipo
        """
        fantasmas = [e for e in self.game_manager.entities if isinstance(e, Enemigo)]
        orden_usuario = [e[0] for e in self.game_manager.tipos_enemigos]
        fantasmas.sort(key=lambda x: orden_usuario.index(x.nombre_enemigo) if x.nombre_enemigo in orden_usuario else 99)
        return fantasmas

    def _verificar_salida_fantasmas(self):
        """Verifica si algun fantasma debe salir de la casa.

        Compara los puntos comidos con los umbrales de salida y libera
        a los fantasmas progresivamente.
        """
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
            

    
