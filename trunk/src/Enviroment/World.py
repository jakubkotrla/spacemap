

import Affordances
import Objects
import Map
from Global import Global

class World:
    
    def __init__(self, config):
        self.step = 0
        self.agent = None
        
        Global.Map = config.SetUpMap()
        

    def SetAgent(self, agent):
        self.agent = agent
        map = Global.Map
        map.PlaceAgent(agent)

    def Step(self):
        Global.Log("------------------------------ Step " + str(self.step).zfill(5) + " --- " + str(Global.TimeToHumanFormat()) + " ----------")
        self.agent.Step()
        map = Global.Map
        map.Step(self.agent)
        self.step = self.step + 1
            
    
            