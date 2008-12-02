
from Enviroment.Global import Global
from math import sqrt
from random import randint, choice, random

class EnergyPoint:
    def __init__(self, layer, memObject, x, y, energy):
        self.layer = layer
        self.memObject = memObject
        self.x = x
        self.y = y
        self.energy = energy
        
        self.guiId = None
        self.mapRenderer = None
        
        
    def Render(self, mapRenderer):
        self.guiId = mapRenderer.CircleC(self, self.x, self.y, "darkgreen", 0.5, "energylayerpoint info")
        self.mapRenderer = mapRenderer
    def ToString(self):
        strInfo = []
        strXY = '%.4f'%(self.x) + "," + '%.4f'%(self.y)
        strInfo.append("EnergyLayerPoint(" + self.info + ") [" + strXY + "] energy:" + str(self.energy))
        
    def StepUpdate(self, nodesAround):
        cost = self.layer.GetNodeCreateCost()
        chanceNew = self.energy - cost
        diceRoll = randint(0, 100)
        if diceRoll < chanceNew:
            self.layer.CreateNode(self, self.memObject)
            self.energy = self.energy - cost
        
        #get effect - gravity strength
        effect = self.energy / Global.EnergyLayerEnergyPointCreateCoef
            
        for node in nodesAround:
            node.Train(self, effect)

        self.energy = self.energy * Global.EnergyLayerEnergyFadeCoef
        if self.energy < Global.EnergyLayerEnergyFadeLimit:
            self.mapRenderer.DeleteGuiObject(self.guiId)
            self.layer.DeleteEneryPoint(self)
    

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
        
        self.guiId = None
        self.mapRenderer = None
        
    def Render(self, mapRenderer):
        self.guiId = mapRenderer.PixelC(self, self.x, self.y, "green", 2, "energylayernode info")
        self.mapRenderer = mapRenderer
    def renderMove(self):
        self.mapRenderer.DeleteGuiObject(self.guiId)
        self.guiId = self.mapRenderer.PixelC(self, self.x, self.y, "green", 2, "energylayernode info")
    def renderDelete(self):
        self.mapRenderer.DeleteGuiObject(self.guiId)
    def ToString(self):
        strInfo = []
        strXY = '%.4f'%(self.x) + "," + '%.4f'%(self.y)
        strInfo.append("EnergyLayerNode" + str(self.index) + "(" + self.info + ") [" + strXY + "]")
        for link in self.linkToObjects:
            strInfo.append(link.ToString())        
        return strInfo

    def Delete(self):
        self.renderDelete()
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

            gCoef = 1.0 / max(Global.MinPositiveNumber, dist2)

            usageCoef = Global.EnergyLayerNodeUsageCoef / (max(1, self.GetUsage())*max(1,node.GetUsage()))
            usageCoef = min(1, usageCoef)
            gCoef = gCoef * usageCoef
            
            gCoef = min(1, gCoef)
            gCoef = gCoef * (random() * 0.4 + 0.8) #Global.EnergyLayerAntigravityNoise
            
            gDiff = Global.EnergyLayerAntigravityCoef * gCoef
            gDiffCoef = gDiff /  max(Global.MinPositiveNumber, dist) 
            
            diffX = ldx * gDiffCoef
            diffY = ldy * gDiffCoef
            
            self.stepDiffX += diffX
            self.stepDiffY += diffY
        for link in self.linkToObjects:
            link.StepUpdate()
        
        
    def StepUpdateMove(self):
        massCoef = 1.0/max(1, self.GetUsage())
        
        self.x = self.x + self.stepDiffX * massCoef
        self.y = self.y + self.stepDiffY * massCoef
        if self.x < 1: self.x = 1
        if self.y < 1: self.y = 1
        if self.x > self.area.width-1: self.x = self.area.width-1
        if self.y > self.area.height-1: self.y = self.area.height-1 
        self.renderMove()
        self.stepDiffX = 0
        self.stepDiffY = 0
            
    def Train(self, point, effect):
        diffX = point.x - self.x
        diffY = point.y - self.y
        if diffX == diffY == 0: return
        
        #dist = sqrt(diffX**2+diffY**2)
        #gCoef = 1.0 / dist**2
        gCoef = 1.0 / (diffX**2+diffY**2)
        
        gCoef = gCoef * (1.0/max(0.1, self.GetUsage()))
        
        gCoef = gCoef * (random() * 0.4 + 0.8) #Global.EnergyLayerGravityNoise
        
        gCoef = gCoef * effect
        
        gCoef = min(1, gCoef)
        self.x = self.x + diffX * gCoef
        self.y = self.y + diffY * gCoef
        
        self.renderMove()
            


