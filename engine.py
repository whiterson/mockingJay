__author__ = 'Nathan'

import pygame
import graphics
import game


class GameEngine(object):
    """
    here we will essentially manage everything and probably handle the controls
    """
    constants = range(1)
    is_looping = False
    tributes = []
    @staticmethod
    def start():
        #create actions right now just moves
        moveUp = action(2, "", 1, 0)
        moveDown = action(2, "", 1, 1)
        moveRight = action(2, "", 1, 2)
        moveLeft = action(2, "", 1, 3)

        #create the goals here
        #not really needed right now

        #creates all the
        actions = [moveUp,moveDown,moveLeft,moveRight]
        for i in range(0, 11):
            tributes.append(Tribute([],actions))


        """
            Create the tributes here
            also need to create the goals
            and actions
        """
        is_looping = True
        while is_looping and GameEngine.loop():
            pass

    @staticmethod
    def stop():
        is_looping = False

    @staticmethod
    def loop():
        """
        What to do on each loop iteration
        @return: None
        """
        view = graphics.GameView(500, 500)
        state = game.GameState()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        for tribute in tributes:
            action = tribute.bestAction()
            doAction(action)
        view.render(state)

        return True

    @staticmethod
    def doAction(action):
        #Need to apply the action here