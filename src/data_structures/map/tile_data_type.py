from ..entity import Entity

class Tile(Entity):
    def __init__(self, pos, activo, sprite, is_wall):
        super().__init__(pos, activo, sprite)
        self.is_wall = is_wall
        self.contains_pellet = False
        self.contains_power_pellet = False
    def place_pellet(self):
        self.contains_pellet = True
    def place_power_pellet(self):
        self.contains_power_pellet = True
    def remove_pellet(self):
        self.contains_pellet = False
    def remove_power_pellet(self):
        self.contains_power_pellet = False