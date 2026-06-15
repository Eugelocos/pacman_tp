
import os
import sys
import pygame
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import constantes as c
from data_structures.entity import Entity
from scripts.ManagerGlobal.game_scene import GameScene
from scripts.ManagerGlobal.menu_scene import WelcomeScene, SelectFantasmas
from scripts.ManagerGlobal.game_over import GameOver
from Mapa.map import matriz_mapa
from Mapa.grid_manager import GridManager
from scripts.ManagerGlobal.rutina_manager import RutinaManager
from scripts.ManagerGlobal.intermision import Intermision

class GameManager():
    """Administrador principal del juego. Gestiona la ventana, las escenas, los recursos y el bucle principal.

    Esta clase es el corazon del juego. Coordina:
    - El cambio entre escenas (menu, juego, game over, etc.)
    - El escalado de la pantalla (mantiene la proporcion 476x612)
    - El estado de pausa
    - La musica de fondo segun la escena activa
    - El grid del mapa y las entidades del juego

    Attributes:
        pausado (bool): Indica si el juego esta en pausa.
        entities (pygame.sprite.Group): Grupo con todas las entidades del juego.
        ventana (pygame.Surface): Superficie interna de resolucion fija (476x612).
        ventana_real (pygame.Surface): Superficie de pantalla real (redimensionable).
        high_score (int): Puntaje mas alto alcanzado.
        score (int): Puntaje actual.
        nivel (int): Nivel actual del juego.
        tipos_enemigos (list): Lista de enemigos seleccionados por el jugador.
        grid_manager (GridManager): Administrador de la grilla del mapa.
        rutina_manager (RutinaManager): Administrador de rutinas (scatter/chase y asustado).
        celdas_pasillo (list): Celdas transitables del mapa.
        scenes (dict): Diccionario con todas las escenas del juego.
        current_scene (str): Clave de la escena actual.
    """

    def __init__(self):
        """Inicializa el GameManager, la ventana, el grid, las escenas y los recursos.

        Crea la ventana interna de 476x612 y la ventana real redimensionable.
        Inicializa el grid del mapa, las entidades, las rutinas y las escenas.
        La escena inicial es "welcome".
        """
        self.pausado = False
        self.entities = pygame.sprite.Group()

        ANCHO_RETRO, ALTO_RETRO = 476, 612
        self.ventana = pygame.Surface((ANCHO_RETRO, ALTO_RETRO))

        self.ventana_real = pygame.display.set_mode(
            (c.ANCHO_VENTANA, c.ALTO_VENTANA), 
            pygame.RESIZABLE
        )
        with open("pacman_tp//assets//high_score") as archivo:
            self.high_score=int(archivo.readline())
        self.score=0 
        self.nivel=0
        self.tipos_enemigos=[] # [("fantasma_... ,  (esquina)"), ... ]
        self.grid_manager = GridManager(matriz_mapa)
        self.rutina_manager=RutinaManager(self)
        entidades_creadas, self.celdas_pasillo = self.grid_manager.grid
        for entity in entidades_creadas:
            self.add_entity(entity)

        self.scenes = {
            "welcome": WelcomeScene(self),
            "select_fantasmas": SelectFantasmas(self),
            "game": GameScene(self),
            "game_over": GameOver(self),
            "intermision": Intermision(self)
        }
        

        self.current_scene = "welcome"
        self.change_scene("welcome")

        

    def add_entity(self, entity: Entity):
        """Agrega una entidad al grupo de entidades del juego.

        Args:
            entity (Entity): Entidad (Jugador, Tile, Enemigo) que se agregara.
        """
        self.entities.add(entity)
    
    def remove_entity(self, entity: Entity):
        """Remueve una entidad del grupo de entidades del juego.

        Args:
            entity (Entity): Entidad (Jugador, Tile, Enemigo) que se removera.
        """
        self.entities.remove(entity)
    
    def change_scene(self, new_scene: object):
        """Cambia la escena activa y maneja la musica correspondiente.

        Ejecuta on_exit() de la escena actual, cambia a la nueva escena,
        ejecuta on_enter() de la nueva y reproduce la musica asociada.

        Args:
            new_scene: Clave de la nueva escena ("welcome", "game", "game_over", etc.).
        """
        if new_scene in self.scenes:
            self.scenes.get(self.current_scene).on_exit()
            self.current_scene=new_scene
            self.scenes.get(self.current_scene).on_enter()
        if new_scene in c.MUSICA:
            pygame.mixer.music.load(c.MUSICA[new_scene])
            pygame.mixer.music.play(loops=-1)
            pygame.mixer.music.set_volume(0.5)
        elif new_scene not in c.MUSICA:
            pygame.mixer.music.stop()

    def render(self):
        """Renderiza todo el juego y maneja la pantalla de pausa

        Si el juego esta en pausa, dibuja un overlay negro con el 
        texto Pausa. Si no, delega el renderizado a la escena actual. 
        Luego redimensiona la superficie interna a la ventana real manteniendo 
        proporcion y centrandola en el eje x.
        """
        ancho_actual, alto_actual = self.ventana_real.get_size()

        if self.pausado:
            s = pygame.Surface((self.ventana.get_width(), self.ventana.get_height()))
            s.set_alpha(128)
            s.fill((0, 0, 0))
            self.ventana.blit(s, (0, 0))
            
            fuente_pausa = pygame.font.Font(None, 74)
            texto_pausa = fuente_pausa.render("PAUSA", True, (255, 255, 255))
            rect_texto = texto_pausa.get_rect(center=(self.ventana.get_width() // 2, self.ventana.get_height() // 2))
            self.ventana.blit(texto_pausa, rect_texto)


        else:
            self.scenes.get(self.current_scene).render()

        escala = min(ancho_actual / c.ANCHO_VENTANA, alto_actual / c.ALTO_VENTANA)
        ancho_escalado = int(c.ANCHO_VENTANA * escala)
        alto_escalado = int(c.ALTO_VENTANA * escala)

        superficie_escalada = pygame.transform.scale(self.ventana, (ancho_escalado, alto_escalado))

        pos_x = (ancho_actual - ancho_escalado) // 2
        pos_y = (alto_actual - alto_escalado) // 2

        self.ventana_real.fill((0, 0, 0)) 
        self.ventana_real.blit(superficie_escalada, (pos_x, pos_y))
        pygame.display.flip()
    
    def update(self, delta_time=0, eventos=None):
        """Maneja la logica de pausa y la acutalizacion de la escena actual

        Si esta en pausa ejecuta logica propia para poder resumir el juego. 
        Si no, ejecuta la actualizacion de la escena actual junto a la actualizacion de rutina_manager

        Args:
            delta_time (int | float): Tiempo transcurrido desde el ultimo frame (en ms).
            eventos (_type_, optional): Lista de eventos de pygame. Defaults to None.
        """
        if eventos is None:
            eventos = pygame.event.get()
        #agregar logica de pausa, hacer update de la escena solo si no esta en pausa
        if self.pausado:
            for evento in eventos:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN or evento.key == pygame.K_ESCAPE:
                        self.pausado = False
        else:
            for evento in eventos:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.pausado = True
            self.rutina_manager.update(delta_time)
            self.scenes.get(self.current_scene).update(delta_time, eventos)

    def resetear_grilla(self):
        """Metodo que limpia el grupo de entidades y crea un nuevo GridManager, 
        luego anade las entidades del grid manager al grupo de entidades
        """
        self.entities.empty()

        self.grid_manager = GridManager(matriz_mapa, tipos_enemigos=self.tipos_enemigos)
        entidades_creadas, self.celdas_pasillo = self.grid_manager.grid
        for entity in entidades_creadas:
            self.add_entity(entity)

    def actualizar_enemigos(self, nuevos_enemigos: list[tuple[str, tuple[int,int]]]):
        """Metodo para actualizar los tipos de enemigos que utilizara el grid manager

        Args:
            nuevos_enemigos (list[tuple[str, tuple[int,int]]]): Lista de tuplas de enemigos donde el primer elemento 
                es el nombre del enemigo y el segundo es la esquina asignada a dicho enemigo como target para el modo Scatter
        """
        self.tipos_enemigos=nuevos_enemigos
        self.resetear_grilla()
