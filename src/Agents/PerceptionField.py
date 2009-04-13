## @package Agents.PerceptionField
# Contains PerceptionField and Phantom.

import copy
from Enviroment.Global import Global
from PerceptionFilter import PerceptionFilter

## REpresents Phantom of seen object.
class Phantom:
    def __init__(self, rObject, memoryPhantom=None):
        self.object      = rObject
        self.affordance  = None
        self.ownerProcess = None
        habEffect = rObject.curAttractivity * rObject.visibility
        self.habituation = Global.PFPhantomHabCreate * habEffect
        ## Pointer to MemoryPhantom, if object was looked for and there is corresponding MemoryPhantom i MemoryArea. None otherwise.
        self.memoryPhantom = memoryPhantom
    
    ## Increase habituation as a result of ObjectNoticedAgain.
    def Update(self, rObject):
        hab = Global.PFPhantomHabUpdate * rObject.curAttractivity * rObject.visibility
        self.habituation += hab
    
    ## Decrease habituation of Phantom.
    def Habituate(self, amount):
        self.habituation -= amount
        return self.habituation < 1
        
    def SetOwnerProcess(self, process):
        if self.ownerProcess != None:
            Global.Log("Programmer.Error: Phantom with owner process set again: " + self.object.ToString())
        self.ownerProcess = process
        process.resources.append(self)
    
    ## Deletes self and recreates MemoryPhantom in MemoryArea if any.    
    def DeletedOrLost(self):
        if self.ownerProcess != None:
            if self in self.ownerProcess.resources:
                self.ownerProcess.resources.remove(self)
                #if EnvPhantom deleted but there is memoryPhantom of it, relink process.resources back to memoryPhantom
                if self.memoryPhantom != None and self.memoryPhantom.ownerProcess == self.ownerProcess:
                    self.ownerProcess.resources.append(self.memoryPhantom)
        self.ownerProcess = None
        self.memoryPhantom = None
        #self will be deleted
    
    ## Reset ist ownerProcess, its MemoryPhantom's ownerProcess as well.
    def OwnerProcessTerminated(self):
        #self.ownerProcess.resources.remove(self) - meaningless, process will never be used again, is only stored in episodic memory
        self.ownerProcess = None
        if self.memoryPhantom != None:
            self.memoryPhantom.ownerProcess = None
            self.memoryPhantom = None
    
    def GetType(self):
        return "e"
     
    def ToString(self):
        if (self.ownerProcess != None):
            s = "Phantom(E, " + str(self.habituation) + ") of " + self.object.ToString() + " linked to " + self.ownerProcess.process.name
        else:
            s = "Phantom(E, " + str(self.habituation) + ") of " + self.object.ToString()
        return s

