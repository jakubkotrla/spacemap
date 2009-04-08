
from Agents.Intentions import Intentions, Intention
from Enviroment.Affordances import *
from Enviroment.Objects import *
from Agents.Processes import Processes, Process
from Enviroment.Global import Global
from Enviroment.Map import Map, Point

from EmptyRoom import EmptyRoom
from FullRoom import FullRoom
from Corridor import Corridor
from Lobby import Lobby
from CrazyRoom import CrazyRoom
from SmallRoom import SmallRoom
from SwitchRoom import SwitchRoom
from HeapRoom import HeapRoom
from HeapLineRoom import HeapLineRoom


class ConfigSingleton:
    def __init__(self):
        self.configs = {}
        self.configs["EmptyRoom"] = EmptyRoom()
        self.configs["FullRoom"] = FullRoom()
        #self.configs["Corridor"] = Corridor()
        #self.configs["Lobby"] = Lobby()
        #self.configs["CrazyRoom"] = CrazyRoom()
        #self.configs["SmallRoom"] = SmallRoom()
        #self.configs["SwitchRoom"] = SwitchRoom()
        #self.configs["HeapRoom"] = HeapRoom()
        #self.configs["HeapLineRoom"] = HeapLineRoom()
        
    def GetConfigs(self):
        cfgs = self.configs.keys()
        cfgs.sort()
        return cfgs     
    
    def Get(self, configFile):
        self.config = self.configs[configFile]
        return self  
        
    def GetAgentIntentions(self, actionSelector):
        self.config.GetAgentIntentions(actionSelector)
        
    def SetUpMap(self):
        map = Map()
        self.config.SetUpMap(map)
        map.CalculateEdges()
        return map
    
    def GetWorldEvents(self):
        return self.config.GetWorldsEvents()
        
Config = ConfigSingleton()
        
