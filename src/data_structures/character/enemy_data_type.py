from .character_data_type import Character

class Enemy(Character):
    def __init__(self, position, visibility, sprite, direction, state, target):
        super().__init__(position, visibility, sprite, direction)
        self.state=state
        self.pos_inicial=0
        self.target=target

    
    def change_sprite_by_direction(self):
        self.ruta=f"pacman_tp/assets/images/{self.sprite}/"
        if self.direction[0]==0 and self.direction[1]==-1:
            ruta=ruta+f"/abajo/{self.sprite}_abajo_.png"