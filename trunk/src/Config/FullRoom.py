
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
     
    def prepareProcessIntentions(self):
        P_Smoke = Process("Smoking", [], [Smokeability], [], [], 300)
        self.processes.AddProcess(P_Smoke)
        I_Smoke = Intention("Smoke", [P_Smoke])
        self.intentions.AddIntention(I_Smoke)
        self.intentions.AddHighLevelIntention(I_Smoke)
        
        P_Read = Process("Reading", [], [Zoomability, Readability], [], [], 4000)
        self.processes.AddProcess(P_Read)
        I_Read = Intention("Read", [P_Read])
        self.intentions.AddIntention(I_Read)
        self.intentions.AddHighLevelIntention(I_Read)
        
        #P_Wash = Process("Washing", [], [Washability, Wetability], [Wetability], [], 600)
        P_Wash = Process("Washing", [], [Washability], [Wetability], [], 600)
        self.processes.AddProcess(P_Wash)
        I_Wash = Intention("Wash", [P_Wash])
        self.intentions.AddIntention(I_Wash)
        self.intentions.AddHighLevelIntention(I_Wash)
        
        #P_Heat = Process("Heating", [], [Fireability, Lightability], [Fireability], [], 1200)
        P_Heat = Process("Heating", [], [Fireability], [Fireability], [], 1200)
        self.processes.AddProcess(P_Heat)
        I_Heat = Intention("Heat", [P_Heat])
        self.intentions.AddIntention(I_Heat)
        self.intentions.AddHighLevelIntention(I_Heat)
        
        P_Watch = Process("Watching", [], [Watchability], [], [], 4000)
        self.processes.AddProcess(P_Watch)
        I_Watch = Intention("Watch", [P_Watch])
        self.intentions.AddIntention(I_Watch)
        self.intentions.AddHighLevelIntention(I_Watch)
        
        P_Play = Process("Playing", [], [Playability], [], [], 900)
        self.processes.AddProcess(P_Play)
        I_Play = Intention("Play", [P_Play])
        self.intentions.AddIntention(I_Play)
        self.intentions.AddHighLevelIntention(I_Play)
        
        P_Sit = Process("Sitting", [], [Sitability], [], [], 1200)
        self.processes.AddProcess(P_Sit)
        I_Sit = Intention("Sit", [P_Sit])
        self.intentions.AddIntention(I_Sit)
        self.intentions.AddHighLevelIntention(I_Sit)

        #P_Repair = Process("Repairing", [], [Repairability, Screwability], [], [], 600)
        P_Repair = Process("Repairing", [], [Repairability], [], [], 600)
        self.processes.AddProcess(P_Repair)
        I_Repair = Intention("Repair", [P_Repair])
        self.intentions.AddIntention(I_Repair)
        self.intentions.AddHighLevelIntention(I_Repair)
        
        #P_Nail = Process("Nailing", [], [Hammerability, Nailability], [], [], 120)
        P_Nail = Process("Nailing", [], [Nailability], [Nailability], [], 120)
        self.processes.AddProcess(P_Nail)
        I_Nail = Intention("Nail", [P_Nail])
        self.intentions.AddIntention(I_Nail)
        self.intentions.AddHighLevelIntention(I_Nail)   
       
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
        map.AddObject(Chess, 20, 62)
        map.AddObject(Cards, 19, 59)
        
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
        
        
