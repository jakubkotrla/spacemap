# -*- coding: UTF-8 -*-

import parameters
from Enviroment.Time import Time

class Emotion:
    def __init__(self, filename, time):
        f = open(filename,'r')
        exec(f.read())
        self.time = Time(time.day, time.hour, time.minute)
        self.pleasure = self.Function(time)[0]
        self.intensity = self.Function(time)[1]
    
    def Update(self, time):
        while self.time.Before(time):
            self.time.AddMinutes(1)
            self.pleasure = self.pleasure - parameters.pleasureRecoveryRate*(self.pleasure - self.Function(self.time)[0])
            self.intensity = self.intensity - parameters.intensityRecoveryRate*(self.intensity - self.Function(self.time)[1])
    
    def SuccessfulProcess(self):
        self.pleasure = self.pleasure + parameters.pleasureChange_SuccessfulProcess
        self.intensity = self.intensity + parameters.intensityChange_SuccessfulProcess
    
    def ItemFound(self):
        self.pleasure = self.pleasure + parameters.pleasureChange_ItemFound
        self.intensity = self.intensity + parameters.intensityChange_ItemFound
        
    def FailedProcess(self):
        self.pleasure = self.pleasure + parameters.pleasureChange_FailedProcess
        self.intensity = self.intensity + parameters.intensityChange_FailedProcess
        
    def ItemNotFound(self):
        self.pleasure = self.pleasure + parameters.pleasureChange_ItemNotFound
        self.intensity = self.intensity + parameters.intensityChange_ItemNotFound
