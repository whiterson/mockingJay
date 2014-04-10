__author__ = 'Nathan'

import random as r


class GameState(object):
    """
    represents, well, the state of the game.
    how should we separate the line between the map and the game state?
    for now, I'm making the crude assumption that the map read parses to an empty game-state
    """
    def __init__(self, width=50, height=50):
        # for now, this is just a dummy class with a 10x10 tile grid
        self.world = {
            'ground': (),
            'particle': ()
        }

        self.grid = {
            'ground': [(x, y, (r.randint(0, 255), r.randint(0, 255), r.randint(0, 255), 0)) for x in range(width) for y in range(height)],
            'particle': []
        }

        self.particles = []
