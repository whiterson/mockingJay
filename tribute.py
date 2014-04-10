import random


class Particle(object):
    def __init__(self, x=0, y=0, width=1, height=1):
        pass


class Tribute(Particle):
    #Goals = list of goals for tribute
    #actions = list of possible actions tribute can do
    def __init__(self, goals, actions, x=0, y=0):
        Particle.__init__(self, x, y, 1, 1)
        self.goals = goals
        self.actions = actions

    #Need to figure out exactly how far
    #/ how we want to handle depth in this function
    #it will be very important
    def bestAction(self):
        return random.randint(0, len(self.actions))

