## @package Config.Config
# Singleton containing all available worlds - configs.

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

## Singleton containing all available worlds - configs.
class ConfigSingleton:
    def __init__(self):
        self.configs = {}
        self.configs["EmptyRoom"] = EmptyRoom()
        self.configs["FullRoom"] = FullRoom()
        self.configs["Corridor"] = Corridor()
        self.configs["Lobby"] = Lobby()
        self.configs["CrazyRoom"] = CrazyRoom()
        self.configs["SmallRoom"] = SmallRoom()
        self.configs["SwitchRoom"] = SwitchRoom()
        self.configs["HeapRoom"] = HeapRoom()
        self.configs["HeapLineRoom"] = HeapLineRoom()
    
    ## Returns all available configs name sorted.   
    def GetConfigs(self):
        cfgs = self.configs.keys()
        cfgs.sort()
        return cfgs     
    
    ## Sets config with given name as active.
    def Get(self, configFile):
        self.config = self.configs[configFile]
        return self  
        
    ## Set-ups agent's ActionSelector by calling active config.
    def GetAgentIntentions(self, actionSelector):
        self.config.GetAgentIntentions(actionSelector)
    
    ## Set-ups virtual world by calling active config.    
    def SetUpMap(self):
        map = Map()
        self.config.SetUpMap(map)
        map.CalculateEdges()
        return map
    
    ## Returns world's future history by calling active config.
    def GetWorldEvents(self):
        return self.config.GetWorldsEvents()
        
Config = ConfigSingleton()
        
