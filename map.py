import mapReader
import PIL
import game


class Map:
    def __init__(self, path):
        self.map_image = PIL.Image.open(path)
        self.pixel_map = self.map_image.load()

    def seed_game_state(self, parts):
        gs = game.GameState(parts)
        gs.world['ground'] = self
        gs.grid['ground'] = [(x, y, self.pixel_map[x, y]) for x in range(gs.width) for y in range(gs.height)]
        return gs