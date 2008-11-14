# -*- coding: UTF-8 -*-

from Intentions         import Intentions, Intention
from Enviroment.Affordances import *
from Processes          import Processes, Process
from Scenarios          import Scenarios, Scenario
from Enviroment.Global import Global
from sets               import *
import random


## Trieda reprezentujúca selektor zámerov
# - Atribúty triedy:
#   - agent ... pointer na agenta    
#   - intentions ... zámery agenta
#   - processes ... procesy ktoré môže agent vykonávať
#   - scenarios ... scenáre pre výber zámerov
#   - actualScenario ... aktuálne vykonávaný scenár
#   - shortTermMemory ... pointer na krátkodobú pamäť
class ActionSelector:
    ## Inicializácia inštancie triedy
    # @param self pointer na selektor zámerov
    # @param intentionsFile súbor so zámermi a procesmi agenta
    # @param shortTermMemory pointer na krátkodobú pamäť 
    def __init__(self, agent, intentionsFile, processesArea, perceptionField, episodicMemory, spaceMap):
        self.agent           = agent
        self.intentions      = Intentions()
        self.processes       = Processes()
        self.scenarios       = Scenarios()
        self.processesArea   = processesArea
        self.perceptionField = perceptionField
        self.episodicMemory  = episodicMemory
        self.spaceMap        = spaceMap
        
        f = open(intentionsFile,'r')
        a = f.read()
        exec(a)
        
        self.intentions.wantInt = Intention("Want", [self.processes.atomic["Explore"],
                                                     self.processes.atomic["LookUpInMemory"],
                                                     self.processes.atomic["SearchRandom"]])
        
    
    def GetAction(self, emotion):
        if self.processesArea.HasNoIntention():
            self.ChooseIntention()
        #agent has intention (in self.PA.actInt)
        excIntention = self.processesArea.GetActIntention()
        excProcess = self.processesArea.GetActProcess()
        
        #what is active - I or P ?
        if excIntention.parentExcProcess == excProcess:
            #if I under P -> we have active I and need some process to do it  (or this is HL intention)
            process = self.ChooseProcessForIntention(emotion, excIntention.intention, excIntention.parentExcProcess)
            if process == None:
                self.processesArea.TerminateIntentionFalse(emotion)
                #impossible to finnish this intention -> terminate int and parent process, try to choose another process in parent intention
                return self.GetAction(emotion)
            excProcess = self.processesArea.ActivateProcess(emotion, process, excIntention, excIntention.parentExcProcess)
        else:
            #if P under I -> we have already selected process for this intention previously, go on
            process = excProcess.process         
        
        #now we have intention and under it process to do
        
        #process atomic?
        if process.intentions != []:
            #process is not atomic -> choose first not completed sub-intention
            intention = SetFirstDifference(process.intentions, excProcess.completedIntentions)
            self.processesArea.ActivateIntention(intention, excProcess)
            return self.GetAction(emotion)    #go deeper for atomic process
        else:
            # proces is atomic
            return self.GetAtomicAction(emotion, excProcess)


    def ChooseProcessForIntention(self, emotion, intention, parentProcess):
        processes = intention.processes
        if parentProcess != None:
            processes = SetDifference(processes, parentProcess.failedProcesses)
            
        if len(processes) == 0:
            return None
        if intention.name == "Want":    #for Want intention the order of process matters
            return processes[0]
        else:
            return processes[random.randint(0,len(processes)-1)]



    def GetAtomicAction(self, emotion, excProcess):
        #if excProcess is already atomic (because of Want/SearchRandom/..more.. intention), just return it
        if excProcess.IsSmartProcess():
            return self.GetAtomicActionforSmartProcess(emotion, excProcess)
        
        #ok, normal way
        missingSources = excProcess.GetMissingSources()

        if len(missingSources) > 0:
            #try to use something already seen
            self.perceptionField.TryToLinkPhantomsFor(excProcess, missingSources)
            #still missing?
            missingSources = excProcess.GetMissingSources()
            if len(missingSources) > 0:            
                #actually add intention Want(Aff) and immediately start with process Explore
                excWantInt = self.processesArea.ActivateIntention(self.intentions.wantInt, excProcess)
                excWantInt.data["affordance"] = missingSources[0] 
                
                atomicProcess = self.processesArea.ActivateProcess(emotion, self.processes.atomic["Explore"], excWantInt, excProcess)
                atomicProcess.data["parent"] = "intention"
                atomicProcess.data["process"] = excProcess
                atomicProcess.data["affordance"] = missingSources[0]
            else:
                #we have everything
                atomicProcess = self.processesArea.ActivateProcess(emotion, self.processes.atomic["Execute"], excProcess.excParentIntention, excProcess)
                atomicProcess.data["process"] = excProcess.process
                atomicProcess.data["execution-time"] = excProcess.process.durationTime
        else:
            #we have everything
            atomicProcess = self.processesArea.ActivateProcess(emotion, self.processes.atomic["Execute"], excProcess.excParentIntention, excProcess)
            atomicProcess.data["process"] = excProcess.process
            atomicProcess.data["execution-time"] = excProcess.process.durationTime
        return atomicProcess


    def GetAtomicActionforSmartProcess(self, emotion, excProcess):
        if (excProcess.process.name == "SearchRandom"):

            if (excProcess.data["step"] == "MoveTo"):
                excProcess.data["tries"] = excProcess.data["tries"] - 1
                if excProcess.data["tries"] < 1:
                    self.processesArea.TerminateProcess(emotion, False)
                    return self.GetAction(emotion)
                excProcess.data["step"] = "Explore"
                
                map = Global.Map
                canMove = False
                while not canMove:
                    newX = random.randint(-20, 20) + self.agent.x
                    newY = random.randint(-20, 20) + self.agent.y
                    canMove = map.CanMoveAgent(self.agent, newX, newY)
                
                atomicProcess = self.processesArea.ActivateProcess(emotion, self.processes.atomic["MoveTo"], excProcess.excParentIntention, excProcess)
                atomicProcess.data["process"] = excProcess.process
                atomicProcess.data["newx"] = newX
                atomicProcess.data["newy"] = newY
                return atomicProcess                                
                
            elif (excProcess.data["step"] == "Explore"):
                excProcess.data["step"] = "MoveTo"
                atomicProcess = self.processesArea.ActivateProcess(emotion, self.processes.atomic["Explore"], excProcess.excParentIntention, excProcess)
                atomicProcess.data["parent"] = "process"
                atomicProcess.data["process"] = excProcess.excParentIntention.parentExcProcess
                atomicProcess.data["affordance"] = excProcess.data["affordance"]
                return atomicProcess
            
        elif (excProcess.process.name == "LookUpInMemory"):
            
            if (excProcess.data["step"] == "Remember"):
                excProcess.data["step"] = "MoveTo"
                atomicProcess = self.processesArea.ActivateProcess(emotion, self.processes.atomic["Remember"], excProcess.excParentIntention, excProcess)
                atomicProcess.data["process"] = excProcess.process
                atomicProcess.data["affordance"] = excProcess.data["affordance"]
                return atomicProcess
            
            elif (excProcess.data["step"] == "MoveTo"):
                excProcess.data["step"] = "LookForObject"
                atomicProcess = self.processesArea.ActivateProcess(emotion, self.processes.atomic["MoveTo"], excProcess.excParentIntention, excProcess)
                atomicProcess.data["process"] = excProcess.process
                atomicProcess.data["newx"] = excProcess.data["phantom"].object.x
                atomicProcess.data["newy"] = excProcess.data["phantom"].object.y
                return atomicProcess
            
            elif (excProcess.data["step"] == "LookForObject"):
                atomicProcess = self.processesArea.ActivateProcess(emotion, self.processes.atomic["LookForObject"], excProcess.excParentIntention, excProcess)
                atomicProcess.data["process"] = excProcess.process
                atomicProcess.data["affordance"] = excProcess.data["affordance"]
                atomicProcess.data["phantom"] = excProcess.data["phantom"]
                return atomicProcess    
            
            return None        
        else:
            return excProcess

    
    def ChooseIntention(self):
        mostActiveIntention = self.scenarios.GetMostActiveIntention()
        if mostActiveIntention == None:
            mostActiveIntention = self.intentions.GetRandomHighLevelIntention()
        self.processesArea.ActivateIntention(mostActiveIntention, None) 
        
        
    def ActionDone(self, emotion):
        actExcProcess = self.processesArea.GetActProcess()
        actProcess = actExcProcess.process
        if actProcess.name == "Execute":
            self.processesArea.TerminateAtomicProcess(emotion)   #terminates Execute
            self.processesArea.TerminateProcess(emotion)         #terminates the executed process
                                            #chooses another intention or no intention will be actual
        elif actProcess.name == "MoveTo":
            #nothing smart to do here except of terminating atomic Moveto
            self.processesArea.TerminateAtomicProcess(emotion)   #terminates Execute
            
        elif actProcess.name == "SearchRandom":
            # check we got it.. - is done in child LookForObject process!
            # this actually never called - its either MoveTo or Explore child process!
            pass
            
        elif actProcess.name == "LookUpInMemory":
            # check we got it.. - is done in child Explore process!
            # this actually never called - its either Remember, MoveTo or LookForObject child process!
            pass
         
        elif actProcess.name == "Remember":
            if actExcProcess.data["phantom"] != None:
                #success, terminates, next step AS will go for MoveTo
                actExcProcess.parent.data["phantom"] = actExcProcess.data["phantom"]
                self.processesArea.TerminateAtomicProcess(emotion)
            else:
                # whole LookUpInMemory failed - terminate Remember and LookUpInMemory
                # ToDo - now try different location
                self.processesArea.TerminateAtomicProcess(emotion, False)
                self.processesArea.TerminateProcess(emotion, False)
            
        elif actProcess.name == "LookForObject":
            if actExcProcess.data["object"] != None:
                #success, whole LookUpInMemory is done - terminate LookForObject, LookUpInMemory, I_Want
                self.processesArea.TerminateAtomicProcess(emotion, True)
                self.processesArea.TerminateAtomicProcess(emotion, True)
                self.processesArea.TerminateIntentionWant(emotion)
            else:
                # whole LookUpInMemory failed - terminate LookForObject and LookUpInMemory
                # ToDo - now try different location
                self.processesArea.TerminateAtomicProcess(emotion, False)
                self.processesArea.TerminateProcess(emotion, False)
            
        elif actProcess.name == "Explore":
            #check if we got required affordance
            excProcess = actExcProcess.data["process"]
            wantedAff = actExcProcess.data["affordance"]
            missingSources = excProcess.GetMissingSources()
            if wantedAff in missingSources:
                #still we do not have it - fail
                if (actExcProcess.data["parent"] == "process"):
                    #we have to terminate only Explore, no SearchRandom
                    self.processesArea.TerminateAtomicProcess(emotion, False)
                else:
                    self.processesArea.TerminateProcess(emotion, False)
            else:
                #we got it - success
                self.processesArea.TerminateAtomicProcess(emotion, True)
                if (actExcProcess.data["parent"] == "process"):
                    #we have to terminate SearchRandom - the only other place P_Explore can be in And-Or tree
                    self.processesArea.TerminateAtomicProcess(emotion, True)
                self.processesArea.TerminateIntentionWant(emotion)
    
  
