import pygame

class Entity(pygame.sprite.Sprite):

    def __init__(self, position, visibility, sprite, tile_size):
        super().__init__()
        self.visibility=visibility
        self.image=pygame.image.load(sprite).convert_alpha()
        self.image=pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect=self.image.get_rect()
        x,y=position
        self.rect.x=x
        self.rect.y=y

