import random
import engine
import json
import copy
import sys
from probability import uniform_variable as U

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

        # remove the fight action. we don't want them fighting unless someone is in range
        self.fight_action = actions[5]
        self.actions = self.actions[:5] + self.actions[6:]

        self.district = district
        self.has_weapon = False
        self.weapon = 'none'
        self.has_ally = False
        self.allies = []
        self.fighting_state = FIGHT_STATE['not_fighting']
        self.opponent = None
        self.last_opponent = None
        self.sighted = None
        self.last_action = None

        if do_not_load:
            self.attributes = None
            self.gender = gender
            self.stats = None
            self.last_name = None
            self.first_name = None
            self.killed = None
        else:
            d = json.load(open('./distributions/stats.json'))

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
                'crafting_skill': U(d['crafting_skill'][self.district]['mean'], d['crafting_skill'][self.district]['spread']),
                'bloodlust': U(d['bloodlust']['mean'], d['bloodlust']['spread']),
                'max_health': U(d['max_health']['mean'], d['max_health']['spread'])
            }
            self.gender = gender
            self.stats = {
                'health': self.attributes['max_health'],
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
        n.sighted = self.sighted
        n.last_action = self.last_action
        n.last_opponent = self.last_opponent
        return n

    def __repr__(self):
        s = '<Tribute>(' + self.last_name + ', ' + self.first_name + ', ' + self.gender + ')'
        return s

    def engage_in_combat(self, t):
        if self.fighting_state == FIGHT_STATE['not_fighting']:
            self.fighting_state = FIGHT_STATE['fighting']
            self.opponent = t
            t.engage_in_combat(self)
            print str(self) + ' is engaging in combat with ' + str(t) + '!'

    def disengage_in_combat(self, t):
        if self.fighting_state != FIGHT_STATE['not_fighting']:
            self.fighting_state = FIGHT_STATE['not_fighting']
            self.opponent = None
            t.disengage_in_combat(self)
            print str(self) + ' is disengaging in combat with ' + str(t) + '!'

    def surmise_enemy_hit(self, tribute):
        """
        returns the estimate average HP hit for an enemy
        :param tribute: the enemy to surmise about
        :return: the surmised value
        """
        return 1 + int(tribute.has_weapon) * 5 + int(tribute.attributes['strength']) / 2

    def surmise_escape_turns(self, tribute):
        turns = -1
        if self.attributes['speed'] >= tribute.attributes['speed']:
            turns = sys.maxint
        else:
            s = tribute.attributes['speed'] - self.attributes['speed']
            distance = abs(self.state[0] - tribute.state[0]) + abs(self.state[1] - tribute.state[1])
            turns = distance / s

        return turns

    def surmise_enemy_weakness(self, tribute):
        index = tribute.attributes['max_health'] - tribute.stats['health']
        val = float(index) / tribute.attributes['max_health']
        return int(round(val * 5))

    def enemy_in_range(self, game_state):
        for t in game_state.grid['particle']:
            p = t[3]
            d = abs(t[0] - self.state[0]) + abs(t[1] - self.state[1])
            if 0 < d < 5 and p not in self.allies:
                return p

    def hurt(self, damage, place):
        print str(self) + ' was hit in the ' + place + ' for ' + str(damage) + ' damage'
        self.stats['health'] -= damage
        self.goals[7].value += damage
        if self.stats['health'] <= 0:
            self.killed = True
            self.killedBy = self.opponent
            print str(self) + ' was killed by ' + str(self.killedBy)
            self.disengage_in_combat(self.opponent)

    #Need to figure out exactly how far
    #/ how we want to handle depth in this function
    #it will be very important
    def calc_min_discomfort(self, depth, max_depth, gameMap, actions):
        min_val = sys.maxint

        if depth == max_depth:
            return self.calc_discomfort()

        for action in actions:
            tribute = self.clone()
            tribute.apply_action(action, gameMap)
            min_val = min(tribute.calc_min_discomfort(depth + 1, max_depth, gameMap, actions), min_val)

        return min_val

    def decide_fight_move(self, game_map):
        if self.goals[7].value < random.randrange(5, 20):
            actions = ['attack_head', 'attack_chest', 'attack_gut', 'attack_legs']
            return random.choice(actions)
        else:
            print str(self), ' became scared and is trying to flee!'
            return 'flee'

    def act(self, gameMap, game_state):
        if self.fighting_state != FIGHT_STATE['fighting']:
            best_action = (None, sys.maxint)
            actions = self.actions

            self.sighted = self.enemy_in_range(game_state)

            if self.sighted:
                actions = self.actions + [self.fight_action]

            for a in actions:
                t = copy.deepcopy(self)
                t.apply_action(a, gameMap)
                v = t.calc_min_discomfort(0, 2, gameMap, actions)
                if v < best_action[1]:
                    best_action = (a, v)

            if self.fighting_state == FIGHT_STATE['fleeing']:
                pass

            self.do_action(best_action[0], gameMap)

        elif self.fighting_state == FIGHT_STATE['fighting']:
            best_action = self.decide_fight_move(gameMap)
            self.do_fight_action(best_action)


    def do_fight_action(self, action_name):
        self.last_action = action_name
        damage = 0
        # with weapon 1d6 damage + 1d(str/2) + 1
        if self.has_weapon:
            damage = random.randrange(1, 7) + random.randrange(1, self.attributes['strength'] / 2) + 1
        else:  # without, 1d2 damage + 1d(str)
            damage = random.randrange(1, 3) + random.randrange(1, self.attributes['strength'] + 1)
        draw = random.random()
        chance_mult = 1

        if self.attributes['fighting_skill'] > 3:
            chance_mult += 0.1

        if self.attributes['fighting_skill'] > 7:
            chance_mult += 0.15

        if action_name == 'attack_head':
            if draw < 0.5 * chance_mult:
                self.opponent.hurt(damage + 2, 'head')
                self.goals[7].value = max(self.goals[7].value - (damage + 2) / 2, 0)
        elif action_name == 'attack_chest':
            if draw < 0.8 * chance_mult:
                self.opponent.hurt(damage + 1, 'chest')
                self.goals[7].value = max(self.goals[7].value - (damage + 1) / 2, 0)
        elif action_name == 'attack_gut':
            if draw < 0.8 * chance_mult:
                self.opponent.hurt(damage, 'gut')
                self.goals[7].value = max(self.goals[7].value - (damage) / 2, 0)
        elif action_name == 'attack_legs':
            if draw < 0.9 * chance_mult:
                self.opponent.hurt(damage - 1, 'legs')
                self.goals[7].value = max(self.goals[7].value - (damage - 1) / 2, 0)
        elif action_name == 'flee':
            self.opponent.disengage_in_combat(self)
            for goal in self.goals:
                if goal.name == "kill":
                    goal.value = 0
            self.fighting_state = FIGHT_STATE['fleeing']

    def do_action(self, action, game_map):
        self.last_action = action
        rand = random.randint(0, 1)
        loc = game_map[self.state[0]][self.state[1]]
        if action.index >= 0 and action.index <= 3:  # moving so don't know what gonna do here
            loc.setTribute(None)
            self.state = ((self.state[0] + action.delta_state[0]) % engine.GameEngine.map_dims[0],
                (self.state[1] + action.delta_state[1]) % engine.GameEngine.map_dims[1])
            (game_map[self.state[0]][self.state[1]]).setTribute(self)
        elif action.index == 4:  # find food
            food_prob = loc.getFoodChance()
            for goal in self.goals:
                if goal.name == "hunger":
                    if rand <= food_prob:
                        goal.value -= action.values[0]
        elif action.index == 5:  # kill
            self.sighted.engage_in_combat(self)
        elif action.index == 6:  # scavenger
            pass
        elif action.index == 7:  # craft
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
            if goal.name == "kill" and self.fighting_state != FIGHT_STATE['fleeing']:
                goal.value += ((self.attributes["bloodlust"]-1)/5.0)
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
                if(goal.name == "ally" and not self.has_ally and not self.has_weapon):
                    goal.value +=0.05
                if(goal.name == "hide" and not self.has_ally and not self.has_weapon):
                    goal.value += 0.01
                if goal.name == "ally" and not self.has_ally and not self.has_weapon:
                    goal.value += 0.05
            if goal.name == "hunger":
                goal.value += ((1/self.attributes['endurance']) + (self.attributes['size']/5))
            if goal.name == "thirst":
                goal.value += 1/self.attributes['endurance']
            if goal.name == "rest":
                goal.value += (1/self.attributes['stamina'] + self.goals[0].value/50 + self.goals[1].value/30)
            if goal.name == 'fear':
                goal.value -= 1


    #Action will update the state of the world by calculating
    #Goal updates and where it is / fuzzy logic of where other tributes are
    #will update current selfs world.
    def apply_action(self, action, gameMap):
        loc = gameMap[self.state[0]][self.state[1]]
        if 3 >= action.index >= 0:  # moving so don't know what gonna do here
            distance_before = 0
            if self.opponent:
                distance_before = abs(self.state[0] - self.last_opponent.state[0]) + \
                                  abs(self.state[1] + self.last_opponent.state[1])
            self.state = ((self.state[0] + action.delta_state[0]) % engine.GameEngine.map_dims[0],
                          (self.state[1] + action.delta_state[1]) % engine.GameEngine.map_dims[1])

            distance_after = 1
            if self.opponent:
                distance_after = abs(self.state[0] - self.last_opponent.state[0]) + \
                                 abs(self.state[1] + self.last_opponent.state[1])

            if distance_after <= distance_before:
                self.goals[7].value += random.randrange(1, 10)

            g = random.choice(self.goals)
            g.value -= -0.5
        elif action.index == 4:#find food
             foodProb = loc.getFoodChance()
             for goal in self.goals:
                if goal.name == "hunger":
                    goal.value -= foodProb* action.values[0]
        elif action.index == 5: #kill
            for goal in self.goals:
                if goal.name == "kill":
                    goal.value -= action.values[0]
                if goal.name == "fear":
                    if self.surmise_enemy_hit(self.sighted) > self.surmise_enemy_hit(self):
                        goal.value += 10
                    if self.surmise_escape_turns(self.sighted) < 5:
                        goal.value += 10

                    weakness = self.surmise_enemy_weakness(self.sighted)
                    goal.value -= weakness
                    if weakness < 1:
                        goal.value -= 11

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
