

from Enviroment.Global import Global

from GridLayer import GridLayer
from KMLayer import KMLayer
from GLayer import GLayer 

class MemoryObject:
    def __init__(self, rObject, node, intensity=1):
        self.type = rObject.type
        self.node = node
        self.object = rObject
        self.x = int(node.x)
        self.y = int(node.y)
        self.intensity = intensity
        self.maxIntensity = 10
        
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
        node = self.GLayer.ObjectNoticed(rObject, 10)
        
        for aff in rObject.type.affordances:
            if aff not in self.affsToMemObjs:
                self.affsToMemObjs[aff] = []
            memObjs = self.affsToMemObjs[aff]
            memObj = None 
            if node.HasObject(rObject):
                for mO in memObjs:
                    if mO.object == rObject:
                        memObj = mO
                        break
                #hope it was found
            else:
                node.objects.append(rObject)    #ToDo udrzovat aktualni
                memObj = MemoryObject(rObject, node)
                self.affsToMemObjs[aff].append(memObj)  
            memObj.Intense()  
                
        memObj = MemoryObject(rObject, node)
        for aff in rObject.type.affordances:
            if aff not in self.affsToMemObjs:
                self.affsToMemObjs[aff] = []
            self.affsToMemObjs[aff].append(memObj)  
    
        
    def ObjectNoticedKM(self, rObject):
        #node = self.KMLayer.ObjectNoticed(rObject)
#        nodes = self.KMLayer.PositionToKMLNodes(rObject.x, rObject.y)
        
        #node = nodes[0]
        node = self.KMLayer.ObjectNoticed(rObject, 10)
        
        for aff in rObject.type.affordances:
            if aff not in self.affsToMemObjs:
                self.affsToMemObjs[aff] = []
            memObjs = self.affsToMemObjs[aff]
            memObj = None 
            if node.HasObject(rObject):
                for mO in memObjs:
                    if mO.object == rObject:
                        memObj = mO
                        break
                #hope it was found
            else:
                node.objects.append(rObject)    #ToDo udrzovat aktualni
                memObj = MemoryObject(rObject, node)
                self.affsToMemObjs[aff].append(memObj)  
            memObj.Intense()  
                
        memObj = MemoryObject(rObject, node)
        for aff in rObject.type.affordances:
            if aff not in self.affsToMemObjs:
                self.affsToMemObjs[aff] = []
            self.affsToMemObjs[aff].append(memObj)  
        
    
        
    def ObjectFound(self, rObject):
        pass
        
    def ObjectNotFound(self, rObject):
        Global.Log("SM: object not found: " + rObject.type.name)
        
    def ObjectUsed(self, rObject):
        pass
        
        
    def ObjectUsedUp(self, rObject):
        pass

