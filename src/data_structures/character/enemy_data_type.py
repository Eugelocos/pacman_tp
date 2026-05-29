from .character_data_type import Character

class Enemy(Character):
    def __init__(self, position, visibility, sprite, direction, state, target):
        super().__init__(position, visibility, sprite, direction)
        self.state=state
        self.pos_inicial=0
        self.target=target

    
    def change_sprite_by_direction(self):
        self.ruta="pacman_tp/assets/images/"+self.nombre_ruta+"/"
        if self.direction[0]==0 and self.direction[1]==-1:
            self.ruta=self.ruta+f"/abajo/{self.sprite}_abajo_1.png"
        elif self.direction[0]==0 and self.direction[1]==1:
            self.ruta=self.ruta+f"/arriba/{self.sprite}_arriba_1.png"
        elif self.direction[1]==0:
            self.ruta=self.ruta+f"/lateral/{self.sprite}_horizontal_1.png"