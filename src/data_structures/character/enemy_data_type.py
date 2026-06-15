import pygame
import os
import sys
import math
import constantes as c 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from data_structures.character.character_data_type import Personaje
from scripts.Utils.visual import AnimacionExplosion
from scripts.Fantasmas.phantom import decidir_movimiento


class Enemigo(Personaje):
    """Clase que representa a un fantasma enemigo en el juego.

    Hereda de Personaje e implementa comportamientos especificos de cada fantasma:
    rojo, rosa, cyan, naranja, verde y violeta (kamikaze). Maneja diferentes
    estados (scatter, chase, asustado, muerto, explotando), animaciones
    y logica de movimiento segun el tipo.

    Estados posibles:
        - scatter: Va a su esquina asignada.
        - chase: Persigue al jugador con logica individual.
        - asustado: Huye del jugador (color azul).
        - asustado_parpadeando: Parpadea antes de volver a normal.
        - muerto: Ojos que vuelven a la casa.
        - cargando_explosion: Preparando explosion (solo violeta).
        - explotando: Explotando (solo violeta).

    Attributes:
        sprites_cache (dict): Cache de frames por nombre de enemigo (variable de clase).
        sprite_asustado (pygame.Surface): Sprite azul de fantasma asustado.
        sprite_blanco (pygame.Surface): Sprite blanco de fantasma parpadeante.
        sprite_ojos (dict): Sprites de ojos por direccion (arriba, abajo, etc.).

        velocidad (float): Velocidad del fantasma.
        state (str): Estado actual (scatter, chase, asustado, etc.).
        pos_inicial (tuple): Posicion de la esquina en modo scatter.
        target (tuple): Celda objetivo actual.
        nombre_enemigo (str): Tipo de fantasma (fantasma_rojo, etc.).
        jugador_ref (Jugador): Referencia al jugador (PacMan).
        esta_en_casa (bool): True si esta dentro de la casa de fantasmas.
        esta_esperando (bool): True si esperando turno para salir de la casa.
        ultima_celda (tuple): Ultima celda visitada (evita ciclos).
    """
    sprites_cache={}
    sprite_asustado=None    #>v
    sprite_blanco=None      # > flags
    sprite_ojos=None        #>^
    def __init__(self, position:tuple, visibility:bool, nombre_enemigo: str, tile_size: int|float, direction="derecha", state='scatter', pos_inicial=(0,0), target=(0,0)):
        """Inicializa los atributos de la instancia de la clase Enemigo

        Args:
            position (tuple): Posicion de la entidad en pixeles
            visibility (bool): Booleana que determina si se dibujara o no
            direction (str): Clave especifica del diccionario DIRECTIONS que se utiliza para mejorar legibilidad del codigo, representa la direccion inicial.
            tile_size (int | float): EL tamano de celda por el que se escalara la imagen, caulquier entidad lo tiene
            nombre_enemigo (str): Nombre del archivo donde se encuentra la imagen del enemigo, se utiliza ademas para logica de movimiento especifica
            state (str, optional): Estado del fantasma, puede ser scatter, chase, muerto, asustado, asustado parpadeando, entre otros. Defaults to 'scatter'.
            pos_inicial (tuple, optional): Esquina asignada como target en el modo scatter. Defaults to (0,0).
            target (tuple, optional): Target del fantasma al cual buscara ir. Defaults to (0,0).
        """
        ruta_inicial = f"pacman_tp/assets/imagenes/characters/enemies/{nombre_enemigo}/horizontal/{nombre_enemigo}_0.png"
        super().__init__(position, visibility, direction, tile_size, ruta_inicial, False)
        self.velocidad = c.VELOCIDAD_BASE * 0.75 * c.MULTIPLICADOR_VELOCIDAD_ENEMIGOS[nombre_enemigo]
        self.state=state
        self.pos_inicial=pos_inicial
        self.target=target
        self.nombre_enemigo=nombre_enemigo
        self.jugador_ref=None   #flag
        self.esta_en_casa=True  #flag
        self.esta_esperando=True    #flag
        self.ultima_celda=None  #flag

        #carga de imagenes
        if self.nombre_enemigo not in Enemigo.sprites_cache:
            self.cargar_frames()
        if Enemigo.sprite_asustado is None:
            Enemigo.sprite_asustado = pygame.transform.scale(cargar_con_transparencia("pacman_tp//assets//imagenes//characters//enemies//fantasma_asustado//fantasma_asustado_0.png"), (self.tile_size, self.tile_size))
        if Enemigo.sprite_blanco is None:
            Enemigo.sprite_blanco= pygame.transform.scale(cargar_con_transparencia("pacman_tp//assets//imagenes//characters//enemies//fantasma_asustado//fantasma_asustado_1.png"), (self.tile_size, self.tile_size))
        if Enemigo.sprite_ojos is None: 
            ruta_ojos_vert="pacman_tp//assets//imagenes//characters//enemies//ojos_fantasmas//ojos_vertical.png"
            ruta_ojos_hor="pacman_tp//assets//imagenes//characters//enemies//ojos_fantasmas//ojos_horizontal.png"
            ojos_arriba=pygame.transform.scale(cargar_con_transparencia(ruta_ojos_vert), (self.tile_size, self.tile_size))
            ojos_derecha=pygame.transform.scale(cargar_con_transparencia(ruta_ojos_hor), (self.tile_size, self.tile_size))
            ojos_abajo=pygame.transform.flip(ojos_arriba,False,True)
            ojos_izquierda=pygame.transform.flip(ojos_derecha,True,False)
            Enemigo.sprite_ojos={"arriba":ojos_arriba,
                                 "abajo":ojos_abajo,
                                 "derecha":ojos_derecha,
                                 "izquierda":ojos_izquierda}         

    def cargar_frames(self):
        """Carga los frames y se los asgina a la variable de la clase(no instancia) por utilizar buenas practicas.

        Notas: Se podria haber hecho una clase que maneje la carga de imagenes de las clase (no instancias), como un Singleton.
        """
        for direccion in ["arriba", "abajo", "derecha", "izquierda"]:
            for i in range(2):
                if self.nombre_enemigo not in Enemigo.sprites_cache:
                    Enemigo.sprites_cache[self.nombre_enemigo]={}
                if direccion.lower() not in Enemigo.sprites_cache[self.nombre_enemigo]:
                    Enemigo.sprites_cache[self.nombre_enemigo][direccion.lower()]=[]
                if direccion == "izquierda" or direccion == "derecha":
                    ruta=f"pacman_tp/assets/imagenes/characters/enemies/{self.nombre_enemigo}/horizontal/{self.nombre_enemigo}_{i}.png"
                    if direccion == "izquierda":
                        Enemigo.sprites_cache[self.nombre_enemigo][direccion.lower()].append(pygame.transform.scale(cargar_con_transparencia(ruta), (self.tile_size, self.tile_size)))
                    else:
                        Enemigo.sprites_cache[self.nombre_enemigo][direccion.lower()].append(pygame.transform.scale(pygame.transform.flip(cargar_con_transparencia(ruta), True, False), (self.tile_size, self.tile_size)))
                else:
                    ruta=f"pacman_tp/assets/imagenes/characters/enemies/{self.nombre_enemigo}/{direccion.lower()}/{self.nombre_enemigo}_{i}.png"
                    Enemigo.sprites_cache[self.nombre_enemigo][direccion.lower()].append(pygame.transform.scale(cargar_con_transparencia(ruta), (self.tile_size, self.tile_size)))
        self.cambiar_sprite_por_direccion()


    def cambiar_sprite_por_direccion(self):
        """Maneja el cambio de animaciones dependiendo de la direccion actual

        Notes: En estado "muerto", se asigna una lista de un solo frame (sin animacion)
              porque los ojos no parpadean ni se mueven al caminar.
        """
        if self.state=="muerto":
            if self.direction[0]==0 and self.direction[1]==-1:
                self.frames=[Enemigo.sprite_ojos["arriba"]]
            elif self.direction[0]==0 and self.direction[1]==1:
                self.frames=[Enemigo.sprite_ojos["abajo"]]
            elif self.direction[0]==1 and self.direction[1]==0:
                self.frames=[Enemigo.sprite_ojos["derecha"]]
            elif self.direction[0]==-1 and self.direction[1]==0:
                self.frames=[Enemigo.sprite_ojos["izquierda"]]    
            self.frame_actual = 0
            self.image = self.frames[self.frame_actual]
            return
        
        if self.direction[0]==0 and self.direction[1]==-1:
            self.frames=Enemigo.sprites_cache[self.nombre_enemigo]["arriba"]
        elif self.direction[0]==0 and self.direction[1]==1:
            self.frames=Enemigo.sprites_cache[self.nombre_enemigo]["abajo"]
        elif self.direction[0]==1 and self.direction[1]==0:
            self.frames=Enemigo.sprites_cache[self.nombre_enemigo]["derecha"]
        elif self.direction[0]==-1 and self.direction[1]==0:
            self.frames=Enemigo.sprites_cache[self.nombre_enemigo]["izquierda"]
            
        self.frame_actual=0
        self.image=self.frames[self.frame_actual]

    def actualizar_animacion(self, delta_time):
        """Actualiza la animacion del fantasma segun su estado.

        Logica:
            - asustado: Sprite azul fijo (sin animacion).
            - asustado_parpadeando: Alterna entre azul y blanco cada 250ms.
              Esto avisa que el power up esta por terminar.
            - otros: Animacion normal por frames (heredada de Personaje).

        Notes: 
            El parpadeo usa tiempo real con get_ticks() en lugar de delta_time
            porque queremos que parpadee a intervalos fijos independientemente
            del framerate.
        """
        if self.state=="asustado":
            self.image=Enemigo.sprite_asustado
        elif self.state=="asustado_parpadeando":
            tiempo=pygame.time.get_ticks()
            if (tiempo//250) % 2 == 0:
                self.image = Enemigo.sprite_asustado  
            else:
                self.image = Enemigo.sprite_blanco    
        else:
            super().actualizar_animacion(delta_time)

    def update(self, pantalla: pygame.Surface, delta_time: int|float, escena: object, eventos=None):
        """Actualiza el estado y comportamiento del enemigo en cada frame.

        Gestiona la logica de movimiento segun el estado actual del enemigo, 
        maneja la ruitna de explosion (carga y detonacion), y actualiza la 
        animacion si esta en espera.

        Args:
            pantalla (pygame.Surface): Superficie de pygame donde se dibuja el enemigo.
            delta_time (int | float): Tiempo transcurrido desde el ultimo frame (en ms).
            escena (object): Referencia a la escena actual (GameScene), usada para acceder al jugador, 
                            rutinas, sonidos, etc.
            eventos (_type_, optional): Lista de eventos de pygame. Defaults to None.
        """
        if not self.jugador_ref:
            self.jugador_ref = escena.jugador

        estados_validos = ["asustado", "asustado_parpadeando", "muerto", "explotando", "cargando_explosion"]
        if self.state not in estados_validos:
            self.state = escena.game_manager.rutina_manager.get_modo_actual().lower()

        if self.state == "cargando_explosion":
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_inicio_carga >= 3000:
                escena.sonido_pre_explosion.stop()
                escena.sonido_explosion.play()
                self.detonar(escena)

        elif self.state != "explotando" and not self.esta_esperando:
            self.proxima_direccion = decidir_movimiento(self.jugador_ref, self, escena.game_manager)

        if self.esta_esperando:
            self.actualizar_animacion(delta_time)   
        else:
            super().update(pantalla, delta_time, escena, eventos)
        
    def detonar(self, escena):
        """Maneja logica de explosion,se utiliza en el fantasma kamikaze

        Gestiona los sonidos, radio de explosion, y estados. Ademas, se utiliza a la clase AnimacionExplosion que se encarga de la animacion especifica

        Args:
            escena (object): Referencia a la escena actual (GameScene), usada para acceder al jugador, 
                            rutinas, sonidos, etc
        """
        centro_explosion = (self.rect.centerx, self.rect.centery)
        radio_explosion = 5 * c.TAMAÑO_PARED 

        for entity in escena.game_manager.entities:
            if entity == self:
                continue

            centro_entidad = (entity.rect.centerx, entity.rect.centery)
            distancia = math.hypot(centro_entidad[0] - centro_explosion[0], centro_entidad[1] - centro_explosion[1])

            if distancia <= radio_explosion:
                if entity == escena.jugador:
                    if not escena.estado_muerto:
                        escena.perder_vida()
                    
                elif hasattr(entity, 'nombre_enemigo'):
                    entity.state = "muerto"
                    entity.velocidad = c.VELOCIDAD_BASE * 1.5               
                    entity.cambiar_sprite_por_direccion()                   
                    if hasattr(entity, 'destino_kamikaze'):
                        del entity.destino_kamikaze

        animacion = AnimacionExplosion(centro_explosion[0], centro_explosion[1], radio_explosion)
        escena.game_manager.entities.add(animacion)
        
        self.state = "muerto"
        self.velocidad = c.VELOCIDAD_BASE * 1.5                                                         
        self.cambiar_sprite_por_direccion()                                                             
        
        # Limpieza de timers y targets
        if hasattr(self, 'destino_kamikaze'):
            del self.destino_kamikaze   
        if hasattr(self, 'tiempo_inicio_explosion'):
            del self.tiempo_inicio_explosion


def cargar_con_transparencia(ruta):
    """Helper para cargar las imagenes (frames) de la animacion sin el fondo

    Args:
        ruta (str): Ruta de la imagen a cargar

    Returns:
        pygame.Surface: Superficie con la imagen ya sin el fondo
    """
    img = pygame.image.load(ruta).convert()  
    img.set_colorkey((0, 0, 0))             
    return img.convert_alpha()