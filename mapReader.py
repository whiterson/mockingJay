__author__ = 'Whitney'

import sys
import PIL
import pygame
from PIL import Image
import numpy


def dirt():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Dirt')
    testFile.close()

def grass():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Dirt')
    testFile.close()

def ice():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Dirt')
    testFile.close()

def lightForest():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Dirt')
    testFile.close()

def lowVegetation():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Dirt')
    testFile.close()

def mud():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Dirt')
    testFile.close()

def rock():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Dirt')
    testFile.close()

def sand():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Dirt')
    testFile.close()

def shallowWater():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Dirt')
    testFile.close()

def snow():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Dirt')
    testFile.close()

def swimmingWater():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Dirt')
    testFile.close()

def tallGrass():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Dirt')
    testFile.close()

def wadingWater():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Dirt')
    testFile.close()

"""My Python Switch Case Based on Pixel Value"""
"""I have terrains stored, and I was going to get the pixel value of each color, and use them
    as the switch case values. Because Python isn't working though, I haven't done that yet. So everything's
    set up, I just need the switch case stuff. Blargh."""
switch = {0 : deepForest,
                1 : dirt,
                4 : grass,
                9 : ice,
                2 : lightForest,
                3 : lowVegetation,
                5 : mud,
                7 : rock,
                8 : sand,
                9 : shallowWater,
                10: snow,
                11: swimmingWater,
                12: tallGrass,
                13: wadingWater
}

def readMap():
    testFile = open('maptest.txt', 'a')
    testFile.write('=============================\nNew Map Test\n=============================\n\n')
    map = Image.open('terrains/deepForest.jpg')
    pixelMap = map.load()
    for pixel in pixelMap:
        """This is where the terrain arguments will go"""
        switch[pixel]()
    testFile.close()