
from Agents.Intentions import Intentions, Intention
from Enviroment.Affordances import *
from Enviroment.Objects import *
from Agents.Processes import Processes, Process
from Agents.Scenarios import Scenarios, Scenario
from Enviroment.Global import Global
from Enviroment.Map import Map, Point, Waypoint
from BaseConfig import BaseConfig

class Lobby(BaseConfig):
    def __init__(self):
        BaseConfig.__init__(self)
        
       
    def prepareMap(self, map):
        map.points = [ Point(0,0), Point(100,0), Point(100,30), Point(60,30), Point(60,70), Point(100,70), Point(100,100), Point(0,100) ]
        map.wayPoints = [ Waypoint(59,29), Waypoint(59,31), Waypoint(10,10), Waypoint(10,90), Waypoint(80,15), Waypoint(80,85) ]
        map.width = 100
        map.height = 100
        map.SetAgentStart(20, 50)
        
        
        map.AddObject(Door, 100, 15)
        map.AddObject(Painting, 100, 20)
        map.AddObject(Flower, 98, 6)
        
        map.AddObject(Door, 100, 85)
        map.AddObject(Painting, 100, 76)
        map.AddObject(Chair, 95, 96)
        
        map.AddObject(Door, 0, 45)
        map.AddObject(Door, 0, 55)
        map.AddObject(Painting, 0, 50)
        
        map.AddObject(Table, 55, 60)
        map.AddObject(Chair, 53, 62)
        map.AddObject(Chair, 55, 64)
        map.AddObject(Chair, 58, 58)
        map.AddObject(Chair, 58, 62)
        map.AddObject(Armchair, 55, 38)
        map.AddObject(Armchair, 55, 42)
        
        map.AddObject(Flower, 5, 80)
        map.AddObject(Armchair, 10, 90)
        map.AddObject(Painting, 5, 100)
        
        map.AddObject(Sandwich, 54, 59)
        map.AddObject(Apple, 53, 58)
        map.AddObject(Apple, 54, 57)
        map.AddObject(Orange, 53, 56)
        map.AddObject(Orange, 54, 55)
        map.AddObject(CocaColaCan, 53, 54)
        
        map.AddObject(Journal, 50, 10)
        map.AddObject(Journal, 52, 9)
        map.AddObject(Newspapers, 45, 6)
        map.AddObject(Newspapers, 48, 15)
        map.AddObject(Glasses, 49, 2)
        
        
        