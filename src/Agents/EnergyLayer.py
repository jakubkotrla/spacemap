
from Enviroment.Global import Global
from math import sqrt
from Enviroment.Map import Point


class EnergyPoint:
    def __init__(self, layer, memObject, x, y, energy):
        self.layer = layer
        self.memObject = memObject
        self.x = x
        self.y = y
        self.energy = energy
       
        
    def ToString(self):
        strInfo = []
        strXY = '%.4f'%(self.x) + "," + '%.4f'%(self.y)
        strInfo.append("EnergyLayerPoint[" + strXY + "] energy:" + str(self.energy))
        
    def StepUpdate(self, nodesAround):
        cost = self.layer.GetNodeCreateCost()
        chanceNew = 100 * float(self.energy - cost) / cost
        diceRoll = Global.DiceRoll()
        if diceRoll < chanceNew:
            self.layer.CreateNode(self, self.memObject)
            self.energy = self.energy - cost
        
        effect = self.energy / Global.ELEnergyPointCreateEnergy
            
        for node in nodesAround:
            node.Train(self, effect)

        self.energy = self.energy * Global.ELEnergyFadeCoef
        if self.energy < Global.ELEnergyFadeLimit:
            self.layer.DeleteEnergyPoint(self)
    

class EnergyLayerNode:
    def __init__(self, layer, x, y, index):
        self.layer = layer
        self.area = layer.area
        self.x = x
        self.y = y
        self.linkToObjects = []
        self.index = index
                
        self.stepDiffX = 0
        self.stepDiffY = 0

    def ToString(self):
        strInfo = []
        strXY = '%.4f'%(self.x) + "," + '%.4f'%(self.y)
        strInfo.append("EnergyLayerNode" + str(self.index) + "[" + strXY + "]")
        for link in self.linkToObjects:
            strInfo.append(link.ToString())        
        return strInfo

    def Delete(self):
        for link in self.linkToObjects:
            link.NodeDeleted()

    def GetUsage(self):
        usage = 0
        for link in self.linkToObjects:
            usage = usage + link.intensity
        return usage
                
    def isMaxObject(self, objectName):
        maxUsage = 0
        maxObject = None
        for link in self.linkToObjects:
            if link.intensity > maxUsage:
                maxUsage = link.intensity
                maxObject = link.object
        if maxObject != None:
            if maxObject.type.name == objectName:
                return True
        return False
                
    def StepUpdate(self, nodesAround):
        diffX = 0
        diffY = 0
                    
        for node in nodesAround:
            ldx = (self.x - node.x) 
            ldy = (self.y - node.y)
            dist2 = ldx**2+ldy**2
            dist = sqrt(dist2)

            gDiffCoef = dist2 * max(0.5, self.GetUsage())*max(0.5,node.GetUsage())
            gDiffCoef = Global.ELAntigravityCoef*1.0 / max(Global.MinPositiveNumber, gDiffCoef)
            
            diffX = ldx * gDiffCoef
            diffY = ldy * gDiffCoef
            
            self.stepDiffX += diffX
            self.stepDiffY += diffY
       
        
    def StepUpdateMove(self):
        massCoef = 1.0/max(1, self.GetUsage())
        
        newX = self.x + self.stepDiffX * massCoef
        newY = self.y + self.stepDiffY * massCoef
        
        hit = self.area.CanMoveEx(self, newX, newY)
        if hit.hit:
            newX = hit.x
            newY = hit.y
        self.x = newX
        self.y = newY
        self.stepDiffX = self.stepDiffY = 0
            
    def Train(self, point, effect):
        diffX = point.x - self.x
        diffY = point.y - self.y
        if diffX == diffY == 0: return
        
        gCoef = 1.0 / (diffX**2+diffY**2)
        gCoef = gCoef * (1.0/max(0.1, self.GetUsage()))
        gCoef = gCoef * effect
        
        gCoef = Global.ELGravityCoef * min(1, gCoef)
        newX = self.x + diffX * gCoef
        newY = self.y + diffY * gCoef
        
        hit = self.area.CanMoveEx(self, newX, newY)
        if hit.hit:
            newX = hit.x
            newY = hit.y
        self.x = newX
        self.y = newY        
            


