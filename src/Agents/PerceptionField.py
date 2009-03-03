
import copy
from Enviroment.Global import Global
from PerceptionFilter import PerceptionFilter


class Phantom:
    def __init__(self, rObject, memoryPhantom=None):
        self.object      = rObject
        self.affordance  = None
        self.ownerProcess = None
        habEffect = rObject.curAttractivity * rObject.visibility
        self.habituation = Global.PFPhantomHabCreate * habEffect
        self.memoryPhantom = memoryPhantom
        
    def Update(self, rObject):
        hab = Global.PFPhantomHabUpdate * rObject.curAttractivity * rObject.visibility
        self.habituation += hab
    
    def Habituate(self, amount):
        self.habituation -= amount
        return self.habituation < 1
        
    def SetOwnerProcess(self, process):
        if self.ownerProcess != None:
            Global.Log("Programmer.Error: Phantom with owner process set again: " + self.object.ToString())
        self.ownerProcess = process
        process.resources.append(self)
        
    def ResetOwnerProcess(self):
        if self.ownerProcess != None:
            self.ownerProcess.resources.remove(self)
        self.ownerProcess = None
        if self.memoryPhantom != None:
            self.memoryPhantom.UnlinkFromOwnerProcess()
            self.memoryPhantom = None
    
    def GetType(self):
        return "e"
     
    def ToString(self):
        if (self.ownerProcess != None):
            s = "Phantom(E," + str(self.habituation) + ") of " + self.object.ToString() + " linked to " + self.ownerProcess.process.name
        else:
            s = "Phantom(E," + str(self.habituation) + ") of " + self.object.ToString()
        return s


class PerceptionField:
    def __init__(self, processArea, spaceMap, memoryArea):
        self.environmentPhantoms = []
        self.processArea = processArea
        self.spaceMap = spaceMap
        self.memoryArea = memoryArea
        self.perceptionFilter = PerceptionFilter()

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
                    self.processArea.PhantomAddedForMemoryPhantom(phantom, memPhantom)
                    phantomsToSpaceMap[phantom] = "ObjectFound"
                    Global.Log("PF: Adding phantom for object " + rObj.ToString() + " instead of " + memPhantom.ToString())
                else:
                    phantom = Phantom(rObj)
                    self.environmentPhantoms.append(phantom)
                    self.processArea.PhantomAdded(phantom)
                    phantomsToSpaceMap[phantom] = "ObjectNoticed"
                    Global.Log("PF: Adding phantom for object " + rObj.ToString())
        #phantoms updated, truncate to PF.Size
        phantoms = self.environmentPhantoms
        phantoms.sort(lambda b,a: cmp(a.habituation,b.habituation))
        phantomsToDelete = phantoms[Global.PFSize:]
        for phantomToDelete in phantomsToDelete:
            self.environmentPhantoms.remove(phantomToDelete)
            phantomToDelete.ResetOwnerProcess()
            Global.Log("PF: removing(over PF.size) phantom for object " + phantomToDelete.object.ToString())
        
        for phantom in self.environmentPhantoms:
            if phantom not in phantomsToSpaceMap:
                #happens when agent changes viewCones and object is not in normal VCs (was added by explore VCs)
                continue
            if phantomsToSpaceMap[phantom] == "ObjectNoticedAgain":
                self.spaceMap.ObjectNoticedAgain(phantom.object)
            elif phantomsToSpaceMap[phantom] == "ObjectFound":
                self.spaceMap.ObjectFound(phantom.object)
            elif phantomsToSpaceMap[phantom] == "ObjectNoticed":
                self.spaceMap.ObjectNoticed(phantom.object)

    def Update(self, action):
        habituatedPhantoms = []
        for phantom in self.environmentPhantoms:
            if self.processArea.IsPhantomUsedNow(phantom): continue
            if phantom.Habituate(action.duration):
                habituatedPhantoms.append(phantom)
        for habituatedPhantom in habituatedPhantoms:
            self.environmentPhantoms.remove(habituatedPhantom)
            habituatedPhantom.ResetOwnerProcess()
            Global.Log("PF: removing(habituated) phantom for object " + habituatedPhantom.object.ToString())

    def GetPhantomForObj(self, rObj):
        for phantom in self.environmentPhantoms:
            if phantom.object == rObj:
                return phantom
        return None 
    
    def TryToLinkPhantomsFor(self, excProcess, missingSources):
        for wantedAff in missingSources:
            phantomForAff = None
            for phantom in self.environmentPhantoms:
                if wantedAff in phantom.object.type.affordances:
                    phantomForAff = phantom
            if phantomForAff != None:
                phantomForAff.SetOwnerProcess(excProcess)
                phantomForAff.affordance = wantedAff
                        
    def UseObjectPhantoms(self, excProcess):
        for phantom in excProcess.resources:
            self.spaceMap.ObjectUsed(phantom.object)
        
        map = Global.Map
        usedSources = [] #excProcess.process.usedSources ToDo: object.amount/dynamic world
        for usedSource in usedSources:
            for phantom in excProcess.resources:
                if usedSource == phantom.affordance:
                    if map.UseObject(excProcess, phantom.object):   #true means object is used Up
                        self.spaceMap.ObjectUsedUp(phantom.object)
                        self.environmentPhantoms.remove(phantom)
                        Global.Log("PF: removing(used) phantom for object " + phantom.object.ToString())
        #reset all phantoms used by that process - to avoid phantom.Error when object/phantom used second time
        phantoms = copy.copy(excProcess.resources)
        for phantom in phantoms:
            phantom.ResetOwnerProcess()
        
    def UpdatePhantomsBecauseOfMove(self, agent):
        map = Global.Map
        lostPhantoms = []
        for phantom in self.environmentPhantoms:
            if not map.IsObjectVisible(agent, phantom.object):
                lostPhantoms.append(phantom)
        for phantom in lostPhantoms:
            self.environmentPhantoms.remove(phantom)
            phantom.ResetOwnerProcess()
            Global.Log("PF: removing(lost) phantom for object " + phantom.object.ToString())
    
    def LookForObject(self, memoryPhantom):
        memObject = memoryPhantom.object
        map = Global.Map
        rObj = map.GetRealObjectIfThere(memObject)

        if rObj != None:
            phantom = self.GetPhantomForObj(rObj)
            if phantom != None:
                phantom.Update(rObj)
                phantom.memoryPhantom = memoryPhantom
                self.spaceMap.ObjectNoticedAgain(rObj)
                Global.Log("PF: RE-adding phantom(lookFor) for object " + rObj.ToString())
            else:
                phantom = Phantom(rObj, memoryPhantom)
                self.environmentPhantoms.append(phantom)
                self.processArea.PhantomAddedForMemoryPhantom(phantom, memoryPhantom)
                self.spaceMap.ObjectFound(rObj)
                Global.Log("PF: Adding phantom(lookFor) for object " + rObj.ToString())
        else:
            self.spaceMap.ObjectNotFound(memoryPhantom.object)
            self.memoryArea.RemovePhantom(memoryPhantom)
            memoryPhantom.ResetOwnerProcess()
        return rObj
    
          
        

