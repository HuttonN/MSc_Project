# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 15:15:18 2023

@author: Admin
"""


import pygame
import math

# Set the ID of the next track.


def setNextID(self, x):
    global NextID
    self.NextID = x
# Set the ID of the previous track.


def setPrevID(self, x):
    global PrevID
    self.PrevID = x
# Set the ID of the current track.


def setID(self, x):
    global ID
    self.ID = x
# Set the coordinates of the end of this track.


def setCoordinates(self, x, y):
    global xCo
    global yCo
    self.xCo = x
    self.yCo = y
# Set the branch that this track is on.


def setBranch(self, x):
    global branch
    self.branch = x


class LongLeft(pygame.sprite.Sprite):

    global ID
    global PrevID
    global NextID
    global xCo
    global yCo
    global branch
    global occupied

    # Initialise the track piece.
    def __init__(self, screen, currentID, previousID, nextID, branch):
        super(LongLeft, self).__init__()
        setID(self, currentID)
        setPrevID(self, previousID)
        setNextID(self, nextID)
        setBranch(self, branch)

    # Set whether the track is occupied.
    def setOccupied(self, x):
        global occupied
        self.occupied = x

    # Adjust the compass to match the direction of the end of the track piece.
    def adjustCompass(self, compass):
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

    def getID(self):
        return self.ID

    def isOccupied(self):
        return self.occupied

    def getPrevID(self):
        return self.PrevID

    def getNextID(self):
        return self.NextID

    def getCoordinates(self):
        return self.xCo, self.yCo

    def getBranch(self):
        return self.branch

    def getType(self):
        return "LongLeft"

    # Draws the track on the screen and sets the end coordinates accordingly.
    def drawTrack(self, x, y, compass, screen, trackColour=(255, 128, 0)):
        global xCo
        global yCo
        # trackColour = (255, 128, 0)
        # Obtained using radius * cosine(angle) and radius * sine(angle) to give the approximate positon of each 45 degree angle
        trueCoordinate = 106.0660172
        # Obained using pythagoras to get the x and y shifts for each piece of diagonal track
        trueDiagonal = 1.767766953
        # List of if statements that are instructions for how to draw the track depending on what direction the compass is facing
        # Lots of trial and error required to get this part to work properly
        if compass == "N":
            # This draws the arc on the screen inside a 300x300 sized square between the angles 2*pi and pi/4 with a width of 5.
            pygame.draw.arc(screen, trackColour, [
                            x-300, y-150, 300, 300], 2*math.pi, math.pi/4, 5)
            # Sets the coordinates of the track piece.
            setCoordinates(self, x, y)
            # Moves the x and y values to the end of the track piece, which become the coordinates it is drawn at.
            x = x - (150 - trueCoordinate)
            y = y - trueCoordinate
            return x, y
        elif compass == "NE":
            pygame.draw.arc(screen, trackColour, [
                            x-(150 + trueCoordinate), y-(150 + trueCoordinate), 300, 300], 7*math.pi/4, 2*math.pi, 5)
            setCoordinates(self, x, y)
            x = x + (150 - trueCoordinate)
            y = y - trueCoordinate
            return x, y
        elif compass == "E":
            pygame.draw.arc(screen, trackColour, [
                            x-150, y-300, 300, 300], 3*math.pi/2, 7*math.pi/4, 5)
            setCoordinates(self, x, y)
            x = x + trueCoordinate
            y = y - (150 - trueCoordinate)
            return x, y
        elif compass == "SE":
            pygame.draw.arc(screen, trackColour, [x - (150 - trueCoordinate), y-(
                150 + trueCoordinate), 300, 300], 5*math.pi/4, 3*math.pi/2, 5)
            setCoordinates(self, x, y)
            x = x + trueCoordinate
            y = y + (150 - trueCoordinate)
            return x, y
        elif compass == "S":
            pygame.draw.arc(screen, trackColour, [
                            x, y-150, 300, 300], math.pi, 5*math.pi/4, 5)
            setCoordinates(self, x, y)
            x = x + (150 - trueCoordinate)
            y = y + trueCoordinate
            return x, y
        elif compass == "SW":
            pygame.draw.arc(screen, trackColour, [
                            x-(150 - trueCoordinate), y-(150 - trueCoordinate), 300, 300], 3*math.pi/4, math.pi, 5)
            setCoordinates(self, x, y)
            x = x - (150 - trueCoordinate)
            y = y + trueCoordinate
            return x, y
        elif compass == "W":
            pygame.draw.arc(screen, trackColour, [
                            x-150, y, 300, 300], math.pi/2, 3*math.pi/4, 5)
            setCoordinates(self, x, y)
            x = x - trueCoordinate
            y = y + (150 - trueCoordinate)
            return x, y
        elif compass == "NW":
            pygame.draw.arc(screen, trackColour, [
                            x - (150 + trueCoordinate), y - (150-trueCoordinate), 300, 300], math.pi/4, math.pi/2, 5)
            setCoordinates(self, x, y)
            x = x - trueCoordinate
            y = y - (150 - trueCoordinate)
            return x, y
