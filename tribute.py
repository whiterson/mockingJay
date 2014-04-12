import random
import engine


class Particle(object):
    def __init__(self, state=(0, 0), width=1, height=1):
        self.state = state
        self.width, self.height = width, height

class Tribute(Particle):
    #Goals = list of goals for tribute
    #actions = list of possible actions tribute can do
    def __init__(self, goals, actions, x=0, y=0):
        Particle.__init__(self, (x, y), 1, 1)
        self.goals = goals
        self.actions = actions
        self.ret = []

    #Need to figure out exactly how far
    #/ how we want to handle depth in this function
    #it will be very important
    def best_action(self, depth, maxdepth, actionName, ret):
        index = random.randint(0, len(self.actions) - 1)

        for action in self.actions:
            if depth == maxdepth:
                ret.append((self.calcDisc(),action))
            else:
                #Apply action to world copy and update and go one depth farther in
                self.applyAction(action)
                if depth == 0:
                    self.best_action(depth+1, 4, action, ret)
                else:
                    self.best_action(depth+1, 4, actionName, ret)



    def act(self):
        #this function will have to be customized for each action
        del self.ret[:]
        self.best_action(0,4, '', self.ret)
        bestVal = 1000000
        for pairs in self.ret:
            if pairs[0] < bestVal:
                bestVal = pairs[0]
                action = pairs[1]
        
        self.state = ((self.state[0] + action.delta_state[0]) % engine.GameEngine.dims[0], (self.state[1] + action.delta_state[1]) % engine.GameEngine.dims[1])

    #Action will update the state of the world by calculating
    #Goal updates and where it is / fuzzy logic of where other tributes are
    #will update current selfs world.
    def applyAction(self, action):
        return []

    def calcDisc(self):
        val = 0
        for goal in self.goals:
            val += goal.value*goal.value
        return val