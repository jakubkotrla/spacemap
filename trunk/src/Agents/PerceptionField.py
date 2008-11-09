# -*- coding: UTF-8 -*-
from random import *
import copy
from Enviroment.Global import Global
#from PerceptionFilter import PerceptionFilter


class Phantom:
    def __init__(self, realObject, habituation):
        self.object      = realObject
        self.affordance  = None     #which object affordance will be used - to speed up things
        self.ownerProcess  = None
        self.positionX   = realObject.x
        self.positionY   = realObject.y
        self.habituation = habituation
        self.memoryPhantom = None
        
    def Update(self, realObject, habituation):
        self.positionX   = realObject.x
        self.positionY   = realObject.y
        self.habituation = habituation
    
    def Habituate(self):
        self.habituation -= 1
        return self.habituation < 1
        
    def SetOwnerProcess(self, process):
        if self.ownerProcess != None:
            Global.Log("PocketPhantom.Error:" + self.object.type.name)
        self.ownerProcess = process
        process.resources.append(self)
        
    def ResetOwnerProcess(self):
        if self.ownerProcess != None:
            self.ownerProcess.resources.remove(self)
        self.ownerProcess = None
        
    def ToString(self):
        if (self.ownerProcess != None):
            str = "Phantom(E) of " + self.object.ToString() + " linked to " + self.ownerProcess.process.name
        else:
            str = "Phantom(E) of " + self.object.ToString()
        return str
        
class PocketPhantom:
    def __init__(self, objectPlacement):
        self.object        = objectPlacement.object
        self.oldLocation   = objectPlacement.location
        self.oldPositionX  = objectPlacement.positionX
        self.oldPpositionY = objectPlacement.positionY
        self.ownerProcess  = None
    
    def SetOwnerProcess(self, process):
        if self.ownerProcess != None:
            Global.Log("PocketPhantom.Error")
        self.ownerProcess = process
        process.resources.append(self)
        
    def ResetOwnerProcess(self, process):
        self.ownerProcess = None
        process.resources.remove(self)

## Trieda reprezentujúca percepčné pole krátkodobej pamäte
# - Atribúty triedy:
#   - perceptionFilter ... percepčný filter
#   - phantoms ... slovník fantómov v percepčnom poli
#   - perceptionFieldSize ... maximálny počet fantómov v percepčnom poli
#   - perceptionHabituationTime ... čas za ktorý agent zabudne na objekt
class PerceptionField:

    def __init__(self, processesArea, spaceMap):
