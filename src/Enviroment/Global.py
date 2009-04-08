
from Time import Time
from math import exp, sqrt, log
from random import randint, choice, random

class GlobalVariables:
    def __init__(self):
        self.Reset()
        self.outLog = None
        self.path = None
        self.outFiles = {}
    
    def Reset(self):
        self.SafeMode = True
        self.Time = Time()
        self.World = None
        self.Map = None
        self.MaxNumber = 9999999
        self.MinPositiveNumber = 0.0000001
        self.logLines = []
        self.LogLinesCount = 30
      
        self.WorldDynamic = 0    #chance to add/remove objects every 100 world step
      
        self.SaveELNodesStatus = True
        self.RenderVisibilityHistory = False    #show visibility objects
        self.CalculateVisibilityHistory = False #calculate visibility of visibility objects
        self.VisibilityHistoryArea = 2          #visibility object is square AxA
        self.AgentMoveHistoryLength = 4         #how many agent moves are displayed

        self.RandomSeeds = [468219]   #seeds to test
        self.MaxTestSteps = 5000      #should be more than one day
        self.MaxTestStepAfter = 25000 
        
        self.MaxAgentMove = 10      #max distance agent can move in one MoveToPartial
        self.WayPointArea = 10      #agent sees waypoints closer than WayPointArea
        self.WayPointNoise = 10     #how much can agent miss waypoint (when going to it)
        
        self.PFSize = 7                    #number of active/real phatoms in PF
        self.PFPhantomHabCreate = 100      #habituation of new phantom(E)
        self.PFPhantomHabUpdate = 50       #habituation added when objNoticed again in PF
        self.MAPhantomHabituation = 100    #habituation of new phantom(M)
        
        self.MapPickUpDistance = 2         #agent can use objects closer than this distance        
        self.ObjDefaultAttractivity = 1    #default object attractivity    
                
        self.TrainEffectNoticed = 1.0
        self.TrainEffectNoticedAgain = 0.3
        self.TrainEffectUsed = 3.0
        self.TrainEffectFound = 2.0
        self.TrainEffectNotFound = 1.0
        self.TrainEffectUsedUp = 1.0
        
        self.SMUpdateMaxDuration = 100  #if action takes more seconds, SP.StepUpdate call Layer.StepUpdate multiple times 
        self.SMNodeAreaDivCoef = 1      #when MemObj's linkToNodes are intensed - alter node's gauss area
        self.SMNodeAreaGaussCoef = 10   #as above
        
        self.SMTrainRange = 10              #how far will SpaceMap intense objects to nodes
        self.MemObjIntenseToNewNode = 1.0       #intensity of new link to new ELNode
        self.MemObjIntensityFadeOut = 0.01      #amount to decrease intensity of memObjs every step
        self.LinkMemObjToNodeFadeOut = 0.005    #amount to decrease intensity of links memObj-node every step
                                
        self.ELDensity = 10       #one node will be created for area of appr. ELDensity x ELDensity
        self.ELCreateNoise = 3    #noise when creating nodes, >ELDensity or ==-1 leads to completely random xy
                
        self.ELNodeUsageFadeOut = 0.005     #amount to decrease intensity of el-node every step
                
        self.ELGravityRange = 20
        self.ELGravityCoef = 1.0
        self.ELAntigravityCoef = 8.0
        self.ELAntigravityRange = 20
        self.MaxELNodeMove = 4.0
        
        self.EPCreateEnergy = 140
        self.ELNodeAddNoise = 2
        self.EPFadeCoef = 0.5
        self.EPFadeLimit = 10
        
        self.ELNodeCreateCostCoef = 50
        
        self.ELForgetNodeRate = 5           #how much EL.forgetEnergy is added each step
        self.ELDeleteNodeReTrainCount = 20
        self.ELDeleteNodeReTrainRange = 20
        
        self.SMBigUpdateFreq = 9
        self.ELAGAddCoef = 3
        self.ELAGFadeOut = 0.1
        self.HLFadeOut = 1
        self.HLAGNeeded = 4000
        self.HLAGNeededSum = 50000
        
        self.HLAGAddCoef = 2
        self.HLAGFadeOut = 1
        
        self.CreatePlaces = False
        self.PlacesAGNeeded = 1500
        self.PlacesAGMin = 500
        self.PlaceAGFadeOut = 0.5
        self.PlaceMoveCoef = 0.02
        
        self.ELUseMapGeometry = False
        self.ELMapGeometryAttractivity = 10
    
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
        self.path = path
    def Log(self, msg):
        print msg
        self.outLog.write(msg + "\n")
        self.logLines.append(msg)
        if len(self.logLines) > self.LogLinesCount:
            self.logLines.pop(0)
    def LogData(self, tag, data):
        if tag not in self.outFiles:
            self.outFiles[tag] = open(self.path+"data-" + tag + ".txt",'a')
        outData = self.outFiles[tag]
        outData.write(data + "\n")
                
    def LogEnd(self, tag=None):
        if tag != None:
            self.outFiles[tag].close()
        else:
            self.outLog.close()
            for f in self.outFiles.values():
                f.close()
            self.outFiles = {}
                
    def Gauss(self, x, c=1):
        return exp( - (x*x) / (2*(c*c)) )
    def GaussInverse(self, y, c=1):
        if y > 1: raise ValueError
        return sqrt( - 2*c*c * log(y) )
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
    def GetStep(self):
        return self.World.step

Global = GlobalVariables()     