class EnergyLayer:
    def __init__(self, area):
        self.area = area
        self.nodes = []
        self.energyPoints = []
        self.energyPointsToDelete = []
        self.forgetEnergy = 0
        self.mapRenderer = None
        self.nodeIndex = 1
        
    def CreateMap(self):
        density = Global.EnergyLayerDensity
        xCount = self.area.width / density
        yCount = self.area.height / density
        
        if Global.EnergyLayerCreateNoise == -1:
            count = xCount * yCount
            for i in range(count):
                x = randint(0, self.area.width-1)
                y = randint(0, self.area.height-1)
                node = EnergyLayerNode(self, x, y, self.nodeIndex)
                self.nodeIndex = self.nodeIndex + 1
                self.nodes.append(node)
                node.info = str(x) + "," + str(y)
        else: 
            for y in range(yCount):
                for x in range(xCount):
                    xNoise = randint(-Global.EnergyLayerCreateNoise, Global.EnergyLayerCreateNoise)
                    yNoise = randint(-Global.EnergyLayerCreateNoise, Global.EnergyLayerCreateNoise)
                    x = x*density+density/2+xNoise
                    y = y*density+density/2+yNoise
                    node = EnergyLayerNode(self, x, y, self.nodeIndex)
                    self.nodeIndex = self.nodeIndex + 1
                    self.nodes.append(node)
                    node.info = str(x) + "," + str(y)
        #end of Global.EnergyLayerCreateNoise == -1
        
    def PositionToNodes(self, x, y):
        inNodes = []
        closestNode = None
        closestDistance = Global.MaxNumber
        per = Global.EnergyLayerGravityRange
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
            ep.StepUpdate(self.getNodesAround(ep, Global.EnergyLayerGravityRange))
        for node in self.nodes:
            node.StepUpdate(self.getNodesAround(node, Global.EnergyLayerAntigravityRange))
        for node in self.nodes:
            node.StepUpdateMove()
            
        for ep in self.energyPointsToDelete:
            self.energyPoints.remove(ep)
        self.energyPointsToDelete = []

        #ToDo: melo by zaviset na poctu node
        diceRoll = randint(0, 100)
        self.forgetEnergy = self.forgetEnergy + 1
        if diceRoll < Global.EnergyLayerForgetNodeChance*0:
            if self.forgetEnergy > self.GetNodeDeleteCost():
                self.forgetEnergy = self.forgetEnergy - self.GetNodeCreateDeleteCost()
                chosenNode = choice(self.nodes)
                chosenNode.Delete()
                self.nodes.remove(chosenNode)
            else:
                #nothing - not enough energy - should be in chance
                pass 
        
    def CreateNode(self, point, memObject):
        xNoise = randint(-Global.EnergyLayerNodeAddNoise, Global.EnergyLayerNodeAddNoise)
        yNoise = randint(-Global.EnergyLayerNodeAddNoise, Global.EnergyLayerNodeAddNoise)
                
        x = point.x + xNoise
        y = point.y + yNoise
        newNode = EnergyLayerNode(self, x, y, self.nodeIndex)
        self.nodeIndex = self.nodeIndex + 1
        self.nodes.append(newNode)
        newNode.info = str(x) + "," + str(y)
        newNode.Render(self.mapRenderer)
        
        memObject.AddLinkToNode(newNode)
        memObject.IntenseToNode(newNode, 5)
        return newNode
    
    def Train(self, memObject, effect):
        foundEP = None
        for ep in self.energyPoints:
            if ep.x == memObject.x and ep.y == memObject.y:
                foundEP = ep
                break
        if foundEP != None:
            foundEP.energy = foundEP.energy + effect * Global.EnergyLayerEnergyPointCreateCoef
        else:                
            ep = EnergyPoint(self, memObject, memObject.x, memObject.y, effect * Global.EnergyLayerEnergyPointCreateCoef)
            self.energyPoints.append(ep)
            ep.Render(self.mapRenderer)
        
    def DeleteEneryPoint(self, energyPoint):
        self.energyPointsToDelete.append(energyPoint)
        
    def GetNodeCreateCost(self):
        desiredNodeCount = self.area.width * self.area.height / 100
        cost = max(1, (1.0* len(self.nodes) - desiredNodeCount)) ** 2
        return cost
    def GetNodeDeleteCost(self):
        desiredNodeCount = self.area.width * self.area.height / 100
        cost = max(1, (desiredNodeCount - 1.0* len(self.nodes))) ** 2
        return cost
        
    def getNodesAround(self, node, range):
        map = Global.Map
        nodesAround = []
        range = range ** 2
        for n in self.nodes:
            if n == node: continue
            dist = (n.x-node.x)**2+(n.y-node.y)**2 #map.DistanceObjs(n, node)
            if dist < range:
                nodesAround.append(n)
        return nodesAround

    
    def ObjectNoticed(self, memObject, intensity=1):
        self.Train(memObject, Global.TrainEffectNotice)
    
    def ObjectFound(self, rObject):
        pass
    
    def ObjectNotFound(self, rObject):
        pass
    
    def ObjectUsed(self, rObject):
        pass
    
    def ObjectUsedUp(self, rObject):
        pass
