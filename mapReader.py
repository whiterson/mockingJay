__author__ = 'Whitney'

import sys
import PIL
import pygame
import locationDef
from PIL import Image

def deepForest():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID DeepForest\n')
    testFile.close()

def dirt():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Dirt\n')
    testFile.close()

def grass():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Grass\n')
    testFile.close()

def ice():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Ice\n')
    testFile.close()

def lightForest():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID lightForest\n')
    testFile.close()

def lowVegetation():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID lowVegetation\n')
    testFile.close()

def mud():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Mud\n')
    testFile.close()

def rock():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Rock\n')
    testFile.close()

def sand():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Sand\n')
    testFile.close()

def shallowWater():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID shallowWater\n')
    testFile.close()

def snow():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID snow\n')
    testFile.close()

def swimmingWater():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID swimmingWater\n')
    testFile.close()

def tallGrass():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID tallGrass\n')
    testFile.close()

def wadingWater():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID wadingWater\n')
    testFile.close()

def cornucopia():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID cornucopia\n')
    testFile.close()

def startSpot():
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID startSpot\n')
    testFile.close()

"""My Python Switch Case Based on Pixel Value"""
switch = {(1, 35, 18) : deepForest,
          (97, 63, 2) : dirt,
          (70, 152, 18) : grass,
          (233, 244, 248) : ice,
          (2, 117, 62) : lightForest,
          (104, 142, 65) : lowVegetation,
          (58, 43, 20) : mud,
          (155, 154, 150) : rock,
          (246, 238, 176) : sand,
          (184, 224, 236) : shallowWater,
          (247, 249, 248) : snow,
          (38, 100, 121): swimmingWater,
          (169, 153, 18): tallGrass,
          (88, 156, 179): wadingWater,
          (0,0,0): cornucopia,
          (0,0,100): startSpot
}

def readMap(map):
    testFile = open('maptest.txt', 'a')
    testFile.write('\n\n=============================\nNew Map Test\n=============================\n\n')
    map = Image.open('terrains/wadingWater.jpg')
    pixelMap = map.load()
    for i in range(map.size[0]):    # for every pixel:
        for j in range(map.size[1]):
            pixel = pixelMap[i,j]
            if pixel in switch:
                switch[pixel]()
            else:
                testFile.write("Color Error\n")
    testFile.close()
    return gameMap