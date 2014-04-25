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

    def draw(self, tribute, tributes):
        self.layers['particle'][0].fill((255, 0, 255))
        if bool(self.state):
            for layer in self.layers:
                for x, y, color in self.state.grid[layer]:
                    tile = pygame.Rect(x * self.cell_size[0], y * self.cell_size[1], *self.cell_size)
                    pygame.draw.rect(self.layers[layer][0], pygame.Color(*color), tile, 0)

        layers_ordered = sorted(self.layers.iteritems(), key=lambda g: g[1][1])
        for layer in layers_ordered:
            self.screen.blit(layer[1][0], (0, 0))

        self.textTribute(tribute)
        self.textStats(tributes)
        pygame.display.flip()

    def render(self, gs, tribute, tributes):
        """
        here, we set the game state to render
        @param gs: the game state to render
        """
        self.state = gs
        self.draw(tribute, tributes)

    def textStats(self, tributes):
        fontobject=pygame.font.SysFont('Arial', 18)
        sY = 520
        sX = 70
        for i in range(2, 4):
            if i%2==0:
                self.screen.blit(fontobject.render('District ' + str(i/2), 1, (255,255,255)), (sX, sY))
                if (i-2)%4==0 and i!=2:
                    sY+= 40
                    sX-=800
            #Check if alive here
            print sX
            print sY
            self.screen.blit(fontobject.render(tributes[i-2].first_name + ' - Alive', 1, (255, 255, 255)), (sX-15, sY+25))
            #Print weapons here
            #Print alive here
            sY+= 20
            if i%2 == 0 and i!=2:
                sX+=200
                sY -= 40

    def textTribute(self, tribute):
        fontobject=pygame.font.SysFont('Arial', 18)
        self.screen.blit(fontobject.render((tribute.first_name+ ' ' + tribute.last_name), 1, (255, 255, 255)), (510, 20))
        self.screen.blit(fontobject.render(('*****************************************'), 1, (255, 255, 255)), (505, 55))
        self.screen.blit(fontobject.render(('Size: ' +str(tribute.attributes['size'])), 1, (255, 255, 255)), (510, 80))
        self.screen.blit(fontobject.render(('Strength: ' +str(tribute.attributes['strength'])), 1, (255, 255, 255)), (650, 80))
        self.screen.blit(fontobject.render(('Speed: ' +str(tribute.attributes['speed'])), 1, (255, 255, 255)), (510, 120))
        self.screen.blit(fontobject.render(('Hunting: ' +str(tribute.attributes['hunting_skill'])), 1, (255, 255, 255)), (650, 120))
        self.screen.blit(fontobject.render(('Fighting: ' +str(tribute.attributes['fighting_skill'])), 1, (255, 255, 255)), (510, 160))
        self.screen.blit(fontobject.render(('Camo Skill: ' +str(tribute.attributes['camouflage_skill'])), 1, (255, 255, 255)), (650, 160))
        self.screen.blit(fontobject.render(('Friendliness: ' +str(tribute.attributes['friendliness'])), 1, (255, 255, 255)), (510, 200))
        self.screen.blit(fontobject.render(('Stamina: ' +str(tribute.attributes['stamina'])), 1, (255, 255, 255)), (650, 200))
        self.screen.blit(fontobject.render(('Endurance: ' +str(tribute.attributes['endurance'])), 1, (255, 255, 255)), (510, 240))
