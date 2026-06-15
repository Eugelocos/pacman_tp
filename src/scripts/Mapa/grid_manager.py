"""
Módulo del Administrador de la Grilla (grid_manager.py)

Acá está la clase GridManager, que es la encargada de traducir todo el tiempo 
el mundo real (píxeles en la pantalla) al mundo lógico (celdas de la grilla).
Nos sirve para saber en qué casillero exacto está parado Pac-Man o un fantasma,
y manejar la lógica del mapa (como los túneles).
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.Mapa.crear_mapa import crear_mapa
import constantes as c 

class GridManager:
    """Clase que maneja los mapeos entre posiciones discretas y continuas
    """
    def __init__(self, matriz_mapa,cell_size=c.TAMAÑO_PARED, tipos_enemigos: list[tuple[str, tuple[int,int]]]=[("fantasma_amarillo", (0,2)), ("fantasma_rosa", (0,29)), ("fantasma_rojo", (30,2)), ("fantasma_cian", (30, 29))]):
        """
        Inicializa el GridManager. Genera los objetos físicos (paredes, pastillas)
        leyendo la matriz del mapa y guarda las dimensiones de la grilla.

        Args:
            matriz_mapa (list): La lista de strings que leímos del txt del mapa.
            cell_size (int, optional): El tamaño en píxeles de cada celda cuadrada.
            tipos_enemigos (list, optional): Lista con los fantasmas elegidos y sus esquinas asignadas.
        """
        self.grid=crear_mapa(matriz_mapa, None, tipos_enemigos)
        self.width = c.MAPA_ANCHO
        self.height = c.MAPA_ALTO
        self.cell_size = cell_size

    def check_position(self, pos):
        """
        Se fija si la posición que le pasás tiene sentido (es una tupla de 2 números) 
        y no se va afuera de los bordes lógicos del mapa.

        Args:
            pos (tuple): Coordenadas en píxeles (x, y).

        Returns:
            bool: True si la posición es válida y está dentro del mapa, False si no.
        """
        
        if not (isinstance(pos, (list, tuple)) and len(pos) == 2):
            return False
        x, y = pos
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
            return False
        return self.check_limits(pos)
    
    def check_limits(self, pos):
        """
        Verifica matemáticamente si una coordenada en píxeles cae dentro de nuestra grilla.

        Args:
            pos (tuple): Coordenadas en píxeles (x, y).

        Returns:
            bool: True si está dentro, False si se salió del mapa.
        """
        x, y = self.world_to_grid((int(pos[0]), int(pos[1])))
        
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get_cell_by_position(self, pos, entities):
        """
        Busca qué entidad (pared, túnel, pastilla) está físicamente apoyada en 
        esa coordenada exacta de la pantalla.

        Args:
            pos (tuple): Posición en píxeles (x, y) a revisar.
            entities (Group/list): Lista de todas las entidades del juego.

        Returns:
            Entity | None: Te devuelve el objeto que está en esa celda, o None si está vacía.
        """
        if not self.check_position(pos): return

        celda_buscada=self.world_to_grid(pos)
        for entity in entities:
            snapped_pos=self.world_to_grid((entity.rect.centerx, entity.rect.centery))
            if not self.check_position(snapped_pos): continue
            if snapped_pos==celda_buscada:
                return entity        
    
    def world_to_grid(self, pos):
        """
        Traduce de píxeles a celdas lógicas. Por ejemplo, te pasa de (170px, 340px) 
        a la columna 10, fila 20.

        Args:
            pos (tuple): Coordenadas en píxeles (x, y).

        Returns:
            tuple: Coordenadas lógicas de la grilla (columna, fila).
        """
        x, y = pos
        tile_size = self.cell_size
        return (int(x // tile_size), int(y // tile_size))
    
    def grid_to_world(self, pos):
        """
        Hace el camino inverso: le pasás una celda y te devuelve las coordenadas 
        en píxeles exactas del CENTRO de esa celda. 

        Args:
            pos (tuple): Coordenadas lógicas de la grilla (columna, fila).

        Returns:
            tuple: Coordenadas en píxeles (x, y) marcando el centro de la celda.
        """
        x, y = pos
        tile_size = self.cell_size
        return (x * tile_size + self.cell_size // 2, y * tile_size + self.cell_size // 2)
    
    def grid_to_world_center(self, grid_pos):
        """
        Hace exactamente lo mismo que grid_to_world. Devuelve el centro de la celda en píxeles.

        Args:
            grid_pos (tuple): Coordenadas de la celda (x, y).

        Returns:
            tuple: Coordenadas del centro en píxeles.
        """
        x, y = grid_pos
        return (x * self.cell_size + self.cell_size // 2,
                y * self.cell_size + self.cell_size // 2)

    def snap_position(self, pos, direccion):
        """
        Ajusta una posición "desalineada" a los rieles lógicos de la cuadrícula.
        Ideal para que el personaje se encarrille perfecto al doblar.

        Args:
            pos (tuple): Posición actual en píxeles.
            direccion (tuple): Vector de dirección en la que se mueve (ej: (1, 0)).

        Returns:
            tuple: Nueva posición en píxeles ya encarrilada a la grilla.
        """
        if not self.check_position(pos): return
        x,y=pos
        grid_x, grid_y=self.world_to_grid(pos)
        if direccion==(0,0):        
            snapped_x=grid_x*self.cell_size
            snapped_y=grid_y*self.cell_size
            return (snapped_x, snapped_y)
        elif direccion[1]!=0:
            snapped_x=grid_x*self.cell_size
            return (snapped_x, y)
        elif direccion[0]!=0:
            snapped_y=grid_y*self.cell_size
            return (x, snapped_y)
        return pos
    
    def check_collision(self, pos, direccion, entities):
        """
        Calcula hacia dónde te vas a mover (posición + dirección), y te dice 
        si en esa celda futura hay alguna entidad estorbando.

        Args:
            pos (tuple): Tu coordenada actual en píxeles.
            direccion (tuple): Hacia dónde querés ir (ej: (0, -1) para arriba).
            entities (Group/list): Todas las entidades del juego.

        Returns:
            Entity | None: La entidad con la que vas a chocar, o None si está despejado.
        """
        if not self.check_position(pos): return
        celda_actual=self.world_to_grid(pos)
        celda_futura=((celda_actual[0]+direccion[0]),(celda_actual[1]+direccion[1]))
        if not self.check_position(self.grid_to_world(celda_futura)): return
        entidad=self.get_cell_by_position(self.grid_to_world(celda_futura),entities)     
        return entidad 
    
    #funcion para "teletransportar" una entidad de tunel a tunel
    def wrap_position(self, celda):
        """
        La magia del túnel de Pac-Man. Si te salís del mapa por un lado, 
        te teletransporta lógicamente hacia la otra punta.

        Args:
            celda (tuple): Coordenadas de la grilla a la que te querías mover.

        Returns:
            tuple: La nueva coordenada en la grilla corregida por el túnel.
        """
        x, y = celda
        if x < 0:
            x = self.width - 1
        elif x >= self.width:
            x = 0
        return (x, y)
        
        
        
        

