import sys
import os
from statistics import mean

import pygame
import ctypes
import random
import subprocess
import shlex
import time

from Button import Button

from TrackPieces.Junction import Junction
from TrackPieces.LongLeft import LongLeft
from TrackPieces.LongRight import LongRight
from TrackPieces.LongStraight import LongStraight
from TrackPieces.ShortLeft import ShortLeft
from TrackPieces.ShortRight import ShortRight
from TrackPieces.ShortStraight import ShortStraight
from TrackPieces.Station import Station
from Trains.carriage import Carriage
from Trains.train import Train
import trainMover
from train_pddl import TrainPDDLProblem

# displays track selection menu
def showTrackSelection(selectedTrack):
    trackOptions = []

    ## variables for track options
    # keeps each track option button separated from each other
    runningY = 0
    changeInY = screenHeight * 0.09

    # where the first track option button will be placed
    xPosition = screenWidth * 0.12
    yPosition = screenHeight * 0.02

    #draw_button(screen, menuColour, 130, 115, 550, 480)

    #draw_button(screen, (150, 150, 150), 130, 115, 10, 480)
    #draw_button(screen, (100, 100, 100), 130, scrollBarY, 10, 57)

    # show all the tracks for selection
    # if there are more than 7 track files,
    if len(trackFiles) > 7:
        for f in range(startScroll, startScroll + 7):
            trackOptions.append(
            Button((xPosition, yPosition + runningY), trackButtonSize,
                   trackFiles[f][0:len(trackFiles[f]) - 4], buttonFont, buttonColour, textColour)
            )

            runningY += changeInY
    else:
        for f in trackFiles:
            trackOptions.append(
            Button((xPosition, yPosition + runningY), trackButtonSize,
                   f[0:len(f) - 4], buttonFont, buttonColour, textColour)
            )

            runningY += changeInY

    for trackButton in trackOptions:
        trackButton.render(screen)

    # give track option buttons functionality and get the selected track if one is clicked
    selectedTrack = _handleTrackSelection(trackOptions, selectedTrack)

    # if track selected show selected track image
    if selectedTrack:
        tempString = selectedTrack[0:len(selectedTrack) - 4]

        if os.path.isfile("Images/" + tempString + ".png"):
            trackImage = pygame.image.load("Images/" + tempString + ".png")
        else:
            trackImage = pygame.image.load("Images/placeholder.png")
        screen.blit(trackImage, (screenWidth * 0.28, screenHeight * 0.1))
    else:
        pass

    # draw select button
    trackSelect = Button((screenWidth * 0.30, screenHeight * 0.47), buttonSize,
                         "Select", buttonFont, buttonColour, textColour)
    trackSelect.render(screen)

    if selectedTrack:
        _handleSelectButtonInTrack(trackSelect, selectedTrack)

    return selectedTrack

def _handleTrackSelection(trackOptions, selectedTrack):
    for trackOptionButton in trackOptions:
        if trackOptionButton.clicked(events):
            selectedTrack = trackOptionButton.getText() + ".txt"
            return selectedTrack

    return selectedTrack

# generate track when track select button is clicked
def _handleSelectButtonInTrack(selectButton, selectedTrack):
    global generateTrack

    if not selectButton.clicked(events):
        return

    _resetTrackInfo()

    trackDictionary = _openTrack(selectedTrack)
    _loadTrack(trackDictionary)


    generateTrack = True

def _openTrack(trackName):
    """
    Loads track information from a specified file and populates relevant dictionaries.

    This function clears the existing data in `track` and `tracksDict`
    and then reads the track data from the specified file located in the `ExampleTracks`
    directory. Each line in the file is expected to be a semicolon-separated list of
    track attributes. The function parses each line, constructs a dictionary with the
    parsed data, and appends this dictionary to `trackDictionary`.

    Args:
        trackName (str): The name of the track file to be opened and loaded.

    Raises:
        FileNotFoundError: If the specified track file does not exist.
        IOError: If there is an error reading the file.

    Note:
        - The function assumes the global variables, `track`,
          and `tracksDict` are defined elsewhere in the code.
        - The file's format is assumed to have semicolon-separated values in the
          following order: TrackType, TrackID, PreviousID, NextID, Branch.
    """

    track.clear()

    trackDictionary = []

    with open(directory+"/ExampleTracks/"+trackName, "r") as file:
        for x in file:
            temp = x.split(";")

            tempDictionary = {
                "TrackType": temp[0],
                "TrackID": temp[1],
                "PreviousID": temp[2],
                "NextID": temp[3],
                "Branch": temp[4]
            }

            trackDictionary.append(tempDictionary)

    return trackDictionary

def _loadTrack(trackDictionary):
    for T in trackDictionary:
        if 'LongRight' in T['TrackType']:
            track.append(
                LongRight(screen, T['TrackID'], T['PreviousID'], T['NextID'], T['Branch']))

        elif 'LongStraight' in T['TrackType']:
            track.append(LongStraight(
                screen, T['TrackID'], T['PreviousID'], T['NextID'], T['Branch']))

        elif 'ShortStraight' in T['TrackType']:
            track.append(ShortStraight(
                screen, T['TrackID'], T['PreviousID'], T['NextID'], T['Branch']))

        elif 'Station' in T['TrackType']:
            track.append(
                Station(screen, T['TrackID'], T['PreviousID'], T['NextID'], T['Branch']))

        elif 'LongLeft' in T['TrackType']:
            track.append(
                LongLeft(screen, T['TrackID'], T['PreviousID'], T['NextID'], T['Branch']))

        elif 'ShortRight' in T['TrackType']:
            track.append(ShortRight(
                screen, T['TrackID'], T['PreviousID'], T['NextID'], T['Branch']))

        elif 'ShortLeft' in T['TrackType']:
            track.append(
                ShortLeft(screen, T['TrackID'], T['PreviousID'], T['NextID'], T['Branch']))

        elif 'Junction' in T['TrackType']:
            temp = T['NextID'].split(",")
            track.append(Junction(
                screen, T['TrackID'], T['PreviousID'], temp[0], temp[1], T['Branch']))

    # Generating a new track will clear the trains, so this will ensure all tracks are set to unoccupied.
    for x in track:
        x.setOccupied(False)

