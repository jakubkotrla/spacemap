
import random

class Intention:
    def __init__(self, name, processes):
        self.name      = name
        self.processes = processes    
        self.data = {}            

class Intentions:
    def __init__(self):
        self.intentions = []
        self.highLevelIntentions = []

    def AddIntention(self, intention):
        self.intentions.append(intention)

    def AddHighLevelIntention(self, intention):
        self.highLevelIntentions.append(intention)
        
    def GetRandomHighLevelIntention(self):
        return self.highLevelIntentions[random.randint(0,len(self.highLevelIntentions)-1)]