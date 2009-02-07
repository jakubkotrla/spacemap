# -*- coding: UTF-8 -*-

from PerceptionField import PerceptionField
from ProcessesArea   import ProcessesArea
from SpaceMap         import SpaceMap
from MemoryArea     import MemoryArea
from ActionSelector  import ActionSelector
from Emotion         import Emotion
from Enviroment.Global import Global
from EpisodicMemory  import EpisodicMemory


class Intelligence:
    def __init__(self, agent, config):
        self.agent            = agent
        self.episodicMemory   = EpisodicMemory()
        self.spaceMap         = SpaceMap(agent)
        self.processesArea    = ProcessesArea(self.episodicMemory)
        self.memoryArea       = MemoryArea(self.agent, self.spaceMap, self.processesArea)
        self.perceptionField  = PerceptionField(self.processesArea, self.spaceMap, self.memoryArea)
        self.actionSelector   = ActionSelector(agent, config, self.processesArea, self.perceptionField, self.episodicMemory, self.spaceMap)
        self.stress           = 0
        self.curiousness      = 0
        self.emotion          = Emotion("emotion1", Global.Time)
        

    def GetAction(self):
        return self.actionSelector.GetAction(self.emotion)

    def ActionDone(self):
        self.actionSelector.ActionDone(self.emotion)
        self.spaceMap.StepUpdate()
        
    def TellTheStory(self, txt):
        self.episodicMemory.Print()
    def ShowPF(self, txt):
        self.perceptionField.Show(txt)

        
    def NoticeObjectsToPF(self, visibleObjects):
        self.perceptionField.NoticeObjects(visibleObjects)
        
    def RememberObjectsFor(self, affordance):
        return self.memoryArea.RememberObjectsFor(affordance)
    
    def LookForObject(self, memoryPhantom):
        return self.perceptionField.LookForObject(memoryPhantom)
                
    def UseObjects(self, excProcess):
        self.perceptionField.UseObjectPhantoms(excProcess)
        
    def UpdatePhantomsBecauseOfMove(self):
        self.perceptionField.UpdatePhantomsBecauseOfMove(self.agent)
        
        