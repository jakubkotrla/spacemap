
from Intentions import Intentions, Intention
from Enviroment.Affordances import *
from Processes import Processes, Process
from Scenarios import Scenario
from Enviroment.Global import Global
from Enviroment.Map import Hit, Point
from copy import copy


class ActionSelector:
    def __init__(self, agent, config, processArea, perceptionField, episodicMemory, spaceMap):
        self.agent           = agent
        self.intentions      = Intentions()
        self.processes       = Processes()
        self.scenario       = Scenario()
        self.processArea   = processArea
        self.perceptionField = perceptionField
        self.episodicMemory  = episodicMemory
        self.spaceMap        = spaceMap
        
        config.GetAgentIntentions(self)
        self.intentions.wantInt = Intention("Want", [self.processes.atomic["Explore"],
                                                     self.processes.atomic["LookUpInMemory"],
                                                     self.processes.atomic["SearchRandom"]])
    
    def GetAction(self, emotion):
        if self.processArea.HasNoIntention():
            self.ChooseIntention()
        #agent has intention (in self.PA.actInt)
        excIntention = self.processArea.GetActIntention()
        excProcess = self.processArea.GetActProcess()
        
        #what is active - I or P ?
        if excIntention.parentExcProcess == excProcess:
            #if I under P -> we have active I and need some process to do it  (or this is HL intention)
            process = self.ChooseProcessForIntention(emotion, excIntention.intention, excIntention.parentExcProcess)
            if process == None:
                self.processArea.TerminateIntentionFalse(emotion)
                #impossible to finish this intention -> terminate int and parent process, try to choose another process in parent intention
                return self.GetAction(emotion)
            excProcess = self.processArea.ActivateProcess(emotion, process, excIntention, excIntention.parentExcProcess)
        else:
            #if P under I -> we have already selected process for this intention previously, go on
            process = excProcess.process         
        
        #now we have intention and under it process to do
        
        #process atomic?
        if process.intentions != []:
            #process is not atomic -> choose first not completed sub-intention
            intention = Global.SetFirstDifference(process.intentions, excProcess.completedIntentions)
            self.processArea.ActivateIntention(intention, excProcess)
            return self.GetAction(emotion)    #go deeper for atomic process
        else:
            # process is atomic
            return self.GetAtomicAction(emotion, excProcess)


    def ChooseProcessForIntention(self, emotion, intention, parentProcess):
        processes = intention.processes
        if parentProcess != None:
            processes = Global.SetDifference(processes, parentProcess.failedProcesses)
            
        if len(processes) == 0:
            return None
        if intention.name == "Want":    #for Want intention the order of process matters
            return processes[0]
        else:
            return Global.Choice(processes)



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
                excWantInt = self.processArea.ActivateIntention(self.intentions.wantInt, excProcess)
                excWantInt.data["affordance"] = missingSources[0] 
                
                atomicProcess = self.processArea.ActivateProcess(emotion, self.processes.atomic["Explore"], excWantInt, excProcess)
                atomicProcess.data["parent"] = "intention"
                atomicProcess.data["process"] = excProcess
                atomicProcess.data["affordance"] = missingSources[0]
            else:
                #we have everything
                atomicProcess = self.processArea.ActivateProcess(emotion, self.processes.atomic["Execute"], excProcess.excParentIntention, excProcess)
                atomicProcess.data["process"] = excProcess.process
                atomicProcess.duration = excProcess.process.durationTime
        else:
            #we have everything
            atomicProcess = self.processArea.ActivateProcess(emotion, self.processes.atomic["Execute"], excProcess.excParentIntention, excProcess)
            atomicProcess.data["process"] = excProcess.process
            atomicProcess.duration = excProcess.process.durationTime
        return atomicProcess


    def GetAtomicActionforSmartProcess(self, emotion, excProcess):
        if (excProcess.process.name == "SearchRandom"):

            if (excProcess.data["step"] == "MoveTo"):
                
                if excProcess.data["waypoints"] == None:
                    map = Global.Map
                    ws = copy(map.wayPoints)
                    ws.sort(lambda a,b: cmp(a.lastVisited,b.lastVisited))
                    excProcess.data["waypoints"] = ws
                    
                if len(excProcess.data["waypoints"]) < 1:
                    self.processArea.TerminateProcess(emotion, False)
                    return self.GetAction(emotion)
                
                wayPointToGo = Global.Choice(excProcess.data["waypoints"])
                excProcess.data["waypoints"].remove(wayPointToGo)
                excProcess.data["step"] = "Explore"
                
                canMove = False
                map = Global.Map
                while not canMove:
                    newX = Global.Randint(-Global.WayPointNoise, Global.WayPointNoise) + wayPointToGo.x
                    newY = Global.Randint(-Global.WayPointNoise, Global.WayPointNoise) + wayPointToGo.y
                    canMove = map.IsInside( Point(newX,newY) )
                    
                atomicProcess = self.processArea.ActivateProcess(emotion, self.processes.atomic["MoveTo"], excProcess.excParentIntention, excProcess)
                atomicProcess.data["process"] = excProcess.process
                atomicProcess.data["newx"] = newX
                atomicProcess.data["newy"] = newY
                return self.GetAtomicActionforSmartProcess(emotion, atomicProcess)                                
                
            elif (excProcess.data["step"] == "Explore"):
                excProcess.data["step"] = "MoveTo"
                atomicProcess = self.processArea.ActivateProcess(emotion, self.processes.atomic["Explore"], excProcess.excParentIntention, excProcess)
                atomicProcess.data["parent"] = "process"
                atomicProcess.data["process"] = excProcess.excParentIntention.parentExcProcess
                atomicProcess.data["affordance"] = excProcess.data["affordance"]
                return atomicProcess
            
        elif (excProcess.process.name == "LookUpInMemory"):
            
            if (excProcess.data["step"] == "Remember"):
                excProcess.data["step"] = "MoveTo"
                atomicProcess = self.processArea.ActivateProcess(emotion, self.processes.atomic["Remember"], excProcess.excParentIntention, excProcess)
                atomicProcess.data["process"] = excProcess.process
                atomicProcess.data["affordance"] = excProcess.data["affordance"]
                return atomicProcess
            
            elif (excProcess.data["step"] == "MoveTo"):
                excProcess.data["step"] = "LookForObject"
                atomicProcess = self.processArea.ActivateProcess(emotion, self.processes.atomic["MoveTo"], excProcess.excParentIntention, excProcess)
                atomicProcess.data["process"] = excProcess.process
                
                memObj = excProcess.data["phantom"].object
                atomicProcess.data["newx"] = memObj.x
                atomicProcess.data["newy"] = memObj.y
                return self.GetAtomicActionforSmartProcess(emotion, atomicProcess)
            
            elif (excProcess.data["step"] == "LookForObject"):
                atomicProcess = self.processArea.ActivateProcess(emotion, self.processes.atomic["LookForObject"], excProcess.excParentIntention, excProcess)
                atomicProcess.data["process"] = excProcess.process
                atomicProcess.data["affordance"] = excProcess.data["affordance"]
                atomicProcess.data["phantom"] = excProcess.data["phantom"]
                return atomicProcess    
            
            return None    
        elif (excProcess.process.name == "MoveTo"):
            if excProcess.data["path"] == None:
                map = Global.Map
                path = map.GetPath(self.agent, excProcess.data["newx"], excProcess.data["newy"])
                if path == None:
                    self.processArea.TerminateProcess(emotion, False)
                    return self.GetAction(emotion)
                excProcess.data["path"] = path[1:]
            #we have path (without start)
            nextPoint = excProcess.data["path"].pop(0)
            atomicProcess = self.processArea.ActivateProcess(emotion, self.processes.atomic["MoveToPartial"], excProcess.excParentIntention, excProcess)
            atomicProcess.data["process"] = excProcess.process
            atomicProcess.data["newx"] = nextPoint.x
            atomicProcess.data["newy"] = nextPoint.y
            return atomicProcess
        else:
            return excProcess

    
    def ChooseIntention(self):
        mostActiveIntention = self.scenario.GetActiveIntention()
        if mostActiveIntention == None:
            mostActiveIntention = self.intentions.GetRandomHighLevelIntention()
        self.processArea.ActivateIntention(mostActiveIntention, None) 
        
        
    def ActionDone(self, emotion):
        actExcProcess = self.processArea.GetActProcess()
        actProcess = actExcProcess.process
        if actProcess.name == "Execute":
            self.processArea.TerminateAtomicProcess(emotion)   #terminates Execute
            self.processArea.TerminateProcess(emotion)         #terminates the executed process
                                            #chooses another intention or no intention will be actual
        elif actProcess.name == "MoveTo":
            # check we're at the end - is done in child MoveToPartial process!
            # this actually gets never called - its MoveToPartial child process!
            pass
        elif actProcess.name == "MoveToPartial":
            #nothing smart to do here except of terminating atomic MoveToPartial and possibly MoveTo
            self.processArea.TerminateAtomicProcess(emotion) #terminates MoveToPartial
            process = self.processArea.GetActProcess()
            if len(process.data["path"]) == 0:
                self.processArea.TerminateAtomicProcess(emotion)   #terminates Moveto
            
        elif actProcess.name == "SearchRandom":
            # check we got it.. - is done in child Explore process!
            # this actually gets never called - its either MoveTo or Explore child process!
            pass            
        elif actProcess.name == "LookUpInMemory":
            # check we got it.. - is done in child LookForObject process!
            # this actually gets never called - its either Remember, MoveTo or LookForObject child process!
            pass
         
        elif actProcess.name == "Remember":
            if actExcProcess.data["phantom"] != None:
                #success, terminates, next step AS will go for MoveTo and MoveToPartial
                actExcProcess.parent.data["phantom"] = actExcProcess.data["phantom"]
                self.processArea.TerminateAtomicProcess(emotion)
            else:
                # whole LookUpInMemory failed - terminate Remember and LookUpInMemory
                self.processArea.TerminateAtomicProcess(emotion, False)
                self.processArea.TerminateProcess(emotion, False)
            
        elif actProcess.name == "LookForObject":
            if actExcProcess.data["object"] != None:
                #success, whole LookUpInMemory is done - terminate LookForObject, LookUpInMemory, I_Want
                self.processArea.TerminateAtomicProcess(emotion, True)
                self.processArea.TerminateAtomicProcess(emotion, True)
                self.processArea.TerminateIntentionWant(emotion)
            else:
                # whole LookUpInMemory failed - terminate LookForObject and LookUpInMemory
                # ToDo: dynamicWorld: now try different location
                self.processArea.TerminateAtomicProcess(emotion, False)
                self.processArea.TerminateProcess(emotion, False)
            
        elif actProcess.name == "Explore":
            excProcess = actExcProcess.data["process"]
            wantedAff = actExcProcess.data["affordance"]
                
            #check if we got required affordance
            missingSources = excProcess.GetMissingSources()
            if wantedAff in missingSources:
                #still we do not have it - fail
                if (actExcProcess.data["parent"] == "process"):
                    #we have to terminate only Explore, no SearchRandom
                    self.processArea.TerminateAtomicProcess(emotion, False)
                else:
                    self.processArea.TerminateProcess(emotion, False)
            else:
                #we got it - success
                self.processArea.TerminateAtomicProcess(emotion, True)
                if (actExcProcess.data["parent"] == "process"):
                    #we have to terminate SearchRandom - the only other place P_Explore can be in And-Or tree
                    self.processArea.TerminateAtomicProcess(emotion, True)
                self.processArea.TerminateIntentionWant(emotion)
    
  
