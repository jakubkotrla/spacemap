
from Agents.Intentions import Intentions, Intention
from Enviroment.Affordances import *
from Enviroment.Objects import *
from Agents.Processes import Processes, Process
from Enviroment.Global import Global
from Enviroment.Map import Map, Point, Waypoint
from BaseConfig import BaseConfig

class SmallRoom(BaseConfig):
    def __init__(self):
        BaseConfig.__init__(self)
    
    def prepareProcessIntentions(self):
        self.intentions.AddHighLevelIntention("Smoke")
        self.intentions.AddHighLevelIntention("Watch")
        self.intentions.AddHighLevelIntention("Play")
        self.intentions.AddHighLevelIntention("Sit")

    def prepareMap(self, map):
        map.points = [ Point(10,10), Point(70,10), Point(70,80), Point(30,80), Point(30,30), Point(10,30) ]
        map.wayPoints = [ Waypoint(20,20), Waypoint(33,27), Waypoint(60,20), Waypoint(50,70) ]
        map.width = 70
        map.height = 80
        map.SetAgentStart(50, 50)
        
        map.AddObject(Door, 70, 20)
        
        map.AddObject(Sink, 20, 20)
        map.AddObject(Plate, 15, 22)
        map.AddObject(Fork, 17, 21)
        map.AddObject(Knife, 22, 19)
        map.AddObject(Cup, 23, 20)
        
        map.AddObject(Flower, 32, 32)
        map.AddObject(Flower, 68, 78)
        
        map.AddObject(Chair, 35, 78)
        map.AddObject(Cards, 32, 72)
        
        map.AddObject(Table, 65, 50)
        map.AddObject(Chair, 66, 51)
        map.AddObject(Chess, 60, 55)
        map.AddObject(Apple, 63, 51)
        