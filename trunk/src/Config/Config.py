
from Agents.Intentions import Intentions, Intention
from Enviroment.Affordances import *
from Enviroment.Objects import *
from Agents.Processes import Processes, Process
from Agents.Scenarios import Scenarios, Scenario
from Enviroment.Global import Global
from Enviroment.Map import Map, Point

class Config:
    def __init__(self, configFile):
        self.intentions      = Intentions()
        self.processes       = Processes()
        self.scenarios       = Scenarios()
        
        self.prepareScenarios()
        
    def prepareScenarios(self):
        pass
       
    def prepareMap(self, map):
        map.points = [ Point(0,0), Point(100,0), Point(100,100), Point(0, 100), Point(0, 80), Point(70, 50), Point(0, 20) ]
        map.width = 100
        map.height = 100
        
        #map.AddObject(Meal, 20, 25, amount=10)
        map.AddObject(Snickers, 80, 55)
        map.AddObject(CocaColaCan, 50, 35)
        #map.AddObject(Glasses, 50, 55)
        #map.AddObject(Book, 51, 56)
        map.AddObject(Plate, 90, 55)
        map.AddObject(Water, 80, 75)
        #map.AddObject(Wood, 51, 52)
        #map.AddObject(Torch, 50, 52)
        map.AddObject(Pipe, 30, 25) 


    def SetUpMap(self):
        map = Map()
        self.prepareMap(map)
        map.CalculateEdges()
        return map 
        
        
        
