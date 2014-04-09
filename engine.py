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
    @staticmethod
    def start():
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

        view.render(state)

        return True