def _resetTrackInfo():
    global viewDisplacementX, viewDisplacementY, spawning, spawnIteration, trainsRunning, spawnStation, startingTracks
    global occupiedSpawns, stationList, spawnTimer, waiting, playerTrainExists, playerTrainMoving

    # set the above global variables back to their default
    spawning = False
    spawnIteration = 0
    trainsRunning = False
    spawnStation = None
    startingTracks = (None, None)
    occupiedSpawns = []
    stationList = []
    spawnTimer = 0
    waiting = False
    playerTrainExists = False
    playerTrainMoving = False
    viewDisplacementX = viewDisplacementY = 0

    # clear the train-specific lists
    spawnColour.clear()
    trainList.clear()
    tracksDict.clear()
    trainCompassDict.clear()
    swapTrainCompass.clear()
    angle.clear()
    circleCenter.clear()
    junctionDirection.clear()
    stationStop.clear()
    timer.clear()
    switch.clear()
    carriageStop.clear()
    instructions.clear()
    currentInstruction.clear()
    instructionCounter.clear()

def showTrainTrack():
    # the X point at which the first track is drawn
    startPointX = screenWidth / 2 + viewDisplacementX

    # the Y point at which the first track is drawn
    startPointY = screenHeight / 2 + viewDisplacementY

    # The compass is used to tell the program what rotation the next track should be placed in.
    compass = "E"
    savePoints = []

    currentCoX, currentCoY = startPointX, startPointY

    # This iterates through all the tracks in the current branch.
    for c in track:
        toDraw = True

        for s in savePoints:
            if c.getID() == s[0]:
                if not s[-1]:
                    currentCoX = s[1]
                    currentCoY = s[2]
                    compass = s[3]

                toDraw = False

        if not toDraw:
            continue

        # If the next track is a junction,
        # it will create a "save point" containing the coordinates and compass direction.
        if c.getType() == "Junction":
            nextTrackId = c.getNextID()
            secondNextTrackID = c.getSecondNextID()

            next, secondNext = c.drawTrack(
                currentCoX, currentCoY, compass, screen,
                _getTrack(nextTrackId), _getTrack(secondNextTrackID), trackColour=trackColour)

            currentCoX, currentCoY = next[1], next[2]
            compass = next[3]

            savePoints.append(next)
            savePoints.append(secondNext)

        # If it isn't a junction then change the coordinates and compass as normal.
        else:
            # The drawTrack function is what actually draws the track pies on the screen.
            # It returns the new coordinates to draw the next track.
            currentCoX, currentCoY = c.drawTrack(
                currentCoX, currentCoY, compass, screen, trackColour=trackColour)

            compass = c.adjustCompass(compass)

        # These if statements move the track if it gets too close to the edge of the screen.
        # FIXME: Code below displaces the track pieces that are too close to the edge away from the rest of the track
        #   Either:
        #   - Change to move the track as a whole instead of individual pieces
        #   - Remove since it will conflict with the feature to move the view around
        # if currentCoX > screenWidth - 50:
        #     startPointX = startPointX - (currentCoX - screenWidth + 50)
        #     currentCoX = screenWidth-50
        # if currentCoY > screenHeight-50:
        #     startPointY = startPointY - \
        #         (currentCoY - screenHeight + 50)
        #     currentCoY = screenHeight - 50
        # if currentCoY < 120:
        #     startPointY = startPointY + (120 - currentCoY)
        #     currentCoY = 120

def _getTrack(trackID):
    for t in track:
        if t.getID() == trackID:
            return t
    print("Track with the given id not found!")

def showStationSelectMenu(spawnStation):
    runningX = 0
    stations = []

    for t in track:
        if t.getType() == "Station":
            stations.append((Button((screenWidth * 0.10 + runningX, screenHeight * 0.02), buttonSize,
                                   "Station " + t.getID(), buttonFont, buttonColour, textColour), t.getID()))

            runningX += screenWidth * 0.09

    for station in stations:
        station[0].render(screen)

    # onStationHover(stations)

    spawnStation = _handleStationSelect(stations, spawnStation)

    return spawnStation


