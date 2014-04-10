class Action:
    def __init__(self, values, effected, duration, index):
        self.values = values
        self.effected = effected
        self.duration = duration
        self.index = index

    def getGoalChange(self, curGoal):
        count = 0
        ret = 0.0
        for st in self.effected:
            if eff == curGoal.name:
                ret = curGoal.value - value[count]
                break
            count += 1
        return ret