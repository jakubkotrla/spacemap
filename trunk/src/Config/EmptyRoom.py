
from Agents.Intentions import Intentions, Intention
from Enviroment.Affordances import *
from Enviroment.Objects import *
from Agents.Processes import Processes, Process
from Agents.Scenarios import Scenarios, Scenario
from Enviroment.Global import Global
from Enviroment.Map import Map, Point, Waypoint
from BaseConfig import BaseConfig

class EmptyRoom(BaseConfig):
    def __init__(self):
        BaseConfig.__init__(self)
    
    def prepareProcessIntentions(self):
        P_Smoke = Process("Smoking", [], [Smokeability], [], [], 300)
        self.processes.AddProcess(P_Smoke)
        I_Smoke = Intention("Smoke", [P_Smoke])
        self.intentions.AddIntention(I_Smoke)
        self.intentions.AddHighLevelIntention(I_Smoke)
       
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

    def prepareMap(self, map):
        map.points = [ Point(0,0), Point(100,0), Point(100,100), Point(0, 100) ]
        map.wayPoints = [ Waypoint(50,50), Waypoint(10,10), Waypoint(90,10), Waypoint(10,90), Waypoint(90,90) ]
        map.width = 100
        map.height = 100
        map.SetAgentStart(50, 50)
        
        #map.AddObject(Nail, 20, 25, amount=10)
        #map.AddObject(Hammer, 20, 30)
        map.AddObject(Flower, 20, 25)
        map.AddObject(Chess, 20, 30)
        map.AddObject(Pipe, 94, 40)
        map.AddObject(Box, 40, 60)
