
from Agents.Intentions import Intentions, Intention
from Enviroment.Affordances import *
from Enviroment.Objects import *
from Agents.Processes import Processes, Process
from Agents.Scenarios import Scenarios, Scenario
from Enviroment.Global import Global
from Enviroment.Map import Map, Point, Waypoint
from BaseConfig import BaseConfig

class CrazyRoom(BaseConfig):
    def __init__(self):
        BaseConfig.__init__(self)
     
    def prepareProcessIntentions(self):
        P_Eat = Process("Eating", [], [Eatability], [Eatability], [], 1800)
        self.processes.AddProcess(P_Eat)
        I_Eat = Intention("Eat", [P_Eat])
        self.intentions.AddIntention(I_Eat)
        self.intentions.AddHighLevelIntention(I_Eat)
        
        P_Drink = Process("Drinking", [], [Drinkability], [Drinkability], [], 60)
        self.processes.AddProcess(P_Drink)
        I_Drink = Intention("Drink", [P_Drink])
        self.intentions.AddIntention(I_Drink)
        self.intentions.AddHighLevelIntention(I_Drink)
        
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
        
        P_Watch = Process("Watching", [], [Watchability], [], [], 4000)
        self.processes.AddProcess(P_Watch)
        I_Watch = Intention("Watch", [P_Watch])
        self.intentions.AddIntention(I_Watch)
        self.intentions.AddHighLevelIntention(I_Watch)
        
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
        
       
    def prepareMap(self, map):
        map.points = [ Point(0,0), Point(30,0), Point(30,20), Point(50,10), Point(70,20), Point(100,0), Point(70,80), Point(100,80), Point(100,100), Point(0,100), Point(0,80), Point(40,50), Point(20,40), Point(0,40)]
        map.wayPoints = [ Waypoint(29,22), Waypoint(70,22), Waypoint(68,82), Waypoint(41,50), Waypoint(10,90) ]
        map.width = 100
        map.height = 100
        map.SetAgentStart(50, 50)
        
        map.AddObject(Painting, 5, 20)
         
        map.AddObject(Flower, 51, 14)
        map.AddObject(Apple, 48, 21)
        map.AddObject(Pipe, 46, 20)
         
        map.AddObject(Sofa, 80, 20)
        map.AddObject(Table, 88, 12)
        map.AddObject(Armchair, 93, 6)
        
        map.AddObject(Newspapers, 10, 92)
        map.AddObject(Journal, 5, 98)
        map.AddObject(Glasses, 14, 88)
        map.AddObject(Book, 15, 93)
        map.AddObject(BottleOfWine, 20, 79)
        map.AddObject(Television, 17, 95)
        
        map.AddObject(Pot, 81, 95)
        map.AddObject(Orange, 87, 91)
        map.AddObject(Knife, 93, 84)
        map.AddObject(Cover, 95, 92)
        
        map.AddObject(CocaColaCan, 51, 92, amount=10)
        map.AddObject(Photoalbum, 57, 97)
        
        map.AddObject(Plate, 60, 68)
        map.AddObject(Sink, 62, 50)
        map.AddObject(Cup, 40, 30)
        map.AddObject(Fork, 44, 32)
        map.AddObject(Screwdriver, 60, 42)
   
     
  
        
        