def _handleStationSelect(stations, spawnStation):
    """
    This method is used to check what station the user has clicked on and when.
    """
    global spawning

    global tempStartPoint
    global spawningCompass
    global startingTracks

    for station in stations:
        # skip to the next station if the current station button hasn't been clicked
        if not station[0].clicked(events):
            continue

        # if no spawnStation has been set and the station isn't occupied, set it, get coordinates for spawning train,
        # and enable train spawning.
        if not spawnStation:
            # find the spawning station from the track list.
            for t in track:
                if t.getID() == station[1]:
                    if t.isOccupied():
                        return spawnStation

                    # add the station to the list of occupied stations.
                    occupiedSpawns.append(t.getID())

                    # temporary variables used for spawning the train.
                    tempStartPoint = (t.getCoordinates()[0], t.getCoordinates()[1])
                    spawningCompass = t.getCompass()

                    # for the PDDL section
                    startingTracks = (t, startingTracks[1])
                    spawnStation = t

                    # gets the id for the next track.
                    # if the next track is a junction and the train needs to turn, it would derail.
                    # this data is overwritten before the train starts to move so it will not be a problem.
                    for t2 in track:
                        if t2.getID() == t.getNextID():
                            startingTracks = (startingTracks[0], t2)
                            break

                    spawning = True
                    break

            break

        # go through the track list and adds the station the user clicked on to the path.
        if not spawning:
            for t in track:
                if t.getID() == station[1] and t not in stationList and t != spawnStation:
                    stationList.append(t)
                    break

        break

    return spawnStation

# def onStationHover(stations):
#     for x in stations:
#         # This is used to draw a line from the station button to the actual station when the mouse hovers over it.
#         if x[0].hovered():
#             for t in track:
#                 if t.getID() == x[1]:
#                     pygame.draw.line(
#                         screen, (255, 102, 102), (x[0].getPosition, x[0].getPosition[1]), (t.getCoordinates()[0], t.getCoordinates()[1]), 2)

def showPlanningMenu(spawnStation):
    menuXPos = screenWidth * 0.10
    menuWidth = screenWidth * 0.13

    menuXCentre = menuXPos + menuWidth / 2

    # keep each selected station text displaced from each other
    runningY = screenHeight * 0.16
    changeInY = screenHeight * 0.025

    localButtonSize = (menuWidth - screenWidth * 0.01, screenHeight * 0.05)

    # draw the menu box
    pygame.draw.rect(screen, menuColour,
                     pygame.Rect((menuXPos, screenHeight * 0.11), (menuWidth, screenHeight * 0.8)))

    text = buttonFont.render("Station " + str(spawnStation.getID()), True, textColour)
    screen.blit(text, text.get_rect(center=(menuXCentre, runningY)))

    runningY += changeInY

    for s in stationList:
        text = buttonFont.render("v", True, textColour)
        screen.blit(text, text.get_rect(center=(menuXCentre, runningY)))

        runningY += changeInY

        text = buttonFont.render("Station " + str(s.getID()), True, textColour)
        screen.blit(text, text.get_rect(center=(menuXCentre, runningY)))

        runningY += changeInY

    removeButton = Button((menuXCentre - localButtonSize[0] / 2, screenHeight * 0.73), localButtonSize,
           "Remove Last Station", buttonFont, buttonColour, textColour)

    createButton = Button((menuXCentre - localButtonSize[0] / 2, screenHeight * 0.79), localButtonSize,
           "Create Plan", buttonFont, buttonColour, textColour)

    cancelButton = Button((menuXCentre - localButtonSize[0] / 2, screenHeight * 0.85), localButtonSize,
           "Cancel", buttonFont, buttonColour, textColour)

    _handleRemoveButtonInSidebar(removeButton)

    spawnStation = _handleCreateButtonInSidebar(createButton, spawnStation)

    spawnStation = _handleCancelButtonInSidebar(cancelButton, spawnStation)

    return spawnStation

def _handleRemoveButtonInSidebar(button):
    button.render(screen)

    if button.clicked(events):
        if stationList:
            stationList.pop()

def _handleCreateButtonInSidebar(button, spawnStation):
    button.render(screen)

    if button.clicked(events):
        _generatePddlPath(spawnStation)
        spawnStation = None

    return spawnStation

