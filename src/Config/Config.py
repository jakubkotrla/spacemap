
from Agents.Intentions import Intentions, Intention
from Enviroment.Affordances import *
from Enviroment.Objects import *
from Agents.Processes import Processes, Process
from Agents.Scenarios import Scenarios, Scenario
from Enviroment.Global import Global
from Enviroment.Map import Map, Point

from EmptyRoom import EmptyRoom
from FullRoom import FullRoom
from Corridor import Corridor
from Lobby import Lobby
from CrazyRoom import CrazyRoom


class Config:
    def __init__(self, configFile):
        self.configs = {}
        self.configs["EmptyRoom"] = EmptyRoom()
        self.configs["FullRoom"] = FullRoom()
        self.configs["Corridor"] = Corridor()
        self.configs["Lobby"] = Lobby()
        self.configs["CrazyRoom"] = CrazyRoom()
        
        self.config = self.configs[configFile] 
        
        
    def GetAgentIntentions(self, actionSelector):
        self.config.GetAgentIntentions(actionSelector)
        
    def SetUpMap(self):
        map = Map()
        self.config.SetUpMap(map)
        map.CalculateEdges()
        return map 
        
        
        