
from Enviroment.Global import Global
from math import sqrt
from collections import deque

class GravityLayerNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.linkToObjects = []
        
        self.guiId = None
        self.mapRenderer = None
        
    def Train(self, rObject, effect, nn):
        difX = rObject.x - self.x
        difY = rObject.y - self.y
        
        map = Global.Map
        gCoef = map.DistanceObjs(self, rObject)
        
        lCoef = effect * rObject.attractivity*1.0/rObject.maxAttractivity
        difX *= lCoef
        difY *= lCoef
        #we have vector of learning, now vector of anti-gravity with neighbours...
        antiGcoef = 0.5 #0.5 - switched off
        for n in nn:   # ToDo: must work for actual space neighbours not just in KHmap
            ldx = (self.x - n.x) 
            ldy = (self.y - n.y)
            
            dist = sqrt(ldx**2+ldy**2)
            if dist < self.minimumDistance:
                difX += ldx * antiGcoef
                difY += ldy * antiGcoef
      
        self.x = self.x + difX
        self.y = self.y + difY
            


class GravityLayer:
    def __init__(self, area):
        self.area = area
        self.nodes = []
        
    def CreateMap(self, map):
        xCount = self.area.width / self.density
        yCount = self.area.height / self.density
        nodesMap = [[0 for col in range(xCount)] for row in range(yCount)]
        for y in range(yCount):
            for x in range(xCount):
                node = GravityLayerNode(x*self.density+self.density/2, y*self.density+self.density/2)
                self.nodes.append(node)
                nodesMap[x][y] = node
                if y>0:
                    node.neighbours.append(nodesMap[x][y-1])
                    nodesMap[x][y-1].neighbours.append(node)
                if x>0:
                    node.neighbours.append(nodesMap[x-1][y])
                    nodesMap[x-1][y].neighbours.append(node)
                # baseline objects
                #map.AddObject(InternalLearningObj, x*self.density+self.density/2, y*self.density+self.density/2, 5)
        
    def PositionToNodes(self, x, y):
        inNodes = []
        closestNode = None
        closestDistance = Global.MaxNumber
        per = Global.KMLayerNodeSize
        map = Global.Map
        for node in self.nodes:
            distance = map.DistanceObj(x, y, node)
            if distance < closestDistance:
                closestNode = node
                closestDistance = distance
            if node.x-per < x < node.x+per and node.y-per < y < node.y+per:
                inNodes.append(node)
        if len(inNodes) > 0:
            nls = {}
            for node in inNodes:
                nls[node] = map.DistanceObj(x,y,node)
            inNodes.sort(lambda a,b: cmp(nls[a],nls[b]))
            return inNodes
        else:
            return [closestNode]
    
    def Train(self, node, memObject, effect):
        trainQueue = deque([[node,0]])
        trainedList = set()
        
        map = Global.Map
        
        while trainQueue:
            [node,ncoef] = trainQueue.popleft()
            if node in trainedList: continue
            
            nn = []
            for n in self.nodes:
                dist = map.DistanceObj(n.x, n.y, node)
                if dist < node.minimumDistance:
                    nn.append(n)
            node.Train(memObject, effect, ncoef, nn)
            trainedList.add(node)
            for n in node.neighbours:
                trainQueue.append([n,ncoef+1])
            
        
    
    def ObjectNoticed(self, memObject, intensity):
        inNodes = self.PositionToKMLNodes(memObject.x, memObject.y)
        for node in inNodes:
            self.Train(node, memObject, self.trainEffectNotice)
        return inNodes[0]
    
    def ObjectFound(self, rObject):
        pass
    
    def ObjectNotFound(self, rObject):
        pass
    
    def ObjectUsed(self, rObject):
        pass
    
    def ObjectUsedUp(self, rObject):
        pass
