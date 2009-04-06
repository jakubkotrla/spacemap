
from Agents.Intentions import Intentions, Intention
from Enviroment.Affordances import *
from Enviroment.Objects import *
from Agents.Processes import Processes, Process
from Enviroment.Global import Global
from Enviroment.Map import Map, Point, Waypoint
from BaseConfig import BaseConfig

class HeapLineRoom(BaseConfig):
    def __init__(self):
        BaseConfig.__init__(self)
     
    def prepareProcessIntentions(self):
        self.intentions.AddHighLevelIntention("Smoke")
        self.intentions.AddHighLevelIntention("Read")
        self.intentions.AddHighLevelIntention("Wash")
        self.intentions.AddHighLevelIntention("Heat")
        self.intentions.AddHighLevelIntention("Watch")
        self.intentions.AddHighLevelIntention("Play")
        self.intentions.AddHighLevelIntention("Sit")
        self.intentions.AddHighLevelIntention("Repair")
        self.intentions.AddHighLevelIntention("Nail")   
       
    def prepareMap(self, map):
        map.points = [ Point(0,0), Point(100,0), Point(100,100), Point(0, 100) ]
        map.wayPoints = [ Waypoint(50,50), Waypoint(15,15), Waypoint(85,15), Waypoint(15,85), Waypoint(85,85) ]
        map.width = 100
        map.height = 100
        map.SetAgentStart(50, 50)
        
        map.AddObject(Chair, 10, 10)
        map.AddObject(Chair, 10, 12)
        
        map.AddObject(Wood, 60, 70)
        
        map.AddObject(Hammer, 90, 5)
        map.AddObject(Nail, 90, 10, amount=20)
        map.AddObject(Hammer, 90, 15)
        map.AddObject(Screwdriver, 92, 14)
        map.AddObject(Screwdriver, 86, 8)
        map.AddObject(Nail, 88, 12, amount=10)
        map.AddObject(Torch, 96, 2)
        map.AddObject(Pipe, 98, 6)

        map.AddObject(Plate, 50, 30)
        map.AddObject(Cup, 52, 35)
        map.AddObject(Fork, 45, 32)
        map.AddObject(Cover, 52, 30)
        
        map.AddObject(Flower, 22, 71) 
        map.AddObject(Painting, 17, 82)
        map.AddObject(Flower, 22, 81)
        map.AddObject(Book, 18, 79)
        map.AddObject(Photoalbum, 20, 83)
        
        map.AddObject(Newspapers, 25, 81)
        map.AddObject(Painting, 29, 79)
        map.AddObject(Journal, 28, 81)
        map.AddObject(Book, 26, 79)
        
        map.AddObject(Sofa, 35, 81)
        map.AddObject(Armchair, 33, 82)
        map.AddObject(Cards, 37, 83)
        map.AddObject(Chair, 33, 80)
                
        map.AddObject(Chair, 42, 80)
        map.AddObject(Chess, 44, 82)
        map.AddObject(Cards, 39, 80)
        map.AddObject(GameBoy, 41, 83)
        map.AddObject(Knife, 47, 91)
        map.AddObject(Fork, 48, 93)
        
        
        
