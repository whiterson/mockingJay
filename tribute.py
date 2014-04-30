import random
import engine
import json
import copy
import sys
from probability import uniform_variable as U
from weaponInfo import weaponInfo
from weapon import weapon
import mapReader

class Particle(object):
    def __init__(self, state=(0, 0), width=1, height=1):
        self.state = state
        self.width, self.height = width, height

FIGHT_STATE = {'not_fighting': 0, 'fleeing': 1, 'fighting': 2}
NAVIGATION_POINTS = [(25, 25), (5, 5), (45, 5), (45, 45), (5, 45)]
FIGHT_EMERGENCY_CUTOFF = 80

class Tribute(Particle):
    #Goals = list of goals for tribute
    ################ ACTIONS
    # movement l,r,u,d
    # hunt
    # fight
    # scavenge
    # craft
    # hide
    # water
    # rest
    # talk
    ID_COUNTER = 0
    def __init__(self, goals, actions, x=0, y=0, district='d12', gender='male', do_not_load=False):
        Particle.__init__(self, (x, y), 1, 1)
        self.id = Tribute.ID_COUNTER
        Tribute.ID_COUNTER += 1
        self.goals = goals
        self.actions = actions

        # remove the fight action. we don't want them fighting unless someone is in range
        self.fight_action = actions[5]
        self.explore_action = actions[12]
        self.actions = self.actions[:5] + self.actions[6:12]

        self.district = district
        self.has_weapon = False
        self.weapon = weapon('')
        self.has_ally = False
        self.allies = []
        self.craftPouch = []
        self.fighting_state = FIGHT_STATE['not_fighting']
        self.opponent = None
        self.last_opponent = None
        self.sighted = None
        self.last_sighted_location = None
        self.last_action = None
        self.printy_action = 'none'
        self.old_state = self.state
        self.visited_set = set()
        self.explore_point_index = 0
        self.explore_point = NAVIGATION_POINTS[self.explore_point_index]

        self.hidden = False

        self.weaponInfo = weaponInfo()
        self.wepCanCraft = ''
        self.bestScavChoice = ''
        self.bestScavPoints = 0

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
        n_actions =  self.actions[:5] + [self.fight_action] + self.actions[5:12] + [self.explore_action]
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
        n.printy_action = self.printy_action
        n.last_opponent = self.last_opponent
        n.bestScavChoice = self.bestScavChoice
        n.bestScavPoints = self.bestScavPoints
        n.visited_set = self.visited_set.copy()
        n.explore_point = self.explore_point
        n.explore_point_index = self.explore_point_index
        n.craftPouch = self.craftPouch
        n.wepCanCraft = self.wepCanCraft
        n.hidden = self.hidden
        n.last_sighted_location = self.last_sighted_location
        n.id = self.id
        return n

    def __repr__(self):
        s = '<Tribute>(' + self.last_name + ', ' + self.first_name + ', ' + self.gender + ')'
        return s

    def engage_in_combat(self, t):
        if self.fighting_state == FIGHT_STATE['not_fighting']:
            self.fighting_state = FIGHT_STATE['fighting']
            self.opponent = t
            self.last_opponent = self.opponent
            t.engage_in_combat(self)
            if engine.GameEngine.FIGHT_MESSAGES:
                print str(self) + ' is engaging in combat with ' + str(t) + '!'
        elif self.fighting_state == FIGHT_STATE['fleeing']:
            self.opponent = t

            if self.opponent.fighting_state != FIGHT_STATE['fleeing']:
                t.engage_in_combat(self)

            if engine.GameEngine.FIGHT_MESSAGES:
                print str(self) + ' is being chased by ' + str(t) + '!'

    def disengage_in_combat(self, t):
        if self.fighting_state != FIGHT_STATE['not_fighting']:
            self.fighting_state = FIGHT_STATE['not_fighting']
            self.opponent = None
            t.disengage_in_combat(self)
            if engine.GameEngine.FIGHT_MESSAGES:
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
        return None

    def hurt(self, damage, place):
        if engine.GameEngine.FIGHT_MESSAGES:
            print str(self) + ' was hit in the ' + place + ' for ' + str(damage) + ' damage'

        self.goals[3].modify_value(-3)
        self.stats['health'] -= damage
        self.goals[7].value += damage*10
        if self.stats['health'] <= 0:
            self.killed = True
            self.killedBy = self.opponent
            if engine.GameEngine.FIGHT_MESSAGES:
                print str(self) + ' was killed by ' + str(self.killedBy)
            self.disengage_in_combat((self.opponent or self.killedBy or self.last_opponent))

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
        if self.goals[7].value < random.randrange(105, 150):
            actions = ['attack_head', 'attack_chest', 'attack_gut', 'attack_legs']
            return random.choice(actions)
        else:
            ###print str(self), ' became scared and is trying to flee!'
            return 'flee'

    def act(self, gameMap, game_state):
        if self.fighting_state != FIGHT_STATE['fighting']:
            best_action = (None, sys.maxint)
            actions = self.actions

            self.sighted = self.enemy_in_range(game_state)
            if self.sighted:
                self.last_sighted_location = self.sighted.state

            if self.sighted and not self.sighted.killed:
                actions = self.actions + [self.fight_action]

            if self.goals[0].value > 90 or self.goals[1].value > 50:
                actions = self.actions + [self.explore_action]
                self.explore_point = NAVIGATION_POINTS[self.explore_point_index]
            elif self.goals[3].value > FIGHT_EMERGENCY_CUTOFF and not self.sighted:
                actions = self.actions + [self.explore_action]
                if self.last_sighted_location:
                    self.explore_point = self.last_sighted_location

            neighbors = mapReader.get_neighbors2(gameMap, self.state)
            forbidden_states = []
            for trib in engine.GameEngine.tributes:
                if trib.state in neighbors and trib.id != self.id:
                    forbidden_states.append(trib.state)

            for a in actions:
                n_pos = mapReader.add_states(self.state, a.delta_state)
                if n_pos in forbidden_states:
                    continue
                t = copy.deepcopy(self)
                t.apply_action(a, gameMap)
                v = t.calc_min_discomfort(0, 2, gameMap, actions)
                if v < best_action[1]:
                    best_action = (a, v)
            thirst = 0
            hung = 0
            rest = 0

            # for goal in self.goals:
            #     rand = random.randint(0,2)
            #     #very hungry and slightly hungry
            #     if goal.name == 'hunger' and ((goal.value > 22 and goal.value < 26) or (goal.value >13 and goal.value <16)):
            #         best_action = (self.actions[rand], 100)
            #         hung = goal.value
            #
            #
            #     #very thirsty and slightly thirsty
            #     if goal.name == 'thirst' and ((goal.value > 22 and goal.value < 26) or (goal.value>13 and goal.value < 16)):
            #         best_action = (self.actions[rand], 100)
            #         thirst = goal.value
            #
            # if self.goals[3].value >= 150 and thirst < 33 and hung < 33 and rest < 40:
            #     best_action = (self.actions[rand+1], 100)

            self.do_action(best_action[0], gameMap)

        elif self.fighting_state == FIGHT_STATE['fighting']:
            best_action = self.decide_fight_move(gameMap)
            self.do_fight_action(best_action)

    def do_fight_action(self, action_name):

        if self.opponent and mapReader.l1_dist(self.state, self.opponent.state) > 2:
            return

        if self.opponent.killed:
            self.disengage_in_combat(self.opponent)
            return

        self.goals[3].modify_value(-1)

        if self.opponent.hidden:
            print str(self), ' cannot find ', str(self.opponent)

        self.last_action = action_name
        self.printy_action = action_name
        damage = 0
        # with weapon 1d6 damage + 1d(str/2) + 1
        if self.has_weapon:
            damage = self.weapon.damage + random.randrange(1, (self.attributes['strength'] / 4) + 2) + random.randint(0, self.attributes['weapon_skill']/2 + 1)+ 1
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

        ##IF you can Craft a weapon, do it
        ##if(not self.has_weapon):
        ##    for weapon in self.weaponInfo.weaponList:
        ##        if self.weaponInfo.canCraft(weapon, self.craftPouch):
        ##            action.index = 7
         ##           self.wepCanCraft = weapon


        self.hidden = False

        self.last_action = action
        self.printy_action = action.description
        rand = (random.randint(1, 10)) / 10
        loc = game_map[self.state[0]][self.state[1]]
        if action.index >= 0 and action.index <= 3:  # moving so don't know what gonna do here
            loc.setTribute(None)
            self.old_state = self.state
            (game_map[self.state[0]][self.state[1]]).setTribute(None)
            self.state = ((self.state[0] + action.delta_state[0]) % engine.GameEngine.map_dims[0],
                (self.state[1] + action.delta_state[1]) % engine.GameEngine.map_dims[1])
            (game_map[self.state[0]][self.state[1]]).setTribute(self)
        elif action.index == 4:  # find food
            food_prob = loc.getFoodChance()
            for goal in self.goals:
                if goal.name == "hunger":
                    if rand <= food_prob:
                        goal.value -= action.values[0]*3
        elif action.index == 5:  # fight
            self.sighted.engage_in_combat(self)
            self.goals[3].value = max(self.goals[3].value - action.values[0], 0)
        elif action.index == 6:  # scavenge
            wep_prob = loc.getWeaponChance()
            for goal in self.goals:
                if goal.name == "getweapon":
                    if wep_prob > 0.9:
                        if rand <= wep_prob:
                            self.getWeapon()
                            goal.value -= action.values[0]
                    else:
                        #doCraftScavenge will return zero if you fail to find something, and one if you succeed
                        num = self.checkCraftScavenge(game_map)
                        goal.value -= self.bestScavPoints * self.doCraftScavenge(game_map, self.bestScavChoice)
        elif action.index == 7:  # craft
            ##Crafting Probability is factored into doCraftWeapon
            self.checkCraftWeapon()
            if self.wepCanCraft != '':
                for goal in self.goals:
                    if goal.name == "getweapon":
                        ## Returns boolean if you did it or not
                        crafted = self.doCraftWeapon(game_map, self.wepCanCraft)
                        if crafted:
                            goal.value = 0
                        else:
                            goal.value -= (self.attributes['crafting_skill'])
        elif action.index == 8:  # hide
            ub = self.attributes['camouflage_skill']
            if random.randrange(0, 11) < ub:
                self.hidden = True

        elif action.index == 9:  # get water
            water_prob = loc.getWaterChance()
            for goal in self.goals:
                if goal.name == "thirst":
                    if rand <= water_prob:
                        goal.value -= action.values[0]

        elif action.index == 10:  # rest
            for goal in self.goals:
                if goal.name == "rest":
                    goal.value -= action.values[0]
        elif action.index == 11:  # talk ally
            f1 = self.attributes['friendliness']
            x = self.state[0]
            y = self.state[1]
            w = engine.GameEngine.map_dims[0]
            h = engine.GameEngine.map_dims[1]
            targ = game_map[(x + 1) % w][y].tribute or \
                   game_map[(x - 1) % w][y].tribute or \
                   game_map[x][(y + 1) % h].tribute or \
                   game_map[x][(y - 1) % h].tribute
            if not targ:
                print 'No target for ally!'
            elif targ not in self.allies and targ.id != self.id:
                f2 = targ.attributes['friendliness']
                a1 = self.attributes['district_prejudices'][targ.district]
                a2 = targ.attributes['district_prejudices'][self.district]
                v = (f1 + f2 + a1 + a2) / 224.0
                if random.random() < v:
                    ##print str(self), ' and ', str(targ), ' have gotten allied!'
                    self.allies.append(targ)
                    targ.allies.append(self)
                    self.goals[6].value = 0

        elif action.index == 12:  # explore
            directions = mapReader.get_neighbors(game_map, self.state)
            evals = []

            for i, direction in enumerate(directions):
                if game_map[direction[0]][direction[1]].tribute is None:
                    evals.append((mapReader.l1_dist(direction, self.explore_point), direction, i))
            if len(evals) > 0:
                direction = min(evals, key=lambda x: x[0] + random.random() / 1000)  # rand is for breaking ties
                if mapReader.l1_dist(self.explore_point, direction[1]) < 3:
                    if self.goals[3].value > FIGHT_EMERGENCY_CUTOFF:
                        self.explore_point = (self.explore_point[0] + U(0, 16),
                                              self.explore_point[1] + U(0, 16))
                    else:
                        self.explore_point_index = (self.explore_point_index + 1) % len(NAVIGATION_POINTS)
                        self.explore_point = NAVIGATION_POINTS[self.explore_point_index]
            ##print 'exploring!!'
                self.state = direction[1]



    def calc_disc(self, gameMap):
        ret = 0
        for goals in self.goals:
            ret += goals.value * goals.value
        return ret

    def end_turn(self):
        for goal in self.goals:
            if goal.name == "kill" and self.fighting_state != FIGHT_STATE['fleeing']:
                goal.value += ((self.attributes["bloodlust"]-1)/5.0) + 1
            if (int(self.district[1:]) == 1 or int(self.district[1:]) or int(self.district[1:]) == 4):
                if goal.name == 'kill':
                    goal.value +=0.1
                if(goal.name == 'getweapon' and not self.has_weapon):
                    goal.value += 0.05
            if (int(self.district[1:]) == 1 or int(self.district[1:]) or int(self.district[1:]) == 4):
                if goal.name == 'kill':
                    goal.value +=0.25
                if goal.name == 'getweapon' and not self.has_weapon:
                    goal.value += (1/(self.attributes['size'] + self.attributes['strength']))
            if (self.attributes['size'] + self.attributes['strength']) < 4:
                if goal.name == 'weapon' and not self.has_weapon:
                    goal.value += 0.1
                if(goal.name == 'ally' and not self.has_ally and not self.has_weapon):
                    goal.value +=0.05
                if(goal.name == 'hide' and not self.has_ally and not self.has_weapon):
                    goal.value += 0.01
                if goal.name == 'ally':
                    goal.value += 0.05 / (len(self.allies) + 1)**2
            if goal.name == 'hunger':
                goal.value += ((1.0/self.attributes['endurance']) + (self.attributes['size']/5.0))
            if goal.name == 'thirst':
                goal.value += 1.0/self.attributes['endurance']
            if goal.name == 'rest':
                goal.value += (1.0/self.attributes['stamina'] + self.goals[0].value/50.0 + self.goals[1].value/30.0)
            if goal.name == 'fear':
                goal.value = max(goal.value - 2.5, 0)
                if goal.value < 30 and self.fighting_state == FIGHT_STATE['fleeing']:
                    self.fighting_state = FIGHT_STATE['not_fighting']
            if goal.name == 'getweapon' and not self.has_weapon:
                goal.value += 0.5

            goal.value = max(goal.value, 0)


    #Action will update the state of the world by calculating
    #Goal updates and where it is / fuzzy logic of where other tributes are
    #will update current selfs world.
    def apply_action(self, action, gameMap):
        # [hunger, thirst, rest, kill, hide, getweapon, ally, fear]
        loc = gameMap[self.state[0]][self.state[1]]

        distance_before = 0
        if self.last_opponent and self.fighting_state == FIGHT_STATE['fleeing']:
            distance_before = abs(self.state[0] - self.last_opponent.state[0]) + \
                              abs(self.state[1] + self.last_opponent.state[1])

        if 3 >= action.index >= 0:  # moving so don't know what gonna do here
            self.old_state = self.state
            self.state = ((self.state[0] + action.delta_state[0]) % engine.GameEngine.map_dims[0],
                          (self.state[1] + action.delta_state[1]) % engine.GameEngine.map_dims[1])

            g = random.choice(self.goals)
            g.value -= -0.5
        elif action.index == 4:  # hunt
            foodProb = loc.getFoodChance()
            self.goals[0].value -= foodProb * action.values[0]
        elif action.index == 5:  # kill

            if abs(self.sighted.state[0] - self.state[0]) + abs(self.sighted.state[1] - self.state[1]) <= 2:
                self.goals[3].value = max(self.goals[3].value - action.values[0]*10, 0)

            if self.surmise_enemy_hit(self.sighted) > self.surmise_enemy_hit(self):
                self.goals[7].value += 5
            if self.surmise_escape_turns(self.sighted) < 5:
                self.goals[7].value += 5
            weakness = self.surmise_enemy_weakness(self.sighted)
            # self.goals[7].value -= weakness
            if weakness < 1:
                self.goals[7].value -= 11

        elif action.index == 6:  # scavenge
            wepChance = loc.getWeaponChance()
            if wepChance > 0.9 and not self.has_weapon:
                self.goals[5].value -= wepChance * action.values[0]
            elif(not self.has_weapon):
                self.goals[5].value -= self.checkCraftScavenge(gameMap)

        elif action.index == 7:  # craft
            craftProb = self.checkCraftWeapon()
            self.goals[5].value -= (self.goals[5].value * craftProb)

        elif action.index == 8:  # hide
            self.goals[7].modify_value(-(action.values[0] * (self.attributes['camouflage_skill'] / 10.0)))
        elif action.index == 9:  # get_water
            waterProb = loc.getWaterChance()
            self.goals[1].value -= waterProb * action.values[0]
        elif action.index == 10:  # rest
            self.goals[2].value -= action.values[0]
        elif action.index == 11: # talk ally
            x = self.state[0]
            y = self.state[1]
            w = engine.GameEngine.map_dims[0]
            h = engine.GameEngine.map_dims[1]
            if (gameMap[(x + 1) % w][y].tribute is not None and gameMap[(x + 1) % w][y].tribute not in self.allies) or \
               (gameMap[(x - 1) % w][y].tribute is not None and gameMap[(x - 1) % w][y].tribute not in self.allies) or \
               (gameMap[x][(y + 1) % h].tribute is not None and gameMap[x][(y + 1) % h].tribute not in self.allies) or \
               (gameMap[x][(y - 1) % h].tribute is not None and gameMap[x][(y - 1) % h].tribute not in self.allies):
                self.goals[6].value -= action.values[0]
        elif action.index == 12:  # explore
            self.goals[0].value = max(self.goals[0].value - action.values[0], 0)
            self.goals[1].value = max(self.goals[1].value - action.values[1], 0)
            self.goals[3].value = max(self.goals[1].value - action.values[2], 0)

        distance_after = 1
        if self.last_opponent and self.fighting_state == FIGHT_STATE['fleeing']:
            distance_after = abs(self.state[0] - self.last_opponent.state[0]) + \
                             abs(self.state[1] + self.last_opponent.state[1])

        if distance_after <= distance_before and self.fighting_state == FIGHT_STATE['fleeing']:
            self.goals[7].value += 100

    def calc_discomfort(self):
        val = 0
        for goal in self.goals:
            if(goal.value > 0):
                val += goal.value*goal.value
        return val

    def checkDead(self):
        for goal in self.goals:
            if goal.name == "hunger":
                if goal.value >= 200:
                    self.killed = True
                    return " starvation "
            #You get thirsty a lot faster than you get hungry
            if goal.name == "thirst":
                if goal.value >= 200:
                    self.killed = True
                    return " terminal dehydration "
            if goal.name == "rest":
                if goal.value >= 250:
                    self.killed = True
                    return " exhaustion "

        if self.killed:
            return self.killedBy
        else:
            return None

    def getWeapon(self):
        self.has_weapon = True
        weaponType = random.randint(1, 10)
        self.weapon = weapon(self.weaponInfo.weaponType(weaponType))
        print str(self), ' has picked up a ', str(self.weapon)


    def checkCraftScavenge(self, game_map):
        self.bestScavChoice = ''
        self.bestScavPoints = 0
        location = game_map[self.state[0]][self.state[1]]
        craftTypes = self.weaponInfo.craftTypes
        bestPossPoints = 0
        for type in craftTypes:
            poss = (self.retScavTypeProb(type, location) * 10)
            if poss != 0:
                mockPouch = copy.deepcopy(self.craftPouch)
                ##If you've already got what you're scavenging for
                already_have = 0
                for item in mockPouch:
                    if item == type:
                        already_have = 1
                if already_have < 1:
                    mockPouch.append(type)
                    for weapon in self.weaponInfo.weaponList:
                        possPoints = 0
                        canCraft = self.weaponInfo.canCraft(weapon,mockPouch)
                        if canCraft:
                            possPoints += 5 + (self.weaponInfo.weaponStrength(weapon)/2)
                            if possPoints > self.bestScavPoints:
                                self.bestScavPoints = possPoints
                                self.bestScavChoice = type
                                bestPossPoints = possPoints
                                return bestPossPoints
                        else:
                            numItemsNeedToCraft = len(self.weaponInfo.itemsNeededToCraft(weapon,mockPouch))
                            possPoints += 5 - numItemsNeedToCraft + (self.weaponInfo.weaponStrength(weapon)/10) + poss
                            if possPoints > self.bestScavPoints:
                                self.bestScavPoints = possPoints
                                self.bestScavChoice = type
                                bestPossPoints = possPoints

        return bestPossPoints

    def doCraftScavenge(self, game_map, type):
        loc = game_map[self.state[0]][self.state[1]]
        crTyProb = self.retScavTypeProb(type, loc)
        chance = random.randint(1, 10)
        if chance <= (10*crTyProb):
            cValue = 1
            self.craftPouch.append(type)
        else:
            cValue = 0
        return cValue

    def retScavTypeProb(self, type, loc):
        if type == 'shortStick':
            crTyProb = loc.shortStickChance
        elif type == 'sharpStone':
            crTyProb = loc.sharpStoneChance
        elif type == 'feather':
            crTyProb = loc.featherChance
        elif type == 'vine':
            crTyProb = loc.vineChance
        elif type == 'longStick':
            crTyProb = loc.longStickChance
        elif type == 'broadStone':
            crTyProb  = loc.broadStoneChance
        elif type == 'longGrass':
            crTyProb  = loc.longGrassChance
        elif type == 'reeds':
            crTyProb  = loc.reedsChance
        elif type == 'pebbles':
            crTyProb  = loc.pebblesChance
        elif type == 'thorns':
            crTyProb = loc.thornsChance
        else:
            crTyProb = 0

        return crTyProb

    #Returns the probability of Crafting a Weapon based on your items & skill
    def checkCraftWeapon(self):
        probCraft = self.attributes['crafting_skill']

        craftableWeapon = None
        maxWepStrength = 0
        numItemsCraftWep = 0
        canCraft = 0

        for wepType in self.weaponInfo.weaponList:
            ans = self.weaponInfo.canCraft(wepType, self.craftPouch)
            if(ans):
                canCraft = 1
                strength = self.weaponInfo.weaponStrength(wepType)
                if strength > maxWepStrength:
                    maxWepStrength = strength
                    numItemsCraftWep = self.weaponInfo.totalNumItemsToCraft(wepType)
                    craftableWeapon = wepType
                elif strength == maxWepStrength:
                    if self.weaponInfo.totalNumItemsToCraft(wepType) < numItemsCraftWep:
                        maxWepStrength = strength
                        numItemsCraftWep = self.weaponInfo.totalNumItemsToCraft(wepType)
                        craftableWeapon = wepType
                else:
                    craftableWeapon = self.wepCanCraft

        self.wepCanCraft = craftableWeapon
        return probCraft*canCraft*100

    #Craft the weapon based on your skill. If you fail to craft, you still lose the items. Wah-wah.
    def doCraftWeapon(self, game_map, wepToCraft):
        itemsUsed = self.weaponInfo.totalItemsToCraft(wepToCraft)
        for needed in itemsUsed:
            for supply in self.craftPouch:
                if needed == supply:
                    self.craftPouch.remove(supply)
        chance = random.randint(1,10)
        if chance <= self.attributes['crafting_skill']:
            crafted = True
            self.weapon = weapon(wepToCraft)
        else:
            crafted = False

        self.wepCanCraft = None
        self.has_weapon = crafted
        return crafted
