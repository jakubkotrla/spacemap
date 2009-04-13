## @package Agents.Intentions
# Contains Intentions, collection of Intention.

from Enviroment.Global import Global

## Represents one agent's intention.
class Intention:
    def __init__(self, name, processes):
        self.name      = name
        self.processes = processes    
        self.data = {}            

## Holds all agent's possible intentions.
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