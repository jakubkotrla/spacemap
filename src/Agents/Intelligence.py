## @package Agents.Intelligence
# Contains Intelligence representing collection of classes implementing agent's intelligence.

from PerceptionField import PerceptionField
from ProcessArea import ProcessArea
from SpaceMap import SpaceMap
from MemoryArea import MemoryArea
from ActionSelector import ActionSelector
from Emotion import Emotion
from Enviroment.Global import Global
from EpisodicMemory import EpisodicMemory

## Collection of classes to implement agent's intelligence
class Intelligence:
    def __init__(self, agent, config):
        self.agent            = agent
        self.episodicMemory   = EpisodicMemory()
        self.spaceMap         = SpaceMap(agent)
        self.processArea      = ProcessArea(self.episodicMemory)
        self.memoryArea       = MemoryArea(self.agent, self.spaceMap, self.processArea)
        self.perceptionField  = PerceptionField(self.agent, self.processArea, self.spaceMap, self.memoryArea)
        self.actionSelector   = ActionSelector(agent, config, self.processArea, self.perceptionField, self.episodicMemory, self.spaceMap)
        self.stress           = 0
        self.curiousness      = 0
        self.emotion          = Emotion("emotion1", Global.Time)
        
    ## Calls ActionSelector.GetAction().
    def GetAction(self):
        return self.actionSelector.GetAction(self.emotion)

    ## Calls ActionSelector.ActionDone().
    def ActionDone(self):
        self.actionSelector.ActionDone(self.emotion)
    
    ## Calls EpisodicMemory.TellTheStory().   
    def TellTheStory(self, txt):
        self.episodicMemory.Print()

    ## Calls PerceptionField.NoticeObjects().
    def NoticeObjects(self, visibleObjects, action):
        self.perceptionField.NoticeObjects(visibleObjects, action)
    
    ## Calls MemoryArea.RemerberObjecsForAffordance() that calls SpaceMap.
    def RememberObjectsFor(self, affordance):
        return self.memoryArea.RememberObjectsFor(affordance)
    
    ## Calls PerceptionField.LookForObject().
    def LookForObject(self, memoryPhantom):
        return self.perceptionField.LookForObject(memoryPhantom)
    
    ## Calls PerceptionField.UseObjectPhantoms().
    def UseObjects(self, excProcess):
        self.perceptionField.UseObjectPhantoms(excProcess)
    
    ## Calls PerceptionField.UpdatePhantomsBecauseOfMove().
    def UpdatePhantomsBecauseOfMove(self):
        self.perceptionField.UpdatePhantomsBecauseOfMove(self.agent)
        
        
