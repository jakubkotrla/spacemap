
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
        
       
    def prepareMap(self, map):
        map.points = [ Point(0,0), Point(100,0), Point(100,100), Point(0, 100) ]
        map.wayPoints = [ Waypoint(50,50), Waypoint(10,10), Waypoint(90,10), Waypoint(10,90), Waypoint(90,90) ]
        map.width = 100
        map.height = 100
        map.SetAgentStart(50, 50)
        
        map.AddObject(Nail, 20, 25, amount=10)
        map.AddObject(Hammer, 20, 30)
        map.AddObject(Pipe, 94, 40)
        map.AddObject(Box, 40, 60)
