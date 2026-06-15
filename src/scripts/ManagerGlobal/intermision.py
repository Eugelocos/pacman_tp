import pygame
import os
import sys
import math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.funciones_aux import dibujar_texto

import constantes as c
from scripts.ManagerGlobal.escena import EscenaBase


class Intermision(EscenaBase):
    """Escena de transicion entre niveles.

    Muestra el numero de nivel, un mensaje "PREPARESE", el puntaje actual
    y una animacion de Pacman cruzando la pantalla. Dura 3 segundos
    y luego cambia a la escena de juego.

    Attributes:
        frames (list): Lista de frames de animacion de Pacan (variable de clase).
        nivel_siguiente (int): Numero del nivel que esta por comenzar.
        timer (float): Tiempo transcurrido en la escena (segundos).
        duracion (int): Duracion total de la escena en segundos (3).
        alpha (int): Valor de transparencia para efecto fade (no implementado).
        mostrar_puntos (bool): Flag para mostrar puntaje.
        font_grande (pygame.font.Font): Fuente de 48px para el nivel.
        font_mediana (pygame.font.Font): Fuente de 32px para el mensaje.
        font_pequena (pygame.font.Font): Fuente de 20px para el puntaje.
        frame_actual (int): Indice del frame actual de animacion.
        frame_timer (float): Acumulador de tiempo para cambio de frame.
        frame_delay (int): Tiempo entre cambios de frame (ms).
        x_pacman (float): Posicion X actual de Pacman en la animacion.
        sonido (pygame.mixer.Sound): Sonido que se reproduce al salir de la escena.
    """
    frames = None
    def __init__(self, game_manager):
        """Inicializa la escena de intermision.

        Carga fuentes, animacion de PacMan y configura el temporizador.

        Args:
            game_manager: Referencia al administrador principal del juego.
        """
        super().__init__(game_manager)
        self.nivel_siguiente = game_manager.nivel
        self.timer = 0
        self.duracion = 3  # seg
        self.alpha = 0  # fade(degrade)
        self.mostrar_puntos = True
        

        self.font_grande = pygame.font.Font(os.path.join("pacman_tp","assets", "fonts", "PressStart2P.ttf"), 48)
        self.font_mediana = pygame.font.Font(os.path.join("pacman_tp","assets", "fonts", "PressStart2P.ttf"), 32)
        self.font_pequena = pygame.font.Font(os.path.join("pacman_tp","assets", "fonts", "PressStart2P.ttf"), 20)
        
        self.frame_actual = 0
        self.frame_timer = 0
        self.frame_delay = 40
        self.x_pacman = -100

        if not Intermision.frames:
            Intermision.frames = [pygame.transform.scale(pygame.image.load(f"pacman_tp/assets/imagenes/characters/pacman/horizontal/pacman_{i}.png").convert_alpha(), (30, 30)) for i in range(4)]

        self.sonido = pygame.mixer.Sound(c.EFECTOS["jugar"])
        
    def on_enter(self):
        """Se ejecuta al entrar a la escena. Reinicia timer y fade, pausa rutinas."""
        self.timer = 0
        self.alpha = 0
        
        self.game_manager.rutina_manager.pausar()
    
    def on_exit(self):
        """Se ejecuta al salir de la escena. Reproduce sonido de inicio."""
        self.sonido.play()
        
    def update(self, delta_time: int|float, eventos = None):
        """Actualiza la escena de intermision.

        Incrementa el timer, mueve a PacMan horizontalmente y actualiza
        su animacion. Cuando el timer alcanza la duracion, cambia a GameScene.

        Args:
            delta_time (int | float): Tiempo transcurrido desde el ultimo frame (en ms).
            eventos(_type_): Lista de eventos de pygame.
        """
        delta_seg = delta_time / 1000.0
        self.timer += delta_seg
        self.x_pacman = self.game_manager.ventana.get_width() * (self.timer / self.duracion)
        self.actualizar_animacion(delta_time)

        if self.timer >= self.duracion:
            self.game_manager.rutina_manager.reiniciar()
            self.game_manager.rutina_manager.reanudar()
            self.game_manager.change_scene("game")
    
    def render(self):
        """Renderiza la escena de intermision.

        Dibuja en orden:
            1. Fondo negro.
            2. Texto "NIVEL X" en amarillo.
            3. Texto "PREPARESE" en blanco.
            4. Texto "PUNTAJE: Y" en verde.
            5. Animacion de PacMan cruzando la pantalla.
        """
        ventana = self.game_manager.ventana
        ancho = ventana.get_width()
        alto = ventana.get_height()
        
        ventana.fill(c.COLOR_BG)
        
        texto_nivel = f"NIVEL {self.nivel_siguiente}"
        x = ancho // 2
        y = alto // 3
        dibujar_texto(texto_nivel, ventana, self.font_grande, c.AMARILLO, x, y, True)
        
        texto_prepare = "PREPARESE"
        x = ancho // 2
        y = alto // 2
        dibujar_texto(texto_prepare, ventana, self.font_mediana, c.BLANCO, x, y, True)
        
        texto_score = f"PUNTAJE: {self.game_manager.score}"
        x = ancho // 2
        y = alto * 3 // 4
        dibujar_texto(texto_score, ventana, self.font_pequena, c.VERDE, x, y, True)

        pacman_y = alto // 2 + 50
        ventana.blit(Intermision.frames[self.frame_actual], (self.x_pacman, pacman_y))
    

    def actualizar_animacion(self, delta_time: int|float):
        """Actualiza la animacion de Pac-Man.

        Cambia de frame cada frame_delay milisegundos.

        Args:
            delta_time (int | float): Tiempo transcurrido desde el ultimo frame (en ms).
        """
        self.frame_timer += delta_time
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.frame_actual = (self.frame_actual + 1) % len(Intermision.frames)
            self.image=Intermision.frames[self.frame_actual]