def _generatePddlPath(spawnStation):
    global trainPathSelectMenu

    startingTrack = startingTracks[0]

    # Initialize the variables that will be used to create the plan file.
    junctionList = []
    stations = []
    connected = []
    branches = []
    stationWBranches = []
    branches.append("1")
    stopPoints = []

    for t in track:
        # This is used to add the information about each stop to a dictionary.
        if t in stationList:
            stopPoints.append(t.getID())

        # This is used to add a new branch from the junctions.
        if t.getType() == "Junction":
            junctionList.append(t.getID())

            for g in track:
                if g.getID() == t.getSecondNextID():
                    connected.append(
                        (t.getBranch()[0:len(t.getBranch()) - 1], t.getID(), (str(int(g.getBranch())))))

                    branches.append((str(int(g.getBranch()))))

        # This creates a list of all stations and combines them with what branch they are on.
        if t.getType() == "Station":
            stations.append(t.getID())

            stationWBranches.append(
                (t.getID(), t.getBranch()[0:len(t.getBranch()) - 1]))

    # This appends the initial station to the stop list.
    stopPoints.append(startingTrack.getID())
    stationList.append(startingTrack)

    # This creates a new object that is an instance of the train_pddl.py file.
    problem = TrainPDDLProblem(junctionList, connected, stations, stationWBranches,
                               branches, stopPoints, startingTrack.getBranch()[0:len(startingTrack.getBranch()) - 1])

    # This generates the problem file using the information above.
    problem.generate_problem_pddl()

    # This converts a piece of text to something the command line can read.
    # This is used to generate a PDDL plan using a domain that I wrote and the previously generated problem file.
    command = shlex.split("python -B -m pddl_parser.planner '" +
                          directory + "/domain.pddl' '" + directory + "/problem.pddl'")
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable=sys.executable)

    plan = process.communicate()

    # # Decode byte strings and keep regular strings as they are
    plan = ''.join(
        [part.decode('utf-8').replace('\n', '\\n') if isinstance(part, bytes)
         else part.replace('\n', '\\n') for part in plan]
    )

    # The following lines of code are used to trim the output of the previous command into
    # a format that my system can read.
    plan = plan.split('\\n')
    plan.pop(0)
    plan.pop(0)
    plan.pop(len(plan) - 1)

    for p in range(0, len(plan)):
        plan[p] = plan[p].replace("track", "")
        plan[p] = plan[p].replace("tn ", "")

    tempPlan = []

    for p in plan:
        p = p.replace("station", "")
        p = p.replace("branch", "")
        p = p.replace("junction", "")
        tempPlan.append(p.split(" "))

    if tempPlan[0][1] != startingTrack.getID():
        temp = tempPlan[0]
        tempPlan[0] = tempPlan[len(tempPlan) - 1]
        tempPlan[len(tempPlan) - 1] = temp

    # This section will append a final instruction to switch at the next junction
    # when the initial station is not on the first branch.
    # This is required to send the train back to the appropriate starting station
    # after it has completed the list of instructions.
    # This is not required if the train starts on the first branch because
    # all branches eventually connect to the first.
    if startingTrack.getBranch() != 1:
        for t in track:
            if t.getType() == "Junction":
                if int(t.getBranch()) + 1 == int(startingTrack.getBranch()):
                    tempPlan.append(("switch", t.getID(), t.getBranch()[0:len(t.getBranch()) - 1],
                                     str(int(t.getBranch()) + 1)))

    # Three sets of instructions need to be appended to account for trains being sets of 3.
    # The other two sets of instructions will not be used.

    instructions.append(tempPlan)
    instructions.append(tempPlan)
    instructions.append(tempPlan)

    currentInstruction.append(instructions[len(instructions) - 1][0])
    currentInstruction.append(instructions[len(instructions) - 1][0])
    currentInstruction.append(instructions[len(instructions) - 1][0])

    instructionCounter.append(0)
    instructionCounter.append(0)
    instructionCounter.append(0)

    # Empties the list of stops and closes the spawning menu.
    stationList.clear()
    trainPathSelectMenu = False

def _handleCancelButtonInSidebar(button, spawnStation):
    global track, trainPathSelectMenu

    button.render(screen)

    if button.clicked(events):
        spawnStation.setOccupied(False)
        spawnStation = None
        trainPathSelectMenu = False
        stationList.clear()

        # reverse the actions of spawning a train
        for _ in range(3):
            trainList.pop()
            spawnColour.pop()
            tracksDict.pop()
            trainCompassDict.pop()
            angle.pop()
            swapTrainCompass.pop()
            circleCenter.pop()
            junctionDirection.pop()
            stationStop.pop()
            timer.pop()
            carriageStop.pop()
            switch.pop()

    return spawnStation

def showControls():
    menuPosX = screenWidth * 0.8
    # starting y position of an empty box that will change based on number of lines of text
    menuPosY = screenHeight * 0.83

    menuWidth = screenWidth * 0.18
    # height of an empty box that will change based on number of lines of text
    menuHeight = screenHeight * 0.05

    runningY = 0
    changeInY = screenHeight * 0.04

    text1 = buttonFont.render("W - Move Forward",True, textColour)
    text2 = buttonFont.render("Space - Turn Junctions",True, textColour)
    text3 = buttonFont.render("↑→↓← - Move track view",True, textColour)

    controlList = [text1, text2, text3]

    controlLength = len(controlList)

    # change menu y position and height based on number of lines of text
    menuPosY -= controlLength * changeInY
    menuHeight += controlLength * changeInY

    controlsRect = pygame.Rect((menuPosX, menuPosY), (menuWidth, menuHeight))
    pygame.draw.rect(screen, menuColour, controlsRect)

    for control in controlList:
        screen.blit(control, (menuPosX + screenWidth * 0.02, menuPosY + screenWidth * 0.02 + runningY))

        runningY += changeInY

def setupTrains():
    global spawnTimer, waiting, spawnIteration, trainsRunning, spawning, trainPathSelectMenu, playerTrainExists

    # if the system is waiting for space to be cleared for another carriage spawning, add to spawnTimer
    if waiting:
        for _ in range(trainSpeed):
            # This adds one to the timer that stops trains and carriages from spawning on top of each other.
            spawnTimer += 1

            # If the spawn timer is 190 (enough time for train to clear spawn point),
            # reset the timer and stop the train from moving.
            if spawnTimer == 190:
                waiting = False
                spawnTimer = 0
                break

    # ensures no trains or carriages appear while the timer is counting.
    if waiting:
        return

    # change the angle the trains spawn at based on what compass direction they are on.
    match spawningCompass:
        case "N":
            spawningAngle = 90
        case "NE":
            spawningAngle = 45
        case "E":
            spawningAngle = 0
        case "SE":
            spawningAngle = 315
        case "S":
            spawningAngle = 270
        case "SW":
            spawningAngle = 225
        case "W":
            spawningAngle = 180
        case "NW":
            spawningAngle = 135
        case _:
            spawningAngle = 0

    tracksDict.append((startingTracks[0], startingTracks[1]))
    trainCompassDict.append(spawningCompass)
    angle.append(spawningAngle)
    swapTrainCompass.append(False)
    circleCenter.append((0, 0))
    junctionDirection.append(0)
    stationStop.append(False)
    timer.append(0)
    waiting = True
    carriageStop.append(False)
    switch.append(False)

    if spawnIteration == 0:
        if playerSpawning:
            trainList.append(Train(screen, tempStartPoint[0], tempStartPoint[1], playerControlled=True))
        else:
            trainList.append(Train(screen, tempStartPoint[0], tempStartPoint[1]))

        trainColours = ["red", "blue", "yellow", "green", "purple"]
        trainColour = trainColours[random.randint(0, len(trainColours) - 1)]

        for _ in range(3):
            spawnColour.append(trainColour)

        spawnStation.setOccupied(True)
    else:
        if playerSpawning:
            trainList.append(Carriage(screen, tempStartPoint[0], tempStartPoint[1], playerControlled=True))
        else:
            trainList.append(Carriage(screen, tempStartPoint[0], tempStartPoint[1]))

    if spawnIteration == 2:
        trainsRunning = False
        spawning = False
        spawnIteration = 0

        if not playerSpawning:
            trainPathSelectMenu = True
        else:
            playerTrainExists = True
    else:
        trainsRunning = True
        spawnIteration += 1

