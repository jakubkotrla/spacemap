

from Time import Time
from math import exp

class GlobalVariables:
    def __init__(self):
        self.Time    = Time()
        self.MaxNumber = 9999999
        self.MinPositiveNumber = 0.00000001
        self.LogTags = ["error", "debug"]
        self.logLines = []
        self.LogLinesCount = 30
        
        self.World = None
        self.Map = None
        
        self.wndLog = None
        self.wndPA = None
        self.SaveFreq = 0
        self.AgentMoveHistoryLength = 10
        
        self.MapObjectPickupDistance = 10
        
        self.PFSize = 10
        self.PFPhantomHabituation = 10
        
        self.TrainEffectNoticed = 1.0
        self.TrainEffectNoticedAgain = 0.1
        self.TrainEffectUsed = 3.0
        self.TrainEffectFound = 2.0
        self.TrainEffectNotFound = 1.0
        self.TrainEffectUseUp = 1.0
        
        self.ELDensity = 10             #one node will represent area of appr. ELDensity x ELDensity
        self.ELCreateNoise = 2
        self.ELGravityRange = 20
        self.ELGravityCoef = 1
        self.ELAntigravityCoef = 2.0
        self.ELAntigravityRange = 15
        self.ELAntigravityNoise = 0.2
        self.ELNodeUsageCoef = 10.0
        self.ELNodeUsageLimit = 15
        
        self.ELEnergyPointCreateCoef = 100
        self.ELNodeAddCost = 100
        self.ELNodeAddNoise = 2
        self.ELEnergyFadeCoef = 0.5
        self.ELEnergyFadeLimit = 10
        
        self.ELForgetNodeChance = 5    #max=1..100% each step
           
        
        
    def Log(self, msg, tag="msg"):
        #if not tag in self.LogTags: return
        msg = tag + "> " + msg
        print msg
        if self.wndLog != None:
            self.wndLog.txtLog.insert("end", msg)
        self.logLines.append(msg)
        if len(self.logLines) > self.LogLinesCount:
            self.logLines.pop(0)
        
    def Gauss(self, x, c=1):
        return exp( - ((x)**2) / 2*(c**2) )
    def Sign(self, int):
        if(int < 0): return -1;
        elif(int > 0): return 1;
        else: return int;
        
    def TimeToHumanFormat(self, full=False):
        return self.Time.TimeToHumanFormat(full)
    
    def GetSeconds(self):
        return self.Time.GetSeconds()
        

Global = GlobalVariables()     
