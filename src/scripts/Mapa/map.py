import pygame
import pacman_tp.src.scripts.constantes as c
from ...data_structures.character.character_data_type import Character 
from ...data_structures.entity import Entity 

#abrir el mapa 

with open("pacman_tp/assets/Mapa/mapa.txt","r") as mapa:
    matriz_mapa=[]
    caracteres_validos=["X",".","P","o"," ","G","-","T"]
    for linea in mapa:
        l=linea.strip()
        for letra in l:
            if letra not in caracteres_validos:
                print("mapa invalido")
                break    
        matriz_mapa.append(l)

def crear_mapa(matriz,ventana):
    for x in range(31):
        for y in range(28):
            if matriz[x][y]=="X":
                pared=pygame.Rect(y*c.TAMAÑO_PARED,x*c.TAMAÑO_PARED,c.TAMAÑO_PARED,c.TAMAÑO_PARED)
                pygame.draw.rect(ventana,c.AZUL,pared)
            elif matriz[x][y]==".":
                #pun_peq=Item(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,1,[punto_pequeño])
                #grupo_items.add(pun_peq)
            elif matriz[x][y]=="o":
                #pun_gran=Item(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,2,[punto_grande])
                #grupo_items.add(pun_gran)
            elif matriz[x][y]=="P":
                #crear jugador 
                #jugador=Personaje(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,c.COLOR_PERSONAJE,animaciones) 
            elif matriz[x][y]=="G":
                #crear enemigo
                #for i in range(4):
                #    fantasma_amarillo=Personaje(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,c.COLOR_PAREDES,animaciones_enemigos[0])
                #    fantasma_cian=Personaje(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,c.COLOR_PAREDES,animaciones_enemigos[1])
                #    fantasma_rojo=Personaje(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,c.COLOR_PAREDES,animaciones_enemigos[2])
                #    fantasma_rosa=Personaje(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,c.COLOR_PAREDES,animaciones_enemigos[3])

                #crear lista de enemigos
                lista_enemigos=[]
                lista_enemigos.append(fantasma_amarillo)
                lista_enemigos.append(fantasma_cian)
                lista_enemigos.append(fantasma_rojo)
                lista_enemigos.append(fantasma_rosa)

    return jugador,lista_enemigos
        



        
# ---------------
# DUPLICADO
# ---------------


#abrir el mapa 

with open("pacman_tp/assets/scripts/Mapa/mapa.txt","r") as mapa:
    matriz_mapa=[]
    caracteres_validos=["X",".","P","o"," ","G","-","T"]
    for linea in mapa:
        l=linea.strip()
        for letra in l:
            if letra not in caracteres_validos:
                print("mapa invalido")
                break    
        matriz_mapa.append(l)

#funcion de crear el mapa
def crear_mapa(matriz,ventana):
    for x in range(31):
        for y in range(28):
            if matriz[x][y]=="X":
                pared=pygame.Rect(y*c.TAMAÑO_PARED,x*c.TAMAÑO_PARED,c.TAMAÑO_PARED,c.TAMAÑO_PARED)
                pygame.draw.rect(ventana,c.AZUL,pared)
            elif matriz[x][y]==".":
                pun_peq=Item(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,1,[punto_pequeño])
                grupo_items.add(pun_peq)
            elif matriz[x][y]=="o":
                pun_gran=Item(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,2,[punto_grande])
                grupo_items.add(pun_gran)
            elif matriz[x][y]=="P":
                #crear jugador 
                jugador=Personaje(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,c.COLOR_PERSONAJE,animaciones) 
            elif matriz[x][y]=="G":
                #crear enemigo
                for i in range(4):
                    fantasma_amarillo=Personaje(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,c.COLOR_PAREDES,animaciones_enemigos[0])
                    fantasma_cian=Personaje(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,c.COLOR_PAREDES,animaciones_enemigos[1])
                    fantasma_rojo=Personaje(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,c.COLOR_PAREDES,animaciones_enemigos[2])
                    fantasma_rosa=Personaje(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,c.COLOR_PAREDES,animaciones_enemigos[3])

                #crear lista de enemigos
                lista_enemigos=[]
                lista_enemigos.append(fantasma_amarillo)
                lista_enemigos.append(fantasma_cian)
                lista_enemigos.append(fantasma_rojo)
                lista_enemigos.append(fantasma_rosa)

    return jugador,lista_enemigos

class GridManager:
    """Clase que maneja los mapeos entre posiciones discretas y continuas
    """
    def __init__(self, grid, cell_size=32.0):
        """Inicializa el GridManager con una cuadrícula y un tamaño de celda."""
        self.grid=grid
        self.width = len(grid[1])
        self.height = len(grid)
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
        x, y = self.world_to_grid(int(pos[0]), int(pos[1]))
        
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