def operateTrains():
    # This iterates through the list of trains and carries out instructions accordingly.
    for i in range(trainSpeed):
        for counter, train in enumerate(trainList):
            # stops non-spawning trains from running when trains are spawning
            if spawning:
                if counter < len(trainList) - spawnIteration:
                    continue
            elif not train.getPlayerControlled():
                _haltTrainWhenRequired(counter, train)

            # carry out the train's instructions if it is neither at a station nor behind occupied tracks.
            if not ((stationStop[counter] or carriageStop[counter]) or (train.getPlayerControlled() and not spawning)):
                _moveTrain(counter, train)

        if spawning and i == 190:
            break

def _haltTrainWhenRequired(counter, train):
    # If the current train is at a station then increase the stop timer.
    if stationStop[counter]:
        timer[counter] += 1

    # If the timer is at 1000 then perform the actions to start the train again.
    if timer[counter] >= 1000:
        # This loads the next instruction for the train.
        currentInstruction[counter] = instructions[counter][instructionCounter[counter]]

        # if the next instruction is to switch at a junction,
        # activate the switch variable for the train and the next two carriages.
        if "switch" in currentInstruction[counter][0]:
            switch[counter] = True
            switch[counter + 1] = True
            switch[counter + 2] = True

        # If the next instruction is to return then move into the next instruction.
        elif "return" in currentInstruction[counter][0]:
            instructionCounter[counter] += 1
            currentInstruction[counter] = instructions[counter][instructionCounter[counter]]

        # Reset the station stop variable for the train.
        stationStop[counter] = False

    # This is used to find out if the next track is occupied, if it is it will stop the train accordingly.
    # Only runs if there is more than one train running as otherwise there are no trains to stop for.
    tempT = tracksDict[counter][1]

    for t in track:
        if t.getID() == tracksDict[counter][1].getNextID():
            tempT = t

    if train.getType() == "Train":
        carriageStop[counter] = tempT.isOccupied()

    # copy the instructions of a train to the two following carriages.
    if train.getType() == "Train":
        carriageStop[counter + 1] = carriageStop[counter + 2] = carriageStop[counter]
        stationStop[counter + 1] = stationStop[counter + 2] = stationStop[counter]

