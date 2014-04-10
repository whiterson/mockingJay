import mapReader

class Map:

    def __init__(self):
        self.pixelMap = []
        self.playerMap= []
        self.itemsMap = []
        readMap()
