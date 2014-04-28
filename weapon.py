import random
from weaponInfo import weaponInfo

class weapon:
    def __init__(self, type):
        ## All weapons start w/ a base d, and they gain or lose depending on what kind of weapon they're fighting against
        self.weaponInfo = weaponInfo()
        self.type = type
        self.damageCap = 0
        self.isRanged = False
        self.range = 1
        self.damage = self.findDamage()
        self.selfConstructed = False
        self.usesLeft = 50

        self.setRanged()
        self.damageCap = self.weaponInfo.weaponStrength(self.type)


    def findDamage(self):
        return random.randint(1,self.weaponInfo.weaponStrength(self.type))


    def isInRange(self, distToTarget):
        inRange = False
        if(self.isRanged and distToTarget <= 1):
            inRange = False
        elif(self.isRanged and (distToTarget > 1) and (distToTarget < self.range)):
            inRange = True
        elif((not self.isRanged) and distToTarget > 1):
            inRange = False
        elif((not self.isRanged) and distToTarget <= 1):
            inRange = True
        else:
            inRange = False

        return inRange

    def setRanged(self):
        if(self.type == 'bow'):
            self.isRanged = True
        elif(self.type == 'slingshot'):
            self.isRanged = True
        elif(self.type == 'blowgun'):
            self.isRanged = True
        else:
            self.isRanged = False
        self.range = self.weaponInfo.weaponRange(self.type)

    def getRanged(self):
        return self.isRanged

    #First is the weapon that we're looking for the damage for
    #Second it the weapon that it's fighting against
    def getDamage(self, wepAgainst):
        against = wepAgainst.type
        weapon = self.type
        damage = self.damage

        if((not wepAgainst.isRanged) and (not self.isRanged)):
            if(weapon == 'spear'):
                if(against == 'none'):
                    damage += 4
                elif(against == 'axe' or against == 'sword' or against == 'dagger'):
                    damage += 3
                else:
                    damage += -1
            elif(weapon == 'axe'):
                if(against == 'none'):
                    damage += 4
                elif(against == 'sword' or against == 'dagger' or against == 'mace' or against == 'hammer'):
                    damage += 3
                else:
                    damage += -1
            elif(weapon == 'sword'):
                if(against == 'none'):
                    damage += 4
                elif(against == 'dagger' or against == 'mace' or against == 'hammer'):
                    damage += 3
                else:
                    damage += -1
            elif(weapon == 'dagger'):
                if(against == 'none'):
                    damage += 4
                elif(against == 'mace' or against == 'hammer' or against == 'trident'):
                    damage += 3
                else:
                    damage += -1
            elif(weapon == 'mace'):
                if(against == 'none'):
                    damage += 4
                elif(against == 'hammer' or against == 'trident' or against == 'spear'):
                    damage += 3
                else:
                    damage += -1
            elif(weapon == 'hammer'):
                if(against == 'none'):
                    damage += 4
                elif(against == 'trident' or against == 'spear'):
                    damage += 3
                else:
                    damage += -1
            elif(weapon == 'trident'):
                if(against == 'none'):
                    damage += 4
                elif(against == 'spear' or against == 'axe' or against == 'sword'):
                    damage += 3
                else:
                    damage += -1
            else:
                damage += 0

        elif(wepAgainst.isRanged and (not self.isRanged)):
            damage += 4

        elif((not wepAgainst.isRanged) and self.isRanged):
            damage -= 1

        elif(wepAgainst.isRanged and self.isRanged):
            if(weapon == 'slingshot'):
                if(against == 'none'):
                    damage += 1
                elif(against == 'blowgun'):
                    damage += 2
                else:
                    damage += -1
            elif(weapon == 'blowgun'):
                if(against == 'none'):
                    damage += 1
                elif(against == 'bow'):
                    damage += 2
                else:
                    damage += -1
            elif(weapon == 'bow'):
                if(against == 'none'):
                    damage += 1
                elif(against == 'slingshot'):
                    damage += 2
                else:
                    damage -= 1
            else:
                damage += 0
        else:
            damage += 0

        return damage

