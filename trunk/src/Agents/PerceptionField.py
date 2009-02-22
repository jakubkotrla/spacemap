
import copy
from Enviroment.Global import Global
from PerceptionFilter import PerceptionFilter


class Phantom:
    def __init__(self, realObject, habituation, memoryPhantom=None):
        self.object      = realObject
        self.affordance  = None
        self.ownerProcess = None
        self.positionX   = realObject.x
        self.positionY   = realObject.y
        self.habituation = habituation
        self.memoryPhantom = memoryPhantom
        
    def Update(self, realObject, habituation):
        self.positionX   = realObject.x
        self.positionY   = realObject.y
        self.habituation = habituation
    
    def Habituate(self, amount):
        self.habituation -= amount
        return self.habituation < 1
        
    def SetOwnerProcess(self, process):
        if self.ownerProcess != None:
            Global.Log("EnviromentPhantom.Error:" + self.object.type.name)
        self.ownerProcess = process
        process.resources.append(self)
        
    def ResetOwnerProcess(self):
        if self.ownerProcess != None:
            self.ownerProcess.resources.remove(self)
        self.ownerProcess = None
        self.memoryPhantom = None
    
    def GetType(self):
        return "e"
     
    def ToString(self):
        if (self.ownerProcess != None):
            str = "Phantom(E) of " + self.object.ToString() + " linked to " + self.ownerProcess.process.name
        else:
            str = "Phantom(E) of " + self.object.ToString()
        return str


