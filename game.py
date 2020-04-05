import enum


class GameState(enum.Enum):
    recruitment = 1
    combat = 2
    not_ready = 10


class Game:
    def __init__(self, id):
        self.id = id
        self.state = GameState.not_ready
