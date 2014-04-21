__author__ = 'Nathan'

import random as r
import tribute


class GameState(object):
    """
    represents, well, the state of the game.
    how should we separate the line between the map and the game state?
    for now, I'm making the crude assumption that the map read parses to an empty game-state
    """
    def __init__(self, particles, width=50, height=50):
        self.width, self.height = width, height

        self.world = {
            'ground': (),
            'particle': ()
        }

        self.particles = particles

        self.grid = {
            'ground': [(x, y, (r.randint(0, 255), r.randint(0, 255), r.randint(0, 255), 0)) for x in range(width) for y in range(height)],
            'particle': [(p.state[0], p.state[1], (255, 0, 0, 0)) for p in self.particles]
        }

    def update(self):
        for particle in self.particles:
            particle.act()
        self.grid['particle'] = [(p.state[0], p.state[1], (255, 0, 0, 0)) for p in self.particles]

    def apply_action(self):
        pass