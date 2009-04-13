## @package Agents.SpaceMap
# Implements agent's spatial map.

from Enviroment.Global import Global
from EnergyLayer import EnergyLayer
from Enviroment.Map import Point, RealObject
from math import log

## Represents "pametova stopa predmetu".
class MemoryObject:
    def __init__(self, rObject, intensity=1):
        self.object = rObject
        self.type = rObject.type
        self.x = rObject.x
        self.y = rObject.y
        self.linkToNodes = []
        self.intensity = intensity
        self.effectivity = intensity    #only for SpaceMap to find best MemObj (intensity and distance) 
    
    ## Creates new link to node.    
    def AddLinkToNode(self, node, intensity=1):
        l = LinkMemoryObjectToNode(self, node, intensity)
        self.linkToNodes.append(l)
        node.linkToObjects.append(l)
        
    ## Increases intensity of link to given node, creates one if not found.
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
            
    ## Increases self-intensity.
    def Intense(self, intensity):
        self.intensity = self.intensity + intensity

    ## Decreases self-intensity and intensity of all its links to nodes.
    def StepUpdate(self):
        self.intensity = self.intensity - Global.MemObjIntensityFadeOut
        for link in self.linkToNodes:
            link.StepUpdate()
            
    def ToString(self):
        strXY = '%.2f'%(self.x) + ";" + '%.2f'%(self.y)
        return self.type.name + "(M) at [" + strXY + "]"
    

## Represents link MemoryObject-Node.
class LinkMemoryObjectToNode:
    def __init__(self, object, node, intensity):
        self.object = object
        self.node = node
        self.intensity = intensity
        self.node.Intense(intensity)
        
    ## Increases self-intensity.
    def Intense(self, intensity):
        self.intensity = self.intensity + intensity
        self.node.Intense(intensity)
    
    ## Decreaes self-intensity, eventually deleting self. Called from MemoryObject.StepUpdate().
    def StepUpdate(self):
        self.intensity = self.intensity - Global.LinkMemObjToNodeFadeOut
        if self.intensity <= 0:
            self.object.linkToNodes.remove(self)
            self.node.linkToObjects.remove(self)
    
    ## Propagates deletion of node to MemoryObject.        
    def NodeDeleted(self):
        self.object.linkToNodes.remove(self)
    def ToString(self):
        strInt = '%.4f'%(self.intensity)
        return "LinkTo( " + strInt + " ): " + self.object.ToString()
    
