import tribute

class locationDef(object):
    def __init__(self):
        self.startSpace = False     #True/False
        self.playerThere = False    #True/False
        self.tribute = None         #Tribute that is in a space. Null otherwise
        self.terrain = 0            #0-15 Value for terrain Type
        self.foodChance = 0         #integer value for probability of food
        self.waterChance = 0        #integer value for probability of water
        self.visibility = 0         #integer value for visibility
        self.shortStickChance = 0   #for crafting: Integer Value probability of stick
        self.sharpStoneChance = 0   #for crafting: integer value probablity of sharp stone
        self.featherChance = 0      #for crafting: integer value probablilty of feather
        self.vineChance = 0         #for crafting: integer value probablity of vine
        self.speedChange = 0        #integer value movement speed changes
        self.weaponChance = 0        #inter value for probability of weapon
        self.longStickChance = 0
        self.broadStoneChance = 0
        self.longGrassChance = 0
        self.reedsChance = 0
        self.pebblesChance = 0
        self.thornsChance = 0

    ########### GETS ##############

    def getStartSpace(self):
        return self.startSpace

    def getPlayerThere(self):
        return self.playerThere

    def getTribute(self):
        return self.tribute

    def getTerrain(self):
        return self.terrain

    def getFoodChance(self):
        return self.foodChance

    def getWaterChance(self):
        return self.waterChance

    def getShortStickChance(self):
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

    def getWeaponChance(self):
        return self.weaponChance

    def getLongStickChance(self):
        return self.longStickChance

    def getBroadStoneChance(self):
        return self.broadStoneChance

    def getLongGrassChance(self):
        return self.longGrassChance

    def getReedsChance(self):
        return self.reedsChance

    def getPebblesChance(self):
        return self.pebblesChance

    def getThornsChance(self):
        return self.thornsChance

    ########### SETS ##############
    def setStartSpace(self, input):
        self.startSpace = input

    def setPlayerThere(self, input):
        self.playerThere = input

    def setTribute(self, input):
        self.tribute = input

    def setTerrain(self, input):
        self.terrain = input

    def setFoodChance(self, input):
        self.foodChance = input

    def setWaterChance(self, input):
        self.waterChance = input

    def setShortStickChance(self, input):
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

    def setWeaponChance(self, input):
        self.weaponChance = input

    def setLongStickChance(self, input):
        self.longStickChance = input

    def setBroadStoneChance(self, input):
        self.broadStoneChance = input

    def setLongGrassChance(self, input):
        self.longGrassChance = input

    def setReedsChance(self, input):
        self.reedsChance = input

    def setPebblesChance(self, input):
        self.pebblesChance = input

    def setThornsChance(self, input):
        self.thornsChance = input
