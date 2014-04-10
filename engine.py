__author__ = 'Nathan'

import pygame
import graphics
import game
from action import Action
from tribute import Tribute


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
        move_up = Action(2, '', 1, 0)
        move_down = Action(2, '', 1, 1)
        move_right = Action(2, '', 1, 2)
        move_left = Action(2, '', 1, 3)

        #create the goals here
        #not really needed right now

        #creates all the
        actions = [move_up, move_down, move_right, move_left]
        for i in range(0, 11):
            me.tributes.append(Tribute([], actions))

        me.view = graphics.GameView(50, 50)
        me.state = game.GameState()
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
            action = tribute.bestAction()
            GameEngine.doAction(action)

        me.view.render(me.state)
        return True

    @staticmethod
    def doAction(action):
        #Need to apply the action here
        pass