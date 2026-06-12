import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.Mapa.crear_mapa import crear_mapa
import constantes as c 

class GridManager:
    """Clase que maneja los mapeos entre posiciones discretas y continuas
    """
    def __init__(self, matriz_mapa,cell_size=c.TAMAÑO_PARED, tipos_enemigos: list[tuple[str, tuple[int,int]]]=[("fantasma_amarillo", (0,2)), ("fantasma_rosa", (0,29)), ("fantasma_rojo", (30,2)), ("fantasma_cian", (30, 29))]):
        """Inicializa el GridManager con una cuadrícula y un tamaño de celda."""
        self.grid=crear_mapa(matriz_mapa, None, tipos_enemigos)
        self.width = c.MAPA_ANCHO
        self.height = c.MAPA_ALTO
        self.cell_size = cell_size

    def check_position(self, pos):
        """Verifica si la posición es válida (es una tupla o lista de dos números) y si está dentro de los límites del grid."""
        if not (isinstance(pos, (list, tuple)) and len(pos) == 2):
            return False
        x, y = pos
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
            return False
        return self.check_limits(pos)
    
    def check_limits(self, pos):
        """Verifica si la posicion esta dentro de los limites del grid"""
        x, y = self.world_to_grid((int(pos[0]), int(pos[1])))
        
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get_cell_by_position(self, pos, entities):
        """Obtiene la entidad en la celda correspondiente a la posición dada, si existe."""
        if not self.check_position(pos): return

        celda_buscada=self.world_to_grid(pos)
        for entity in entities:
            snapped_pos=self.world_to_grid((entity.rect.centerx, entity.rect.centery))
            if not self.check_position(snapped_pos): continue
            if snapped_pos==celda_buscada:
                return entity        
    
    def world_to_grid(self, pos):
        """Convierte una posición en el mundo a coordenadas de cuadrícula."""
        x, y = pos
        tile_size = self.cell_size
        return (int(x // tile_size), int(y // tile_size))
    
    def grid_to_world(self, pos):
        """Convierte coordenadas de cuadrícula a una posición en el mundo (centro de la celda)."""
        x, y = pos
        tile_size = self.cell_size
        return (x * tile_size + self.cell_size // 2, y * tile_size + self.cell_size // 2)
    
    def grid_to_world_center(self, grid_pos):
        """Devuelve el centro de la celda en píxeles"""
        x, y = grid_pos
        return (x * self.cell_size + self.cell_size // 2,
                y * self.cell_size + self.cell_size // 2)

    def snap_position(self, pos, direccion):
        """Ajusta una posición a la cuadrícula más cercana."""
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
         Detecta si hay una entidad en la celda hacia la que se está moviendo.
    
        Convierte la posición actual en píxeles a coordenadas de celda, calcula
        la celda futura sumando el vector de dirección, y devuelve la entidad
        que se encuentre en esa celda si existe.

        """
        if not self.check_position(pos): return
        celda_actual=self.world_to_grid(pos)
        celda_futura=((celda_actual[0]+direccion[0]),(celda_actual[1]+direccion[1]))
        if not self.check_position(self.grid_to_world(celda_futura)): return
        entidad=self.get_cell_by_position(self.grid_to_world(celda_futura),entities)     
        return entidad 
    
    #funcion para "teletransportar" una entidad de tunel a tunel
    def wrap_position(self, celda):
        x, y = celda
        if x < 0:
            x = self.width - 1
        elif x >= self.width:
            x = 0
        return (x, y)
        
        
        
        

