class LocationDef(object):
    def __init__(self):
        self.definition = {
        'startSpace': (),       #True/False
        'playerThere': (),      #True/False
        'terrain': (),          #0-15 Value for terrain Type
        'foodChance': (),       #integer value for probability of food
        'waterChance': (),      #integer value for probability of water
        'visibility': (),       #integer value for visibility
        'stickChance': (),      #for crafting: Integer Value probability of stick
        'sharpStoneChance': (), #for crafting: integer value probablity of sharp stone
        'featherChance': (),    #for crafting: integer value probablilty of feather
        'vineChance': (),       #for crafting: integer value probablity of vine
        'speedChange': ()       #integer value movement speed changes
    }

def getDefinition(self):
    return self.definition

def setDefinition(self, newDef):
    self.definition = newDef
