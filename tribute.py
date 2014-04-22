import random
import engine
import json


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
    def best_action(self, depth, max_depth, action_name, ret):
        index = random.randint(0, len(self.actions) - 1)

        for action in self.actions:
            if depth == max_depth:
                ret.append((self.calc_disc(), action))
            else:
                # Apply action to world copy and update and go one depth farther in
                self.apply_action(action)
                if depth == 0:
                    self.best_action(depth + 1, 4, action, ret)
                else:
                    self.best_action(depth + 1, 4, action_name, ret)

    def act(self):
        # this function will have to be customized for each action
        del self.ret[:]
        self.best_action(0, 4, '', self.ret)
        best_val = 1000000
        for pairs in self.ret:
            if pairs[0] < best_val:
                best_val = pairs[0]
                action = pairs[1]
        
        self.state = ((self.state[0] + action.delta_state[0]) % engine.GameEngine.dims[0],
                      (self.state[1] + action.delta_state[1]) % engine.GameEngine.dims[1])

    # Action will update the state of the world by calculating
    # Goal updates and where it is / fuzzy logic of where other tributes are
    # will update current selfs world.
    def apply_action(self, action):
        return []

    def calc_disc(self):
        val = 0
        for goal in self.goals:
            val += goal.value*goal.value
        return val