class EnergyLayer:
    def __init__(self, area):
        self.area = area
        self.nodes = []
        self.energyPoints = []
        self.energyPointsCountHistory = []
        self.energyPointsToDelete = []
        self.forgetEnergy = 0
        self.nodeIndex = 1
        self.desiredNodeCount = 0
        
    def CreateMap(self):
        areaArea = self.area.GetArea()
        nodeCount = areaArea / Global.ELDensity ** 2
        self.desiredNodeCount = nodeCount * 2
        
        if Global.ELCreateNoise > Global.ELDensity or Global.ELCreateNoise == -1:
            while len(self.nodes) < nodeCount:
                x = Global.Randint(0, self.area.width-1)
                y = Global.Randint(0, self.area.height-1)
                
                if self.area.IsInside( Point(x,y) ):                
                    node = EnergyLayerNode(self, x, y, self.nodeIndex)
                    self.nodeIndex = self.nodeIndex + 1
                    self.nodes.append(node)
        else:
            xCount = self.area.width / Global.ELDensity
            yCount = self.area.height / Global.ELDensity
            density = Global.ELDensity
            for y in range(yCount):
                for x in range(xCount):
                    xNoise = Global.Randint(-Global.ELCreateNoise, Global.ELCreateNoise)
                    yNoise = Global.Randint(-Global.ELCreateNoise, Global.ELCreateNoise)
                    xx = x*density+density/2+xNoise
                    yy = y*density+density/2+yNoise
                    
                    if self.area.IsInside( Point(xx,yy) ):    
                        node = EnergyLayerNode(self, xx, yy, self.nodeIndex)
                        self.nodeIndex = self.nodeIndex + 1
                        self.nodes.append(node)
        
    def PositionToNodes(self, x, y, per):
        inNodes = []
        closestNode = None
        closestDistance = Global.MaxNumber
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

        diceRoll = Global.DiceRoll()
        self.forgetEnergy = self.forgetEnergy + Global.ELForgetNodeRate
        cost = self.GetNodeDeleteCost()
        chanceForget = 100 * float(self.forgetEnergy - cost) / cost
        if diceRoll < chanceForget:
            self.forgetEnergy = self.forgetEnergy - cost
            self.DeleteNode(Global.Choice(self.nodes))
        self.energyPointsCountHistory.append(len(self.energyPoints))
     
    def DeleteNode(self, node):
        node.Delete()
        self.nodes.remove(node)
        nodesToRun = nodes = self.getNodesAround(node, Global.ELDeleteNodeReTrainRange) 
        for i in range(Global.ELDeleteNodeReTrainCount):
            for n in nodesToRun:
                n.StepUpdate(self.getNodesAround(n, Global.ELAntigravityRange))
                n.StepUpdateMove() 
        
    def CreateNode(self, point, memObject):
        xNoise = Global.Randint(-Global.ELNodeAddNoise, Global.ELNodeAddNoise)
        yNoise = Global.Randint(-Global.ELNodeAddNoise, Global.ELNodeAddNoise)
        x = point.x + xNoise
        y = point.y + yNoise
        
        while not self.area.IsInside( Point(x,y) ):
            xNoise = Global.Randint(-Global.ELNodeAddNoise, Global.ELNodeAddNoise)
            yNoise = Global.Randint(-Global.ELNodeAddNoise, Global.ELNodeAddNoise)
            x = point.x + xNoise
            y = point.y + yNoise
            
        newNode = EnergyLayerNode(self, x, y, self.nodeIndex)
        self.nodeIndex = self.nodeIndex + 1
        self.nodes.append(newNode)
        
        memObject.AddLinkToNode(newNode)
        memObject.IntenseToNode(newNode, Global.MemObjIntenseToNewNode)
        return newNode
    
    def Train(self, memObject, effect):
        foundEP = None
        for ep in self.energyPoints:
            if ep.x == memObject.x and ep.y == memObject.y:
                foundEP = ep
                break
        if foundEP != None:
            foundEP.energy = foundEP.energy + effect * Global.ELEnergyPointCreateEnergy
        else:                
            ep = EnergyPoint(self, memObject, memObject.x, memObject.y, effect * Global.ELEnergyPointCreateEnergy)
            self.energyPoints.append(ep)
        
    def DeleteEnergyPoint(self, energyPoint):
        self.energyPointsToDelete.append(energyPoint)
        
    def GetNodeCreateCost(self):
        x = 200 * float(len(self.nodes) - self.desiredNodeCount) / self.desiredNodeCount
        cost = 100 * (3 ** (float(x)/50))
        return cost
    def GetNodeDeleteCost(self):
        x = 200 * float(len(self.nodes) - self.desiredNodeCount) / self.desiredNodeCount
        cost = 100 * (3 ** (float(-x)/50))
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

 
