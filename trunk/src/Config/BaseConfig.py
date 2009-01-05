
from Agents.Intentions import Intentions, Intention
from Agents.Processes import Processes, Process
from Agents.Scenarios import Scenarios, Scenario

class BaseConfig:
    def __init__(self):
        self.intentions      = Intentions()
        self.processes       = Processes()
        self.scenarios       = Scenarios()
        
    def prepareScenarios(self):
        pass
        
    def GetAgentIntentions(self, actionSelector):
        self.prepareScenarios()
        actionSelector.processes = self.processes
        actionSelector.intentions = self.intentions
        actionSelector.scenarios = self.scenarios
       
    def prepareMap(self, map):
        pass

    def SetUpMap(self, map):
        self.prepareMap(map)
        
