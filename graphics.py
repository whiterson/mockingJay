__author__ = 'Nathan'
import pygame


class GameView(object):
    """
    GameView constructs the main GUI window and handles all the drawing routines
    """

    def __init__(self, width, height, cell_size=(10, 10)):
        self.size = self.width, self.height = width * 10, height * 10
        self.screen = pygame.display.set_mode(self.size)
        self.state = None
        self.cell_size = cell_size
        self.layers = {
            'ground': (pygame.Surface(self.size), 0),
            'particle': (pygame.Surface(self.size), 1)
        }

        self.layers['particle'][0].set_colorkey((255, 0, 255))
        self.layers['particle'][0].fill((255, 0, 255))

    def draw(self):
        self.layers['particle'][0].fill((255, 0, 255))
        if bool(self.state):
            for layer in self.layers:
                for x, y, color in self.state.grid[layer]:
                    tile = pygame.Rect(x * self.cell_size[0], y * self.cell_size[1], *self.cell_size)
                    pygame.draw.rect(self.layers[layer][0], pygame.Color(*color), tile, 0)

        layers_ordered = sorted(self.layers.iteritems(), key=lambda g: g[1][1])
        for layer in layers_ordered:
            print 'Blitting layer ' + str(layer)
            self.screen.blit(layer[1][0], (0, 0))

        pygame.display.flip()

    def render(self, gs):
        """
        here, we set the game state to render
        @param gs: the game state to render
        """
        self.state = gs
        self.draw()