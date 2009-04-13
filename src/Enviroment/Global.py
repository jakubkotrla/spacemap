## @package Enviroment.Global
# Main configuration file, contains all model settings.

from Time import Time
from math import exp, sqrt, log
from random import randint, choice, random

## Represents model settings.
class GlobalVariables:
    def __init__(self):
        self.Reset()
        self.outLog = None
        self.path = None
        self.outFiles = {}
    
    ## Resets settings to defaults.
    def Reset(self):
        self.SafeMode = True            ## If True, TestAll mode will catch any exception and go on.
        self.Time = Time()
        self.World = None
        self.Map = None
        self.MaxNumber = 9999999
        self.MinPositiveNumber = 0.0000001
        self.logLines = []
        self.LogLinesCount = 30     #count of log lines show on screen.
      
        self.WorldDynamic = 0    #chance to add/remove objects every 100 world step
      
        ## Whether save status of EnergyLayerNodes
        self.SaveELNodesStatus = True
        
        ## Whether show visibility objects, to set this True CalculateVisibilityHistory must be True.
        self.RenderVisibilityHistory = False
        ## Whether calculate visibility of visibility objects - extrmely slow.
        self.CalculateVisibilityHistory = False 
        ## VisibilityObject is square AxA
        self.VisibilityHistoryArea = 2  
                
        ## How many last agent's moves are displayed
        self.AgentMoveHistoryLength = 4         

        ## Random seeds to test in TestAll mode
        self.RandomSeeds = [468219]
        
        ## How many steps do in TestAll mode, 500-1000 ~ should be one day in anget's life
        self.MaxTestSteps = 5000
        ## How many steps do in TestAll mode with agent out of world, after MaxTestSteps
        self.MaxTestStepAfter = 0     
        
        ## Max distance agent can move in one MoveToPartial, in step
        self.MaxAgentMove = 10      
        ## Agent sees waypoints closer than WayPointArea
        self.WayPointArea = 10      
        ## How much can agent miss waypoint (when going to it)
        self.WayPointNoise = 10     
        
        ## Maximum number of active/real phatoms in PF
        self.PFSize = 7 
        
        ## Habituation of new Phantom           
        self.PFPhantomHabCreate = 100      
        ## Habituation added when objNoticed again in PF
        self.PFPhantomHabUpdate = 50       
        ## Habituation of new MemoryPhantom
        self.MAPhantomHabituation = 100    
        
        ## Agent can use objects closer than this distance
        self.MapPickUpDistance = 2         
        
        ## Default object attractivity        
        self.ObjDefaultAttractivity = 1        
                
        self.TrainEffectNoticed = 1.0
        self.TrainEffectNoticedAgain = 0.3
        self.TrainEffectUsed = 3.0
        self.TrainEffectFound = 2.0
        self.TrainEffectNotFound = -1.0
        
        ## If action takes more seconds, SP.StepUpdate call Layer.StepUpdate multiple times 
        self.SMUpdateMaxDuration = 100  
        
        ## When MemObj's linkToNodes are intensed - alter node's gauss area
        self.SMNodeAreaDivCoef = 1
        ## When MemObj's linkToNodes are intensed - alter node's gauss area      
        self.SMNodeAreaGaussCoef = 10
        
        ## How far will SpaceMap intense objects to nodes
        self.SMTrainRange = 10
        ## Intensity of new link to new ELNode
        self.MemObjIntenseToNewNode = 1.0       
        ## Amount to decrease intensity of memObjs every step
        self.MemObjIntensityFadeOut = 0.01      
        ## Amount to decrease intensity of links memObj-node every step
        self.LinkMemObjToNodeFadeOut = 0.005    
                                
        ## One node will be created for area of appr. ELDensity x ELDensity
        self.ELDensity = 10       
        ## Noise when creating nodes, ==-1 leads to completely random xy
        self.ELCreateNoise = 3    
                
        ## Amount to decrease intensity of el-node every step
        self.ELNodeUsageFadeOut = 0.005     
        
        ## Gravity range
        self.ELGravityRange = 20
        ## Gravity strength
        self.ELGravityCoef = 1.0
        ## Antigravity range
        self.ELAntigravityRange = 20
        ## Antigravity strength
        self.ELAntigravityCoef = 8.0
        ## Influence of usage on antigravity
        self.ELAGUsageCoef = 0.8
        self.ELAGUsageCoef2 = self.ELAGUsageCoef * self.ELAGUsageCoef       #only precomputed value
        ## Max distance ELNode can move in one step.
        self.MaxELNodeMove = 4.0
        
        ## Initial EnergyPoint energy.
        self.EPCreateEnergy = 140
        ## Noise when creating ELNodes from EnergyPoint.
        self.ELNodeAddNoise = 2
        ## How fast EnergyPoint's energy fades out.
        self.EPFadeCoef = 0.5
        ## Minimal energy of EnergyPoint, if lower EP is deleted.
        self.EPFadeLimit = 10
        
        ## How much EL.forgetEnergy is added each step 
        self.ELForgetNodeRate = 5
        ## How many local antigravity steps are done after node deletion           
        self.ELDeleteNodeReTrainCount = 20
        ## Range of local antigravity steps after node deletion
        self.ELDeleteNodeReTrainRange = 20
        
        ## How often update memoryObject locatin and save it - only for getting data
        self.SMBigUpdateFreq = 9
        ## Coeficient used when increasing node.AGamount    
        self.ELAGAddCoef = 3
        ## How fast node.AGamount fades out.
        self.ELAGFadeOut = 0.1
        
        ## Whether to create places.
        self.CreatePlaces = True
        ## Minimum AGamount of place to be splitted to subplaces
        self.PlacesAGNeeded = 1500
        ## Minimum totalAGamount of place, if lower place is deleted
        self.PlacesAGMin = 500
        ## How fast place.AGamount fades out
        self.PlaceAGFadeOut = 0.5
        ## How much place will move to weighted centroid
        self.PlaceMoveCoef = 0.02
        ## How fast place.AGamount grows
        self.PlacesAGGrow = 0.1

    
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
        
    ## Weaks coeficient, for weakBy=2 maps coef range 0-1 to coef range 0.5-1
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
