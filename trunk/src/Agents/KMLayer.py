
from Enviroment.Global import Global
from math import exp

class KMLNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = []
        self.size = 10  #ToDo use a constant for setting
        self.objects = []
        self.learnCoef = 0.2    #ToDo make a constant
        self.neighboursCoefLimit = 0.1 #ToDo make a constant
        
    def Train(self, rObject, effect, neighboursCoef = 0):
        nG = self.Gausse(neighboursCoef)
        if nG < self.neighboursCoefLimit: return 
        
        # Wv(t + 1) = Wv(t) + neighboursCoef(v, t)*learnCoef(t)(D(t) - Wv(t))
        difX = rObject.x - self.x
        difY = rObject.y - self.y
        
        lCoef = nG * self.learnCoef
        
        self.x = self.x + difX * lCoef
        self.y = self.y + difY * lCoef
        self.guiMoved(self)
        
        for n in self.neighbours:
            n.Train(rObject, effect, neighboursCoef+1)
            
    def Gausse(self, x):
        return exp( - ((x)**2) / 2 )

class KMLayer:
    def __init__(self, area):
        self.area = area
        self.nodes = []
        self.trainEffectNotice = 1
        
        
    def CreateMap(self):
        xCount = self.area.width / 10
        yCount = self.area.height / 10
        nodesMap = [[0 for col in range(xCount)] for row in range(yCount)]
        
        for y in range(yCount):
            for x in range(xCount):
                node = KMLNode(x*10+5, y*10+5)
                self.nodes.append(node)
                nodesMap[x][y] = node
                
                if y>0:
                    node.neighbours.append(nodesMap[x][y-1])
                    nodesMap[x][y-1].neighbours.append(node)
                if x>0:
                    node.neighbours.append(nodesMap[x-1][y])
                    nodesMap[x-1][y].neighbours.append(node)
        Global.Log("KM-layer created")
        
    def PositionToKMLNodes(self, x, y):
        inNodes = []
        for node in self.nodes:
            if node.x-node.size < x < node.x+node.size and node.y-node.size < y < node.y+node.size:
                inNodes.append(node)
        nls = {}
        for node in inNodes:
            nls[node] = self.area.DistanceObj(x,y,node)
        inNodes.sort(lambda a,b: cmp(nls[a],nls[b]))
        return inNodes
    
    
    
    
    def ObjectNoticed(self, rObject):
        inNodes = self.PositionToKMLNodes(rObject.x, rObject.y)
        if len(inNodes)>0:
            inNodes[0].Train(rObject, self.trainEffectNotice)
        return inNodes[0]
    
    def ObjectFound(self, rObject):
        pass
    
    def ObjectNotFound(self, rObject):
        pass
    
    def ObjectUsed(self, rObject):
        pass
    
    def ObjectUsedUp(self, rObject):
        pass
