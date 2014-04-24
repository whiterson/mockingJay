import random
import engine
import json
import copy
import sys

class Particle(object):
    def __init__(self, state=(0, 0), width=1, height=1):
        self.state = state
        self.width, self.height = width, height

FIGHT_STATE = {'not_fighting': 0, 'fleeing': 1, 'fighting': 2}

class Tribute(Particle):
    #Goals = list of goals for tribute
    #actions = list of possible actions tribute can do
    def __init__(self, goals, actions, x=0, y=0, district='d12', gender='male', do_not_load=False):

        Particle.__init__(self, (x, y), 1, 1)
        self.goals = goals
        self.actions = actions
        self.district = district
        self.has_weapon = False
        self.weapons = []
        self.has_ally = False
        self.allies = []
        self.fighting_state = FIGHT_STATE['not_fighting']
        self.opponent = None
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
            'endurance': U(d['endurance']['mean'], d['endurance']['spread']),
            'crafting_skill': U(d['crafting_skill']['mean'], d['crafting_skill']['spread']),
            'bloodlust': U(d['bloodlust']['mean'], d['bloodlust']['spread'])
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

        if do_not_load:
            self.attributes = None
            self.gender = gender
            self.stats = None
            self.last_name = None
            self.first_name = None
            self.killed = None
        else:
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
                'endurance': U(d['endurance']['mean'], d['endurance']['spread']),
                'crafting_skill': U(d['crafting_skill']['mean'], d['crafting_skill']['spread']),
                'bloodlust': U(d['bloodlust']['mean'], d['bloodlust']['spread'])
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

            self.killed = False
            pass

    def clone(self):
        n_goals = [g.clone() for g in self.goals]
        n_actions = self.actions[:]
        n_district = self.district[:]
        n_gender = self.gender[:]
        n = Tribute(n_goals, n_actions, x=self.state[0], y=self.state[1], district=n_district,
                    gender=n_gender, do_not_load=True)
        n.killed = self.killed
        n.attributes = self.attributes.copy()
        n.stats = self.stats.copy()
        n.opponent = self.opponent
        return n

    def __repr__(self):
        s = '<Tribute>(' + self.last_name + ', ' + self.first_name + ', ' + self.gender + '): '
        s += '\n' + str(self.attributes)
        return s

    def engage_in_combat(self, t):
        if self.fighting_state != FIGHT_STATE['not_fighting']:
            self.fighting_state = FIGHT_STATE['fighting']
            self.opponent = t
            t.engage_in_combat(self)

    #Need to figure out exactly how far
    #/ how we want to handle depth in this function
    #it will be very important
    def calc_min_discomfort(self, depth, max_depth, gameMap):
        min_val = sys.maxint

        if depth == max_depth:
            return self.calc_discomfort()

        for action in self.actions:
            tribute = self.clone()
            tribute.apply_action(action, gameMap)
            min_val = min(tribute.calc_min_discomfort(depth + 1, max_depth, gameMap), min_val)

        return min_val

    def best_action_fighting(self, depth, maxdepth, actionName, ret, gameMap):
        for action in self.actions:
            tribute = copy.deepcopy(self)
            tribute.apply_action(action, gameMap)
            if depth == maxdepth:
                ret.append((tribute.calc_discomfort(), action))
            elif depth==0:
                tribute.best_action(depth+1, maxdepth, action, ret, gameMap)
            else:
                tribute.best_action(depth+1, maxdepth, actionName, ret, gameMap)

    def act(self, gameMap):
        if self.fighting_state == FIGHT_STATE['not_fighting']:
            best_action = (None, sys.maxint)
            for a in self.actions:
                t = copy.deepcopy(self)
                t.do_action(a, gameMap)
                v = t.calc_min_discomfort(0, 2, gameMap)
                if v < best_action[1]:
                    best_action = (a, v)

            print 'Doing action: ' + str(best_action[0])
            self.do_action(best_action[0], gameMap)

        elif self.fighting_state == FIGHT_STATE['fighting']:
            pass
    
    def do_action(self, action, game_map):
        rand = random.randint(0,1)
        loc = game_map[self.state[0]][self.state[1]]
        if action.index >= 0 and action.index <= 3:  # moving so don't know what gonna do here
            loc.setTribute(None)
            self.state = ((self.state[0] + action.delta_state[0]) % engine.GameEngine.dims[0],
                (self.state[1] + action.delta_state[1]) % engine.GameEngine.dims[1])
            (game_map[self.state[0]][self.state[1]]).setTribute(self)
        elif action.index == 4:  # find food
            food_prob = loc.getFoodChance()
            for goal in self.goals:
                if goal.name == "hunger":
                    if rand <= food_prob:
                        goal.value -= action.values[0]
        elif action.index == 5:  # kill
            pass
        elif action.index == 6:  # scavenger
            pass
        elif action.index == 7: #craft
            craft_prob = loc.getSharpStoneChance()
            for goal in self.goals:
                if goal.name == "getweapon":
                    if rand <= craft_prob:
                        goal.value -= action.values[0]
        elif action.index == 8:  # get water
            water_prob = loc.getWaterChance()
            for goal in self.goals:
                if goal.name == "thirst":
                    if rand <= water_prob:
                        goal.value -= action.values[0]
        elif action.index == 9: #rest
            pass

    def calc_disc(self, gameMap):
        ret = 0
        for goals in self.goals:
            ret += goals.value * goals.value
        return ret

    def end_turn(self):
        for goal in self.goals:
            if goal.name == "kill":
                goal.value += ((self.attribute["bloodlust"]-1)/8)
            if (self.district == 1 or self.district == 2 or self.district == 4):
                if goal.name == "kill":
                    goal.value +=0.1
                if(goal.name == "weapon" and not self.hasWeapon):
                    goal.value += 0.05
            if self.district == 1 or self.district == 2 or self.district == 4:
                if goal.name == "kill":
                    goal.value +=0.25
                if goal.name == "weapon" and not self.has_weapon:
                    goal.value += (1/(self.attributes['size'] + self.attributes['strength']))
            if (self.attributes['size'] + self.attributes['strength']) < 4:
                if goal.name == "weapon" and not self.has_weapon:
                    goal.value += 0.1
                if(goal.name == "ally" and not self.hasAlly and not self.hasWeapon):
                    goal.value +=0.05
                if(goal.name == "hide" and not self.hasAlly and not self.hasWeapon):
                    goal.value += 0.01
                if goal.name == "ally" and not self.has_ally and not self.has_weapon:
                    goal.value += 0.05
            if goal.name == "hunger":
                goal.value += ((1/self.attributes['endurance']) + (self.attributes['size']/5))
            if goal.name == "thirst":
                goal.value += 1/self.attributes['endurance']
            if goal.name == "rest":
                goal.value += (1/self.attributes['stamina'] + self.goals[0]/50 + self.goals[1]/30)


    #Action will update the state of the world by calculating
    #Goal updates and where it is / fuzzy logic of where other tributes are
    #will update current selfs world.
    def apply_action(self, action, gameMap):
        loc = gameMap[self.state[0]][self.state[1]]
        if 3 >= action.index >= 0:  # moving so don't know what gonna do here
            self.state = ((self.state[0] + action.delta_state[0]) % engine.GameEngine.dims[0],
                          (self.state[1] + action.delta_state[1]) % engine.GameEngine.dims[1])
        elif action.index == 4:#find food
             foodProb = loc.getFoodChance()
             for goal in self.goals:
                if goal.name == "hunger":
                    goal.value -= foodProb* action.values[0]
        elif action.index == 5: #kill
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

    def calc_discomfort(self):
        val = 0
        for goal in self.goals:
            if(goal.value > 0):
                val += goal.value*goal.value
        return val

    def checkDead(self):
        for goal in self.goals:
            if goal.name == "hunger":
                if goal.value >= 150:
                    return " starvation "
            #You get thirsty a lot faster than you get hungry
            if goal.name == "thirst":
                if goal.value >= 100:
                    return " terminal dehydration "
            if goal.name == "rest":
                if goal.value >= 300:
                    return " exhaustion "

        if self.killed:
            return self.killedBy
        else:
            return None
