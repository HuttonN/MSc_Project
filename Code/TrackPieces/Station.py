# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 15:06:21 2023

@author: Admin
"""
import pygame
import math


def setCompass(self, compass):
    global thisCompass
    self.thisCompass = compass


def setNextID(self, x):
    global NextID
    self.NextID = x


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


class Station(pygame.sprite.Sprite):

    global ID
    global PrevID
    global NextID
    global xCo
    global yCo
    global branch
    global occupied
    global thisCompass

    def __init__(self, screen, currentID, previousID, nextID, branch):
        super(Station, self).__init__()
        setID(self, currentID)
        setPrevID(self, previousID)
        setNextID(self, nextID)
        setBranch(self, branch)
    # This function does not need to do anything as straight track does not change the direction the track is facing

    def adjustCompass(self, compass):
        return compass

    def setOccupied(self, x):
        global occupied
        self.occupied = x

    def isOccupied(self):
        return self.occupied

    def getID(self):
        return self.ID

    def getCompass(self):
        return self.thisCompass

    def getPrevID(self):
        return self.PrevID

    def getNextID(self):
        return self.NextID

    def getCoordinates(self):
        return self.xCo, self.yCo

    def getBranch(self):
        return self.branch

    def getType(self):
        return "Station"

    def drawTrack(self, x, y, compass, screen,        trackColour=(255, 128, 0)
                  ):
        # This uses the same code for drawing a straight line on screen. The only difference is that it draws a green shape next to the track to represent the station.
        setCompass(self, compass)
        global xCo
        global yCo
        straightLength = 150
        # trackColour = (255, 128, 0)
        # stationColour = (128, 255, 0)
        stationColour = (255, 204, 0)
        # Pythagoras used to find length of x and y coordinates for diagonal straights
        # trueDiagonal = 70.71067812
        trueDiagonal = 106.066017178
        if compass == "N":
            pygame.draw.line(screen, trackColour, (x, y),
                             (x, y-straightLength), 5)
            pygame.draw.line(screen, stationColour,
                             (x-20, y-25), (x-20, y-125), 25)
            setCoordinates(self, x, y)
            x = x
            y = y - straightLength
            return x, y
        elif compass == "NE":
            pygame.draw.line(screen, trackColour, (x, y),
                             (x+trueDiagonal, y-trueDiagonal), 5)
            pygame.draw.line(screen, stationColour,
                             (x-20, y-5), (x+75, y-100), 25)
            setCoordinates(self, x, y)
            x = x + trueDiagonal
            y = y - trueDiagonal
            return x, y
        elif compass == "E":
            pygame.draw.line(screen, trackColour, (x, y),
                             (x+straightLength, y), 5)
            pygame.draw.line(screen, stationColour,
                             (x+20, y+25), (x+120, y+25), 25)
            setCoordinates(self, x, y)
            x = x + straightLength
            y = y
            return x, y
        elif compass == "SE":
            pygame.draw.line(screen, trackColour, (x, y),
                             (x+trueDiagonal, y+trueDiagonal), 5)
            pygame.draw.line(screen, stationColour,
                             (x+20, y-5), (x+125, y+100), 25)
            setCoordinates(self, x, y)
            x = x + trueDiagonal
            y = y + trueDiagonal
            return x, y
        elif compass == "S":
            pygame.draw.line(screen, trackColour, (x, y),
                             (x, y+straightLength), 5)
            pygame.draw.line(screen, stationColour,
                             (x-20, y+25), (x-20, y+125), 25)
            setCoordinates(self, x, y)
            x = x
            y = y + straightLength
            return x, y
        elif compass == "SW":
            pygame.draw.line(screen, trackColour, (x, y),
                             (x-trueDiagonal, y+trueDiagonal), 5)
            pygame.draw.line(screen, stationColour,
                             (x-20, y-5), (x-125, y+100), 25)
            setCoordinates(self, x, y)
            x = x - trueDiagonal
            y = y + trueDiagonal
            return x, y
        elif compass == "W":
            pygame.draw.line(screen, trackColour, (x, y),
                             (x-straightLength, y), 5)
            pygame.draw.line(screen, stationColour,
                             (x-20, y-25), (x-120, y-25), 25)
            setCoordinates(self, x, y)
            x = x - straightLength
            y = y
            return x, y
        elif compass == "NW":
            pygame.draw.line(screen, trackColour, (x, y),
                             (x-trueDiagonal, y-trueDiagonal), 5)
            pygame.draw.line(screen, stationColour,
                             (x-30, y-5), (x-125, y-100), 25)
            setCoordinates(self, x, y)
            x = x - trueDiagonal
            y = y - trueDiagonal
            return x, y
