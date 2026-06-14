import pygame

class AnimacionExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y, radio_pixeles):
        super().__init__()
        
        diametro = radio_pixeles * 2
        
        img1 = pygame.image.load("pacman_tp//assets//imagenes//items//explosion_roja.png").convert_alpha()
        img2 = pygame.image.load("pacman_tp//assets//imagenes//items//explosion_naranja.png").convert_alpha()
        
        self.frames = [
            pygame.transform.scale(img1, (int(diametro), int(diametro))),
            pygame.transform.scale(img2, (int(diametro), int(diametro)))
        ]
            
        self.frame_actual = 0
        self.image = self.frames[self.frame_actual]
        self.rect = self.image.get_rect(center=(x, y))
        
        #parpadeo
        self.tiempo_creacion = pygame.time.get_ticks()
        self.ultimo_cambio = self.tiempo_creacion
        
        self.velocidad_parpadeo = 100 # cada cuantos ms cambia de color (100 = muy frenético)
        self.duracion_total = 500     # cuanto tiempo se queda la explosion en pnartalla(medio segundo)

    def update(self, pantalla, delta_time, escena, eventos=None):
        ahora = pygame.time.get_ticks()
        
        if ahora - self.tiempo_creacion > self.duracion_total:
            self.kill()
            return 
            
        if ahora - self.ultimo_cambio > self.velocidad_parpadeo:
            self.ultimo_cambio = ahora
            
            #cambio constante entre 0 y 1
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)
            self.image = self.frames[self.frame_actual]
            
    def draw(self, ventana):
        ventana.blit(self.image, self.rect)