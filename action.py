class Action:
    def __init__(self, values, effected, duration, index, delta_state, desc=''):
        self.values = values
        self.effected = effected
        self.duration = duration
        self.index = index
        self.delta_state = delta_state
        self.description = desc

    def __repr__(self):
        return '<Action>(' + str(self.index) + ', ' + str(self.delta_state) + ')'

    #def getGoalChange(self, curGoal):
    #    count = 0
    #    ret = 0.0
    #    for eff in self.effected:
    #        if eff == curGoal.name:
    #            ret = curGoal.value - value[count]
    #            break
    #        count += 1
    #    return ret
