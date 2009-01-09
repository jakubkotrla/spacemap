
from Enviroment.Global import Global
from math import sqrt
from Enviroment.Map import Point, Map

class PathFinderNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = []
        
        self.guiId = None
        self.mapRenderer = None
        
        
    def Render(self, mapRenderer):
        self.guiId = mapRenderer.CircleC(self, self.x, self.y, "darkgreen", 0.5, "energylayerpoint info")
        self.mapRenderer = mapRenderer
    def ToString(self):
        strInfo = []
        strXY = '%.4f'%(self.x) + "," + '%.4f'%(self.y)
        strInfo.append("PathFinderNode [" + strXY + "]")
        

class PathFinder:
    def __init__(self, area):
        self.area = area
        self.nodes = []
        self.mapRenderer = None
        
    def CreateMap(self):
        areaArea = self.area.GetArea()
        nodeCount = areaArea / Global.ELDensity ** 2

        xCount = self.area.width / Global.ELDensity
        yCount = self.area.height / Global.ELDensity
        density = Global.ELDensity
        for y in range(yCount):
            for x in range(xCount):
                xNoise = randint(-Global.ELCreateNoise, Global.ELCreateNoise)
                yNoise = randint(-Global.ELCreateNoise, Global.ELCreateNoise)
                xx = x*density+density/2+xNoise
                yy = y*density+density/2+yNoise
                
                if self.area.IsInside( Point(xx,yy) ):    
                    node = EnergyLayerNode(self, xx, yy, self.nodeIndex)
                    self.nodeIndex = self.nodeIndex + 1
                    self.nodes.append(node)
        
    def PositionToNodes(self, x, y):
        inNodes = []
        closestNode = None
        closestDistance = Global.MaxNumber
        per = Global.ELGravityRange
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
    
    def StepUpdate(self):
        
        for ep in self.energyPoints:
            ep.StepUpdate(self.getNodesAround(ep, Global.ELGravityRange))
        for node in self.nodes:
            node.StepUpdate(self.getNodesAround(node, Global.ELAntigravityRange))
        for node in self.nodes:
            node.StepUpdateMove()
        
        for ep in self.energyPointsToDelete:
            self.energyPoints.remove(ep)
        self.energyPointsToDelete = []

        #ToDo: melo by zaviset na poctu node
        diceRoll = randint(0, 100)
        self.forgetEnergy = self.forgetEnergy + 1
        if diceRoll < Global.ELForgetNodeChance*0:
            if self.forgetEnergy > self.GetNodeDeleteCost():
                self.forgetEnergy = self.forgetEnergy - self.GetNodeCreateDeleteCost()
                chosenNode = choice(self.nodes)
                chosenNode.Delete()
                self.nodes.remove(chosenNode)
            else:
                #nothing - not enough energy - should be in chance
                pass 
        
    def CreateNode(self, point, memObject):
        xNoise = randint(-Global.ELNodeAddNoise, Global.ELNodeAddNoise)
        yNoise = randint(-Global.ELNodeAddNoise, Global.ELNodeAddNoise)
        x = point.x + xNoise
        y = point.y + yNoise
        
        while not self.area.IsInside( Point(x,y) ):
            xNoise = randint(-Global.ELNodeAddNoise, Global.ELNodeAddNoise)
            yNoise = randint(-Global.ELNodeAddNoise, Global.ELNodeAddNoise)
            x = point.x + xNoise
            y = point.y + yNoise
            
        newNode = EnergyLayerNode(self, x, y, self.nodeIndex)
        self.nodeIndex = self.nodeIndex + 1
        self.nodes.append(newNode)
        newNode.Render(self.mapRenderer)
        
        memObject.AddLinkToNode(newNode)
        memObject.IntenseToNode(newNode, 1.0)   #ToDo should be some constant
        return newNode
    
    def Train(self, memObject, effect):
        foundEP = None
        for ep in self.energyPoints:
            if ep.x == memObject.x and ep.y == memObject.y:
                foundEP = ep
                break
        if foundEP != None:
            foundEP.energy = foundEP.energy + effect * Global.ELEnergyPointCreateCoef
        else:                
            ep = EnergyPoint(self, memObject, memObject.x, memObject.y, effect * Global.ELEnergyPointCreateCoef)
            self.energyPoints.append(ep)
            ep.Render(self.mapRenderer)
        
    def DeleteEneryPoint(self, energyPoint):
        self.energyPointsToDelete.append(energyPoint)
        
    def GetNodeCreateCost(self):
        desiredNodeCount = self.area.width * self.area.height / 100
        #cost = max(1, (1.0* len(self.nodes) - desiredNodeCount)) ** 2
        if len(self.nodes) - desiredNodeCount < 10: return 10
        cost = len(self.nodes) - desiredNodeCount + 10
        if cost > 100: cost = 100
        return cost
    def GetNodeDeleteCost(self):
        desiredNodeCount = self.area.width * self.area.height / 100
        cost = max(1, (desiredNodeCount - 1.0* len(self.nodes))) ** 2
        return cost
        
    def getNodesAround(self, node, range):
        nodesAround = []
        range = range ** 2
        for n in self.nodes:
            if n == node: continue
            dist = (n.x-node.x)**2+(n.y-node.y)**2
            if dist < range:
                nodesAround.append(n)
        return nodesAround

 
