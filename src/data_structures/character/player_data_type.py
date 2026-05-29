from .character_data_type import Character

class Player(Character):
    def __init__(self, position, visibility, sprite, direction, lives=3):
        super().__init__(position, visibility, sprite, direction)
        self.lives=lives
        self.point=0
    