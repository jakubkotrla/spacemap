

import random
from Enviroment.Global import Global
from KMLayer import KMLayer

class MemoryObject:
    def __init__(self, rObject, node):
        self.type = rObject.type
        self.node = node
        self.x = int(node.x)
        self.y = int(node.y)


class SpaceMap:
    def __init__(self, agent):
        self.agent   = agent
        self.objects = []
        self.map = Global.Map
        self.KMLayer = KMLayer(self.map)
        self.KMLayer.CreateMap()
        self.affsToNodes = {}
       
    def GetMemoryObject(self, affordance):
        if affordance not in self.affsToNodes:
            return None
        memObjs = self.affsToNodes[affordance]
        if len(memObjs) > 0:
            return memObjs[0]
        return None
        
    def ObjectNoticed(self, rObject):
        node = self.KMLayer.ObjectNoticed(rObject)
        memObj = MemoryObject(rObject, node)
        for aff in rObject.type.affordances:
            if aff not in self.affsToNodes:
                self.affsToNodes[aff] = []
            
            self.affsToNodes[aff].append(memObj)  
        
    
        
    def ObjectFound(self, rObject):
        self.KMLayer.ObjectFound(rObject)
        
    def ObjectNotFound(self, rObject):
        Global.Log("SM: object not found: " + rObject.type.name)
        self.KMLayer.ObjectNotFound(rObject)
        
    def ObjectUsed(self, rObject):
        self.KMLayer.ObjectUsed(rObject)
        
    def ObjectUsedUp(self, rObject):
        self.KMLayer.ObjectUsedUp(rObject)
