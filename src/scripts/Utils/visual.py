import pygame

class AnimacionExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y, radio_pixeles):
        super().__init__()
        
        diametro = radio_pixeles * 2
        
        # 1. Cargamos las DOS imágenes (pueden ser simples círculos o destellos de diferente color)
        img1 = pygame.image.load("pacman_tp//assets//imagenes//items//explosion_roja.png").convert_alpha()
        img2 = pygame.image.load("pacman_tp//assets//imagenes//items//explosion_naranja.png").convert_alpha()
        
        # Las escalamos al diámetro exacto del impacto (las 10 celdas)
        self.frames = [
            pygame.transform.scale(img1, (int(diametro), int(diametro))),
            pygame.transform.scale(img2, (int(diametro), int(diametro)))
        ]
            
        self.frame_actual = 0
        self.image = self.frames[self.frame_actual]
        self.rect = self.image.get_rect(center=(x, y))
        
        # 2. Control de tiempo: parpadeo y duración total
        self.tiempo_creacion = pygame.time.get_ticks()
        self.ultimo_cambio = self.tiempo_creacion
        
        self.velocidad_parpadeo = 100 # Cada cuántos milisegundos cambia de color (100 = súper frenético)
        self.duracion_total = 500     # Cuánto tiempo se queda la explosión en pantalla en total (medio segundo)

    # Agregamos *args y **kwargs para que acepte ventana, delta_time, escena, eventos, etc.
    def update(self, *args, **kwargs):
        ahora = pygame.time.get_ticks()
        
        # 1. Chequeamos si ya es hora de desaparecer
        if ahora - self.tiempo_creacion > self.duracion_total:
            self.kill()
            return 
            
        # 2. Si todavía vive, chequeamos si toca alternar la imagen
        if ahora - self.ultimo_cambio > self.velocidad_parpadeo:
            self.ultimo_cambio = ahora
            
            # Cambia de 0 a 1, o de 1 a 0 constantemente
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)
            self.image = self.frames[self.frame_actual]
            
    def draw(self, ventana):
        # Dibujamos la imagen actual en la posición de su rect
        ventana.blit(self.image, self.rect)