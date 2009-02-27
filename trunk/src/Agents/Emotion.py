

#untouched, original from Tomas Korenko source code

from Enviroment.Time import Time

height_imp = 1
time_imp = 0.002
emotion_imp = 0.1

pleasureRecoveryRate = 0.1
intensityRecoveryRate = 0.1

pleasureChange_SuccessfulProcess = 20
intensityChange_SuccessfulProcess = -5

pleasureChange_ItemFound = 4
intensityChange_ItemFound = -1

pleasureChange_FailedProcess = -100
intensityChange_FailedProcess = 100

pleasureChange_ItemNotFound = -20
intensityChange_ItemNotFound = 20


class Emotion:
    def __init__(self, filename, time):
        f = open(filename,'r')
        exec(f.read())
        self.time = Time(time.day, time.hour, time.minute)
        self.pleasure = self.Function(time)[0]
        self.intensity = self.Function(time)[1]
    
    def Update(self, time):
        while self.time.Before(time):
            self.time.AddSeconds(60)
            self.pleasure = self.pleasure - pleasureRecoveryRate*(self.pleasure - self.Function(self.time)[0])
            self.intensity = self.intensity - intensityRecoveryRate*(self.intensity - self.Function(self.time)[1])
    
    def SuccessfulProcess(self):
        self.pleasure = self.pleasure + pleasureChange_SuccessfulProcess
        self.intensity = self.intensity + intensityChange_SuccessfulProcess
    
    def ItemFound(self):
        self.pleasure = self.pleasure + pleasureChange_ItemFound
        self.intensity = self.intensity + intensityChange_ItemFound
        
    def FailedProcess(self):
        self.pleasure = self.pleasure + pleasureChange_FailedProcess
        self.intensity = self.intensity + intensityChange_FailedProcess
        
    def ItemNotFound(self):
        self.pleasure = self.pleasure + pleasureChange_ItemNotFound
        self.intensity = self.intensity + intensityChange_ItemNotFound
