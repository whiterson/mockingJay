__author__ = 'Whitney'

import sys
import PIL
import pygame
from locationDef import locationDef
from PIL import Image

def deepForest(definition):
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID DeepForest\n')
    testFile.close()
    terrainType = 0

    definition.setTerrain(terrainType)
    definition.setFoodChance(0.3)
    definition.setWaterChance(0.0)
    definition.setShortStickChance(0.8)
    definition.setVisibility(0.2)
    definition.setSharpStoneChance(0.1)
    definition.setFeatherChance(0.2)
    definition.setVineChance(0.4)
    definition.setSpeedChange(2)
    definition.setWeaponChance(0.0)
    definition.setLongStickChance(0.6)
    definition.setBroadStoneChance(0.05)
    definition.setLongGrassChance(0.0)
    definition.setReedsChance(0.0)
    definition.setPebblesChance(0.05)
    definition.setThornsChance(0.3)

    return definition

def dirt(definition):
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Dirt\n')
    testFile.close()
    terrainType = 1

    definition.setTerrain(terrainType)
    definition.setFoodChance(0.05)
    definition.setWaterChance(0.0)
    definition.setShortStickChance(0.0)
    definition.setVisibility(1)
    definition.setSharpStoneChance(0.5)
    definition.setFeatherChance(0.05)
    definition.setVineChance(0.0)
    definition.setSpeedChange(1)
    definition.setWeaponChance(0.0)
    definition.setLongStickChance(0.0)
    definition.setBroadStoneChance(0.1)
    definition.setLongGrassChance(0.0)
    definition.setReedsChance(0.0)
    definition.setPebblesChance(0.2)
    definition.setThornsChance(0.0)

    return definition


def grass(definition):
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Grass\n')
    testFile.close()
    terrainType = 2

    definition.setTerrain(terrainType)
    definition.setFoodChance(0.1)
    definition.setWaterChance(0.0)
    definition.setShortStickChance(0.0)
    definition.setVisibility(1)
    definition.setSharpStoneChance(0.1)
    definition.setFeatherChance(0.2)
    definition.setVineChance(0.0)
    definition.setSpeedChange(1)
    definition.setWeaponChance(0.0)
    definition.setLongStickChance(0.0)
    definition.setBroadStoneChance(0.05)
    definition.setLongGrassChance(0.05)
    definition.setReedsChance(0.0)
    definition.setPebblesChance(0.1)
    definition.setThornsChance(0.0)

    return definition

def ice(definition):
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Ice\n')
    testFile.close()
    terrainType = 3

    definition.setTerrain(terrainType)
    definition.setFoodChance(0.0)
    definition.setWaterChance(0.6)
    definition.setShortStickChance(0.0)
    definition.setVisibility(1)
    definition.setSharpStoneChance(0.0)
    definition.setFeatherChance(0.0)
    definition.setVineChance(0.0)
    definition.setSpeedChange(3)
    definition.setWeaponChance(0.0)
    definition.setLongStickChance(0.0)
    definition.setBroadStoneChance(0.0)
    definition.setLongGrassChance(0.0)
    definition.setReedsChance(0.0)
    definition.setPebblesChance(0.0)
    definition.setThornsChance(0.0)

    return definition

def lightForest(definition):
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID lightForest\n')
    testFile.close()
    terrainType = 4

    definition.setTerrain(terrainType)
    definition.setFoodChance(0.3)
    definition.setWaterChance(0.0)
    definition.setShortStickChance(0.9)
    definition.setVisibility(0.9)
    definition.setSharpStoneChance(0.3)
    definition.setFeatherChance(0.6)
    definition.setVineChance(0.05)
    definition.setSpeedChange(1)
    definition.setWeaponChance(0.0)
    definition.setLongStickChance(0.6)
    definition.setBroadStoneChance(0.1)
    definition.setLongGrassChance(0.05)
    definition.setReedsChance(0.0)
    definition.setPebblesChance(0.1)
    definition.setThornsChance(0.1)

    return definition

def lowVegetation(definition):
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID lowVegetation\n')
    testFile.close()
    terrainType = 5

    definition.setTerrain(terrainType)
    definition.setFoodChance(0.6)
    definition.setWaterChance(0.0)
    definition.setShortStickChance(0.05)
    definition.setVisibility(0.05)
    definition.setSharpStoneChance(0.2)
    definition.setFeatherChance(0.2)
    definition.setVineChance(0.0)
    definition.setSpeedChange(1)
    definition.setWeaponChance(0.0)
    definition.setLongStickChance(0.0)
    definition.setBroadStoneChance(0.1)
    definition.setLongGrassChance(0.1)
    definition.setReedsChance(0.0)
    definition.setPebblesChance(0.05)
    definition.setThornsChance(0.6)

    return definition