def _moveTrain(counter, train):
    # These if statements adjust the angle of the current train based on what the current track piece is.
    currentTrackType = tracksDict[counter][0].getType()
    nextTrackType = tracksDict[counter][1].getType()

    if currentTrackType == "LongRight" or (currentTrackType  == "JunctionRight" and junctionDirection[counter] == 1):
        angle[counter] = angle[counter] - 0.1

    if currentTrackType == "ShortRight":
        angle[counter] = angle[counter] - 0.2

    if currentTrackType == "LongLeft" or (currentTrackType == "JunctionLeft" and junctionDirection[counter] == 1):
        angle[counter] = angle[counter] + 0.1

    if currentTrackType == "ShortLeft":
        angle[counter] = angle[counter] + 0.2

    # This if statement is triggered when a train has reached the end of the current track.
    # The numbers don't line up exactly, so they are rounded to four decimal places.
    trainPosX = float("{:.4f}".format(train.getCurrentPosition()[0]))
    trainPosY = float("{:.4f}".format(train.getCurrentPosition()[1]))

    nextTrackX = float("{:.4f}".format(tracksDict[counter][1].getCoordinates()[0]))
    nextTrackY = float("{:.4f}".format(tracksDict[counter][1].getCoordinates()[1]))

    # if the train part has reached the start of the next track
    if (trainPosX == nextTrackX and trainPosY == nextTrackY) or (
            (trainPosX < nextTrackX and trainPosX + 0.3 > nextTrackX) and trainPosY == nextTrackY):

        # This if statement checks if a train is stopped and at a station, then loads in the next instruction for it.
        if (currentTrackType == "Station" and timer[counter] < 1000 and train.getType() == "Train"):
            if not train.getPlayerControlled():
                if ("stop" in currentInstruction[counter][0]
                        and tracksDict[counter][0].getID() == currentInstruction[counter][1]):
                    stationStop[counter] = True
                    instructionCounter[counter] += 1

                    if instructionCounter[counter] == len(instructions[counter]):
                        instructionCounter[counter] = 0

        else:
            # If the train isn't at a station then the timer should always be 0.
            timer[counter] = 0

        # This stops the train if the next track is occupied.
        if tracksDict[counter][1].isOccupied() and train.getType() == "Train":
            carriageStop[counter] = True

        # If the current track is not any kind of straight and the next track is,
        # it needs to adjust the current trains compass once.
        # This is to fix a problem in that the compass wasn't being set properly
        # when a train transitions from a curve to a straight.
        if ((currentTrackType not in ["LongStraight", "ShortStraight", "Station"])
                and(nextTrackType in ["LongStraight", "ShortStraight", "Station"])):

            trainCompassDict[counter] = tracksDict[counter][0].adjustCompass(trainCompassDict[counter])

        # If the next track is a junction and the train has been instructed to switch branch,
        # then it enables the variable that is actually used to change the junction.
        # It also adjusts the compass to match the track piece on the end of the curve.
        # Finally, it loads in the next instruction.
        if nextTrackType == "Junction" and switch[counter]:
            for t in track:
                if t.getID() == tracksDict[counter][1].getSecondNextID():
                    tracksDict[counter] = (tracksDict[counter][0], t)

                    currentTrackType = tracksDict[counter][0].getType()
                    nextTrackType = tracksDict[counter][1].getType()

                    break

            if train.getType() == "Train":
                if not train.getPlayerControlled():
                    if tracksDict[counter][1].getID() == currentInstruction[counter][1]:
                        _updateTrainToTurn(counter, train)

                        instructionCounter[counter] += 1

                        if instructionCounter[counter] == len(instructions[counter]):
                            instructionCounter[counter] = 0

                        currentInstruction[counter] = instructions[counter][instructionCounter[counter]]
                else:
                    _updateTrainToTurn(counter, train)




        # If the next track is a junction and the train doesn't have to turn, it resets the variable.
        elif nextTrackType == "Junction" and not switch[counter]:
            for t in track:
                if t.getID() == tracksDict[counter][1].getNextID():
                    tracksDict[counter] = (tracksDict[counter][0], t)

                    currentTrackType = tracksDict[counter][0].getType()
                    nextTrackType = tracksDict[counter][1].getType()

                    break

            if train.getType() == "Train":
                junctionDirection[counter] = junctionDirection[counter + 1] = junctionDirection[counter + 2] = 0

        # This loop will replace the current track with the next track and fetch the new next track.
        # It will also set and reset track occupation accordingly.
        for t in track:
            if int(t.getID()) == int(tracksDict[counter][1].getNextID()):
                tracksDict[counter][0].setOccupied(False)
                tracksDict[counter] = (tracksDict[counter][1], t)

                currentTrackType = tracksDict[counter][0].getType()
                nextTrackType = tracksDict[counter][1].getType()

                if train.getType() == "Train":
                    tracksDict[counter][0].setOccupied(True)

                break

            if train.getType() == "Train":
                if (tracksDict[counter][1].getNextID() == t.getNextID()) and (
                        tracksDict[counter][1].getID() != t.getID()):
                    t.setOccupied(True)
                else:
                    t.setOccupied(False)

                for c in track:
                    if c.getID() == tracksDict[counter][1].getNextID() and c.getBranch() != \
                            tracksDict[counter][1].getBranch():
                        c.setOccupied(True)

        # If the current track is a curve then it collects information for the vector it will use to
        # move the surrounding trains
        if (currentTrackType in ["LongRight", "LongLeft", "ShortRight", "ShortLeft"] or
                (junctionDirection[counter] == 1 and (currentTrackType in ["JunctionLeft", "JunctionRight"]))):

            circleCenter[counter], angle[counter], swapTrainCompass[counter] = trainMover.setValues(
                currentTrackType, tracksDict[counter][0], trainCompassDict[counter])

    # This moveTrain function will take in all of the information gathered until this point
    # and redraw the train at a new angle and coordinate.

    trainImageList[counter] = train.moveTrain(
        train.getCurrentPosition()[0], train.getCurrentPosition()[1], currentTrackType, screen,
        trainCompassDict[counter], trainImageList[counter], angle[counter], circleCenter[counter],
        junctionDirection[counter])

    # This adjusts the current trains compass.
    if swapTrainCompass[counter]:

        if ("Right" in nextTrackType or "Left" in nextTrackType) and "Junction" not in nextTrackType:
            trainCompassDict[counter] = tracksDict[counter][0].adjustCompass(
                trainCompassDict[counter])

        else:
            trainCompassDict[counter] = tracksDict[counter][1].adjustCompass(
                trainCompassDict[counter])

        swapTrainCompass[counter] = False

def _updateTrainToTurn(counter, train):
    for i in range(3):
        junctionDirection[counter + i] = 1

        r = tracksDict[counter + i][0].adjustCompass(trainCompassDict[counter + i])

        trainCompassDict[counter + i] = r

        # This doesn't happen for player-controlled trains because the player toggles switch manually
        if not train.getPlayerControlled():
            switch[counter + i] = False


# get the project directory
directory = os.getcwd()

# on Windows devices, stop desktop scaling settings from messing with anything
ctypes.windll.user32.SetProcessDPIAware()

# initialise game
pygame.init()

# parameters for the window and rendering of the game
displayInfo = pygame.display.Info()

screenWidth = displayInfo.current_w
screenHeight = displayInfo.current_h

# if the user has a different aspect ratio than the developed-for 16:9, change the window width or height to match
if screenHeight > screenWidth / (16/9):
    screenHeight = screenWidth / (16/9)

if screenWidth > screenHeight / (9/16):
    screenWidth = screenHeight / (9/16)

screen = pygame.display.set_mode((screenWidth, screenHeight), vsync=True)

# initialise fonts
buttonFont = pygame.font.Font('calibri.ttf', int(screenWidth*0.013))
# headingFont = pygame.font.Font('calibri.ttf', 30)
# titleFont = pygame.font.Font('calibri.ttf', 52)

