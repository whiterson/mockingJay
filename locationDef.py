class LocationDef(object):
    def __init__(self):
        self.startSpace = False     #True/False
        self.playerThere = False    #True/False
        self.terrain = 0            #0-15 Value for terrain Type
        self.foodChance = 1         #integer value for probability of food
        self.waterChance = 1        #integer value for probability of water
        self.visibility = 0         #integer value for visibility
        self.stickChance = 1        #for crafting: Integer Value probability of stick
        self.sharpStoneChance = 1   #for crafting: integer value probablity of sharp stone
        self.featherChance = 1      #for crafting: integer value probablilty of feather
        self.vineChance = 1         #for crafting: integer value probablity of vine
        self.speedChange = 0        #integer value movement speed changes

########### GETS ##############
def getStartSpace(self):
    return self.startSpace

def getPlayerThere(self):
    return self.playerThere

def getTerrain(self):
    return self.terrain

def getFoodChance(self):
    return self.foodChance

def getWaterChance(self):
    return self.waterChance

def getStickChance(self):
    return self.stickChance

def getVisibility(self):
    return self.terrain

def getSharpStoneChance(self):
    return self.terrain

def getFeatherChance(self):
    return self.terrain

def getVineChance(self):
    return self.terrain

def getSpeedChange(self):
    return self.terrain

########### SETS ##############
def getStartSpace(self, input):
    self.startSpace = input

def getPlayerThere(self, input):
    self.playerThere = input

def getTerrain(self, input):
    self.terrain = input

def getFoodChance(self, input):
    self.foodChance = input

def getWaterChance(self, input):
    self.waterChance = input

def getStickChance(self, input):
    self.stickChance = input

def getVisibility(self, input):
    self.terrain = input

def getSharpStoneChance(self):
    self.terrain = input

def getFeatherChance(self, input):
    self.terrain = input

def getVineChance(self, input):
    self.terrain = input

def getSpeedChange(self, input):
    self.terrain = input
