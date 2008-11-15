# -*- coding: UTF-8 -*-

from Enviroment.Global import Global


class MemoryPhantom:
    def __init__(self, memoryObject, habituation):
        self.object  = memoryObject
        self.affordance  = None     #which object affordance will be used - to speed up things
        self.ownerProcess  = None
        self.habituation = habituation
        
    def IsMemoryPhantom(self):
        return True
        
    def Update(self, realObject, habituation):
        self.positionX   = realObject.x
        self.positionY   = realObject.y
        self.habituation = habituation
    
    def Habituate(self):
        self.habituation -= 1
        return self.habituation < 1
        
    def SetOwnerProcess(self, process):
        if self.ownerProcess != None:
            Global.Log("MemoryPhantom.Error:" + self.object.type.name)
        self.ownerProcess = process
        process.resources.append(self)
        
    def ResetOwnerProcess(self):
        if self.ownerProcess != None:
            self.ownerProcess.resources.remove(self)
        self.ownerProcess = None
        
    def ToString(self):
        if (self.ownerProcess != None):
            str = "Phantom(M) of " + self.object.ToString() + " linked to " + self.ownerProcess.process.name
        else:
            str = "Phantom(M) of " + self.object.ToString()
        return str


class MemoryArea:
    def __init__(self, agent, spaceMap, processArea):
        self.agent = agent
        self.spaceMap = spaceMap
        self.processArea = processArea
        self.memoryPhantoms = []
        self.perceptionHabituationTime = 10
        
    def RememberObjectsFor(self, affordance):
        memObject = self.spaceMap.GetMemoryObject(affordance)
        if memObject != None:
            memPhantom = MemoryPhantom(memObject, self.perceptionHabituationTime)
            self.memoryPhantoms.append(memPhantom)
            self.processArea.PhantomRemembered(memPhantom)
            return memPhantom
        else:
            return None
        
    def RemovePhantom(self, memoryPhantom):
        if memoryPhantom == None: return
        if memoryPhantom not in self.memoryPhantoms:
            Global.Log("Programmer Error: MemoryArea.RemovePhantom " + memoryPhantom.object.type.name)
            #return
        self.memoryPhantoms.remove(memoryPhantom)
      
    def Show(self, txt):
        txt.delete(0, 1000)
        for phantom in self.memoryPhantoms:
            txt.insert("end", phantom.ToString())  
        
        
        
        
        
        