

import Affordances
import Objects
import Map
from Global import Global

class World:
    
    def __init__(self):
        self.time = 0
        self.agent = None
        

    def SetAgent(self, agent):
        self.agent = agent
        map = Global.Map
        map.PlaceAgent(agent, 10, 10)

    def Step(self):
        Global.Log("--- World step --- " + str(Global.TimeToHumanFormat()))
        self.agent.Step()
            
    
            