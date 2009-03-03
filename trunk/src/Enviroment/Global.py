

from Time import Time
from math import exp
from random import seed, randint, choice, random

class GlobalVariables:
    def __init__(self):
        self.Reset()
        self.outLog = None
        self.outData = None
    
    def Reset(self):
        self.Time = Time()
        self.World = None
        self.Map = None
        self.MaxNumber = 9999999
        self.MinPositiveNumber = 0.0000001
        self.logLines = []
        self.LogLinesCount = 30
      
        self.RenderVisibilityHistory = False    #show visibility objects
        self.VisibilityHistoryArea = 2          #visibility object is square AxA
        self.AgentMoveHistoryLength = 4         #how many agent moves are displayed

        self.RandomSeeds = [718597, 100, 1024, 718597]   #seeds to test
        self.MaxTestSteps = 1000    #should be more than one day 
        
        self.MaxAgentMove = 10      #max distance agent can move in one MoveToPartial
        self.WayPointArea = 10      #agent sees waypoints closer than WayPointArea
        self.WayPointNoise = 5      #how much can agent miss waypoint (when going to it)
        
        self.PFSize = 7                    #number of active/real phatoms in PF
        self.PFPhantomHabCreate = 100      #habituation of new phantom(e)
        self.PFPhantomHabUpdate = 50       #habituation added when objNoticed again in PF
        self.MAPhantomHabituation = 100    #habituation of new phantom(m)
                
        self.ObjDefaultAttractivity = 10   #default object attractivity    
                
        self.TrainEffectNoticed = 1.0
        self.TrainEffectNoticedAgain = 0.3
        self.TrainEffectUsed = 3.0
        self.TrainEffectFound = 2.0
        self.TrainEffectNotFound = 1.0
        self.TrainEffectUsedUp = 1.0
        
        self.SMNodeAreaDivCoef = 1      #when MemObj's linkToNodes are intensed - alter node's gauss area
        self.SMNodeAreaGaussCoef = 10   #as above
        
        self.MemObjIntenseToNewNode = 1.0       #intensity of new link to new ELNode
        self.MemObjIntensityFadeOut = 0.01      #amount to decrease intensity of memObjs every step
        self.LinkMemObjToNodeFadeOut = 0.001    #amount to decrease intensity of links memObj-node every step
        self.LinkMemObjToNodeMaxIntensity = 10  #max intensity of links memObj-node
                
        self.ELDensity = 10       #one node will be created for area of appr. ELDensity x ELDensity
        self.ELCreateNoise = 3    #noise when creating nodes, >ELDensity or ==-1 leads to completely random xy
                
        self.ELGravityRange = 20
        self.ELGravityCoef = 3.0
        self.ELAntigravityCoef = 1.0
        self.ELAntigravityCoefTESTSET = [1.0, 1.5, 2.0, 2.5, 3.0]
        self.ELAntigravityRange = 20
        
        self.ELEnergyPointCreateEnergy = 100
        #self.ELEnergyPointCreateEnergyTESTSET = [100, 150, 200]
        self.ELNodeAddNoise = 2
        self.ELEnergyFadeCoef = 0.5
        self.ELEnergyFadeLimit = 10
        
        self.ELForgetNodeRate = 5    #how much EL.forgetEnergy is added each step
        self.ELDeleteNodeReTrainCount = 50
        self.ELDeleteNodeReTrainRange = 20
  
    def Random(self):
        return random()
    def Randint(self, min, max):
        return randint(min, max)
    def DiceRoll(self):
        return randint(0, 100)
    def Choice(self, list):
        return choice(list)
    
    def LogStart(self, path):
        self.outLog = open(path+"log.txt",'a')
        self.outData = open(path+"data.txt",'a')
    def Log(self, msg):
        self.outLog.write(msg + "\n")
        self.logLines.append(msg)
        if len(self.logLines) > self.LogLinesCount:
            self.logLines.pop(0)
    def LogData(self, data):
        self.outData.write(data + "\n")
    def LogEnd(self):
        self.outLog.close()
        self.outData.close()
        
    def Gauss(self, x, c=1):
        return exp( - (x*x) / (2*(c*c)) )
    def Sign(self, int):
        if(int < 0): return -1;
        elif(int > 0): return 1;
        else: return int;
        
    #for weakBy=2 maps coef range 0-1 to coef range 0.5-1
    def WeakCoef(self, coef, weakBy):
        return coef / weakBy + 1 - float(weakBy-1)/weakBy     

    def SetDifference(self, a, b):
        return filter(lambda x:x not in b,a)
    def SetFirstDifference(self, a, b):
        difference = SetDifference(a,b)
        if len(difference) == 0:
            return None
        return difference[0]
        
    def TimeToHumanFormat(self, full=False):
        return self.Time.TimeToHumanFormat(full)
    def GetSeconds(self):
        return self.Time.GetSeconds()
        

Global = GlobalVariables()     
