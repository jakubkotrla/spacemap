
from Agents.Intentions import Intentions, Intention
from Enviroment.Affordances import *
from Enviroment.Objects import *
from Agents.Processes import Processes, Process
from Agents.Scenarios import Scenarios, Scenario
from Enviroment.Global import Global
from Enviroment.Map import Map, Point, Waypoint
from BaseConfig import BaseConfig

class FullRoom(BaseConfig):
    def __init__(self):
        BaseConfig.__init__(self)
        
       
    def prepareMap(self, map):
        map.points = [ Point(0,0), Point(100,0), Point(100,100), Point(0, 100) ]
        map.wayPoints = [ Waypoint(50,50), Waypoint(10,10), Waypoint(90,10), Waypoint(10,90), Waypoint(90,90) ]
        map.width = 100
        map.height = 100
        map.SetAgentStart(50, 50)
        
        map.AddObject(Chair, 10, 10)
        map.AddObject(Chair, 10, 12)
        
        map.AddObject(Wood, 60, 70)
        
        map.AddObject(Sofa, 20, 60)
        map.AddObject(Armchair, 18, 62)
        
        map.AddObject(Hammer, 90, 5)
        map.AddObject(Nail, 90, 10, amount=20)
        map.AddObject(Hammer, 90, 15)
        map.AddObject(Screwdriver, 92, 14)
        map.AddObject(Screwdriver, 86, 8)
        map.AddObject(Nail, 88, 12, amount=10)
        map.AddObject(Torch, 96, 2)
        map.AddObject(Pipe, 98, 6)

        map.AddObject(Plate, 50, 40)
        map.AddObject(Cup, 52, 45)
        map.AddObject(Fork, 45, 42)
        map.AddObject(Knife, 48, 50)
        map.AddObject(Pot, 55, 45)
        map.AddObject(Cover, 52, 40)
        
        map.AddObject(Book, 50, 90)
        map.AddObject(Journal, 48, 96)
        map.AddObject(Book, 54, 92)
        map.AddObject(Journal, 52, 98)
        map.AddObject(Painting, 46, 95)
        map.AddObject(Photoalbum, 55, 98)
        map.AddObject(Newspapers, 48, 90)
        map.AddObject(Painting, 42, 92)
        map.AddObject(Newspapers, 44, 96)
        map.AddObject(Painting, 47, 98)
        map.AddObject(Book, 53, 91)
        map.AddObject(Book, 51, 97)
        
        
