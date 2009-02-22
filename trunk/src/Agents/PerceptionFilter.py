
from Enviroment.Global import Global

class PerceptionFilter:
    def __init__(self):
        pass

    #sets rObj.curAttractivity based on active process
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
        elif name == "Execute":
            self.SetAllToRegardingAffs(rObjs, action, 0.5)
        else:
            Global.Log("Programmer.Error: PerceptionFilter process name unknown: " + actProcess.name)
         
    def SetAllTo(self, rObjs, attractivity):
        for rObj in rObjs:
            rObj.curAttractivity = attractivity
    
    def SetAllToRegardingAffs(self, rObjs, action, coef):
        sources = action.sources
        sourcesCount = len(sources)
        for rObj in rObjs:
            affs = []
            for aff in rObj.type.affordances:
                if aff in sources:
                    affs.append(aff)
            rObj.curAttractivity = Global.WeakCoef(coef * len(affs)*1.0 / sourcesCount, 2)
        
        
        
        
        