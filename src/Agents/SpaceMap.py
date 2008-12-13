

from Enviroment.Global import Global
from EnergyLayer import EnergyLayer


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
        node.linkToObjects.append(l)
        
    def IntenseToNode(self, node, intensity=1.0):
        foundLink = None
        for l in self.linkToNodes:
            if l.node == node:
                foundLink = l
                break
        if foundLink == None:
            link = LinkMemoryObjectToNode(self, node, intensity)
            self.linkToNodes.append(link)
            node.linkToObjects.append(link)
        else:
            foundLink.Intense(intensity)
        
    def Intense(self, intensity = 1):
        self.intensity = self.intensity + intensity
        if self.intensity > self.maxIntensity: self.intensity = self.maxIntensity
            
    def ToString(self):
        return self.type.name + " at [" + str(self.x) + "," + str(self.y) + "]"

class LinkMemoryObjectToNode:
    def __init__(self, object, node, intensity):
        self.object = object
        self.node = node
        self.intensity = intensity
        self.maxIntensity = 10
        
    def Intense(self, i = 1.0):
        self.intensity = self.intensity + i
        if self.intensity > self.maxIntensity: self.intensity = self.maxIntensity
        
    def StepUpdate(self):
        self.intensity = self.intensity - 0.001
        if self.intensity < 0: self.intensity = 0 
            
    def NodeDeleted(self):
        self.object.linkToNodes.remove(self)
    def ToString(self):
        strInt =  '%.4f'%(self.intensity)
        return "LinkTo( " + strInt + " ): " + self.object.ToString()
    

class SpaceMap:
    def __init__(self, agent):
        self.agent   = agent
        self.objects = []
        self.map = Global.Map
        self.affsToMemObjs = {}
        self.objectsToMemObjs = {}
        
        self.Layer = EnergyLayer(self.map)
        self.Layer.CreateMap()
        
    def StepUpdate(self):
        self.Layer.StepUpdate() 
       
    def GetMemoryObject(self, affordance):
        if affordance not in self.affsToMemObjs:
            return None
        memObjs = self.affsToMemObjs[affordance]
        if len(memObjs) > 0:
            memObjs.sort(lambda a,b: cmp(a.intensity,b.intensity))
            if (memObjs[0].intensity > 0):
                return memObjs[0]
        return None
        
    
    def objectTrain(self, rObject, effect = 1):
        map = Global.Map
        if rObject in self.objectsToMemObjs:
            memObj = self.objectsToMemObjs[rObject]
            memObj.Intense()
        else:  #seen for first time
            memObj = MemoryObject(rObject)
            self.objectsToMemObjs[rObject] = memObj
        
        self.Layer.Train(memObj, effect)
        
        inNodes = self.Layer.PositionToNodes(memObj.x, memObj.y)
        nodesToIntensity = {}
        sumIntensity = 0
        effect = Global.TrainEffectNoticed * 4 * effect
        
        for node in inNodes:
            dist = map.DistanceObjs(node, memObj)
            intensity = Global.Gauss(dist/10.0)
            nodesToIntensity[node] = intensity
            sumIntensity = sumIntensity + intensity
        for node in inNodes:
            #ToDo use rObject.attractivity
            intensity = nodesToIntensity[node] * effect / sumIntensity
            memObj.IntenseToNode(node, intensity)
            
        #ToDo: lower and lower effect on learning of layer

        # put memObject to all its affordances
        for aff in rObject.type.affordances:
            if aff not in self.affsToMemObjs:
                self.affsToMemObjs[aff] = []
            if memObj not in self.affsToMemObjs[aff]:
                self.affsToMemObjs[aff].append(memObj)

    def ObjectNoticed(self, rObject, effect = 1):
        self.objectTrain(rObject, Global.TrainEffectNoticed * effect)
                
    def ObjectNoticedAgain(self, rObject, effect = 1):
        self.objectTrain(rObject, Global.TrainEffectNoticedAgain * effect)    
        
    def ObjectFound(self, rObject, effect = 1):
        self.objectTrain(rObject, Global.TrainEffectFound * effect)
        
    def ObjectNotFound(self, rObject, effect = 1):
        Global.Log("SM: object not found: " + rObject.type.name) #objectTrain TrainEffectNotFound * effect
        
    def ObjectUsed(self, rObject, effect = 1):
        self.objectTrain(rObject, Global.TrainEffectUsed * effect)
        
    def ObjectUsedUp(self, rObject, effect = 1):
        self.objectTrain(rObject, Global.TrainEffectUseUp * effect)

