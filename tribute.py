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

    #Need to figure out exactly how far
    #/ how we want to handle depth in this function
    #it will be very important
    def best_action(self):
        index = random.randint(0, len(self.actions) - 1)
        return self.actions[index]

    def act(self):
        action = self.best_action()
        self.state = ((self.state[0] + action.delta_state[0]) % engine.GameEngine.dims[0], (self.state[1] + action.delta_state[1]) % engine.GameEngine.dims[1])




