
from Agents.Intentions import Intentions, Intention
from Enviroment.Affordances import *
from Enviroment.Objects import *
from Agents.Processes import Processes, Process
from Enviroment.Global import Global
from Enviroment.Map import Map, Point, Waypoint
from BaseConfig import BaseConfig

class HeapRoom(BaseConfig):
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
        map.AddObject(Nail, 90, 10)
        map.AddObject(Hammer, 90, 15)
        map.AddObject(Screwdriver, 92, 14)
        map.AddObject(Screwdriver, 86, 8)
        map.AddObject(Nail, 88, 12)
        map.AddObject(Torch, 96, 2)
        map.AddObject(Pipe, 98, 6)

        map.AddObject(Plate, 50, 30)
        map.AddObject(Cup, 52, 35)
        map.AddObject(Fork, 45, 32)
        map.AddObject(Knife, 48, 40)
        map.AddObject(Pot, 55, 35)
        map.AddObject(Cover, 52, 30)
        
         
        map.AddObject(Sofa, 20, 70)
        map.AddObject(Armchair, 18, 72)
        map.AddObject(Cards, 20, 72)
        map.AddObject(Chair, 19, 69)
        
        map.AddObject(Painting, 20, 85)
        map.AddObject(Flower, 22, 85)
        map.AddObject(Book, 19, 86)
        map.AddObject(Photoalbum, 23, 84)
        
        map.AddObject(Newspapers, 38, 70)
        map.AddObject(Painting, 40, 69)
        map.AddObject(Journal, 41, 68)
        map.AddObject(Book, 37, 65)
        
        map.AddObject(Chair, 32, 80)
        map.AddObject(Chess, 36, 82)
        map.AddObject(Cards, 40, 80)
        map.AddObject(GameBoy, 35, 81)
        
        
        
