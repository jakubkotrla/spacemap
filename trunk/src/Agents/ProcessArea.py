## @package Agents.ProcessArea
# Contains ProcessArea handling and-or tree of ExcitedIntentions and ExcitedProcesses.
# Based on source from Tomas Korenko, changed.

from copy import copy
from Enviroment.Global import Global

## Represents active process in and-or tree.
class ExcitedProcess:
    def __init__(self, process, intention, parent):
        self.process             = process
        self.intention           = intention.intention
        self.excParentIntention  = intention
        ## Parent ExcitedProcess, skip link.
        self.parent              = parent
        self.completedIntentions = []  
        self.failedProcesses     = []
        self.startTime           = copy(Global.Time)
        self.endTime             = None
        self.resources           = []
        self.iteration           = 0       #not used yet
        self.location            = None    #not used yet
        self.successful          = False
        ## Additional data and pointers specific to different types of processes
        self.data                = {}   
     
    ## Terminates self, propagates success or failure to parent Excitedprocess.   
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
        #Future: won't work for intention-competition
    
    ## Returns list of Affordances.
    def GetAllSources(self):
        return self.process.sources
    
    ## Returns list of Affordances.
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

## Represents active intention in and-or tree.
class ExcitedIntention:
    def __init__(self, intention, parentExcProcess):
        self.intention = intention
        self.process   = None
        self.parentExcProcess = parentExcProcess
        self.data = {}
    
    def IsProcess(self): return False
    def ToString(self):
        return "I_" + self.intention.name

## Represents agent's process area.
class ProcessArea:
    def __init__(self, episodicMemory):
        self.episodicMemory = episodicMemory
        self.intentions      = {}
        self.processes       = {}
        self.actualIntention = None
        self.actualProcess   = None
        ## Active process just above intention I_Want in and-or tree.
        self.actualBasicProcess = None
        
    def HasNoIntention(self):
        return self.actualIntention == None    
    
    def GetActIntention(self):
        return self.actualIntention
    
    def GetActProcess(self):
        return self.actualProcess
    
    ## Sets given intention as active, creates ExcitedIntention.
    def ActivateIntention(self, intention, parentExcProcess):
        self.actualIntention = ExcitedIntention(intention, parentExcProcess)
        return self.actualIntention
    
    ## Sets given process as active, creates ExcitedProcess and inits it if is smart.
    def ActivateProcess(self, emotion, process, parentExcIntention, parent=None):
        self.actualProcess = ExcitedProcess(process, parentExcIntention, parent)
        self.episodicMemory.StoreProcess(self.actualProcess, emotion)
        
        if process.HasSources():
            self.actualBasicProcess = self.actualProcess
          
        #init of smart processes  
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
   
   
    ## Terminates atomic process.
    def TerminateAtomicProcess(self, emotion, successful=True):
        if self.actualProcess != None:
            self.actualProcess.TerminateProcess(successful)
            #commented in original: self.episodicMemory.StoreProcess(self.actualProcess, emotion)
            self.actualProcess = self.actualProcess.parent
   
    ## Terminates normal process, updates and-or tree: eventually terminates parent proces.
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

    ## Terminates actual intention as failure.
    def TerminateIntentionFalse(self, emotion):
        self.actualIntention = None
        self.TerminateProcess(emotion, False)
    
    ## Terminates actual intention I_Want.    
    def TerminateIntentionWant(self, emotion):
        self.actualIntention = self.actualProcess.excParentIntention
    
    ## Links given phantom to current process - when Agents notice objects via atomic action Explore.
    def PhantomAdded(self, phantom):
        realProcess = self.actualBasicProcess
        affs = phantom.object.type.affordances
        wantedAffs = realProcess.GetAllSources()
        for aff in affs:
            if aff in wantedAffs:
                phantom.SetOwnerProcess(realProcess)
                phantom.affordance = aff
    
    ## Returns True if agents is looking for given phantom. 
    def LookingForPhantom(self, memPhantom):
        p = self.actualProcess
        while p.process.name != "LookUpInMemory":
            p = p.parent
            if p == None: return False  #not looking for anything now
        return p.data["phantom"] == memPhantom
    
    ## Links given phantom instead of MemoryPhantom to current process - when Agents notice objects via LookForObject.
    def PhantomAddedForMemoryPhantom(self, phantom, memoryPhantom):
        phantom.affordance = memoryPhantom.affordance
        realProcess = self.actualBasicProcess
        if realProcess != memoryPhantom.ownerProcess:
            Global.Log("Programmer.Error: PA.PhantomAddedForMemoryPhantom relinking memPhantom for in-active process")
        phantom.ownerProcess = realProcess
        realProcess.resources.append(phantom)
        realProcess.resources.remove(memoryPhantom)
        
    ## Links given phantom to current process - when Agents remembers objects via Remember.
    def PhantomRemembered(self, phantom):
        affs = phantom.object.type.affordances
        realProcess = self.actualBasicProcess

        wantedAffs = realProcess.GetMissingSources()
        for aff in affs:
            if aff in wantedAffs:
                phantom.SetOwnerProcess(realProcess)
                phantom.affordance = aff
    
    ## Returns True if given phantom is used right now.        
    def IsPhantomUsedNow(self, phantom):
        realProcess = self.actualBasicProcess
        if self.actualProcess.process.name == "ExecuteReal":
            return phantom.ownerProcess == realProcess
        return False
   
    ## Returns state of ProcessArea - and-or tree - as lists of strings. 
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
    
   
