class locationDef(object):
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
        return self.visibility

    def getSharpStoneChance(self):
        return self.sharpStoneChance

    def getFeatherChance(self):
        return self.featherChance

    def getVineChance(self):
        return self.vineChance

    def getSpeedChange(self):
        return self.speedChange

    ########### SETS ##############
    def setStartSpace(self, input):
        self.startSpace = input

    def setPlayerThere(self, input):
        self.playerThere = input

    def setTerrain(self, input):
        self.terrain = input

    def setFoodChance(self, input):
        self.foodChance = input

    def setWaterChance(self, input):
        self.waterChance = input

    def setStickChance(self, input):
        self.stickChance = input

    def setVisibility(self, input):
        self.visibility = input

    def setSharpStoneChance(self, input):
        self.sharpStoneChance = input

    def setFeatherChance(self, input):
        self.featherChance = input

    def setVineChance(self, input):
        self.vineChance = input

    def setSpeedChange(self, input):
        self.speedChange = input
