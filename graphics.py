__author__ = 'Nathan'
import pygame

class GameView(object):
    """
    GameView constructs the main GUI window and handles all the drawing routines
    """

    def __init__(self, width, height, cell_size=(10, 10)):
        self.size = self.width, self.height = width, height
        self.screen = pygame.display.set_mode(self.size)
        self.state = None
        self.cell_size = cell_size
        self.layers = {
            'ground': (pygame.Surface(self.size), 0),
            'particle': (pygame.Surface(self.size), 1)
        }

    def draw(self):
        if bool(self.state):
            for layer in self.layers:
                for x, y, color in self.state.grid[layer]:
                    print 'Rendering layer ' + str(layer)
                    tile = pygame.Rect(x, y, *self.cell_size)
                    pygame.draw.rect(self.layers[layer][0], pygame.Color(*color), tile, 0)

        layers_ordered = sorted(self.layers.iteritems(), key=lambda x: x[1])
        for layer in layers_ordered:
            self.screen.blit(layer[0], (0, 0))

    def render(self, gs):
        """
        here, we set the game state to render
        @param gs: the game state to render
        """
        self.state = gs
        self.draw()