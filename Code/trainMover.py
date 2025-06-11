# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 21:23:09 2024

@author: Admin
"""

#This class only exists to move the very repetitive code for navigating the trains around curves out of the main file to keep it less cluttered.
#All this does is set some values that are required, such as the centre of the curved track circle and the angle.
def setValues(trackType, curr, compass):
    if trackType == "LongRight" or trackType == "JunctionRight":
        if compass == "E":
            return (curr.getCoordinates()[0],curr.getCoordinates()[1]+150),180,True
        elif compass == "SE":
            return (curr.getCoordinates()[0]-106.0660172,curr.getCoordinates()[1]+106.0660172),135,True
        elif compass == "S":
            return (curr.getCoordinates()[0]-150,curr.getCoordinates()[1]),90,True
        elif compass == "SW":
            return (curr.getCoordinates()[0]-106.0660172,curr.getCoordinates()[1]-106.0660172),45,True
        elif compass == "W":
            return (curr.getCoordinates()[0],curr.getCoordinates()[1]-150),0,True
        elif compass == "NW":
            return (curr.getCoordinates()[0]+106.0660172,curr.getCoordinates()[1]-106.0660172),315,True
        elif compass == "N":
            return (curr.getCoordinates()[0]+150,curr.getCoordinates()[1]),270,True
        elif compass == "NE":
            return (curr.getCoordinates()[0]+106.0660172,curr.getCoordinates()[1]+106.0660172),225,True
    if trackType == "LongLeft" or trackType == "JunctionLeft":
        if compass == "N":
            return (curr.getCoordinates()[0]-150,curr.getCoordinates()[1]),90,True
        if compass == "NW":
            return (curr.getCoordinates()[0]-106.0660172,curr.getCoordinates()[1]+106.0660172),135,True
        if compass == "W":
            return (curr.getCoordinates()[0],curr.getCoordinates()[1]+150),180,True
        if compass == "SW":
            return (curr.getCoordinates()[0]+106.0660172,curr.getCoordinates()[1]+106.0660172),225,True
        if compass == "S":
            return (curr.getCoordinates()[0]+150,curr.getCoordinates()[1]),270,True
        if compass == "SE":
            return (curr.getCoordinates()[0]+106.0660172,curr.getCoordinates()[1]-106.0660172),315,True
        if compass == "E":
            return (curr.getCoordinates()[0],curr.getCoordinates()[1]-150),0,True
        if compass == "NE":
            return (curr.getCoordinates()[0]-106.0660172,curr.getCoordinates()[1]-106.0660172),45,True
    if trackType == "ShortRight":
        if compass == "E":
            return (curr.getCoordinates()[0],curr.getCoordinates()[1]+75),180,True
        elif compass == "SE":
            return (curr.getCoordinates()[0]-53.03300859,curr.getCoordinates()[1]+53.03300859),135,True
        elif compass == "S":
            return (curr.getCoordinates()[0]-75,curr.getCoordinates()[1]),90,True
        elif compass == "SW":
            return (curr.getCoordinates()[0]-53.03300859,curr.getCoordinates()[1]-53.03300859),45,True
        elif compass == "W":
            return (curr.getCoordinates()[0],curr.getCoordinates()[1]-75),0,True
        elif compass == "NW":
            return (curr.getCoordinates()[0]+53.03300859,curr.getCoordinates()[1]-53.03300859),315,True
        elif compass == "N":
            return (curr.getCoordinates()[0]+75,curr.getCoordinates()[1]),270,True
        elif compass == "NE":
            return (curr.getCoordinates()[0]+53.03300859,curr.getCoordinates()[1]+53.03300859),225,True
    if trackType == "ShortLeft":
        if compass == "N":
            return (curr.getCoordinates()[0]-75,curr.getCoordinates()[1]),90,True
        if compass == "NW":
            return (curr.getCoordinates()[0]-53.03300859,curr.getCoordinates()[1]+53.03300859),135,True
        if compass == "W":
            return (curr.getCoordinates()[0],curr.getCoordinates()[1]+75),180,True
        if compass == "SW":
            return (curr.getCoordinates()[0]+53.03300859,curr.getCoordinates()[1]+53.03300859),225,True
        if compass == "S":
            return (curr.getCoordinates()[0]+75,curr.getCoordinates()[1]),270,True
        if compass == "SE":
            return (curr.getCoordinates()[0]+53.03300859,curr.getCoordinates()[1]-53.03300859),315,True
        if compass == "E":
            return (curr.getCoordinates()[0],curr.getCoordinates()[1]-75),0,True
        if compass == "NE":
            return (curr.getCoordinates()[0]-53.03300859,curr.getCoordinates()[1]-53.03300859),45,True