#        self.perceptionFilter = PerceptionFilter()
        self.environmentPhantoms = {}
        self.pocketPhantoms = {}
        self.perceptionFieldSize = 50
        self.perceptionHabituationTime = 10
        self.processesArea = processesArea
        self.spaceMap = spaceMap

    ## Funkcia ktorá pridá fantóm objektu do percepčného poľa
    # @param self pointer na percepčné pole
    # @param phantom pointer na fantóm
    # @return vráti False ak sa objekt v percepčnom poli už nachádzal
    def Update(self, realObjects):
        # postupne zabúdame na objekty v percepčnom poli
        habituatedPhantoms = []
        for phantom in self.environmentPhantoms.items():
            if phantom[1].Habituate():
                habituatedPhantoms.append(phantom[0])
        # odstránime zabudnuté objekty z percepčného poľa
        for habituatedPhantom in habituatedPhantoms:
            del self.environmentPhantoms[habituatedPhantom]
        # pridáme spozorované objekty do percepčného poľa
        for rObj in realObjects:
            if rObj in self.environmentPhantoms.keys():
                self.environmentPhantoms[rObj].Update(rObj, self.perceptionHabituationTime)
            else:
                self.environmentPhantoms[rObj] = Phantom(rObj, self.perceptionHabituationTime)
                #link to possible processes
                self.processesArea.PhantomAdded(self.environmentPhantoms[rObj])
                self.spaceMap.ObjectNoticed(rObj)
                Global.Log("PF: Adding phantom for object " + rObj.type.name + " at " + str(rObj.y) + "," + str(rObj.x))
                
        # vyhodíme najstaršie objekty do maximálnej veľkosti percepčného poľa
        if len(self.environmentPhantoms) > self.perceptionFieldSize:
            habituatedObjects = {}
            for object, phantom in self.environmentPhantoms.items():
                if phantom.habituation not in habituatedObjects.keys():
                    habituatedObjects[phantom.habituation] = []
                habituatedObjects[phantom.habituation].append(object)
            forgetCnt = len(self.environmentPhantoms) - self.perceptionFieldSize
            i = 1
            while forgetCnt > 0:
                if i in habituatedObjects.keys():
                    if len(habituatedObjects[i]) > forgetCnt:
                        for object in sample(habituatedObjects[i], forgetCnt):
                            del self.environmentPhantoms[object]
                        forgetCnt = 0
                    else:
                        forgetCnt -= len(habituatedObjects[i])
                        for object in habituatedObjects[i]:
                            del self.environmentPhantoms[object]
                i += 1
                
    def NoticeObjects(self, visibleObjects):
        #perceptivity = max(min(1.3*self.perceptionFieldSize/(len(visibleObjects)+len(self.environmentPhantoms)+1),1),0.5)
        #self.Update(self.perceptionFilter.FilterObjects(visibleObjects, perceptivity))
        self.Update(visibleObjects)
    
    def TryToLinkPhantomsFor(self, excProcess, missingSources):
        for wantedAff in missingSources:
            phantom = self.GetPhantomOfSeenAffordance(wantedAff)
            if phantom != None:
                phantom.SetOwnerProcess(excProcess)
                phantom.affordance = wantedAff
                        
    def GetPhantomOfSeenAffordance(self, affordance):
        for objectPhantom in self.environmentPhantoms.values():
            if affordance in objectPhantom.object.type.affordances:
                return objectPhantom
        return None
    
    def UseObjectPhantoms(self, excProcess):
        for phantom in excProcess.resources:
            self.spaceMap.ObjectUsed(phantom.object)
        
        map = Global.Map
        usedSources = excProcess.process.usedSources
        for usedSource in usedSources:
            for phantom in excProcess.resources:
                if usedSource == phantom.affordance:
                    map.UseObject(excProcess, phantom.object)
                    self.spaceMap.ObjectUsedUp(phantom.object)
                    del self.environmentPhantoms[phantom.object]
                    Global.Log("PF: removing(used) phantom for object " + phantom.object.type.name + " at " + str(phantom.object.y) + "," + str(phantom.object.x))
        #reset all phantoms used by that process - to avoid phantom.Error when object/phantom used second time
        phantoms = copy.copy(excProcess.resources)
        for phantom in phantoms:
            phantom.ResetOwnerProcess()
        
    def UpdatePhantomsBecauseOfMove(self, agent):
        map = Global.Map
        lostPhantoms = []
        for phantom in self.environmentPhantoms.values():
            if not map.IsObjectVisibleFrom(phantom.object, agent.x, agent.y):
                lostPhantoms.append(phantom)
        for phantom in lostPhantoms:
            del self.environmentPhantoms[phantom.object]
            phantom.ResetOwnerProcess()
            Global.Log("PF: removing(lost) phantom for object " + phantom.object.type.name + " at " + str(phantom.object.y) + "," + str(phantom.object.x))
    
    def LookForObject(self, memoryPhantom):
        memObject = memoryPhantom.object
        map = Global.Map
        rObj = map.GetRealObjectIfThere(memObject)
        
        #ToDo - memory movePhantom to RealPhantom - in a smart way!
        
        if rObj != None:
            self.NoticeObjects([rObj])
            self.spaceMap.ObjectFound(memoryPhantom.object)
        else:
            self.spaceMap.ObjectNotFound(memoryPhantom.object)
        return rObj
    
    
    def Show(self, txt):
        txt.delete(0, txt.size())
        for  phantom in self.environmentPhantoms:
            txt.insert("end", phantom.ToString())
        
    #old!
                 
    def SeeAffordance(self, affordance):
        for objectPhantom in self.environmentPhantoms.values():
            if affordance in objectPhantom.object.type.affordances:
                return True
        return False
    
    
    def HaveAffordance(self, affordance):
        for objectPhantom in self.pocketPhantoms.values():
            if affordance in objectPhantom.object.my_type.affordances:
                return True
        return False

        
    def GetPocketObject(self, affordance, process):
        for objectPhantom in self.pocketPhantoms.values():
            if objectPhantom.ownerProcess == None:
                if affordance in objectPhantom.object.my_type.affordances:
                    objectPhantom.SetOwnerProcess(process)
    
    ## Funkcia ktorá vráti objekt v percepčného poli s danou afordanciou
    # @param self pointer na percepčné pole
    # @param affordance hľadaná afordancia
    # @return objekt s danou afordanciou            
    def GetEnvironmentObject(self, affordance):
        for objectPhantom in self.environmentPhantoms.values():
            if affordance in objectPhantom.object.my_type.affordances:
                return objectPhantom

    # pickups object to pocket - PF will be aware of it via its pocetPhantoms
    # link to process which needs it for required affordance          
    def PickUpObject(self, rObject, process, affordance):
        Global.Log("PF.PickUpObject")
        ppo = PocketPhantom(rObject)
        self.pocketPhantoms[rObject] = ppo
        for aff in rObject.type.affordances:
            if aff == affordance: 
                ppo.SetOwnerProcess(process)
        
    def PlaceObject(self, objectPlacement):
        Global.Log("PF.PlaceObject")
        del self.pocketPhantoms[objectPlacement.object]
