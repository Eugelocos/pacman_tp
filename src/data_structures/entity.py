import pygame

class Entity(pygame.sprite.Sprite):

    def __init__(self, position, visibility, tile_size, sprite=None):
        super().__init__()

        self.visibility=visibility
        if sprite:
            self.image=pygame.transform.scale(pygame.image.load(sprite).convert_alpha(), (tile_size, tile_size))
        else:
            self.image=None
        if self.image:
            self.rect = self.image.get_rect()
        else:
            self.rect = pygame.Rect(0, 0, tile_size, tile_size)
        self.tile_size=tile_size
        x,y=position
        x, y = position
        self.rect.centerx = x
        self.rect.centery = y
    def draw(self, pantalla):
        pantalla.blit(self.image, (self.rect.x, self.rect.y))
    def update(self, ventana,  delta_time, escena=None, eventos=None):
        self.actualizar_animacion(delta_time) 
        self.draw(ventana)
    def actualizar_animacion(self, delta_time):
        pass