def mud(definition):
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Mud\n')
    testFile.close()
    terrainType = 6

    definition.setTerrain(terrainType)
    definition.setFoodChance(0.0)
    definition.setWaterChance(0.05)
    definition.setShortStickChance(0.0)
    definition.setVisibility(1)
    definition.setSharpStoneChance(0.05)
    definition.setFeatherChance(0.0)
    definition.setVineChance(0.0)
    definition.setSpeedChange(1)
    definition.setWeaponChance(0.0)
    definition.setLongStickChance(0.0)
    definition.setBroadStoneChance(0.05)
    definition.setLongGrassChance(0.0)
    definition.setReedsChance(0.0)
    definition.setPebblesChance(0.1)
    definition.setThornsChance(0.0)

    return definition

def rock(definition):
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Rock\n')
    testFile.close()
    terrainType = 7

    definition.setTerrain(terrainType)
    definition.setFoodChance(0.0)
    definition.setWaterChance(0.0)
    definition.setShortStickChance(0.0)
    definition.setVisibility(1)
    definition.setSharpStoneChance(0.9)
    definition.setFeatherChance(0.0)
    definition.setVineChance(0.0)
    definition.setSpeedChange(1)
    definition.setWeaponChance(0.0)
    definition.setLongStickChance(0.0)
    definition.setBroadStoneChance(0.7)
    definition.setLongGrassChance(0.0)
    definition.setReedsChance(0.0)
    definition.setPebblesChance(0.8)
    definition.setThornsChance(0.0)

    return definition

def sand(definition):
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID Sand\n')
    testFile.close()
    terrainType = 8

    definition.setTerrain(terrainType)
    definition.setFoodChance(0.0)
    definition.setWaterChance(0.0)
    definition.setShortStickChance(0.0)
    definition.setVisibility(1)
    definition.setSharpStoneChance(0.1)
    definition.setFeatherChance(0.0)
    definition.setVineChance(0.0)
    definition.setSpeedChange(1)
    definition.setWeaponChance(0.0)
    definition.setLongStickChance(0.0)
    definition.setBroadStoneChance(0.05)
    definition.setLongGrassChance(0.0)
    definition.setReedsChance(0.0)
    definition.setPebblesChance(0.1)
    definition.setThornsChance(0.0)

    return definition

def shallowWater(definition):
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID shallowWater\n')
    testFile.close()
    terrainType = 9

    definition.setTerrain(terrainType)
    definition.setFoodChance(0.05)
    definition.setWaterChance(1)
    definition.setShortStickChance(0.0)
    definition.setVisibility(0.0)
    definition.setSharpStoneChance(0.2)
    definition.setFeatherChance(0.0)
    definition.setVineChance(0.05)
    definition.setSpeedChange(1)
    definition.setWeaponChance(0.0)
    definition.setLongStickChance(0.0)
    definition.setBroadStoneChance(0.05)
    definition.setLongGrassChance(0.0)
    definition.setReedsChance(0.6)
    definition.setPebblesChance(0.5)
    definition.setThornsChance(0.0)

    return definition

def snow(definition):
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID snow\n')
    testFile.close()
    terrainType = 10

    definition.setTerrain(terrainType)
    definition.setFoodChance(0.0)
    definition.setWaterChance(0.2)
    definition.setShortStickChance(0.0)
    definition.setVisibility(0.0)
    definition.setSharpStoneChance(0.1)
    definition.setFeatherChance(0.0)
    definition.setVineChance(0.0)
    definition.setSpeedChange(2)
    definition.setWeaponChance(0.0)
    definition.setLongStickChance(0.0)
    definition.setBroadStoneChance(0.05)
    definition.setLongGrassChance(0.0)
    definition.setReedsChance(0.0)
    definition.setPebblesChance(0.1)
    definition.setThornsChance(0.0)

    return definition

def swimmingWater(definition):
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID swimmingWater\n')
    testFile.close()
    terrainType = 11

    definition.setTerrain(terrainType)
    definition.setFoodChance(0.3)
    definition.setWaterChance(1)
    definition.setShortStickChance(0.0)
    definition.setVisibility(0.5)
    definition.setSharpStoneChance(0.0)
    definition.setFeatherChance(0.0)
    definition.setVineChance(0.0)
    definition.setSpeedChange(1)
    definition.setWeaponChance(0.0)
    definition.setLongStickChance(0)
    definition.setBroadStoneChance(0.1)
    definition.setLongGrassChance(0.0)
    definition.setReedsChance(0.0)
    definition.setPebblesChance(0.5)
    definition.setThornsChance(0.0)

    return definition

