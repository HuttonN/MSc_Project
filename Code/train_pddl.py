from py2pddl import Domain, create_type
from py2pddl import predicate, action, goal, init

# This entire domain class is useless and none of this code is ever executed.
# This is because I have written the domain file myself, as it isn't dynamic and doesn't need to change.
# As such, the trainsim.py file will only call the problem class.
# However, this entire file won't compile at runtime unless this is here.
# Ignore this class.


class TrainPDDLDomain(Domain):

    Train = create_type("Train")
    Branch = create_type("Branch")
    Junction = create_type("Junction")
    Station = create_type("Station")

    @predicate()
    def isAt(self, tn, tk):
        """Complete the method signature and specify
        the respective types in the decorator"""

    def isOn(self, tk):
        """Complete the method signature and specify
        the respective types in the decorator"""

    @predicate()
    def connected(self, tk1, tk2):
        """Complete the method signature and specify
        the respective types in the decorator"""

    @predicate()
    def visited(self, s, tn):
        """Complete the method signature and specify
        the respective types in the decorator"""

    @predicate()
    def isBranch(self, s, tn):
        """Complete the method signature and specify
        the respective types in the decorator"""

    @action()
    def moveTrain(self, tn, tk1, tk2):
        precond = [self.isAt(tn, tk1), self.connected(tk1, tk2)]
        effect = [self.isAt(tn, tk2)]
        return precond, effect

    @action(Junction, Station, Train)
    def stopAt(self, tn, s, tk):
        precond = [self.isAt(tn, s), self.connected(s, tk)]
        effect = [self.visited(s, tn), self.isAt(tn, tk)]
        return precond, effect

    @action(Junction, Station, Train)
    def endAt(self, tn, s, tk):
        precond = [self.isAt(tn, s), self.connected(s, tk)]
        effect = [self.visited(s, tn), self.isAt(tn, tk)]
        return precond, effect


class TrainPDDLProblem(TrainPDDLDomain):
    global junctionList
    global stationList
    global connections
    global stationBranches
    global branchList
    global stoppingList
    global firstBranch

    # This creates all of the objects that are in this problem.
    def __init__(self, junctions, connected, stations, stationsWBranches, branches, stopList, startingBranch):
        super().__init__()
        global junctionList
        global stationList
        global connections
        global stationBranches
        global branchList
        global stoppingList
        global firstBranch
        stoppingList = stopList
        junctionList = junctions
        stationList = stations
        connections = connected
        stationBranches = stationsWBranches
        branchList = branches
        firstBranch = startingBranch
        # This creates the first object, which is the train it is making a plan for.
        self.train = TrainPDDLDomain.Train.create_objs(["tn"])
        stationTemp = []
        for s in stationList:
            stationTemp.append("station" + str(s))
        if len(stationTemp) > 0:
            # This creates the station objects.
            self.station = TrainPDDLDomain.Station.create_objs(stationTemp)
        junctionTemp = []
        for j in junctionList:
            junctionTemp.append("junction" + str(j))
        if len(junctionTemp) > 0:
            # This creates the junction objects.
            self.junction = TrainPDDLDomain.Junction.create_objs(junctionTemp)
        branchTemp = []
        for b in branchList:
            branchTemp.append("branch" + str(b))
        if len(branchTemp) > 0:
            # This creates the branch objects.
            self.branch = TrainPDDLDomain.Branch.create_objs(branchTemp)

    # This creates the initial state of the problem using the objects created above and the variables that are passed in.
    @init
    def init(self):
        global junctions
        global stationList
        global connections
        global stationBranches
        global branchList
        global stoppingList
        global firstBranch
        at = []
        # This creates the initial state of the train at the first station the user selected.
        at.append(self.isAt(self.train["tn"],
                  self.branch["branch"+firstBranch]))
        for x in stationBranches:
            # This creates the states of the stations and the branch they are located on.
            at.append(self.isBranch(
                self.station["station" + x[0]], self.branch["branch"+x[1]]))
        for x in connections:
            # This creates the states of the junctions and the two branches they connect.
            at.append(self.connected(
                self.junction["junction" + x[1]], self.branch["branch"+x[0]], self.branch["branch"+x[2]]))

        return at

    # This generates the goal conditions.
    @goal
    def goal(self):
        global stoppingList
        returnList = []
        for s in stoppingList:
            # The only goal conditions are that the train has visited the stations requested by the user, which are found in stoppingList.
            returnList.append(self.visited(
                self.train["tn"], self.station["station" + str(s)]))
        return returnList