class PerceptionField:
    def __init__(self, processArea, spaceMap, memoryArea):
        self.environmentPhantoms = []
        self.processArea = processArea
        self.spaceMap = spaceMap
        self.memoryArea = memoryArea
        self.perceptionFilter = PerceptionFilter()

    def getPhantoms(self):
        phantoms = self.environmentPhantoms
        phantoms.sort(self.cmpHabituation)
        return phantoms[:Global.PFSize]
    def cmpHabituation(self, x, y):
        if x.habituation > y.habituation:
            return -1
        elif x.habituation == y.habituation:
            return 0
        else: # x<y
            return 1

    def Update(self, action):
        habituatedPhantoms = []
        for phantom in self.environmentPhantoms:
            if self.processArea.IsPhantomUsedNow(phantom): continue
            if phantom.Habituate(action.duration):
                habituatedPhantoms.append(phantom)
        for habituatedPhantom in habituatedPhantoms:
            self.environmentPhantoms.remove(habituatedPhantom)
            habituatedPhantom.ResetOwnerProcess()
            Global.Log("PF: removing(habituated) phantom for object " + habituatedPhantom.object.type.name + " at " + str(habituatedPhantom.object.y) + "," + str(habituatedPhantom.object.x))
                
    def NoticeObjects(self, visibleObjects, actProcess):
        self.perceptionFilter.ProcessObjects(visibleObjects, actProcess)
        phantomsToSpaceMap = {}
        for rObj in visibleObjects:
            if rObj.curAttractivity == 0: continue
            phantom = self.GetPhantomForObj(rObj)
            if phantom != None:
                phantom.Update(rObj, Global.PFPhantomHabituation)
                phantomsToSpaceMap[phantom] = "ObjectNoticedAgain"
            else:
                memPhantom = self.memoryArea.GetPhantomForObject(rObj)
                if memPhantom != None and self.processArea.LookingForPhantom(memPhantom):
                    phantom = Phantom(rObj, Global.PFPhantomHabituation, memPhantom)
                    self.environmentPhantoms.append(phantom)
                    self.processArea.PhantomAddedForMemoryPhantom(phantom, memPhantom) #link to possible processes may replace memoryPhantom
                    phantomsToSpaceMap[phantom] = "ObjectFound"
                    Global.Log("PF: Adding phantom for object " + rObj.ToString() + " instead of memoryPhantom " + memPhantom.ToString())
                else:
                    phantom = Phantom(rObj, Global.PFPhantomHabituation)
                    self.environmentPhantoms.append(phantom)
                    self.processArea.PhantomAdded(phantom)
                    phantomsToSpaceMap[phantom] = "ObjectNoticed"
                    Global.Log("PF: Adding phantom for object " + rObj.ToString())
        #phantoms updated, send to SpaceMap only those that fits in PF.Size
        realPhantoms = self.getPhantoms()
        for phantom in realPhantoms:
            if phantom not in phantomsToSpaceMap: continue
            if phantomsToSpaceMap[phantom] == "ObjectNoticedAgain":
                self.spaceMap.ObjectNoticedAgain(phantom.object)
            elif phantomsToSpaceMap[phantom] == "ObjectFound":
                self.spaceMap.ObjectFound(phantom.object)
            elif phantomsToSpaceMap[phantom] == "ObjectNoticed":
                self.spaceMap.ObjectNoticed(phantom.object)

    def GetPhantomForObj(self, rObj):
        for phantom in self.environmentPhantoms:
            if phantom.object == rObj:
                return phantom
        return None 
    
    def TryToLinkPhantomsFor(self, excProcess, missingSources):
        realPhantoms = self.getPhantoms()
        for wantedAff in missingSources:
            phantomForAff = None
            for phantom in realPhantoms:
                if wantedAff in phantom.object.type.affordances:
                    phantomForAff = phantom
            if phantomForAff != None:
                phantomForAff.SetOwnerProcess(excProcess)
                phantomForAff.affordance = wantedAff
                        
    def UseObjectPhantoms(self, excProcess):
        for phantom in excProcess.resources:
            self.spaceMap.ObjectUsed(phantom.object)
        
        map = Global.Map
        usedSources = excProcess.process.usedSources
        for usedSource in usedSources:
            for phantom in excProcess.resources:
                if usedSource == phantom.affordance:
                    rest = map.UseObject(excProcess, phantom.object)
                    if rest < 1:
                        self.spaceMap.ObjectUsedUp(phantom.object)
                        self.environmentPhantoms.remove(phantom)
                        Global.Log("PF: removing(used) phantom for object " + phantom.object.ToString())
        #reset all phantoms used by that process - to avoid phantom.Error when object/phantom used second time
        phantoms = copy.copy(excProcess.resources)
        for phantom in phantoms:
            #if phantom.GetType() == "m":
            #    self.memoryArea.RemovePhantom(phantom)    #ToDo - not ok, move to only when used
            #else:
            #   self.memoryArea.RemovePhantom(phantom.memoryPhantom)    #ToDo - not ok, move to only when used
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
            Global.Log("PF: removing(lost) phantom for object " + phantom.object.type.name + " at " + str(phantom.object.y) + "," + str(phantom.object.x))
    
    def LookForObject(self, memoryPhantom):
        memObject = memoryPhantom.object
        map = Global.Map
        rObj = map.GetRealObjectIfThere(memObject)

        if rObj != None:
            phantom = self.GetPhantomForObj(rObj)
            if phantom != None:
                phantom.Update(rObj, Global.PFPhantomHabituation)
                phantom.memoryPhantom = memoryPhantom
                self.spaceMap.ObjectNoticedAgain(rObj)
                Global.Log("PF: RE-adding phantom(lookFor) for object " + rObj.ToString())
            else:
                phantom = Phantom(rObj, Global.PFPhantomHabituation, memoryPhantom)
                self.environmentPhantoms.append(phantom)
                self.processArea.PhantomAddedForMemoryPhantom(phantom, memoryPhantom)
                self.spaceMap.ObjectFound(rObj)
                Global.Log("PF: Adding phantom(lookFor) for object " + rObj.ToString())
        else:
            self.spaceMap.ObjectNotFound(memoryPhantom.object)
            self.memoryArea.RemovePhantom(memoryPhantom)
        return rObj
    
          
        

