## @package Agents.Scenarios
# Implements pre-generated agent's scenario.


from Enviroment.Global import Global
from random import seed

## Represents pre-generated agent's scenario.
class Scenario:
    def __init__(self):
        self.intentions = []
        self.index = -1
    
    ## Pre-generate scenario based on available intentions.
    def Generate(self, clsIntentions):
        seed(Global.RandomSeeds[0])
        for i in range(100):
            self.intentions.append( clsIntentions.GetRandomHighLevelIntention() )
        
    ## Return next intention to be done.
    def GetActiveIntention(self):
        self.index += 1
        if self.index >= len(self.intentions):
            self.index = 0
        return self.intentions[self.index]
    
    ## Saves scenario to CSV data file.
    def SaveScenario(self):
        for i in self.intentions:
            Global.LogData("scenario", i.name)