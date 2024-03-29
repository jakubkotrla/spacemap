## @package Agents.MemoryArea
# Contains MemoryArea and MemoryPhantom.

from Enviroment.Global import Global

## Represents memory phantom of object retrieved from SpaceMap.
class MemoryPhantom:
    def __init__(self, memoryObject, habituation=Global.MAPhantomHabituation):
        self.object  = memoryObject
        self.affordance  = None
        self.ownerProcess  = None
        self.habituation = habituation
        
    def GetType(self):
        return "m"
    
    ## Decrease self.habituation.
    def Habituate(self, amount):
        self.habituation -= amount
        return self.habituation < 1
        
    def SetOwnerProcess(self, process):
        if self.ownerProcess != None:
            Global.Log("Programmer.Error MemoryPhantom with owner process set again:" + self.object.ToString())
        self.ownerProcess = process
        process.resources.append(self)
    
    ## Removes self from owner process if any.   
    def MemoryObjectNotFound(self):
        if self.ownerProcess != None and self in self.ownerProcess.resources:
            self.ownerProcess.resources.remove(self)
        self.ownerProcess = None
                
    def ToString(self):
        if (self.ownerProcess != None):
            str = "Phantom(M) of " + self.object.ToString() + " linked to " + self.ownerProcess.process.name
        else:
            str = "Phantom(M) of " + self.object.ToString()
        return str

## Represents "pametova cast" of short-term memory
class MemoryArea:
    def __init__(self, agent, spaceMap, processArea):
        self.agent = agent
        self.spaceMap = spaceMap
        self.processArea = processArea
        self.memoryPhantoms = []
    
    ## Retrieves MemoryObject for given affordance and returns it as MemoryPhantom.
    def RememberObjectsFor(self, affordance):
        memPhantom = self.GetPhantomOfThinkedAffordance(affordance)
        if memPhantom == None:
            memObject = self.spaceMap.GetMemoryObject(affordance)
            if memObject != None:
                memPhantom = MemoryPhantom(memObject)
            else:
                return None
        self.memoryPhantoms.append(memPhantom)
        self.processArea.PhantomRemembered(memPhantom)
        return memPhantom
    
    ## Return first MemoryPhantom for given object if exists - agent thinks of it.
    def GetPhantomForObject(self, rObj):
        for phantom in self.memoryPhantoms:
            if rObj == phantom.object.object:
                return phantom
        return None
        
    ## Remove MemoryPhantom when it was not found during LookForObject. Called from PerceptionField. 
    def RemovePhantom(self, memoryPhantom):
        if memoryPhantom == None: return
        if memoryPhantom not in self.memoryPhantoms:
            Global.Log("Programmer.Error: MemoryArea.RemovePhantom not in MA: " + memoryPhantom.object.ToString())
            return
        self.memoryPhantoms.remove(memoryPhantom)
     
    ## Returns MemoryPhantom for givne affordance from MemoryArea if any.           
    def GetPhantomOfThinkedAffordance(self, affordance):
        for phantom in self.memoryPhantoms:
            if affordance in phantom.object.type.affordances:
                return phantom
        return None
    
    ## Decrease habituation of MemoryPhantoms and removes habituated.   
    def Update(self, action):
        habituatedPhantoms = []
        for phantom in self.memoryPhantoms:
            if phantom.ownerProcess == None or (not phantom.ownerProcess.IsInProgress()):
                if phantom.Habituate(action.duration):
                    habituatedPhantoms.append(phantom)
        for habituatedPhantom in habituatedPhantoms:
            self.memoryPhantoms.remove(habituatedPhantom)
        
        
        