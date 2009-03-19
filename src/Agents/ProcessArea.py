# -*- coding: UTF-8 -*-

from copy import copy
from Enviroment.Global import Global

## Trieda reprezentujúca aktivovaný proces
# - Atribúty triedy:
#   - process ... pointer na proces
#   - parent ... pointer na rodičovský aktivovaný proces
#   - startTime ... čas začiatku vykonávania procesu
#   - endTime ... čas ukončenia vykonávania procesu
#   - resources ... zoznam objektov použitých pri vykonávaní procesu
#   - iteration ... počet opakovaní procesu za sebou
#   - location ... lokácia v ktorej bol proces vykonaný
#   - successful ... úspešnosť vykonania procesu
#   - hierarchyLevel ... úroveň procesu v hierarchhickom strome procesov
#   - timeLimit ... maximálny čas na vykonanie procesu     
#   - data ... slovník ďalších dát procesu     
class ExcitedProcess:
    ## Inicializácia inštancie triedy
    # @param self pointer na aktivovaný proces
    # @param process pointer na proces
    def __init__(self, process, intention, parent):
        self.process             = process
        self.intention           = intention.intention
        self.excParentIntention  = intention
        self.parent              = parent
        self.completedIntentions = []  
        self.failedProcesses     = []
        self.startTime           = copy(Global.Time)
        self.endTime             = None
        self.resources           = []
        self.iteration           = 0
        self.location            = None
        self.successful          = False
        self.hierarchyLevel      = 0
        self.timeLimit           = 0 
        self.data                = {}
        
    def TerminateProcess(self, successful=True):
        self.endTime    = copy(Global.Time)
        self.successful = successful
        if self.parent != None:
            if self.successful:
                self.parent.completedIntentions.append(self.intention)
            else:
                self.parent.failedProcesses.append(self.process)
        for phantom in self.resources:
            phantom.OwnerProcessTerminated()
            
    def IsProcess(self): return True            
    def IsSmartProcess(self):
        if (self.process.name == "SearchRandom"):
            return True
        if (self.process.name == "LookUpInMemory"):
            return True
        if (self.process.name == "MoveTo"):
            return True
        if (self.process.name == "Execute"):
            return True
        return False    
    
    def IsInProgress(self):
        return self.endTime == None
        #Future: won't work for intention-competing
    
    def GetAllSources(self):
        return self.process.sources
        
    def GetMissingSources(self):
        affordances = copy(self.process.sources)
        for objectPhantom in self.resources:
            if objectPhantom.GetType() != "e": continue
            
            for affordance in objectPhantom.object.type.affordances:
                if affordance in affordances:
                    affordances.remove(affordance)
        return affordances
    
    def ToString(self):
        return "P_" + self.process.name

## Trieda reprezentujúca aktivovaný zámer
# - Atribúty triedy:
#   - intention ... pointer na zámer
#   - process ... pointer na aktivovaný proces spĺňajúci zámer
#   - activity ... aktuálna aktivita zámeru          
class ExcitedIntention:
    ## Inicializácia inštancie triedy
    # @param self pointer na aktivovaný zámer
    # @param intention pointer na zámer
    def __init__(self, intention, parentExcProcess):
        self.intention = intention
        self.process   = None
        self.parentExcProcess = parentExcProcess
        self.data = {}
        self.activity  = 0
    
    def IsProcess(self): return False
    def ToString(self):
        return "I_" + self.intention.name
          
