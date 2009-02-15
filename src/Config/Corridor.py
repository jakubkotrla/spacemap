
from Agents.Intentions import Intentions, Intention
from Enviroment.Affordances import *
from Enviroment.Objects import *
from Agents.Processes import Processes, Process
from Agents.Scenarios import Scenarios, Scenario
from Enviroment.Global import Global
from Enviroment.Map import Map, Point, Waypoint
from BaseConfig import BaseConfig

class Corridor(BaseConfig):
    def __init__(self):
        BaseConfig.__init__(self)
        
       
    def prepareMap(self, map):
        map.points = [ Point(0,0), Point(20,0), Point(20,80), Point(100,80), Point(100, 100), Point(0, 100) ]
        map.wayPoints = [ Waypoint(10,20), Waypoint(10,90), Waypoint(80,90) ]
        map.width = 100
        map.height = 100
        map.SetAgentStart(10, 90)
        
        map.AddObject(Table, 18, 22)
        map.AddObject(Chair, 16, 22)
        map.AddObject(Painting, 20, 24)
        
        map.AddObject(Flower, 8, 60)
        
        map.AddObject(Newspapers, 39, 82)
        map.AddObject(Glasses, 42, 82)
        map.AddObject(Pipe, 40, 81)
        
        map.AddObject(Sofa, 70, 82)
        
        map.AddObject(Door, 100, 90)
        map.AddObject(Painting, 100, 95)
    
    