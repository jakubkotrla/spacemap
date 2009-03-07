
from Enviroment.Global import Global

class Intention:
    def __init__(self, name, processes):
        self.name      = name
        self.processes = processes    
        self.data = {}            

class Intentions:
    def __init__(self):
        self.intentions = {}
        self.highLevelIntentions = []

    def AddIntention(self, intention):
        self.intentions[intention.name] = intention

    def AddHighLevelIntention(self, intentionName):
        self.highLevelIntentions.append(self.intentions[intentionName])
        
    def GetRandomHighLevelIntention(self):
        return Global.Choice(self.highLevelIntentions)