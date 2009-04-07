
#based on source from Tomas Korenko, changed

class Process:
    def __init__(self, name, intentions, sources, usedSources=[], newObjects=[], durationTime=0, baseTimeLimit=86400, iteration=1):
        self.name          = name
        self.intentions    = intentions
        self.sources       = sources
        self.usedSources   = usedSources
        self.newObjects    = newObjects
        self.baseTimeLimit = baseTimeLimit
        self.durationTime  = durationTime
        self.iteration     = iteration
        self.pleasure      = 0
        self.intensity     = 0
        
    def HasSources(self):
        return len(self.sources) > 0


class Processes:
    def __init__(self):
        self.atomic = { "MoveTo"   : Process("MoveTo",[],[],[],[]),
                        "MoveToPartial"   : Process("MoveToPartial",[],[],[],[]),
                        "Explore"  : Process("Explore",[],[],[],[]),
                        "Execute"  : Process("Execute",[],[],[],[]),
                        "ExecuteGet"  : Process("ExecuteGet",[],[],[],[]),
                        "ExecuteReal"  : Process("ExecuteReal",[],[],[],[]),
                        "LookUpInMemory"  : Process("LookUpInMemory",[],[],[],[]),
                        "Remember"  : Process("Remember",[],[],[],[]),
                        "LookForObject"  : Process("LookForObject",[],[],[],[]),
                        "SearchRandom"  : Process("SearchRandom",[],[],[],[]),
                        "ActionOut"  : Process("ActionOut",[],[],[],[], 10)
                        }        
        self.processes = {}
    
    def AddProcess(self, process):
        self.processes[process.name] = process
