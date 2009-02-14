# -*- coding: UTF-8 -*-



## Trieda reprezentujúca proces ktorý môže agent vykonať
# - Atribúty triedy
#   - name ... meno procesu
#   - sources ... zdroje potrebné na vykonanie procesu - zoznam afordancií
#   - intentions ... zoznam zámerov ktoré je potreba vykonať aby proces úspešne prebehol
#   - baseTimeLimit ... základný čas ktorý sa môže proces vykonávať
#   - durationTime ... čas ktorý sa proces vykonáva po zhromaždení všetkých zdrojov
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


class Processes:
    def __init__(self):
        self.atomic = { "MoveTo"   : Process("MoveTo",[],[],[],[]),
                        "MoveToPartial"   : Process("MoveToPartial",[],[],[],[]),
                        "Explore"  : Process("Explore",[],[],[],[]),
                        "Execute"  : Process("Execute",[],[],[],[]),
                        "LookUpInMemory"  : Process("LookUpInMemory",[],[],[],[]),
                        "Remember"  : Process("Remember",[],[],[],[]),
                        "LookForObject"  : Process("LookForObject",[],[],[],[]),
                        "SearchRandom"  : Process("SearchRandom",[],[],[],[]),
                        "Rest"  : Process("Rest",[],[],[],[]),
                        "Walk"  : Process("Walk",[],[],[],[])
                        }        
        self.processes = []
    
    def AddProcess(self, process):
        self.processes.append(process)
