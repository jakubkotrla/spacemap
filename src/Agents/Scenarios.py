# -*- coding: UTF-8 -*-

from Enviroment.Global import Global
import random

## Trieda reprezentujúca funkciu aktivity zámeru
# - Atribúty triedy:
#   - intention ... pointer na zámer
#   - function ... funkcia aktivity zámeru
class IntentionFunction:
    def __init__(self, intention, function):
        self.intention = intention
        self.function  = function
        
    ## Funkcia ktorá vracia aktuálnu aktivitu zámeru
    def GetActivity(self):
        return self.function(Global.Time.GetSeconds())        

## Trieda reprezentujúca scenár pre jeden deň
# - Atribúty triedy:
#   - intentionFunctions ... zoznam funkcií aktivít zámerov
class Scenario:
    def __init__(self):
        self.intentionFunctions = []
    
    ## Funkcia ktorá pridá do scenára funkciu aktivity zámeru
    # @param intention pointer na zámer
    # @param function funkcia aktivity zámeru    
    def AddIntentionFunction(self, intention, function):
        self.intentionFunctions.append(IntentionFunction(intention, function))
    
    ## Funkcia ktorá vracia zoznam aktívnych procesov
    # @return zoznam aktívnych procesov
    def GetIntentionsActivity(self):
        activeIntentions = []
        for intentionFunction in self.intentionFunctions:
            if intentionFunction.GetActivity() > 0:
                activeIntentions.append(intentionFunction.intention)  
        return activeIntentions
                
    def GetMostActiveIntention(self):
        highestActivity = -1
        mostActiveIntention = None
        for intentionFunction in self.intentionFunctions:     
            if intentionFunction.GetActivity() > highestActivity:
                mostActiveIntention = intentionFunction.intention
                highestActivity = intentionFunction.GetActivity()
        return mostActiveIntention

## Trieda reprezentujúca zoznam možných scenárov pre jednotlivé dni týždňa
# - Atribúty triedy:
#   - scenarios ... zoznam 7 zoznamov scenárov pre jednotlivé dni
class Scenarios:
    ## Inicializácia inštancie triedy
    # @param self pointer na zoznam scenárov
    def __init__(self):
        self.scenarios = [[],[],[],[],[],[],[]]
        self.actualScenario = None
        self.actualDay = -1

    ## Funkcia ktorá pridá scenár do jednotlivých dni v týždni
    # @param self pointer na zoznam scenárov
    # @param days zoznam dní pre ktoré sa môže scenár použiť
    # @param scenario pointer na scenár
    def AddScenario(self, days, scenario):
        for day in days:
            self.scenarios[day].append(scenario)

    def GetMostActiveIntention(self):
        if self.actualDay != Global.Time.GetDay():
            self.actualDay = Global.Time.GetDay()
            if self.scenarios[Global.Time.GetDay()] != []:
                self.actualScenario = self.scenarios[Global.Time.GetDay()][random.randint(0,len(self.scenarios[Global.Time.GetDay()])-1)]
            else:
                self.actualScenario = None
        if self.actualScenario != None:
            return self.actualScenario.GetMostActiveIntention()
        else:
            return None

    ## Funkcia ktorá vráti náhodný scenár pre konkrétny deň
    # @param self pointer na zoznam scenárov    
    def GetTodaysScenario(self):
        return self.scenarios[Global.Time.GetDay()][random.randint(0,len(self.scenarios[Global.Time.GetDay()])-1)]