## Represents "prostorova pamet" and "pamet na predmety". 
class SpaceMap:
    def __init__(self, agent):
        self.agent   = agent
        self.map = Global.Map
        self.affsToMemObjs = {}
        self.objectsToMemObjs = {}
        self.maxTrained = 0
        self.updateStep = 0
        
        self.Layer = EnergyLayer(self.map)
        self.Layer.CreateMap()
     
    ## One step of simulation of SpaceMap. Calls StepUpdate of its MemoryObjecst and underlying node layer. 
    def StepUpdate(self, action):
        if action.duration > Global.SMUpdateMaxDuration:
            count = int( log(3 + action.duration - Global.SMUpdateMaxDuration) )
        else:
            count = 1
            
        for i in range(count):
            self.Layer.StepUpdate()
            memObjs = self.objectsToMemObjs.values()
            for memObj in memObjs:
                memObj.StepUpdate()
            
        if self.updateStep > Global.SMBigUpdateFreq:
            self.updateStep = 1
            self.StepUpdateBig()
        else:
            self.updateStep += 1
     
    ## Used only to save data about error of SpaceMap to CSV data file.       
    def StepUpdateBig(self):
        memObjs = self.objectsToMemObjs.values()
        for memObj in memObjs:
            self.updateMemoryObjectLocation(memObj)
    
    ## Returns most intense and closest MemoryObject with given affordance.   
    def GetMemoryObject(self, affordance):
        if affordance not in self.affsToMemObjs:
            return None
        memObjs = self.affsToMemObjs[affordance]
        if len(memObjs) < 1: return None
        
        if len(memObjs) > 1:
            sumIntensity = sum( map(lambda o: o.intensity, memObjs) )
            if sumIntensity <= 0: return None
            for mo in memObjs:
                dist = self.map.DistanceObjs(self.agent, mo) 
                mo.effectivity = dist * (float(mo.intensity) / sumIntensity) 
            memObjs.sort(lambda b,a: cmp(a.effectivity,b.effectivity))
        
        if (memObjs[0].effectivity > 0):
            return self.updateMemoryObjectLocation(memObjs[0])
        else:
            return None
     
    ## Updates loction of MemoryObject - computes weighted centroid of its links to nodes.   
    def updateMemoryObjectLocation(self, memObject):
        links = memObject.linkToNodes
        x = 0
        y = 0
        if 0 == len(links):
            return memObject
        sumIntensity = 0
        for link in links:
            x += (link.node.x * link.intensity)
            y += (link.node.y * link.intensity)
            sumIntensity += link.intensity 
        x = x / sumIntensity
        y = y / sumIntensity
        p = Point(x,y)
        if not self.map.IsInside(p):  #this should not happen, quick hack - go closer to memObj
            hit = self.map.CanMoveEx(memObject, p.x, p.y)
            if hit.hit:
                p = hit
            else:
                Global.Log("Programmer.Error: SpaceMap: not inside but canMove-not-hit")
        memObject.x = p.x
        memObject.y = p.y
        
        step = Global.GetStep()
        error = self.map.DistanceObjs(p, memObject.object)
        errorStr = '%.2f'%error
        trained = memObject.object.trainHistory
        line = str(step) + ";" + str(trained) + ";" + errorStr + ";" + memObject.object.IdStr()  
        Global.LogData("rememberinfo", line)

        return memObject
        
    ## Internal method to train SpaceMap to given object with given effect. 
    def objectTrain(self, rObject, effect):
        effect = effect * rObject.curAttractivity * rObject.visibility
        rObject.trainHistory = rObject.trainHistory + effect
        self.maxTrained = max(rObject.trainHistory, self.maxTrained)
        
        map = Global.Map
        if rObject in self.objectsToMemObjs:
            memObj = self.objectsToMemObjs[rObject]
            memObj.Intense(effect)
        else:
            memObj = MemoryObject(rObject)
            self.objectsToMemObjs[rObject] = memObj
        
        memObj.x = rObject.x    #little nasty hack, memObj.xy was weighted centorid of links to nodes 
        memObj.y = rObject.y    #this will fix it and make memObj correct for EnergyLayer training
        self.Layer.Train(memObj, effect)    #that will train memObj-to-nodes now and then continually in EP.StepUpdate
                    
        # put memObject to all its affordances
        for aff in rObject.type.affordances:
            if aff not in self.affsToMemObjs:
                self.affsToMemObjs[aff] = []
            if memObj not in self.affsToMemObjs[aff]:
                self.affsToMemObjs[aff].append(memObj)

    ## Train SpaceMap to given object, object was noticed.
    def ObjectNoticed(self, rObject):
        self.objectTrain(rObject, Global.TrainEffectNoticed)
    
    ## Train SpaceMap to given object, object was noticed again.            
    def ObjectNoticedAgain(self, rObject):
        self.objectTrain(rObject, Global.TrainEffectNoticedAgain)    
    
    ## Train SpaceMap to given object, object was found.
    def ObjectFound(self, rObject):
        self.objectTrain(rObject, Global.TrainEffectFound)
        
    ## Train SpaceMap to given object, object was not ofund.
    def ObjectNotFound(self, rObject):
        Global.Log("SM.ObjectNotFound: object not found: " + rObject.ToString())
        #dynamicWorld: objectTrain TrainEffectNotFound TBD.
    
    ## Train SpaceMap to given object, object was used by agent.
    def ObjectUsed(self, rObject):
        self.objectTrain(rObject, Global.TrainEffectUsed)


