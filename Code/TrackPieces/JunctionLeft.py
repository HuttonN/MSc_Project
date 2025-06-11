# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 15:01:40 2023

@author: Admin
"""
import pygame
import math


def setNextID(self, x):
    global NextID
    self.NextID = x


def setSecondNextID(self, x):
    global SecondNextID
    self.SecondNextID = x


def setPrevID(self, x):
    global PrevID
    self.PrevID = x


def setID(self, x):
    global ID
    self.ID = x


def setCoordinates(self, x, y):
    global xCo
    global yCo
    self.xCo = x
    self.yCo = y


def setBranch(self, x):
    global branch
    self.branch = x

#     "LongRight";8;7;9;1
# "LongStraight";9;8;10;1
# "LongStraight";10;9;11;1
# "LongStraight";11;10;12;1
# "LongRight";12;11;13;1
# "LongRight";13;12;14;1
# "Station";14;13;15;1
# "LongRight";15;14;16;1
# "LongRight";16;15;1;1
# "LongRight";17;2;18;2
# "Station";18;17;19;2
# "LongRight";19;18;20;2
# "LongRight";20;19;11;2


class JunctionLeft(pygame.sprite.Sprite):

    global ID
    global PrevID
    global NextID
    global SecondNextID
    global xCo
    global yCo
    global branch
    global occupied

    def __init__(self, screen, currentID, previousID, firstnextID, secondnextID, branch):
        super(JunctionLeft, self).__init__()
        setID(self, currentID)
        setPrevID(self, previousID)
        setNextID(self, firstnextID)
        setSecondNextID(self, secondnextID)
        setBranch(self, branch)

    def adjustCompass(self, compass):
        return compass

    def setOccupied(self, x):
        global occupied
        self.occupied = x

    def adjustJunctionCompass(self, compass):
        if compass == "N":
            return "NW"
        elif compass == "NW":
            return "W"
        elif compass == "W":
            return "SW"
        elif compass == "SW":
            return "S"
        elif compass == "S":
            return "SE"
        elif compass == "SE":
            return "E"
        elif compass == "E":
            return "NE"
        elif compass == "NE":
            return "N"

    def isOccupied(self):
        return self.occupied

    def getID(self):
        return self.ID

    def getPrevID(self):
        return self.PrevID

    def getNextID(self):
        return self.NextID

    def getSecondNextID(self):
        return self.SecondNextID

    def getBranch(self):
        return self.branch

    def getCoordinates(self):
        return self.xCo, self.yCo

    def getType(self):
        return "JunctionLeft"

    def drawTrack(self, x, y, compass, screen, nextTrack, secondNextTrack):
        global xCo
        global yCo
        setCoordinates(self, x, y)
        coXNext, coxNextY = nextTrack.drawTrack(x, y, compass, screen)
        compassNext = nextTrack.adjustCompass(compass)
        coXSecNext, coYSecNext = secondNextTrack.drawTrack(
            x, y, compass, screen)
        compassSecNext = secondNextTrack.adjustCompass(compass)
        return (nextTrack.getID(), coXNext, coxNextY, compassNext, True), (secondNextTrack.getID(), coXSecNext, coYSecNext, compassSecNext, False)
        # global xCo
        # global yCo
        # trackColour = (255, 128, 0)
        # straightLength = 150
        # # Obtained using radius * cosine(angle) and radius * sine(angle) to give the approximate positon of each 45 degree angle
        # trueCoordinate = 106.0660172
        # # Obained using pythagoras to get the x and y shifts for each piece of diagonal track
        # trueDiagonal = 106.066017178
        # # List of if statements that are instructions for how to draw the track depending on what direction the compass is facing
        # # Lots of trial and error required to get this part to work properly
        # if compass == "N":
        #     # Draw a straight line and a curve at the same coordinates.
        #     pygame.draw.arc(screen, trackColour, [
        #                     x-300, y-150, 300, 300], 2*math.pi, math.pi/4, 5)
        #     pygame.draw.line(screen, trackColour, (x, y),
        #                      (x, y-straightLength), 5)
        #     setCoordinates(self, x, y)
        #     # Create two sets of coordinates and return them both.
        #     # x1 and y1 hold the coordinates of the straight, x2 and y2 hold the coordinates of the curve.
        #     x1 = x - (150 - trueCoordinate)
        #     y1 = y - trueCoordinate
        #     x2 = x
        #     y2 = y - straightLength
        #     return x2, y2, x1, y1
        # elif compass == "NE":
        #     pygame.draw.arc(screen, trackColour, [
        #                     x-(150 + trueCoordinate), y-(150 + trueCoordinate), 300, 300], 7*math.pi/4, 2*math.pi, 5)
        #     pygame.draw.line(screen, trackColour, (x, y),
        #                      (x+trueDiagonal, y-trueDiagonal), 5)
        #     setCoordinates(self, x, y)
        #     x1 = x + (150 - trueCoordinate)
        #     y1 = y - trueCoordinate
        #     x2 = x + trueDiagonal
        #     y2 = y - trueDiagonal
        #     return x2, y2, x1, y1
        # elif compass == "E":
        #     pygame.draw.arc(screen, trackColour, [
        #                     x-150, y-300, 300, 300], 3*math.pi/2, 7*math.pi/4, 5)
        #     pygame.draw.line(screen, trackColour, (x, y),
        #                      (x+straightLength, y), 5)
        #     setCoordinates(self, x, y)
        #     x1 = x + trueCoordinate
        #     y1 = y - (150 - trueCoordinate)
        #     x2 = x + straightLength
        #     y2 = y
        #     return x2, y2, x1, y1
        # elif compass == "SE":
        #     pygame.draw.arc(screen, trackColour, [x - (150 - trueCoordinate), y-(
        #         150 + trueCoordinate), 300, 300], 5*math.pi/4, 3*math.pi/2, 5)
        #     pygame.draw.line(screen, trackColour, (x, y),
        #                      (x+trueDiagonal, y+trueDiagonal), 5)
        #     setCoordinates(self, x, y)
        #     x1 = x + trueCoordinate
        #     y1 = y + (150 - trueCoordinate)
        #     x2 = x + trueDiagonal
        #     y2 = y + trueDiagonal
        #     return x2, y2, x1, y1
        # elif compass == "S":
        #     pygame.draw.arc(screen, trackColour, [
        #                     x, y-150, 300, 300], math.pi, 5*math.pi/4, 5)
        #     pygame.draw.line(screen, trackColour, (x, y),
        #                      (x, y+straightLength), 5)
        #     setCoordinates(self, x, y)
        #     x1 = x + (150 - trueCoordinate)
        #     y1 = y + trueCoordinate
        #     x2 = x
        #     y2 = y + straightLength
        #     return x2, y2, x1, y1
        # elif compass == "SW":
        #     pygame.draw.arc(screen, trackColour, [
        #                     x-(150 - trueCoordinate), y-(150 - trueCoordinate), 300, 300], 3*math.pi/4, math.pi, 5)
        #     pygame.draw.line(screen, trackColour, (x, y),
        #                      (x-trueDiagonal, y+trueDiagonal), 5)
        #     setCoordinates(self, x, y)
        #     x1 = x - (150 - trueCoordinate)
        #     y1 = y + trueCoordinate
        #     x2 = x - trueDiagonal
        #     y2 = y + trueDiagonal
        #     return x2, y2, x1, y1
        # elif compass == "W":
        #     pygame.draw.arc(screen, trackColour, [
        #                     x-150, y, 300, 300], math.pi/2, 3*math.pi/4, 5)
        #     pygame.draw.line(screen, trackColour, (x, y),
        #                      (x-straightLength, y), 5)
        #     setCoordinates(self, x, y)
        #     x1 = x - trueCoordinate
        #     y1 = y + (150 - trueCoordinate)
        #     x2 = x - straightLength
        #     y2 = y
        #     return x2, y2, x1, y1
        # elif compass == "NW":
        #     pygame.draw.arc(screen, trackColour, [
        #                     x - (150 + trueCoordinate), y - (150-trueCoordinate), 300, 300], math.pi/4, math.pi/2, 5)
        #     pygame.draw.line(screen, trackColour, (x, y),
        #                      (x-trueDiagonal, y-trueDiagonal), 5)
        #     setCoordinates(self, x, y)
        #     x1 = x - trueCoordinate
        #     y1 = y - (150 - trueCoordinate)
        #     x2 = x - trueDiagonal
        #     y2 = y - trueDiagonal
        #     return x2, y2, x1, y1
