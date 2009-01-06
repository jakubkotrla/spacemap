
from Agents.Intentions import Intentions, Intention
from Enviroment.Affordances import *
from Enviroment.Objects import *
from Agents.Processes import Processes, Process
from Agents.Scenarios import Scenarios, Scenario
from Enviroment.Global import Global
from Enviroment.Map import Map, Point
from BaseConfig import BaseConfig

class EmptyRoom(BaseConfig):
    def __init__(self):
        BaseConfig.__init__(self)
        
    def prepareScenarios(self):
        P_Eat = Process("Eating", [], [Eatability], [Eatability], [], 86400, 1800)
        self.processes.AddProcess(P_Eat)
        I_Eat = Intention("Eat", [P_Eat])
        self.intentions.AddIntention(I_Eat)
        self.intentions.AddHighLevelIntention(I_Eat)
        
        P_Drink = Process("Drinking", [], [Drinkability], [Drinkability], [], 86400, 60)
        self.processes.AddProcess(P_Drink)
        I_Drink = Intention("Drink", [P_Drink])
        self.intentions.AddIntention(I_Drink)
        self.intentions.AddHighLevelIntention(I_Drink)
        
        P_Smoke = Process("Smoking", [], [Smokeability], [], [], 86400, 500)
        self.processes.AddProcess(P_Smoke)
        I_Smoke = Intention("Smoke", [P_Smoke])
        self.intentions.AddIntention(I_Smoke)
        self.intentions.AddHighLevelIntention(I_Smoke)
        
        P_Read = Process("Reading", [], [Zoomability, Readability], [], [], 86400, 4000)
        self.processes.AddProcess(P_Read)
        I_Read = Intention("Read", [P_Read])
        self.intentions.AddIntention(I_Read)
        self.intentions.AddHighLevelIntention(I_Read)
        
        P_Wash = Process("Washing", [], [Washability, Wetability], [Wetability], [], 86400, 600)
        self.processes.AddProcess(P_Wash)
        I_Wash = Intention("Wash", [P_Wash])
        self.intentions.AddIntention(I_Wash)
        self.intentions.AddHighLevelIntention(I_Wash)
        
        P_Heat = Process("Heating", [], [Fireability, Lightability], [Fireability], [], 86400, 1000)
        self.processes.AddProcess(P_Heat)
        I_Heat = Intention("Heat", [P_Heat])
        self.intentions.AddIntention(I_Heat)
        self.intentions.AddHighLevelIntention(I_Heat)
        
        P_Watch = Process("Watching", [], [Watchability], [], [], 86400, 1000)
        self.processes.AddProcess(P_Watch)
        I_Watch = Intention("Watch", [P_Watch])
        self.intentions.AddIntention(I_Watch)
        self.intentions.AddHighLevelIntention(I_Watch)
        
        P_Play = Process("Playing", [], [Playability], [], [], 86400, 1000)
        self.processes.AddProcess(P_Play)
        I_Play = Intention("Play", [P_Play])
        self.intentions.AddIntention(I_Play)
        self.intentions.AddHighLevelIntention(I_Play)
        
        P_Sit = Process("Sitting", [], [Sitability], [], [], 86400, 1000)
        self.processes.AddProcess(P_Sit)
        I_Sit = Intention("Sit", [P_Sit])
        self.intentions.AddIntention(I_Sit)
        self.intentions.AddHighLevelIntention(I_Sit)

        P_Repair = Process("Repairing", [], [Repairability, Screwability], [], [], 86400, 1000)
        self.processes.AddProcess(P_Repair)
        I_Repair = Intention("Repair", [P_Repair])
        self.intentions.AddIntention(I_Repair)
        self.intentions.AddHighLevelIntention(I_Repair)
        
        P_Nail = Process("Nailing", [], [Hammerability, Nailability], [], [], 86400, 1000)
        self.processes.AddProcess(P_Nail)
        I_Nail = Intention("Nail", [P_Nail])
        self.intentions.AddIntention(I_Nail)
        self.intentions.AddHighLevelIntention(I_Nail)
                     
        S_1 = Scenario()
        self.scenarios.AddScenario([0,1,2,3,4,5,6], S_1)
       
    def prepareMap(self, map):
        map.points = [ Point(0,0), Point(100,0), Point(100,100), Point(0, 100), Point(0, 80), Point(70, 50), Point(0, 20) ]
        map.width = 100
        map.height = 100
        
        map.AddObject(Nail, 20, 25, amount=10)
        map.AddObject(Hammer, 20, 30)
        map.AddObject(Pipe, 30, 25)
        map.AddObject(Box, 10, 25)
