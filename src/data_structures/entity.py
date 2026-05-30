import pygame

class Entity(pygame.sprite.Sprite):

    def __init__(self, position, visibility, tile_size, sprite=None):
        super().__init__()

        print(sprite)
        self.visibility=visibility
        if sprite:
            self.image=pygame.transform.scale(pygame.image.load(sprite).convert_alpha(), (tile_size, tile_size))
        else:
            self.image=None
        if self.image:
            self.rect = self.image.get_rect()
        else:
            self.rect = pygame.Rect(0, 0, tile_size, tile_size)
        x,y=position
        self.rect.x=x
        self.rect.y=y
        self.tile_size=tile_size
    def draw(self, pantalla):
        pantalla.blit(self.image, (self.rect.x, self.rect.y))
    def update(self, pantalla, delta_time):
        self.actualizar_animacion(delta_time) 
        self.draw(pantalla)
    def actualizar_animacion(self, delta_time):
        pass


