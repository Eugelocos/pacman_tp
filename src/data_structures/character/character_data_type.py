import os
import sys
import pygame
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from data_structures.entity import Entity
from scripts.Movimiento.movimiento import manejar_movimiento
import constantes as c

class Personaje(Entity):
    """Clase hija de Entity, maneja logica especifica de entidades con movimiento dinamico

    Args:
        Entity (Entity): Entidad base, es la entidad de quien heredan todos los modelos de datos, posee funciones por defecto que pueden ser sobreescritas
    """
    DIRECTIONS={"arriba":(0,-1),"abajo":(0,1),"derecha":(1, 0),"izquierda":(-1,0), "idle":(0,0)}
    def __init__(self,position: tuple, visibility: bool, direction: str, tile_size: int|float, sprite: str, es_jugador: bool):
        """Inicializa los atributos necesarios de la clase

        Args:
            position (tuple): Posicion de la entidad en pixeles
            visibility (bool): Booleana que determina si se dibujara o no
            direction (str): Clave especifica del diccionario DIRECTIONS que se utiliza para mejorar legibilidad del codigo, representa la direccion inicial.
            tile_size (int | float): EL tamano de celda por el que se escalara la imagen, caulquier entidad lo tiene
            sprite (str): Ruta de la imagen que utilizara, si es None se utiliza un pygame.rect simple.
            es_jugador (bool): Flag que representa si el Personaje es jugador o no.
        """
        super().__init__(position, visibility, tile_size, sprite)

        self.velocidad=c.VELOCIDAD_BASE
        self.direction=self.DIRECTIONS[direction]
        self.proxima_direccion=self.direction       # buffer que almacena la siguiente direccion
        self.frames = [self.image]
        self.frame_actual = 0
        self.frame_timer = 0
        self.frame_delay = 40
        self.es_jugador = es_jugador
        self.pos_aparicion = position


    def cambiar_direccion(self, new_dir: str):
        """Helper que maneja el cambio de direccion

        Args:
            new_dir (str): Nueva direccion, clave especifica del diccionario DIRECTIONS
        """
        self.direction=self.DIRECTIONS[new_dir]
        if hasattr(self, 'cambiar_sprite_por_direccion'):
            self.cambiar_sprite_por_direccion()
            self.frame_timer=0
            self.frame_actual=0
    def actualizar_animacion(self, delta_time: float|int):
        """Sobreescribe el placeholder de la clase Entity, se utiliza para manejar la actualizacion de frames en animaciones

        Args:
            delta_time (float|int): Tiempo que tarda el ordenador en procesar y mostrar un único fotograma (o frame) en pantalla
        """
        self.frame_timer += delta_time
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)  # asi no se pasa de la cantidad de frames de la animacion actual
            self.image=self.frames[self.frame_actual]
    
    def update(self, ventana: pygame.Surface, delta_time: int|float, escena=None, eventos=None):
        """Sobreescribe parcialmente el metodo update de la clase Entity, maneja el movimiento de la entidad tipo Personaje

        Args:
            ventana (pygame.Surface): Superficie donde se renderizara la entidad
            delta_time (float|int): Tiempo que tarda el ordenador en procesar y mostrar un único fotograma (o frame) en pantalla
            escena (object, optional): Objeto de la escena a quien pertenece la entidad. Defaults to None.
            eventos (_type_, optional): Lista de eventos de pygame. Defaults to None.
        """
        manejar_movimiento(self, escena, delta_time)
        super().update(ventana, delta_time, escena, eventos)


