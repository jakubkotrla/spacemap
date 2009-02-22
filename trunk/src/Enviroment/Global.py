

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
        self.RenderVisibilityHistory = False
        self.VisibilityHistoryArea = 2
        
        self.World = None
        self.Map = None
        
        self.wndLog = None
        self.wndPA = None
        self.SaveFreq = 0
        self.AgentMoveHistoryLength = 4
        
        self.MaxAgentMove = 10
        
        self.WayPointArea = 10
        self.WayPointNoise = 5
        
        self.PFSize = 7
        self.PFPhantomHabituation = 100
        self.MAPhantomHabituation = 100
                
        self.ObjDefaultAttractivity = 10        
                
        self.TrainEffectNoticed = 1.0
        self.TrainEffectNoticedAgain = 0.1
        self.TrainEffectUsed = 3.0
        self.TrainEffectFound = 2.0
        self.TrainEffectNotFound = 1.0
        self.TrainEffectUsedUp = 1.0
        
        self.SMTRainEffectCoef = 4
        self.SMNodeAreaDivCoef = 10  #when MemObj's linkToNodes are intensed - alter node's gauss area
        self.SMNodeAreaGaussCoef = 1 #as above
        
        self.MemObjMaxIntensity = 10
        self.LinkMemObjToNodeFadeOut = 0.001
        self.LinkMemObjToNodeMaxIntensity = 10
        
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
        
        self.ELForgetNodeChance = 0    #max=1..100% each step
           
        
        
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
        
    #for weakBy=2 maps coef range 0-1 to coef range 0.5-1
    def WeakCoef(self, coef, weakBy):
        coef = coef / weakBy + 1 - (weakBy-1)/weakBy     
        
    def TimeToHumanFormat(self, full=False):
        return self.Time.TimeToHumanFormat(full)
    
    def GetSeconds(self):
        return self.Time.GetSeconds()
        

Global = GlobalVariables()     
