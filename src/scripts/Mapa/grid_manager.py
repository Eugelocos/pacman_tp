from .crear_mapa import crear_mapa
import constantes as c 

class GridManager:
    """Clase que maneja los mapeos entre posiciones discretas y continuas
    """
    def __init__(self, matriz_mapa,cell_size=32.0, tipos_enemigos: list[str]=["Blinky", "Pinky", "Inky", "Clyde"]):
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
        for entity in entities:
            snapped_pos=self.snap_position((entity.x, entity.y))
            if not self.check_position(snapped_pos): continue
            if snapped_pos==pos:
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
        return (x * tile_size + tile_size / 2, y * tile_size + tile_size / 2)

    def snap_position(self, pos):
        """Ajusta una posición a la cuadrícula más cercana."""
        if not self.check_position(pos): return
        x,y=pos
        snapped_x=round(x/self.cell_size)*self.cell_size
        snapped_y=round(y/self.cell_size)*self.cell_size
        return (snapped_x, snapped_y)
    
    def check_collision(self, pos, direccion: str, entities):
        """
         Detecta si hay una entidad en la celda hacia la que se está moviendo.
    
        Convierte la posición actual en píxeles a coordenadas de celda, calcula
        la celda futura sumando el vector de dirección, y devuelve la entidad
        que se encuentre en esa celda si existe.

        """
        
        celda_actual=self.world_to_grid(pos)
        celda_futura=((celda_actual[0]+c.DIRECCIONES[direccion][0]),(celda_actual[1]+c.DIRECCIONES[direccion][1]))
        entidad=self.get_cell_by_position(self.grid_to_world(celda_futura),entities)     
        return entidad 
        
        
        
        

