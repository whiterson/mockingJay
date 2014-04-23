import random
import engine
import json
import copy
import sys

class Particle(object):
    def __init__(self, state=(0, 0), width=1, height=1):
        self.state = state
        self.width, self.height = width, height


class Tribute(Particle):
    #Goals = list of goals for tribute
    #actions = list of possible actions tribute can do
    def __init__(self, goals, actions, x=0, y=0, district='d12', gender='male'):

        Particle.__init__(self, (x, y), 1, 1)
        self.goals = goals
        self.actions = actions
        self.ret = []
        self.district = district
        d = json.load(open('./distributions/stats.json'))

        def U(mean, spread):
            base = random.randrange(0, 2*spread) - spread
            s = base + mean
            return s

        self.attributes = {
            'size': U(d['size']['mean'], d['size']['spread']),
            'strength': U(d['strength']['mean'], d['strength']['spread']),
            'speed': U(d['speed']['mean'], d['speed']['spread']),
            'hunting_skill': U(d['hunting_skill'][self.district]['mean'], d['hunting_skill'][self.district]['spread']),
            'fighting_skill': U(d['fighting_skill'][self.district]['mean'], d['fighting_skill'][self.district]['spread']),
            'weapon_skill': U(d['weapon_skill'][self.district]['mean'], d['weapon_skill'][self.district]['spread']),
            'camouflage_skill': U(d['camouflage_skill'][self.district]['mean'], d['camouflage_skill'][self.district]['spread']),
            'friendliness': U(d['friendliness']['mean'], d['friendliness']['spread']),
            'district_prejudices': dict(d['district_prejudices'][self.district]),
            'stamina': U(d['stamina']['mean'], d['stamina']['spread']),
            'endurance': U(d['endurance']['mean'], d['endurance']['spread'])
        }
        self.gender = gender
        self.stats = {
            'health': U(15, 5),
            'energy': self.attributes['stamina'],
            'hunger_energy': 100
        }

        self.last_name = random.choice(d['last_names'])
        if self.gender == 'male':
            self.first_name = random.choice(d['first_names_male'])
        else:
            self.first_name = random.choice(d['first_names_female'])

        pass

    def __repr__(self):
        s = '<Tribute>(' + self.last_name + ', ' + self.first_name + ', ' + self.gender + '): '
        s += '\n' + str(self.attributes)
        return s

    #Need to figure out exactly how far
    #/ how we want to handle depth in this function
    #it will be very important
    def calc_min_discomfort(self, depth, maxdepth, ret, gameMap):
        min_val = sys.maxint

        for action in self.actions:
            tribute = copy.deepcopy(self)
            tribute.applyAction(action, gameMap)
            if depth == maxdepth:
                return tribute.calcDisc()
            else:
                min_val = min(tribute.calc_min_discomfort(depth + 1, maxdepth, action, ret, gameMap), min_val)

        return min_val

    def best_action_fighting(self, depth, maxdepth, actionName, ret, gameMap):
        for action in self.actions:
            tribute = copy.deepcopy(self)
            tribute.applyAction(action, gameMap)
            if depth == maxdepth:
                ret.append((tribute.calcDisc(), action))
            elif depth==0:
                tribute.best_action(depth+1, maxdepth, action, ret, gameMap)
            else:
                tribute.best_action(depth+1, maxdepth, actionName, ret, gameMap)

    def act(self, gameMap):
        #this function will have to be customized for each action
        best_action = (None, sys.maxint)
        for a in self.actions:
            t = copy.deepcopy(self)
            v = self.calc_min_discomfort(0, 0, self.ret, gameMap)
            if v < best_action[1]:
                best_action = (a, v)

        #State updated now need to update the goals and other things.... for now just goals
        self.doAction(best_action[0], gameMap)

    def doAction(self, action, gameMap):
        rand = random.randint(0,1)
        loc = gameMap[self.state[0]][self.state[1]]
        if(action.index >= 0 and action.index <= 3): #moving so don't know what gonna do here
              self.state = ((self.state[0] + action.delta_state[0]) % engine.GameEngine.dims[0],
                      (self.state[1] + action.delta_state[1]) % engine.GameEngine.dims[1])
        elif(action.index == 4):#find food
             foodProb = loc.getFoodChance()
             for goal in self.goals:
                if goal.name == "hunger":
                    if(rand <= foodProb):
                        goal.value -= action.values[0]
        elif(action.index == 5): #kill
            blah = 0
        elif(action.index == 6): #scavenger
            blah = 0
        elif(action.index == 7): #craft
            craftProb = loc.getSharpStoneChance()
            for goal in self.goals:
                if goal.name == "getweapon":
                    if(rand<=craftProb):
                        goal.value -= action.values[0]
        elif(action.index == 8): #getwater
            waterProb = loc.getWaterChance()
            for goal in self.goals:
                if goal.name == "thirst":
                    if(rand<=waterProb):
                        goal.value -= action.values[0]
        elif(action.index == 9): #rest
            blah = 0

    def calc_disc(self, gameMap):
        ret = 0
        for goals in self.goals:
            ret += goals.value*goals.value
        return ret

    def endTurn(self):
        for goal in self.goals:
            if goal.name == "hunger":
                goal.value += 1
            if goal.name == "thirst":
                goal.value += 1
        #TODO
        #update thirst, tiredness, hunger, etc.... .

    #Action will update the state of the world by calculating
    #Goal updates and where it is / fuzzy logic of where other tributes are
    #will update current selfs world.
    def applyAction(self, action, gameMap):
        loc = gameMap[self.state[0]][self.state[1]]
        if(action.index >= 0 and action.index <= 3): #moving so don't know what gonna do here
             self.state = ((self.state[0] + action.delta_state[0]) % engine.GameEngine.dims[0],
                      (self.state[1] + action.delta_state[1]) % engine.GameEngine.dims[1])
        elif(action.index == 4):#find food
             foodProb = loc.getFoodChance()
             for goal in self.goals:
                if goal.name == "hunger":
                    goal.value -= foodProb* action.values[0]
        elif(action.index == 5): #kill
            blah = 0
        elif(action.index == 6): #scavenger
            blah = 0
        elif(action.index == 7): #craft
            craftProb = loc.getSharpStoneChance()
            for goal in self.goals:
                if goal.name == "getweapon":
                    goal.value -= craftProb* action.values[0]
        elif(action.index == 8): #getwater
            waterProb = loc.getWaterChance()
            for goal in self.goals:
                if goal.name == "thirst":
                    goal.value -= waterProb* action.values[0]
        elif(action.index == 9): #rest
            blah = 0


    def calcDisc(self):
        val = 0
        for goal in self.goals:
            if(goal.value > 0):
                val += goal.value*goal.value
        return val

    def checkDead(self):
        for goal in self.goals:
            if goal.name == " hunger ":
                if goal.value >= 100:
                    return " starvation "
            if goal.name == " thirst ":
                if goal.value >= 100:
                    return " terminal dehydration "

        if self.killed:
            return self.killedBy
        else:
            return None
