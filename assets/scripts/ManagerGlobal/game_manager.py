
import pygame


class GameManager():
    def __init__(self):
        self.entities=pygame.sprite.Group()
        self.scenes={}
        self.pantalla=pygame.display.set_mode((800,600))
        self.scenes={"menu": "Menu", "game": "Game", "game_over": "GameOver"}
        self.current_scene="menu"
    def add_entity(self, entity):
        self.entities.add(entity)
    def render(self, screen):
        for entity in self.entities:
            if entity.visibility:
                screen.blit(entity.image, entity.rect)
    def update(self):
        if self.current_scene=="menu":
            estado_escena_menu=0
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    estado_escena_menu=-1
                elif event.type==pygame.ENTER:
                    if event.button==1:
                        estado_escena_menu=1

        elif self.current_scene=="game":
            pass
        elif self.current_scene=="game_over":
            pass
