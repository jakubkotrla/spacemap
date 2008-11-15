
from Enviroment.Global import Global
from math import sqrt
from collections import deque
from Enviroment.Objects import InternalLearningObj

class KohonenMapLayerNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = []
        self.linkToObjects = []
        
        self.guiId = None
        self.guiLinesIds = {}
        self.mapRenderer = None
        
    def Render(self, mapRenderer):
        self.guiId = mapRenderer.PixelC(self, self.x, self.y, "green", 2, "kohonenmaplayernode info")
        
        for neighbour in self.neighbours:
            if neighbour not in self.guiLinesIds.keys():
                lineId = mapRenderer.Line(self.x, self.y, neighbour.x, neighbour.y, "green", "kmlline")
                self.guiLinesIds[neighbour] = lineId
                neighbour.guiLinesIds[self] = lineId
        self.mapRenderer = mapRenderer
    
    def renderMove(self):
        self.mapRenderer.DeleteGuiObject(self.guiId)
        for lineId in self.guiLinesIds.values():
            self.mapRenderer.DeleteGuiObject(lineId)
        self.guiLinesIds = {}
                    
        self.guiId = self.mapRenderer.PixelC(self, self.x, self.y, "green", 2, "kohonenmaplayernode info")
        for neighbour in self.neighbours:
            lineId = self.mapRenderer.Line(self.x, self.y, neighbour.x, neighbour.y, "green", "kmlline")
            self.guiLinesIds[neighbour] = lineId
            neighbour.guiLinesIds[self] = lineId
                
    def ToString(self):
        strInfo = []
        strInfo.append("KohonenMapLayerNode [" + str(self.x) + "," + str(self.y) + "]")
        for link in self.linkToObjects:
            strInfo.append(link.ToString())        
        return strInfo
                
    def Train(self, memObject, effect, neighboursCoef, nodesAround):
        neighboursCoef = Global.Gauss(neighboursCoef)
        if neighboursCoef < Global.KMLayerNeighbourLimit: return
        
        # Wv(t + 1) = Wv(t) + neighboursCoef(v, t)*learnCoef(t)(D(t) - Wv(t))
        difX = memObject.x - self.x
        difY = memObject.y - self.y
        
        lCoef = neighboursCoef * Global.KMLayerLearningCoef * effect #ToDo * memObject.attractivity*1.0/memObject.maxAttractivity
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
                Global.Log("Programmer.Error KMLNode.Train")
        self.x = self.x + difX
        self.y = self.y + difY
        self.renderMove()
            



class KohonenMapLayer:
    def __init__(self, area):
        self.area = area
        self.nodes = []
        
    def CreateMap(self):
        density = Global.KMLayerDensity
        xCount = self.area.width / density
        yCount = self.area.height / density
        nodesMap = [[0 for col in range(xCount)] for row in range(yCount)]
        for y in range(yCount):
            for x in range(xCount):
                node = KohonenMapLayerNode(x*density+density/2, y*density+density/2)
                self.nodes.append(node)
                nodesMap[x][y] = node
                if y>0:
                    node.neighbours.append(nodesMap[x][y-1])
                    nodesMap[x][y-1].neighbours.append(node)
                if x>0:
                    node.neighbours.append(nodesMap[x-1][y])
                    nodesMap[x-1][y].neighbours.append(node)
                if Global.KMLayerUseBaseLineObjects:
                    map.AddObject(InternalLearningObj, x*density+density/2, y*density+density/2, Global.KMLayerBaseLineObjectAttractivity)
        
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
                if n == node: continue
                dist = map.DistanceObj(n.x, n.y, node)
                if dist < Global.KMLayerAntigravityRange:
                    nodesAround.append(n)
                    
            node.Train(memObject, effect, ncoef, nodesAround)
            trainedList.add(node)
            for n in node.neighbours:
                trainQueue.append([n,ncoef+1])
            
        
    
    def ObjectNoticed(self, memObject, intensity=1):
        inNodes = self.PositionToNodes(memObject.x, memObject.y)
        if Global.KMLayerTrainAll:
            for node in inNodes:
                self.Train(node, memObject, Global.TrainEffectNotice)
        else:
            self.Train(inNodes[0], memObject, Global.TrainEffectNotice)

    
    def ObjectFound(self, rObject):
        pass
    
    def ObjectNotFound(self, rObject):
        pass
    
    def ObjectUsed(self, rObject):
        pass
    
    def ObjectUsedUp(self, rObject):
        pass
