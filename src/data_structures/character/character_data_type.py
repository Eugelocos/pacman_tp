from entity import Entity


class Character(Entity):

    def __init__(self,position, visibility, sprite, direction):
        super().__init__(position, visibility, sprite)
        self.velocity=5
        self.direction=self.DIRECTIONS[direction]
        self.DIRECTIONS={
        "UP":(0,-1),
        "DOWN":(0,1),
        "RIGHT":(0,1),
        "LEFT":(0,-1),   
        }
        self.nombre_ruta=sprite
        self.ruta="pacman_tp/assets/images/"+self.nombre_ruta+"/"+self.nombre_ruta+"_1.png"
    def changeDir(self, new_dir):
        self.direction=new_dir