def tallGrass(definition):
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID tallGrass\n')
    testFile.close()
    terrainType = 12

    definition.setTerrain(terrainType)
    definition.setFoodChance(0.2)
    definition.setWaterChance(0.0)
    definition.setShortStickChance(0.1)
    definition.setVisibility(0.7)
    definition.setSharpStoneChance(0.2)
    definition.setFeatherChance(0.2)
    definition.setVineChance(0.4)
    definition.setSpeedChange(1)
    definition.setWeaponChance(0.0)
    definition.setLongStickChance(0.05)
    definition.setBroadStoneChance(0.0)
    definition.setLongGrassChance(1)
    definition.setReedsChance(0.0)
    definition.setPebblesChance(0.05)
    definition.setThornsChance(0.05)

    return definition

def wadingWater(definition):
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID wadingWater\n')
    testFile.close()
    terrainType = 13

    definition.setTerrain(terrainType)
    definition.setFoodChance(0.1)
    definition.setWaterChance(1)
    definition.setShortStickChance(0.0)
    definition.setVisibility(1)
    definition.setSharpStoneChance(0.4)
    definition.setFeatherChance(0.0)
    definition.setVineChance(0.05)
    definition.setSpeedChange(3)
    definition.setWeaponChance(0.0)
    definition.setLongStickChance(0.0)
    definition.setBroadStoneChance(0.05)
    definition.setLongGrassChance(0.0)
    definition.setReedsChance(0.7)
    definition.setPebblesChance(0.2)
    definition.setThornsChance(0.0)

    return definition

def cornucopia(definition):
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID cornucopia\n')
    testFile.close()
    terrainType = 14

    definition.setTerrain(terrainType)
    definition.setFoodChance(0.5)
    definition.setWaterChance(0.3)
    definition.setShortStickChance(0.0)
    definition.setVisibility(1)
    definition.setSharpStoneChance(0.0)
    definition.setFeatherChance(0.0)
    definition.setVineChance(0.0)
    definition.setSpeedChange(1)
    definition.setWeaponChance(0.9)
    definition.setLongStickChance(0.0)
    definition.setBroadStoneChance(0.0)
    definition.setLongGrassChance(0.0)
    definition.setReedsChance(0.0)
    definition.setPebblesChance(0.0)
    definition.setThornsChance(0.0)

    return definition

def startSpot(definition):
    testFile = open('maptest.txt', 'a')
    testFile.write('Pixel ID startSpot\n')
    testFile.close()
    terrainType = 15

    definition.setTerrain(terrainType)
    definition.setFoodChance(0.0)
    definition.setWaterChance(0.0)
    definition.setShortStickChance(0.0)
    definition.setVisibility(1)
    definition.setSharpStoneChance(0.0)
    definition.setFeatherChance(0.0)
    definition.setVineChance(0.0)
    definition.setSpeedChange(1)
    definition.setWeaponChance(0.0)
    definition.setLongStickChance(0.0)
    definition.setBroadStoneChance(0.0)
    definition.setLongGrassChance(0.0)
    definition.setReedsChance(0.0)
    definition.setPebblesChance(0.0)
    definition.setThornsChance(0.0)

    return definition

def colorError(definition):
    terrainType = 16

    definition.setTerrain(terrainType)
    definition.setFoodChance(0.0)
    definition.setWaterChance(0.0)
    definition.setShortStickChance(0.0)
    definition.setVisibility(0)
    definition.setSharpStoneChance(0.0)
    definition.setFeatherChance(0.0)
    definition.setVineChance(0.0)
    definition.setSpeedChange(0)
    definition.setWeaponChance(0.0)
    definition.setLongStickChance(0.0)
    definition.setBroadStoneChance(0.0)
    definition.setLongGrassChance(0.0)
    definition.setReedsChance(0.0)
    definition.setPebblesChance(0.0)
    definition.setThornsChance(0.0)

    return definition

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
          (84,86,90): startSpot,
          (300,300,300): colorError

}

def readMap(mapInput):
    testFile = open('maptest.txt', 'a')
    testFile.write('\n\n=============================\nNew Map Test\n=============================\n\n')
    map = Image.open(mapInput)

    gameMap = [[0 for t in xrange(map.size[0])] for r in xrange(map.size[1])]

    pixelMap = map.load()
    for i in range(map.size[0]):    # for every pixel:
        for j in range(map.size[1]):
            pixel = pixelMap[i,j]
            if pixel in switch:
                definition = locationDef()
                locDef  = switch[pixel](definition)
                gameMap[i][j] = locDef
            else:
                definition = locationDef()
                locDef = switch[(300,300,300)](definition)
                gameMap[i][j] = locDef
    testFile.close()
    return gameMap


def get_neighbors(map, location):
    w = len(map)
    h = len(map[0])
    up = (location[0], (location[1] - 1) % h)
    left = ((location[0] - 1) % w, location[1])
    down = (location[0], (location[1] + 1) % h)
    right = ((location[0] + 1) % w, location[1])
    return [up, left, down, right]


def l1_dist(state1, state2):
    return abs(state1[0] - state2[0]) + abs(state1[1] - state2[1])