# initialise colours
trackColour = (169, 169, 169)
buttonColour = (60,60,60)
menuColour = (50,50,50)
textColour = (240,240,240)

# button sizes
buttonSize = (screenWidth*0.08, screenHeight*0.08)
trackButtonSize = (screenWidth*0.13, screenHeight*0.08)

# initialise buttons
# main buttons
spawnButton = Button((screenWidth * 0.01, screenHeight * 0.02), buttonSize,
                     "Spawn Train", buttonFont, buttonColour, textColour)
simButton = Button((screenWidth * 0.01, screenHeight * 0.11), buttonSize,
                   "Start Sim", buttonFont, buttonColour, textColour)
trackButton = Button((screenWidth * 0.01, screenHeight * 0.20), buttonSize,
                     "Track", buttonFont, buttonColour, textColour)
statusButton = Button((screenWidth * 0.01, screenHeight * 0.29), buttonSize,
                      "Train Status", buttonFont, buttonColour, textColour)
playerButton = Button((screenWidth * 0.01, screenHeight * 0.38), buttonSize,
                      "Player Train", buttonFont, buttonColour, textColour)
controlsButton = Button((screenWidth * 0.9, screenHeight * 0.9), buttonSize,
                        "Controls", buttonFont, buttonColour, textColour)

mainButtons = [spawnButton, simButton, trackButton, statusButton, playerButton, controlsButton]

## flags to control what to display

spawnSelection = False
trainPathSelectMenu = False
trackSelection = False
controlMenu = False
# used to tell the system when to display the track.
generateTrack = False

## train spawning variables

# used to tell the system when a train is spawning.
spawning = False
# the type of train to be spawned. 0 = train, 1 and 2 = carriages.
spawnIteration = 0
# the station that the user is spawning a train at
spawnStation = None
# defines the starting and next track on train spawning. Overwritten on spawn.
startingTracks = (None, None)
# holds a list of stations that already have a train spawned at them.
occupiedSpawns = []
# holds a list of stations to stop at.
stationList = []
# defines the start point for train spawning.
tempStartPoint = (0,0)
# stores the compass direction to spawn the trains at. This is defined by the station you choose.
spawningCompass = "E"
# used for spawning the carriages of a train.
# It ensures the carriages are spawned one after the other and not on top of each other.
spawnTimer = 0
# stops the spawning code from running while the spawnTimer isn't complete.
waiting = False
# tells the system when the user is spawning their train so that it's different from spawning AI trains
playerSpawning = False
# When this is true, player will be able to control the train they spawned
playerTrainExists = False
# When this is true, the player's train will move
playerTrainMoving = False

## track and train rendering and operating variables

# tells the system when trains can move
trainsRunning = False
# Dictates the speed of the trains. An even number keeps the speed consistent when changing speed
trainSpeed = 8
# Stores the number of pixels the view will be displaced by
viewDisplacementX = 0
viewDisplacementY = 0
# the track file that has been selected
selectedTrack = None
# stores the whole track where each item is a track piece
track = []

# TODO: Turn the train-specific lists below into variables for train and carriage objects

## train-specific variables, where each element in these lists belongs to a specific train
# holds the colours that the trains will spawn in. Also for remembering train colours after spawn
spawnColour = []
# holds a list of active trains.
trainList = []
# holds the current track and the next track for each train.
tracksDict = []
# holds the current compass for each train.
trainCompassDict = []
# holds a boolean value for each train that defines whether or not to change its compass.
swapTrainCompass = []
# This holds the angle each train is currently facing. This is used for train rotation around a curve.
angle = []
# Train movement around a curve uses a vector, which gives coordinates around a circle.
# This holds the centre point of the circle.
circleCenter = []
# This is used to tell trains which direction to turn at a junction.
junctionDirection = []
# This tells a train to stop at a station.
stationStop = []
# This timer states how long a train has been stopped at a station for.
timer = []
# Tells a train that it needs to turn at the next junction.
switch = []
# This is used to stop carriages at stations.
carriageStop = []
# Holds the list of PDDL instructions for each train.
instructions = []
# Holds the current instruction each train is working on.
currentInstruction = []
# Holds the index of the instruction each train is working on.
instructionCounter = []

## other variables to be used throughout the program

# where the track selection scroll is
startScroll = 0
scrollBarY = screenHeight * 0.02

# list of track file names
trackFiles = []

# load "ExampleTracks" file names to trackFiles
for file in os.listdir("ExampleTracks"):
    trackFiles.append(file)

# variables for testing or evaluation purposes:
devTesting = False
oneTrainRunningFPS = []
twoTrainRunningFPS = []
threeTrainRunningFPS = []
fourTrainRunningFPS = []
fiveTrainRunningFPS = []
sixTrainRunningFPS = []

# keeps track of time
clock = pygame.time.Clock()

# keep the game running until false
mainLoop = True

