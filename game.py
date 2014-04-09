__author__ = 'Nathan'


class GameState(object):
    """
    represents, well, the state of the game.
    how should we separate the line between the map and the game state?
    for now, I'm making the crude assumption that the map read parses to an empty game-state
    """
    def __init__(self):
        self.map = {
            'ground': (),
            'particle': ()
        }


