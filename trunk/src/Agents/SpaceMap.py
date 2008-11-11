

import random
from Enviroment.Global import Global
from KMLayer import KMLayer

class MemoryObject:
    def __init__(self, rObject, node, i=1):
        self.type = rObject.type
        self.node = node
        self.intensity = i
        self.x = int(node.x)
        self.y = int(node.y)
    def Intense(self, i = 1):
        self.intensity += i
    def ToString(self):
        return self.type.name + " at [" + str(self.x) + "," + str(self.y) + "]"
    

class SpaceMap:
    def __init__(self, agent):
        self.agent   = agent
        self.objects = []
        self.map = Global.Map
        self.KMLayer = KMLayer(self.map)
        self.KMLayer.CreateMap()
        self.affsToMemObjs = {}
       
    def GetMemoryObject(self, affordance):
        if affordance not in self.affsToMemObjs:
            return None
        memObjs = self.affsToMemObjs[affordance]
        if len(memObjs) > 0:
            memObjs.sort(lambda a,b: cmp(a.intensity,b.intensity))
            if (memObjs[0].intensity > 0):
                return memObjs[0]
        return None
        
    def ObjectNoticed(self, rObject):
        node = self.KMLayer.ObjectNoticed(rObject)
        if node == None:
            Global.Log("Programmer.Error: SpaceMap.ObjectNoticed")
            return        
        memObj = MemoryObject(rObject, node)
        for aff in rObject.type.affordances:
            if aff not in self.affsToMemObjs:
                self.affsToMemObjs[aff] = []
            self.affsToMemObjs[aff].append(memObj)  
        
    
        
    def ObjectFound(self, rObject):
        self.KMLayer.ObjectFound(rObject)
        
    def ObjectNotFound(self, rObject):
        Global.Log("SM: object not found: " + rObject.type.name)
        self.KMLayer.ObjectNotFound(rObject)
        
    def ObjectUsed(self, rObject):
        self.KMLayer.ObjectUsed(rObject)
        
        
    def ObjectUsedUp(self, rObject):
        node = self.KMLayer.PositionToKMLNodes(rObject.x, rObject.y)
        
        for aff in rObject.type.affordances:
            if aff not in self.affsToMemObjs:
                pass
            else:
                for memObj in self.affsToMemObjs[aff]:
                    pass
                
        
        
        #self.KMLayer.ObjectUsedUp(rObject)
