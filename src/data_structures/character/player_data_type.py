import pygame
import sys
import os
import constantes as c
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from data_structures.character.character_data_type import Personaje

class Jugador(Personaje):
    """Clase hija de Personaje que maneja la logica especifica del jugador.

    Incluye control de teclado, manejo de vidas, power-ups y animaciones.
    Los sprites se cargan una sola vez en la variable de clase sprites_cache.

    Attributes:
        sprites_cache (dict): Cache de frames organizados por direccion.
        lives (int): Vidas restantes del jugador.
        is_powered_up (bool): True si tiene efecto de power pellet activo.
        velocidad (float): Velocidad actual del jugador.
    """
    sprites_cache={} # cache(simulado) donde se guardan listas de frames organizados por tipo de animacion
    def __init__(self, position: tuple, visibility: bool, nombre_jugador: str, direction: tuple, tile_size: int|float, lives=3):
        """Inicializa los atributos de la instancia de la clase Jugador

        Args:
            position (tuple): Posicion de la entidad en pixeles
            visibility (bool): Booleana que determina si se dibujara o no
            direction (str): Clave especifica del diccionario DIRECTIONS que se utiliza para mejorar legibilidad del codigo, representa la direccion inicial.
            tile_size (int | float): EL tamano de celda por el que se escalara la imagen, caulquier entidad lo tiene
            nombre_jugador (str): Nombre del archivo donde se encuentra la imagen del jugador
            lives (int, optional): Cantidad de vidas del jugador. Defaults to 3.
        """
        ruta_inicial = f"pacman_tp/assets/imagenes/characters/{nombre_jugador}/horizontal/{nombre_jugador}_0.png" # ruta por defecto con el nombre del archivo pasado por parametros
        super().__init__(position, visibility, direction, tile_size, ruta_inicial, True)
        self.velocidad = c.VELOCIDAD_BASE * 0.80
        self.lives=lives
        self.point=0
        self.nombre=nombre_jugador
        self.is_powered_up=False
        self.muriendo=False
        self.tiempo_muerte=0
        if direction not in Jugador.sprites_cache:
            self.cargar_frames()

    def cargar_frames(self):
        """Carga los frames y se los asgina a la variable de la clase(no instancia) por utilizar buenas practicas.

        Notas:
            - Se podria haber hecho una clase que maneje la carga de imagenes de las clase (no instancias), como un Singleton.
        """
        for direccion in ["arriba", "abajo", "derecha", "izquierda"]:
            for i in range(3):
                if direccion.lower() not in Jugador.sprites_cache:
                    Jugador.sprites_cache[direccion.lower()]=[]
                if direccion == "izquierda" or direccion == "derecha":
                    ruta=f"pacman_tp/assets/imagenes/characters/{self.nombre}/horizontal/{self.nombre}_{i}.png"
                    if direccion == "izquierda":
                        Jugador.sprites_cache[direccion.lower()].append(pygame.transform.scale(pygame.transform.flip(pygame.image.load(ruta).convert_alpha(), True, False), (self.tile_size, self.tile_size)))
                    else:
                        Jugador.sprites_cache[direccion.lower()].append(pygame.transform.scale(pygame.image.load(ruta).convert_alpha(), (self.tile_size, self.tile_size)))
                else:
                    ruta=f"pacman_tp/assets/imagenes/characters/{self.nombre}/vertical/{self.nombre}_{i}.png"
                    if direccion == "abajo":
                        Jugador.sprites_cache[direccion.lower()].append(pygame.transform.scale(pygame.transform.flip(cargar_con_transparencia(ruta), False, True), (self.tile_size, self.tile_size)))
                    else:
                        Jugador.sprites_cache[direccion.lower()].append(pygame.transform.scale(cargar_con_transparencia(ruta), (self.tile_size, self.tile_size)))
            Jugador.sprites_cache[direccion.lower()].append(
                Jugador.sprites_cache[direccion.lower()][1]
            )
       
        self.cambiar_sprite_por_direccion()


    def cambiar_sprite_por_direccion(self):
        """Maneja el cambio de animaciones dependiendo de la direccion actual
        """
        if self.direction[0]==0 and self.direction[1]==-1:
            self.frames=Jugador.sprites_cache["arriba"]
        elif self.direction[0]==0 and self.direction[1]==1:
            self.frames=Jugador.sprites_cache["abajo"]
        elif self.direction[0]==1 and self.direction[1]==0:
            self.frames=Jugador.sprites_cache["derecha"]
        elif self.direction[0]==-1 and self.direction[1]==0:
            self.frames=Jugador.sprites_cache["izquierda"]

        self.frame_actual=0
        self.image=self.frames[self.frame_actual]

    def update(self, ventana: pygame.Surface, delta_time: int|float, escena: object, eventos=None):
        """Maneja la logica propia de el personaje, lee inputs y llama al update de su super clase (Personaje)

        Args:
            ventana (pygame.Surface): Superficie donde se renderizara la entidad
            delta_time (float|int): Tiempo que tarda el ordenador en procesar y mostrar un único fotograma (o frame) en pantalla
            escena (object, optional): Objeto de la escena a quien pertenece la entidad. Defaults to None.
            eventos (_type_, optional): Lista de eventos de pygame. Defaults to None.
        """
        self.leer_inputs(eventos)
        super().update(ventana, delta_time, escena, eventos)

    def leer_inputs(self, eventos=None):
        """Maneja la lectura de teclado y la asignacion de direcciones al buffer proxima direccion

        Args:
            eventos (_type_, optional): Lista de eventos de pygame. Defaults to None.
        """
        if eventos is None:
            eventos = pygame.event.get()
        for event in eventos:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and self.direction != (0, -1):
                    self.proxima_direccion=(0,-1)
                elif event.key == pygame.K_s and self.direction != (0, 1):
                    self.proxima_direccion=(0,1)
                elif event.key == pygame.K_a and self.direction != (-1, 0):
                    self.proxima_direccion=(-1,0)
                elif event.key == pygame.K_d and self.direction != (1, 0):
                    self.proxima_direccion=(1,0)

    def draw(self, ventana: pygame.Surface):
        """Metodo para renderizar la instancia propia en la ventana,
        en esta clase se sobreescribe el metodo draw de Entity para dibujar solo si el jugador tiene mas de 0 vidas.

        Args:
            ventana (pygame.Surface): Superficie donde se renderizara la entidad.
        """
        if self.lives > 0:
            super().draw(ventana)





def cargar_con_transparencia(ruta: str) -> pygame.Surface:
    """Helper para cargar las imagenes (frames) de la animacion sin el fondo

    Args:
        ruta (str): Ruta de la imagen a cargar

    Returns:
        pygame.Surface: Superficie con la imagen ya sin el fondo
    """
    img = pygame.image.load(ruta).convert()  
    img.set_colorkey((0, 0, 0))             
    return img.convert_alpha()  