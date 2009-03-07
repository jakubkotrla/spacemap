
from Agents.Intentions import Intentions, Intention
from Enviroment.Affordances import *
from Enviroment.Objects import *
from Agents.Processes import Processes, Process
from Agents.Scenarios import Scenarios, Scenario
from Enviroment.Global import Global
from Enviroment.Map import Map, Point, Waypoint
from BaseConfig import BaseConfig

class EmptyRoom(BaseConfig):
    def __init__(self):
        BaseConfig.__init__(self)
    
    def prepareProcessIntentions(self):
        self.intentions.AddHighLevelIntention("Smoke")
        self.intentions.AddHighLevelIntention("Watch")
        self.intentions.AddHighLevelIntention("Play")
        self.intentions.AddHighLevelIntention("Sit")

    def prepareMap(self, map):
        map.points = [ Point(0,0), Point(100,0), Point(100,100), Point(0, 100) ]
        map.wayPoints = [ Waypoint(50,50), Waypoint(15,15), Waypoint(85,15), Waypoint(15,85), Waypoint(85,85) ]
        map.width = 100
        map.height = 100
        map.SetAgentStart(50, 50)
        
        #map.AddObject(Nail, 20, 25, amount=10)
        #map.AddObject(Hammer, 20, 30)
        map.AddObject(Flower, 20, 25)
        map.AddObject(Chess, 20, 30)
        map.AddObject(Pipe, 94, 40)
        map.AddObject(Box, 40, 60)
