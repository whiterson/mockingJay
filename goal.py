class Goal:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.rate = 1

    def clone(self):
        g = Goal(self.name[:], self.value)
        g.rate = self.rate
        return g

    def modify_value(self, mod):
        self.value = max(self.value + mod, 0)