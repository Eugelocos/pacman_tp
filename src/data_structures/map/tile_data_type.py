import sys
import os
import pygame
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from data_structures.entity import Entity

class Tile(Entity):
    """Representa una celda individual del mapa del juego.

    Cada tile puede ser:
        - Pared: Bloquea el movimiento (is_wall = True).
        - Pasillo: Transitable, puede contener pellet o power pellet.
        - Tunel: Zona especial donde fantasmas y jugador se teletransportan.
        - Puerta: Entrada/salida de la casa de fantasmas (solo transitable por ellos).

    Args:
        Entity: Superclase que maneja atributos basicos de entidades.
    """
    def __init__(self, posicion: tuple, visibility: bool, sprite: str, is_wall: bool, tile_size: int|float):
        """Inicializa los atributos de la clase Tile

        Args:
            position (tuple): Representa el centro de la entidad en pixeles
            visibility (bool): Si se dibuja o no se dibuja
            tile_size (int | float): EL tamano de celda por el que se escalara la imagen, caulquier entidad lo tiene
            sprite (str, optional): Ruta de la imagen que utilizara, si es None se utiliza un pygame.rect simple.
            is_wall (bool): Representa si es pared o no
        
        Notes: Las celdas se crean en crear_mapa desde el GRidManager al cargar el mapa
        """
        super().__init__(posicion, visibility, tile_size, sprite)
        self.is_wall = is_wall
        self.es_puerta = False
        self.contains_pellet = False
        self.contains_power_pellet = False
        self.is_tunnel = False
        
    def place_pellet(self):
        """Coloca un pellet en el tile
        """
        self.contains_pellet = True
    def place_power_pellet(self):
        """Coloca un power pellet en el tile
        """
        self.contains_power_pellet = True
    def remove_pellet(self):
        """Remueve el pellet del tile
        """
        self.contains_pellet = False
        
    def remove_power_pellet(self):
        """Remueve el power pellet del tile
        """
        self.contains_power_pellet = False
        
    def draw(self, ventana: pygame.Surface):
        """Renderiza la imagen solo si es pared o puerta o tiene power pellet o pellet
        
        Condiciones de dibujo:
            - Contiene pellet o power pellet (visible para el jugador).
            - Es pared (is_wall = True).
            - Es puerta (es_puerta = True).

        Args:
            ventana (pygame.Surface): Superficie donde se renderizara la entidad.

        Notes: Los tiles transitables vacios (pasillos) NO se dibujan, solo
              se ven el fondo negro y los elementos que contienen.
        """
        if self.contains_pellet or self.contains_power_pellet or self.is_wall or self.es_puerta:
            super().draw(ventana)
