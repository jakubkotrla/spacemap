
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
        
    def AddLinkToNode(self, node, intensity=1):
        l = LinkMemoryObjectToNode(self, node, intensity)
        self.linkToNodes.append(l)
        node.linkToObjects.append(l)
        
    def IntenseToNode(self, node, intensity):
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
    def Intense(self, intensity):
        self.intensity = self.intensity + intensity
        if self.intensity > Global.MemObjMaxIntensity: self.intensity = Global.MemObjMaxIntensity

    def StepUpdate(self):
        self.intensity = self.intensity - Global.MemObjIntensityFadeOut
        for link in self.linkToNodes:
            link.StepUpdate()
            
    def ToString(self):
        return self.type.name + "(Memory) at [" + str(self.x) + "," + str(self.y) + "]"
    

class LinkMemoryObjectToNode:
    def __init__(self, object, node, intensity):
        self.object = object
        self.node = node
        self.intensity = intensity
        
    def Intense(self, intensity):
        self.intensity = self.intensity + intensity
        if self.intensity > Global.LinkMemObjToNodeMaxIntensity: self.intensity = Global.LinkMemObjToNodeMaxIntensity
    
    #called from MemoryObject.StepUpdate
    def StepUpdate(self):
        self.intensity = self.intensity - Global.LinkMemObjToNodeFadeOut
        if self.intensity < 0: self.intensity = 0 
            
    def NodeDeleted(self):
        self.object.linkToNodes.remove(self)
    def ToString(self):
        strInt = '%.4f'%(self.intensity)
        return "LinkTo( " + strInt + " ): " + self.object.ToString()
    

class SpaceMap:
    def __init__(self, agent):
        self.agent   = agent
        self.map = Global.Map
        self.affsToMemObjs = {}
        self.objectsToMemObjs = {}
        self.maxTrained = 0
        
        self.Layer = EnergyLayer(self.map)
        self.Layer.CreateMap()
        
    def StepUpdate(self):
        self.Layer.StepUpdate()
        memObjs = self.objectsToMemObjs.values()
        for memObj in memObjs:
            memObj.StepUpdate()
       
    def GetMemoryObject(self, affordance):
        if affordance not in self.affsToMemObjs:
            return None
        memObjs = self.affsToMemObjs[affordance]
        if len(memObjs) > 0:
            memObjs.sort(lambda a,b: cmp(a.intensity,b.intensity)) #ToDo: include distance as cmp param
            if (memObjs[0].intensity > 0):
                return memObjs[0]
        return None
        
    
    def objectTrain(self, rObject, effect):
        rObject.trainHistory = rObject.trainHistory + effect
        self.maxTrained = max(rObject.trainHistory, self.maxTrained)
        
        map = Global.Map
        if rObject in self.objectsToMemObjs:
            memObj = self.objectsToMemObjs[rObject]
            memObj.Intense(effect)
        else:  #seen for first time
            memObj = MemoryObject(rObject)
            self.objectsToMemObjs[rObject] = memObj
        
        self.Layer.Train(memObj, effect)
        
        inNodes = self.Layer.PositionToNodes(memObj.x, memObj.y, Global.ELGravityRange)
        nodesToIntensity = {}
        sumIntensity = 0
        effect = Global.SMTRainEffectCoef * effect
        
        for node in inNodes:
            dist = map.DistanceObjs(node, memObj)
            intensity = Global.Gauss( dist / Global.SMNodeAreaDivCoef, Global.SMNodeAreaGaussCoef)
            nodesToIntensity[node] = intensity
            sumIntensity = sumIntensity + intensity
        for node in inNodes:
            #ToDo: use rObject.attractivity
            intensity = nodesToIntensity[node] * effect / sumIntensity
            memObj.IntenseToNode(node, intensity)
            
        # put memObject to all its affordances
        for aff in rObject.type.affordances:
            if aff not in self.affsToMemObjs:
                self.affsToMemObjs[aff] = []
            if memObj not in self.affsToMemObjs[aff]:
                self.affsToMemObjs[aff].append(memObj)

    def ObjectNoticed(self, rObject):
        self.objectTrain(rObject, Global.TrainEffectNoticed)
                
    def ObjectNoticedAgain(self, rObject):
        self.objectTrain(rObject, Global.TrainEffectNoticedAgain)    
        
    def ObjectFound(self, rObject):
        self.objectTrain(rObject, Global.TrainEffectFound)
        
    def ObjectNotFound(self, rObject):
        Global.Log("SM.ObjectNotFound: object not found: " + rObject.ToString())
        #ToDo: objectTrain TrainEffectNotFound
        
    def ObjectUsed(self, rObject):
        self.objectTrain(rObject, Global.TrainEffectUsed)
        
    def ObjectUsedUp(self, rObject):
        self.objectTrain(rObject, Global.TrainEffectUsedUp)

