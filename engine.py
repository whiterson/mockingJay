__author__ = 'Nathan'

import pygame
import graphics
import random
import map
from action import Action
from tribute import Tribute
from goal import Goal
from mapReader import readMap

class GameEngine(object):
    """
    here we will essentially manage everything and probably handle the controls
    """
    constants = range(1)
    is_looping = False
    tributes = []

    @staticmethod
    def start():
        me = GameEngine
        #create actions right now just moves
        goals = [0, 0, 0, 0, 0, 0, 0]
        actions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        #create the goals here
        #not really needed right now

        init_locations = [(x, y) for x in range(50) for y in range(50)]
        #creates all the actions
        for i in range(0, 1):
            location = random.choice(init_locations)
            init_locations.remove(location)
            me.tributes.append(Tribute(goals, actions, *location, district='d12', gender='male'))

        for i in range(0, 1):
            location = random.choice(init_locations)
            init_locations.remove(location)
            me.tributes.append(Tribute(goals, actions, *location, district='d12', gender='female'))

        for i in range(len(me.tributes)):
            initTribute = me.create_goals(me.tributes[i])
            me.tributes[i].goals = initTribute

        me.dims = (50, 50)
        me.gameMap = readMap('maps/field.png')
        me.view = graphics.GameView(*me.dims)
        me.map = map.Map('maps/field.png')
        me.state = me.map.seed_game_state(me.tributes)  # game.GameState()
        me.is_looping = True
        while me.is_looping and GameEngine.loop():
            pass

    @staticmethod
    def stop():
        GameEngine.is_looping = False

    @staticmethod
    def loop():
        """
        What to do on each loop iteration
        @return: None
        """
        me = GameEngine

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        for tribute in me.tributes:
            tribute.act(me.gameMap) #finds bestAction and does it.
            tribute.endTurn()
            death = tribute.checkDead()
            if not death is None:
                print tribute.first_name, " ", tribute.last_name, " death by ", death
                me.tributes.remove(tribute)
        me.view.render(me.state)

        me.state.update()
        return True

    @staticmethod
    def create_actions(tribute):
        #Move action
        move_up = Action([], '', 1, 0, (0, -1))
        move_down = Action([], '', 1, 1, (0, 1))
        move_right = Action([], '', 1, 2, (1, 0))
        move_left = Action([], '', 1, 3, (-1, 0))


        ################ INDEX LIST
        # 0-3 movement
        # 4 hunt
        # 5 fight
        # 6 scavenge
        # 7 craft
        # 8 hide
        # 9 water
        # 10 rest
        # 11 talk


        #1. How much I get back for doing the action in 2. EDIT THIS ONE
        #2. The action (lists, so it can affect more than one thing.)
        #3. Duration
        #4. Index
        #5. Movement Stuff (don't mess wid that)
        hunt = Action([5], ["hunger"], 1, 4,(0,0))

        fight = Action([5], ["kill"], 1, 5, (0,0))

        scavenger = Action([3], ["getweapon"], 1, 6, (0,0))
        craft = Action([4], ["getweapon"], 1, 7, (0,0))
        hide = Action([5], ["hide"], 1, 8, (0,0))
        getwater = Action([5], ["thirst"], 1, 9, (0,0))
        rest = Action([5], ["rest"], 1, 10, (0,0))
        talkAlly = Action([5], ["ally"], 1, 11, (0,0))

        return tribute

    @staticmethod
    def create_goals(tribute):
        #Just giving default values for now
        #Will figure out exact values later
        #Starting these at zero and plan to increment every turn
        hunger = Goal("hunger", 2)
        thirst = Goal("thirst", 2)
        rest = Goal("rest", 2)

        #KILL and HIDE are Changing Based on Attributes
        district = int(tribute.district[1:])

        #Is going to need to be changed somehow based on attributes
        kill = Goal("kill", 10-tribute.attributes['friendliness'])
        hide = Goal("hide", 0)

        #Also going to be dependent on the value of certain things
        getweapon = Goal("getweapon", 0)
        ally = Goal("ally", tribute.attributes['friendliness'])
        return [hunger, thirst, rest, kill, hide, getweapon, ally]