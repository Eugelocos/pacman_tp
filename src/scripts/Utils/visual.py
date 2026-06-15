"""
Módulo de Efectos Visuales (visual.py)

Acá se encuentran las clases que manejan los efectos visuales extra del juego. 
Se encarga de la animación de explosión que deja el fantasma 
kamikaze (Artur) cuando detona.
"""

import pygame

class AnimacionExplosion(pygame.sprite.Sprite):
    """
    Sprite temporal que dibuja la explosión en pantalla. 
    Básicamente intercala dos imágenes (roja y naranja) súper rápido para dar 
    el efecto de parpadeo/fuego, y después de medio segundo se elimina sola.
    """
    
    def __init__(self, x, y, radio_pixeles):
        """
        Inicializa la explosión. Carga las dos imágenes, las achica o agranda 
        según el radio del daño y prepara los cronómetros.

        Args:
            x (int): Coordenada X donde va el centro de la explosión.
            y (int): Coordenada Y donde va el centro de la explosión.
            radio_pixeles (int): El radio de alcance de la explosión. Lo usamos 
                                 para calcular el diámetro total de la imagen.
        """
        super().__init__()
        #El diámetro es el doble del radio (lógica pura para el tamaño de la imagen)
        diametro = radio_pixeles * 2
        
        #se cargan las imagenes base con transparencia
        img1 = pygame.image.load("pacman_tp//assets//imagenes//items//explosion_roja.png").convert_alpha()
        img2 = pygame.image.load("pacman_tp//assets//imagenes//items//explosion_naranja.png").convert_alpha()
        
        #se escalan para que ocupen el area de daño 
        self.frames = [
            pygame.transform.scale(img1, (int(diametro), int(diametro))),
            pygame.transform.scale(img2, (int(diametro), int(diametro)))
        ]
            
        self.frame_actual = 0
        self.image = self.frames[self.frame_actual]
        self.rect = self.image.get_rect(center=(x, y))
        
        #timers para parpadeo
        self.tiempo_creacion = pygame.time.get_ticks()
        self.ultimo_cambio = self.tiempo_creacion
        
        self.velocidad_parpadeo = 100 # cada cuantos ms cambia de color (100 = muy frenético)
        self.duracion_total = 500     # cuanto tiempo se queda la explosion en pnartalla(medio segundo)

    def update(self, pantalla, delta_time, escena, eventos=None):
        """
        Actualiza la explosión frame a frame. Si ya pasó su tiempo de vida, 
        se auto-destruye. Si no, revisa si le toca cambiar de color para titilar.

        Args:
            pantalla (pygame.Surface): La ventana donde estamos dibujando.
            delta_time (int): Tiempo que pasó desde el último frame.
            escena (EscenaBase): Referencia a la escena actual (GameScene).
            eventos (list, optional): Lista de eventos de Pygame.
        """
        ahora = pygame.time.get_ticks()
        
        #Si ya pasó medio segundo, matamos el sprite para que deje de dibujarse y consumir memoria
        if ahora - self.tiempo_creacion > self.duracion_total:
            self.kill()
            return 
            
        #Si pasó el tiempo de parpadeo, cambiamos a la otra imagen
        if ahora - self.ultimo_cambio > self.velocidad_parpadeo:
            self.ultimo_cambio = ahora
            
            #cambio constante entre 0 y 1
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)
            self.image = self.frames[self.frame_actual]
            
    def draw(self, ventana):
        """
        Pega la imagen actual de la explosión en la pantalla.

        Args:
            ventana (pygame.Surface): La pantalla principal donde renderizamos.
        """
        ventana.blit(self.image, self.rect)