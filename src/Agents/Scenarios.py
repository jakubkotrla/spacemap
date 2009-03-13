
from Enviroment.Global import Global
from random import seed

class Scenario:
    def __init__(self):
        self.intentions = []
        self.index = -1
    
    def Generate(self, clsIntentions):
        seed(Global.RandomSeeds[0])
        for i in range(100):
            self.intentions.append( clsIntentions.GetRandomHighLevelIntention() )
        
    def GetActiveIntention(self):
        self.index += 1
        if self.index >= len(self.intentions):
            self.index = 0
        return self.intentions[self.index]
    
    def SaveScenario(self):
        for i in self.intentions:
            Global.LogData("scenario", i.name)