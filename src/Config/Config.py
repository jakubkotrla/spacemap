
from Agents.Intentions import Intentions, Intention
from Enviroment.Affordances import *
from Enviroment.Objects import *
from Agents.Processes import Processes, Process
from Agents.Scenarios import Scenarios, Scenario
from Enviroment.Global import Global
from Enviroment.Map import Map, Point

from EmptyRoom import EmptyRoom


class Config:
    def __init__(self, configFile):
        self.configs = {}
        self.configs["EmptyRoom"] = EmptyRoom()
        
        self.config = self.configs[configFile] 
        
        
    def GetAgentIntentions(self, actionSelector):
        self.config.GetAgentIntentions(actionSelector)
        
    def SetUpMap(self):
        map = Map()
        self.config.SetUpMap(map)
        map.CalculateEdges()
        return map 
        
        
        