## Represent agent's shortterm memory for seen objects, contains list of objects' phantoms. 
class PerceptionField:
    def __init__(self, agent, processArea, spaceMap, memoryArea):
        self.agent = agent
        self.environmentPhantoms = []
        self.processArea = processArea
        self.spaceMap = spaceMap
        self.memoryArea = memoryArea
        self.perceptionFilter = PerceptionFilter()

    ## Notice new and already seen object to PF.
    #
    # Phantoms are sorted by theirs habiuation and only Global.PFsize of phantoms is stored.
    # Stored phantoms are propagated to ProcessArea and SpaceMap.
    def NoticeObjects(self, visibleObjects, actProcess):
        self.perceptionFilter.ProcessObjects(visibleObjects, actProcess)
        phantomsToSpaceMap = {}
        for rObj in visibleObjects:
            if rObj.curAttractivity == 0: continue
            phantom = self.GetPhantomForObj(rObj)
            if phantom != None:
                phantom.Update(rObj)
                phantomsToSpaceMap[phantom] = "ObjectNoticedAgain"
            else:
                memPhantom = self.memoryArea.GetPhantomForObject(rObj)
                if memPhantom != None and self.processArea.LookingForPhantom(memPhantom):
                    phantom = Phantom(rObj, memPhantom)
                    self.environmentPhantoms.append(phantom)
                    #self.processArea.PhantomAddedForMemoryPhantom(phantom, memPhantom) - later
                    phantomsToSpaceMap[phantom] = "ObjectFound"
                    Global.Log("PF: Adding phantom for object " + rObj.ToString() + " instead of " + memPhantom.ToString())
                else:
                    phantom = Phantom(rObj)
                    self.environmentPhantoms.append(phantom)
                    #self.processArea.PhantomAdded(phantom) - later
                    phantomsToSpaceMap[phantom] = "ObjectNoticed"
                    Global.Log("PF: Adding phantom for object " + rObj.ToString())
        #phantoms updated, truncate to PF.Size
        phantoms = self.environmentPhantoms
        phantoms.sort(lambda b,a: cmp(a.habituation,b.habituation))
        phantomsToDelete = phantoms[Global.PFSize:]
        for phantomToDelete in phantomsToDelete:
            self.environmentPhantoms.remove(phantomToDelete)
            phantomToDelete.DeletedOrLost()
            Global.Log("PF: removing(over PF.size) phantom for object " + phantomToDelete.object.ToString())
        
        for phantom in self.environmentPhantoms:
            if phantom not in phantomsToSpaceMap:
                #happens when agent changes viewCones and object is not in normal VCs (was added by explore VCs) - ignore
                continue
            if phantomsToSpaceMap[phantom] == "ObjectNoticedAgain":
                self.spaceMap.ObjectNoticedAgain(phantom.object)
            elif phantomsToSpaceMap[phantom] == "ObjectFound":
                self.processArea.PhantomAddedForMemoryPhantom(phantom, phantom.memoryPhantom)
                self.spaceMap.ObjectFound(phantom.object)
            elif phantomsToSpaceMap[phantom] == "ObjectNoticed":
                self.processArea.PhantomAdded(phantom)
                self.spaceMap.ObjectNoticed(phantom.object)

    ## One step of simualtion of PF, decrase habituation of phantoms and removes habituated ones. 
    def Update(self, action):
        habituatedPhantoms = []
        for phantom in self.environmentPhantoms:
            #if self.processArea.IsPhantomUsedNow(phantom): continue  - not enough
            if phantom.ownerProcess == None or (not phantom.ownerProcess.IsInProgress()):
                if phantom.Habituate(action.duration):
                    habituatedPhantoms.append(phantom)
        for habituatedPhantom in habituatedPhantoms:
            self.environmentPhantoms.remove(habituatedPhantom)
            habituatedPhantom.DeletedOrLost()
            Global.Log("PF: removing(habituated) phantom for object " + habituatedPhantom.object.ToString())

    ## Returns phantom of given object if any in PF. Otherwise returns None. 
    def GetPhantomForObj(self, rObj):
        for phantom in self.environmentPhantoms:
            if phantom.object == rObj:
                return phantom
        return None 
    
    ## Finds phantoms for given ExcitedProcess to fill in missing slots/sources regarding affordances.
    def TryToLinkPhantomsFor(self, excProcess, missingSources):
        for wantedAff in missingSources:
            phantomForAff = None
            for phantom in self.environmentPhantoms:
                if wantedAff in phantom.object.type.affordances:
                    phantomForAff = phantom
            if phantomForAff != None:
                phantomForAff.SetOwnerProcess(excProcess)
                phantomForAff.affordance = wantedAff
    
    ## Propagate using of objects to SpaceMap.
    #
    # In future this will solve ObjectUsedUp scenario.                  
    def UseObjectPhantoms(self, excProcess):
        for phantom in excProcess.resources:
            if phantom.GetType() != "e":
                Global.Log("Programmer.Error: using memory phantom and memory object: " + phantom.ToString())
                continue
            self.spaceMap.ObjectUsed(phantom.object)
        
        map = Global.Map
        usedSources = [] #excProcess.process.usedSources Future: object.amount TBD.
        for usedSource in usedSources:
            for phantom in excProcess.resources:
                if usedSource == phantom.affordance:
                    if map.UseObject(excProcess, phantom.object):   #true means object is used Up
                        self.spaceMap.ObjectUsedUp(phantom.object)
                        self.environmentPhantoms.remove(phantom)
                        Global.Log("PF: removing(used) phantom for object " + phantom.object.ToString())
        #reset all phantoms used by that process - to avoid phantom.Error when object/phantom used second time
        #above is done more generally in ExcitedProcess.TerminateProcess
    
    ## Updates list of phantoms regarding new agent's location, only removes phantoms not present in agent's field of view.    
    def UpdatePhantomsBecauseOfMove(self, agent):
        map = Global.Map
        lostPhantoms = []
        for phantom in self.environmentPhantoms:
            if not map.IsObjectVisible(agent, phantom.object):
                lostPhantoms.append(phantom)
        for phantom in lostPhantoms:
            self.environmentPhantoms.remove(phantom)
            phantom.DeletedOrLost()
            Global.Log("PF: removing(lost) phantom for object " + phantom.object.ToString())
    
    ## Implements smart action "LookForObject". Simulates PF.NoticeObjects and propagates ObjectFound or ObjectNotFound to SpaceMap.
    def LookForObject(self, memoryPhantom):
        memObject = memoryPhantom.object
        map = Global.Map
        
        visibleObjects = map.GetVisibleObjects(self.agent)
        foundObj = None
        for obj in visibleObjects:
            if obj == memObject.object:
                foundObj = obj
                
        if foundObj == None:
            self.spaceMap.ObjectNotFound(memoryPhantom.object)
            self.memoryArea.RemovePhantom(memoryPhantom)
            memoryPhantom.MemoryObjectNotFound()
            return None
        #else: found:  
        phantom = self.GetPhantomForObj(foundObj)
        if phantom != None:
            phantom.Update(foundObj)
            phantom.memoryPhantom = memoryPhantom
            self.spaceMap.ObjectNoticedAgain(foundObj)
            Global.Log("PF: RE-adding phantom(lookFor) for object " + foundObj.ToString())
        else:
            phantom = Phantom(foundObj, memoryPhantom)
            self.environmentPhantoms.append(phantom)
            self.processArea.PhantomAddedForMemoryPhantom(phantom, memoryPhantom)
            self.spaceMap.ObjectFound(foundObj)
            Global.Log("PF: Adding phantom(lookFor) for object " + foundObj.ToString())
        return foundObj
        

