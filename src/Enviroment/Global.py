

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
        self.MinPositiveNumber = 0.00000001
        self.logLines = []
        self.LogLinesCount = 30
      
        self.RenderVisibilityHistory = False    #show visibility objects
        self.VisibilityHistoryArea = 2          #visibility object is square AxA
        self.AgentMoveHistoryLength = 4         #how many agent moves are displayed

        self.RandomSeeds = [100, 1024, 123456789, 718597]   #seeds to test
        self.MaxTestSteps = 400    #should be more than one day 
        
        self.MaxAgentMove = 10      #max distance agent can move in one MoveToPartial
        self.WayPointArea = 10      #agent sees waypoints closer than WayPointArea
        self.WayPointNoise = 5      #how much can agent miss waypoint (when going to it)
        
        self.PFSize = 7                    #number of active/real phatoms in PF
        self.PFPhantomHabCreate = 100      #habituation of new phantom(e)
        self.PFPhantomHabUpdate = 50       #habituation added when objNoticed again in PF
        self.MAPhantomHabituation = 100    #habituation of new phantom(m)
                
        self.ObjDefaultAttractivity = 10   #default object attractivity    
                
        self.TrainEffectNoticed = 1.0
        self.TrainEffectNoticedAgain = 0.1
        self.TrainEffectUsed = 3.0
        self.TrainEffectFound = 2.0
        self.TrainEffectNotFound = 1.0
        self.TrainEffectUsedUp = 1.0
        
        self.SMTRainEffectCoef = 4   #coef increasing intensity of links memObj-node
        self.SMTRainEffectCoefTESTSET = [4,8]   
        self.SMNodeAreaDivCoef = 10  #when MemObj's linkToNodes are intensed - alter node's gauss area
        self.SMNodeAreaDivCoefTESTSET = [1, 2, 5, 10]
        self.SMNodeAreaGaussCoef = 1 #as above
        self.SMNodeAreaGaussCoefTESTSET = [1, 2, 3, 4, 5]
        
        self.MemObjIntenseToNewNode = 1.0       #intensity of new link to new ELNode
        self.MemObjIntensityFadeOut = 0.01      #amount to decrease intensity of memObjs every step
        self.LinkMemObjToNodeFadeOut = 0.001    #amount to decrease intensity of links memObj-node every step
        self.LinkMemObjToNodeMaxIntensity = 10  #max intensity of links memObj-node
                
        self.ELDensity = 10       #one node will be created for area of appr. ELDensity x ELDensity
        self.ELCreateNoise = -1   #noise when creating nodes, >ELDensity or ==-1 leads to completely random xy
                
        self.ELGravityRange = 20
        self.ELGravityRangeTESTSET = [10, 15, 20, 25, 30]
        self.ELAntigravityCoef = 2.0
        self.ELAntigravityCoefTESTSET = [1.0, 1.5, 2.0, 2.5, 3.0]
        self.ELAntigravityRange = 15
        self.ELAntigravityRangeTESTSET = [10, 15, 20]
        self.ELNodeUsageCoef = 10.0
        
        self.ELEnergyPointCreateEnergy = 100
        self.ELEnergyPointCreateEnergyTESTSET = [75, 100, 125, 150, 175, 200]
        self.ELNodeAddNoise = 2
        self.ELEnergyFadeCoef = 0.5
        self.ELEnergyFadeCoefTESTSET = [0.1, 0.3,  0.5, 0.7, 0.8]
        self.ELEnergyFadeLimit = 10
        
        self.ELForgetNodeRate = 0    #how much EL.forgetEnergy is added each step
        self.ELDeleteNodeReTrainCount = 50
        self.ELDeleteNodeReTrainRange = 20
  
    def Random(self):
        r = random()
        #self.Log("RandomRandom:" + str(r))
        return r
    def Randint(self, min, max):
        r = randint(min, max)
        #self.Log("RandomRandint:" + str(r))
        return r
    def DiceRoll(self):
        r = randint(0, 100)
        #self.Log("RandomDiceRoll:" + str(r))
        return r
    def Choice(self, list):
        #self.Log("RandomChoice")
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
        return exp( - ((x)**2) / 2*(c**2) )
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
