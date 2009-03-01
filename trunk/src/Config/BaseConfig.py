
from Enviroment.Affordances import *
from Enviroment.Objects import *
from Agents.Intentions import Intentions, Intention
from Agents.Processes import Processes, Process
from Agents.Scenarios import Scenarios, Scenario

class BaseConfig:
    def __init__(self):
        self.intentions = Intentions()
        self.processes = Processes()
        self.scenarios = Scenarios()
        
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
                     
    
    def prepareScenarios(self):             
        S_1 = Scenario()
        self.scenarios.AddScenario([0,1,2,3,4,5,6], S_1)
        
    def GetAgentIntentions(self, actionSelector):
        self.intentions = Intentions()
        self.processes = Processes()
        self.scenarios = Scenarios()
        
        self.prepareProcessIntentions()
        self.prepareScenarios()
        
        actionSelector.processes = self.processes
        actionSelector.intentions = self.intentions
        actionSelector.scenarios = self.scenarios
       
    def prepareMap(self, map):
        pass

    def SetUpMap(self, map):
        self.prepareMap(map)
        
