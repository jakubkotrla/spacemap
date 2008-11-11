
from Enviroment.Global import Global
from math import exp
from collections import deque

class KMLNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = []
        self.size = 10  #ToDo use a constant for setting
        self.objects = []
        self.learnCoef = 0.2    #ToDo make a constant
        self.neighboursCoefLimit = 0 #ToDo make a constant
        
    def Train(self, rObject, effect, neighboursCoef):
        nG = self.Gausse(neighboursCoef)
        if nG < self.neighboursCoefLimit: return 
        
        # Wv(t + 1) = Wv(t) + neighboursCoef(v, t)*learnCoef(t)(D(t) - Wv(t))
        difX = rObject.x - self.x
        difY = rObject.y - self.y
        
        lCoef = nG * self.learnCoef * effect
        
        self.x = self.x + difX * lCoef
        self.y = self.y + difY * lCoef
        self.guiMoved(self)
            
    def Gausse(self, x):
        return exp( - ((x)**2) / 2 )


class KMLayer:
    def __init__(self, area):
        self.area = area
        self.nodes = []
        self.trainEffectNotice = 1
        self.density = 10
        
    def CreateMap(self):
        xCount = self.area.width / self.density
        yCount = self.area.height / self.density
        nodesMap = [[0 for col in range(xCount)] for row in range(yCount)]
        for y in range(yCount):
            for x in range(xCount):
                node = KMLNode(x*self.density+self.density/2, y*self.density+self.density/2)
                self.nodes.append(node)
                nodesMap[x][y] = node
                if y>0:
                    node.neighbours.append(nodesMap[x][y-1])
                    nodesMap[x][y-1].neighbours.append(node)
                if x>0:
                    node.neighbours.append(nodesMap[x-1][y])
                    nodesMap[x-1][y].neighbours.append(node)
        
    def PositionToKMLNodes(self, x, y):
        inNodes = []
        closestNode = None
        closestDistance = 9999999
        map = Global.Map
        for node in self.nodes:
            distance = map.DistanceObj(x, y, node)
            if distance < closestDistance:
                closestNode = node
                closestDistance = distance
            if node.x-node.size < x < node.x+node.size and node.y-node.size < y < node.y+node.size:
                inNodes.append(node)
        if len(inNodes) > 0:
            nls = {}
            for node in inNodes:
                nls[node] = self.area.DistanceObj(x,y,node)
            inNodes.sort(lambda a,b: cmp(nls[a],nls[b]))
            return inNodes
        else:
            return [closestNode]
    
    def Train(self, node, rObject, effect):
        trainQueue = deque([[node,0]])
        trainedList = set()
        
        neighboursCoef = 0
        
        while trainQueue:
            [node,ncoef] = trainQueue.popleft()
            if node in trainedList: continue
            node.Train(rObject, effect, ncoef)
            trainedList.add(node)
            for n in node.neighbours:
                trainQueue.append([n,ncoef+1])
            
        
    
    def ObjectNoticed(self, rObject):
        inNodes = self.PositionToKMLNodes(rObject.x, rObject.y)
        if len(inNodes)>0:
            self.Train(inNodes[0], rObject, self.trainEffectNotice)
            return inNodes[0]
        #should never happen
        return None
    
    def ObjectFound(self, rObject):
        pass
    
    def ObjectNotFound(self, rObject):
        pass
    
    def ObjectUsed(self, rObject):
        pass
    
    def ObjectUsedUp(self, rObject):
        pass
