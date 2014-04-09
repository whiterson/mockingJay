__author__ = 'Nathan'

import pygame
import sys
import graphics


class GameEngine(object):
    """
    here we will essentially manage everything and probably handle the controls
    """
    constants = range(1)
    @staticmethod
    def start():
        pass

    @staticmethod
    def stop():
        pass

    @staticmethod
    def loop():
        """
        The main loop of the program
        @return: None
        """
        view = graphics.GameView(500, 500)

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()