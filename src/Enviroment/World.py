

import Affordances
import Objects
import Map
from Global import Global

class World:
    
    def __init__(self, config):
        self.time = 0
        self.agent = None
        
        Global.Map = config.SetUpMap()
        

    def SetAgent(self, agent):
        self.agent = agent
        map = Global.Map
        map.PlaceAgent(agent)

    def Step(self):
        Global.Log("--- World step --- " + str(Global.TimeToHumanFormat()))
        self.agent.Step()
            
    
            