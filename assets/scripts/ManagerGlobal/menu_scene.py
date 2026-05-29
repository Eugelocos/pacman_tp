import pygame

class MenuScene():
    def __init__(self, game_manager):
        self.game_manager=game_manager
    def update(self):
        estado_escena_menu=0
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                estado_escena_menu=-1
            elif event.type==pygame.ENTER:
                if event.button==1:
                    estado_escena_menu=1
    def render(self, screen):
        pass