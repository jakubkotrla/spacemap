
from Agents.Intentions import Intentions, Intention
from Enviroment.Affordances import *
from Enviroment.Objects import *
from Agents.Processes import Processes, Process
from Enviroment.Global import Global
from Enviroment.Map import Map, Point, Waypoint
from BaseConfig import BaseConfig
from Enviroment.World import WorldEvent

class SwitchRoom(BaseConfig):
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
        
        map.AddObject(Sofa, 20, 60)
        map.AddObject(Armchair, 18, 62)
        map.AddObject(Chess, 20, 62)
        map.AddObject(Cards, 19, 59)
        
        map.AddObject(Hammer, 90, 5)
        map.AddObject(Nail, 90, 10)
        self.r1 = map.AddObject(Hammer, 90, 15)
        self.r2 = map.AddObject(Screwdriver, 92, 14)
        map.AddObject(Screwdriver, 86, 8)
        self.r3 = map.AddObject(Nail, 88, 12)
        map.AddObject(Torch, 96, 2)
        map.AddObject(Pipe, 98, 6)

        self.o1 = map.AddObject(Plate, 50, 40)
        self.o2 = map.AddObject(Cup, 52, 45)
        self.o3 = map.AddObject(Fork, 45, 42)
        self.o4 = map.AddObject(Knife, 48, 50)
        self.o5 = map.AddObject(Pot, 55, 45)
        self.o6 = map.AddObject(Cover, 52, 40)
        
        self.d1 = map.AddObject(Book, 50, 90)
        self.d2 = map.AddObject(Journal, 48, 96)
        self.d3 = map.AddObject(Book, 54, 92)
        self.d4 = map.AddObject(Journal, 52, 98)
        self.d5 = map.AddObject(Painting, 46, 95)
        self.d6 = map.AddObject(Photoalbum, 55, 98)
        self.d7 = map.AddObject(Newspapers, 48, 90)
        self.d8 = map.AddObject(Painting, 42, 92)
        self.d9 = map.AddObject(Newspapers, 44, 96)
        map.AddObject(Painting, 47, 98)
        map.AddObject(Book, 53, 91)
        self.d10 = map.AddObject(Book, 51, 97)
        
    def GetWorldsEvents(self):
        events = []
        events.append( WorldEvent(1500, self.r1, "remove") )
        events.append( WorldEvent(1500, self.r2, "remove") )
        events.append( WorldEvent(1500, self.r3, "remove") )
        events.append( WorldEvent(1500, self.o1, "remove") )
        events.append( WorldEvent(1500, self.o2, "remove") )
        events.append( WorldEvent(1500, self.o3, "remove") )
        events.append( WorldEvent(1500, self.o4, "remove") )
        events.append( WorldEvent(1500, self.o5, "remove") )
        events.append( WorldEvent(1500, self.d1, "remove") )
        events.append( WorldEvent(1500, self.d2, "remove") )
        events.append( WorldEvent(1500, self.d3, "remove") )
        events.append( WorldEvent(1500, self.d4, "remove") )
        events.append( WorldEvent(1500, self.d5, "remove") )
        events.append( WorldEvent(1500, self.d6, "remove") )
        events.append( WorldEvent(1500, self.d7, "remove") )
        events.append( WorldEvent(1500, self.d8, "remove") )
        events.append( WorldEvent(1500, self.d9, "remove") )
        events.append( WorldEvent(1500, self.d10, "remove") )
        events.append( WorldEvent(4000, self.d1, "add") )
        events.append( WorldEvent(4000, self.d2, "add") )
        events.append( WorldEvent(4000, self.d3, "add") )
        events.append( WorldEvent(4000, self.d4, "add") )
        events.append( WorldEvent(4000, self.d5, "add") )
        events.append( WorldEvent(4000, self.o6, "remove") )
        map = Global.Map
        oo = map.CreateObject(Fork, 85, 80)
        events.append( WorldEvent(4000, oo, "add") )
        oo = map.CreateObject(Plate, 90, 81)
        events.append( WorldEvent(4000, oo, "add") )
        oo = map.CreateObject(Knife, 80, 82)
        events.append( WorldEvent(4000, oo, "add") )
        oo = map.CreateObject(Cup, 95, 85)
        events.append( WorldEvent(4000, oo, "add") )
        oo = map.CreateObject(Cover, 88, 83)
        events.append( WorldEvent(4000, oo, "add") )
        oo = map.CreateObject(Pot, 92, 84)
        events.append( WorldEvent(4000, oo, "add") )
        return events
    
    
    
        
