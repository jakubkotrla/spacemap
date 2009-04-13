## @package Agents.PerceptionFilter
# Contains PerceptionFilter - simple perception filter.

from Enviroment.Global import Global

## Represents agent's perception filter.
class PerceptionFilter:
    def __init__(self):
        pass

    ## Sets rObj.curAttractivity based on given active process.
    def ProcessObjects(self, rObjs, action):
        name = action.process.name
        if name == "Remember":
            self.SetAllTo(rObjs, 0)
        elif name == "LookForObject":
            self.SetAllTo(rObjs, 0)
        elif name == "MoveToPartial":
            self.SetAllTo(rObjs, 1)
        elif name == "Explore":
            self.SetAllToRegardingAffs(rObjs, action, 1)
        elif name == "ExecuteReal":
            self.SetAllToRegardingAffs(rObjs, action, 0.5)
        else:
            Global.Log("Programmer.Error: PerceptionFilter process name unknown: " + name)
    
    ## Utility method, sets all objects' attractivity to given value.
    def SetAllTo(self, rObjs, attractivity):
        for rObj in rObjs:
            rObj.curAttractivity = attractivity * rObj.attractivity
    
    ## Utility method, sets all objects' attractivity regarding mutual affrodances between given current action and object.
    def SetAllToRegardingAffs(self, rObjs, action, coef):
        sources = action.sources
        sourcesCount = len(sources)
        for rObj in rObjs:
            affs = []
            for aff in rObj.type.affordances:
                if aff in sources:
                    affs.append(aff)
            rObj.curAttractivity = Global.WeakCoef(coef * float(len(affs)) / sourcesCount, 2) * rObj.attractivity
        
        
        
        
        