class ProcessArea:
    def __init__(self, episodicMemory):
        self.episodicMemory = episodicMemory
        self.intentions      = {}
        self.processes       = {}
        self.actualIntention = None
        self.actualProcess   = None
        self.actualBasicProcess = None
        
    def HasNoIntention(self):
        return self.actualIntention == None    
    
    def GetActIntention(self):
        return self.actualIntention
    
    def GetActProcess(self):
        return self.actualProcess
    
    def ActivateIntention(self, excitedIntention, parentExcProcess):
        self.actualIntention = ExcitedIntention(excitedIntention, parentExcProcess)
        return self.actualIntention
    
    def ActivateProcess(self, emotion, process, parentExcIntention, parent=None):
        self.actualProcess = ExcitedProcess(process, parentExcIntention, parent)
        self.episodicMemory.StoreProcess(self.actualProcess, emotion)
        
        if process.HasSources():
            self.actualBasicProcess = self.actualProcess
            
        if process.name == "SearchRandom":
            self.actualProcess.data["step"] = "MoveTo"
            self.actualProcess.data["waypoints"] = None
            self.actualProcess.data["affordance"] = parentExcIntention.data["affordance"]
        elif process.name == "LookUpInMemory":
            self.actualProcess.data["step"] = "Remember"
            self.actualProcess.data["affordance"] = parentExcIntention.data["affordance"]
        elif process.name == "MoveTo":
            self.actualProcess.data["path"] = None
        
        return self.actualProcess
   
   
    #only for terminating atomic processes
    def TerminateAtomicProcess(self, emotion, successful=True):
        if self.actualProcess != None:
            self.actualProcess.TerminateProcess(successful)
            #commented in original: self.episodicMemory.StoreProcess(self.actualProcess, emotion)
            self.actualProcess = self.actualProcess.parent
   
    def TerminateProcess(self, emotion, successful=True):
        if self.actualProcess == None:
            self.actualIntention = None #there is no process left - HL intention finnished
            return
        
        self.actualProcess.TerminateProcess(successful)
        #commented in original: self.episodicMemory.StoreProcess(self.actualProcess, emotion)
        
        if not successful:
            # actual process went wrong, next step AS will select another in parent intention
            self.actualProcess = self.actualProcess.parent
        else:
            # actual process finnished, parent intention as well
            self.actualProcess = self.actualProcess.parent
                
            if self.actualProcess != None:
                notFinishedIntentions = Global.SetDifference(self.actualProcess.process.intentions, self.actualProcess.completedIntentions) 
                if len(notFinishedIntentions) == 0:
                    self.TerminateProcess(True)
                else:
                    # this would be otherwise called in AS next step via AS.ChooseProcessForIntention but randomly 
                    self.ActivateIntention(notFinishedIntentions[0], self.actualProcess)
            else:
                #there is no process left - HL intention finnished
                self.actualIntention = None

    
    def TerminateIntentionFalse(self, emotion):
        self.actualIntention = None
        self.TerminateProcess(emotion, False)
        
    def TerminateIntentionWant(self, emotion):
        self.actualIntention = self.actualProcess.excParentIntention
    
    #links given phantom to current process - when Agents notice objects via explore
    def PhantomAdded(self, phantom):
        realProcess = self.actualBasicProcess
        affs = phantom.object.type.affordances
        wantedAffs = realProcess.GetAllSources()
        for aff in affs:
            if aff in wantedAffs:
                phantom.SetOwnerProcess(realProcess)
                phantom.affordance = aff
    
    def LookingForPhantom(self, memPhantom):
        p = self.actualProcess
        while p.process.name != "LookUpInMemory":
            p = p.parent
            if p == None: return False  #not looking for anything now
        return p.data["phantom"] == memPhantom
    
    #links given phantom instead of MemoryPhantom to current process - when Agents notice objects via LookForObject
    def PhantomAddedForMemoryPhantom(self, phantom, memoryPhantom):
        phantom.affordance = memoryPhantom.affordance
        realProcess = self.actualBasicProcess
        if realProcess != memoryPhantom.ownerProcess:
            Global.Log("Programmer.Error: PA.PhantomAddedForMemoryPhantom relinking memPhantom for in-active process")
        phantom.ownerProcess = realProcess
        realProcess.resources.append(phantom)
        realProcess.resources.remove(memoryPhantom)
        
    #links given phantom to current process - when Agents remembers objects via Remember
    def PhantomRemembered(self, phantom):
        affs = phantom.object.type.affordances
        realProcess = self.actualBasicProcess

        wantedAffs = realProcess.GetMissingSources()
        for aff in affs:
            if aff in wantedAffs:
                phantom.SetOwnerProcess(realProcess)
                phantom.affordance = aff
            
    def IsPhantomUsedNow(self, phantom):
        realProcess = self.actualBasicProcess
        if self.actualProcess.process.name == "ExecuteReal":
            return phantom.ownerProcess == realProcess
        return False
   
    def GetText(self):
        txt = []
        act = self.actualProcess
        if act == None: return []
        txt.insert(0, "  " + act.ToString())
        while True:
            if (act.IsProcess()):
                if (act.parent != None and act.parent.IsSmartProcess()) or act.process.name == "Execute":
                    act = act.parent
                else:
                    act = act.excParentIntention
            else:
                act = act.parentExcProcess
            if act == None: break            
            txt.insert(0, "  " + act.ToString() )
        return txt 
    
   