while mainLoop:
    screen.fill((21, 30, 41))

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            mainLoop = False

        if event.type == pygame.KEYDOWN:
            keyPressed = event.key

            viewPosIncrement = screenHeight * 0.1

            # controls for the player's train
            if playerTrainExists:
                match keyPressed:
                    # starts or stops player train
                    case pygame.K_w:
                        playerTrainMoving = not playerTrainMoving

                    # enables junction switches for player train
                    case pygame.K_SPACE:
                        for i in range(3):
                            switch[i] = not switch[i]
            if not spawning:
                match keyPressed:
                    # double the train's speed
                    case pygame.K_EQUALS:
                        trainSpeed = trainSpeed * 2

                    # half the train's speed
                    case pygame.K_MINUS:
                        trainSpeed = round(trainSpeed / 2)

                        if trainSpeed < 1:
                            trainSpeed = 1

                    # TODO: Refactor left, right, down, and up cases into less repetitive code
                    # move the track and trains right
                    case pygame.K_LEFT:
                        viewDisplacementX += viewPosIncrement

                        for i, train in enumerate(trainList):
                            train.displaceTrain(viewPosIncrement, 0)

                            circleCenter[i] = (circleCenter[i][0] + viewPosIncrement, circleCenter[i][1])

                    # move the track and trains left
                    case pygame.K_RIGHT:
                        viewDisplacementX -= viewPosIncrement

                        for i, train in enumerate(trainList):
                            train.displaceTrain(-viewPosIncrement, 0)

                            circleCenter[i] = (circleCenter[i][0] - viewPosIncrement, circleCenter[i][1])

                    # move the track and trains up
                    case pygame.K_DOWN:
                        viewDisplacementY -= viewPosIncrement

                        for i, train in enumerate(trainList):
                            train.displaceTrain(0, -viewPosIncrement)

                            circleCenter[i] = (circleCenter[i][0], circleCenter[i][1] - viewPosIncrement)

                    # move the track and trains down
                    case pygame.K_UP:
                        viewDisplacementY += viewPosIncrement

                        for i, train in enumerate(trainList):
                            train.displaceTrain(0, viewPosIncrement)

                            circleCenter[i] = (circleCenter[i][0], circleCenter[i][1] + viewPosIncrement)





    if spawnButton.clicked(events):
        if not (trainPathSelectMenu or spawning):
            spawnSelection = not spawnSelection
            trackSelection = False

    if simButton.clicked(events):
        if not (trainPathSelectMenu or spawning) and len(trainList) > 0:
            trainsRunning = not trainsRunning

            # if sim started after clicking, rename button text to "Stop Sim"
            # otherwise, revert button text back to "Start Sim"
            if trainsRunning:
                simButton.setText("Stop Sim")
            else:
                simButton.setText("Start Sim")

    if trackButton.clicked(events):
        if not (trainPathSelectMenu or spawning):
            spawnSelection = False
            trackSelection = not trackSelection

    if playerButton.clicked(events):
        if not (trainPathSelectMenu or spawning):
            playerSpawning = not playerSpawning

    if controlsButton.clicked(events):
        controlMenu = not controlMenu

    # if a track has been chosen, generate it
    if generateTrack:
        showTrainTrack()

    if spawning:
        setupTrains()

    # This holds the list of generated trains.
    trainImageList = []

    for i, train in enumerate(trainList):
        # loads in the images for each train.
        trainImageList.append(train.generateTrain(spawnColour[i]))

        # draw each train on the screen
        train.spawnTrain(
            train.getCurrentPosition()[0], train.getCurrentPosition()[1], screen, trainImageList[i],angle[i])
    
    # The following is everything that occurs when the simulation is running or trains are spawning
    if trainsRunning:
        operateTrains()

    for button in mainButtons:
        button.render(screen)

    if spawnSelection:
        if not trainsRunning or spawning:
            spawnStation = showStationSelectMenu(spawnStation)

    if trainPathSelectMenu:
        spawnStation = showPlanningMenu(spawnStation)

    if trackSelection:
        # show track selection menu but also keep track of the track that was selected
        selectedTrack = showTrackSelection(selectedTrack)

    if controlMenu:
        showControls()

    if playerTrainMoving:
        for j in range(trainSpeed):
            for i in range(3):
                _moveTrain(i, trainList[i])

    if playerSpawning:
        text = buttonFont.render("Experimental: Player spawning enabled. Once spawned, other trains cannot be spawned yet.", True, textColour)
        screen.blit(text, (screenWidth * 0.01, 0))

    pygame.display.update()

    # Keep the game locked to 60 frames per second
    clock.tick(60)

    # For testing. Calculates average FPS depending on number of trains.
    # devTesting variable must be enabled
    if trainsRunning and not spawning and devTesting:
        match len(trainList):
            case 3:
                oneTrainRunningFPS.append(clock.get_fps())
            case 6:
                twoTrainRunningFPS.append(clock.get_fps())
            case 9:
                threeTrainRunningFPS.append(clock.get_fps())
            case 12:
                fourTrainRunningFPS.append(clock.get_fps())
            case 15:
                fiveTrainRunningFPS.append(clock.get_fps())
            case 18:
                sixTrainRunningFPS.append(clock.get_fps())

# For testing. Prints average FPS depending on number of trains
if oneTrainRunningFPS:
    print("Average FPS 1 train: " + str(mean(oneTrainRunningFPS)))

if twoTrainRunningFPS:
    print("Average FPS 2 trains: " + str(mean(twoTrainRunningFPS)))

if threeTrainRunningFPS:
    print("Average FPS 3 trains: " + str(mean(threeTrainRunningFPS)))

if fourTrainRunningFPS:
    print("Average FPS 4 trains: " + str(mean(fourTrainRunningFPS)))

if fiveTrainRunningFPS:
    print("Average FPS 5 trains: " + str(mean(fiveTrainRunningFPS)))

if sixTrainRunningFPS:
    print("Average FPS 6 trains: " + str(mean(sixTrainRunningFPS)))

# Close the game
pygame.quit()
sys.exit()
