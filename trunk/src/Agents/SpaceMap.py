

from Enviroment.Global import Global

from GridLayer import GridLayer
from KMLayer import KMLayer
from GLayer import GLayer 

class MemoryObject:
    def __init__(self, rObject, intensity=1):
        self.object = rObject
        self.type = rObject.type
        self.x = rObject.x
        self.y = rObject.y
        self.linkToNodes = []
        self.intensity = intensity
        self.maxIntensity = 10
        
    def AddLinkToNode(self, node, intensity=1):
        l = LinkMemoryObjectToNode(self, node, intensity)
        self.linkToNodes.append(l)
        
    def Intense(self, i = 1):
        if self.intensity < self.maxIntensity:
            self.intensity += i
            
    def ToString(self):
        return self.type.name + " at [" + str(self.x) + "," + str(self.y) + "]"

class LinkMemoryObjectToNode:
    def __init__(self, object, node, intensity):
        self.object = object
        self.node = node
        self.intensity = intensity
        self.maxIntensity = 10
        
    def Intense(self, i = 1):
        if self.intensity < self.maxIntensity:
            self.intensity += i
    

class SpaceMap:
    def __init__(self, agent):
        self.agent   = agent
        self.objects = []
        self.map = Global.Map
        self.affsToMemObjs = {}
        self.objectsToMemObjs = {}
        
        self.GridLayer = GridLayer(self.map)
        self.GridLayer.CreateMap()
        
        #self.KMLayer = KMLayer(self.map)
        #self.KMLayer.CreateMap(self.map)
        
        #self.GLayer = GLayer(self.map)
        #self.GLayer.CreateMap(self.map)
        
        
        
       
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
        if rObject in self.objectsToMemObjs:
            memObj = self.objectsToMemObjs[rObject]
            memObj.Intense()
            #ToDo: lower and lower effect on learning of layer
        else:
            #seen for first time
            memObj = MemoryObject(rObject)
            inNodes = self.GridLayer.PositionToNodes(memObj.x, memObj.y)
            for node in inNodes:
                memObj.AddLinkToNode(node)  #ToDo: intensity by distance * effect of noticing
        
        node = self.GridLayer.ObjectNoticed(memObj)
        
        # put memObject to all its affordances
        for aff in rObject.type.affordances:
            if aff not in self.affsToMemObjs:
                self.affsToMemObjs[aff] = []
            if memObj not in self.affsToMemObjs[aff]:
                self.affsToMemObjs[aff].append(memObj)
        
    
        
    def ObjectFound(self, rObject):
        pass
        
    def ObjectNotFound(self, rObject):
        Global.Log("SM: object not found: " + rObject.type.name)
        
    def ObjectUsed(self, rObject):
        pass
        
        
    def ObjectUsedUp(self, rObject):
        pass

