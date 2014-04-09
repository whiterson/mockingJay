import random
class Tribute:
    #Goals = list of goals for tribute
    #actions = list of possible actions tribute can do
    def __init__(self, goals, actions):
        self.goals = goals
        self.actions = actions

    #Need to figure out exactly how far
    #/ how we want to handle depth in this function
    #it will be very important
    def bestAction(self):
        return random.randint(0, len(actions))

