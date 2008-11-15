
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
        
    def Render(self, mapRenderer):
        self.guiId = mapRenderer.PixelC(self, self.x, self.y, "green", 2, "gravitylayernode info")
        self.mapRenderer = mapRenderer
    
    def renderMove(self):
        self.mapRenderer.DeleteGuiObject(self.guiId)
        self.guiId = self.mapRenderer.PixelC(self, self.x, self.y, "green", 2, "gravitylayernode info")
                
    def ToString(self):
        strInfo = []
        strInfo.append("GravityLayerNode [" + str(self.x) + "," + str(self.y) + "]")
        for link in self.linkToObjects:
            strInfo.append(link.ToString())        
        return strInfo
                
    def Train(self, memObject, effect, nodesAround):
        difX = memObject.x - self.x
        difY = memObject.y - self.y
        
        lCoef = effect #ToDo * memObject.attractivity*1.0/memObject.maxAttractivity
        difX *= lCoef
        difY *= lCoef
        
        #we have vector of learning, now vector of anti-gravity with neighbours...
        for node in nodesAround:
            ldx = (self.x - node.x) 
            ldy = (self.y - node.y)
            dist = sqrt(ldx**2+ldy**2)
            if dist < Global.KMLayerAntigravityRange:
                difX += ldx * Global.KMLayerAntigravityCoef / dist**2   #imitate Newton law a little
                difY += ldy * Global.KMLayerAntigravityCoef / dist**2
            else:
                Global.Log("Programmer.Error GravityLayerNode.Train")
        self.x = self.x + difX
        self.y = self.y + difY
        self.renderMove()
            


class GravityLayer:
    def __init__(self, area):
        self.area = area
        self.nodes = []
        
    def CreateMap(self, map):
        xCount = self.area.width / self.density
        yCount = self.area.height / self.density
        for y in range(yCount):
            for x in range(xCount):
                node = GravityLayerNode(x*self.density+self.density/2, y*self.density+self.density/2)
                self.nodes.append(node)
        
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
            
            nodesAround = []
            for n in self.nodes:
                dist = map.DistanceObj(n.x, n.y, node)
                if dist < node.minimumDistance:
                    nodesAround.append(n)
            node.Train(memObject, effect, ncoef, nodesAround)
            trainedList.add(node)
            for n in node.neighbours:
                trainQueue.append([n,ncoef+1])
            
        
    
    def ObjectNoticed(self, memObject, intensity):
        inNodes = self.PositionToNodes(memObject.x, memObject.y)
        for node in inNodes:
            self.Train(node, memObject, self.trainEffectNotice)
    
    def ObjectFound(self, rObject):
        pass
    
    def ObjectNotFound(self, rObject):
        pass
    
    def ObjectUsed(self, rObject):
        pass
    
    def ObjectUsedUp(self, rObject):
        pass
