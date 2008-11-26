
from Enviroment.Global import Global
from math import sqrt
from random import randint, choice
from copy import copy

class EnergyPoint:
    def __init__(self, layer, x, y, energy):
        self.layer = layer
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
        self.energy = 0
        for node in nodesAround:
            effect = 1
            node.Train(self, effect)
        #ToDo pritahnout nodes okolo, pripadne vytvorit novy node, odebrat energii
        if self.energy < 1:
            self.mapRenderer.DeleteGuiObject(self.guiId)
            self.layer.DeleteEneryPoint(self)
    

class EnergyLayerNode:
    def __init__(self, layer, x, y):
        self.layer = layer
        self.area = layer.area
        self.x = x
        self.y = y
        self.linkToObjects = []
        
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
        strInfo.append("EnergyLayerNode(" + self.info + ") [" + strXY + "]")
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
                
    def StepUpdate(self, nodesAround):
        diffX = 0
        diffY = 0
            
        for node in nodesAround:
            ldx = (self.x - node.x) 
            ldy = (self.y - node.y)
            dist = sqrt(ldx**2+ldy**2)
            if dist < Global.EnergyLayerAntigravityRange:
                
                gCoef = 1 / max(Global.MinPositiveNumber, dist**2)

                usageCoef = Global.EnergyLayerNodeUsageCoef / (max(1, self.GetUsage())*max(1,node.GetUsage()))
                gCoef = gCoef * usageCoef
                gCoef = min(1, gCoef)
                
                gCoef = gCoef * (1.0/max(1, self.GetUsage()))
                
                diffX = Global.EnergyLayerAntigravityCoef * gCoef * Global.Sign(ldx)
                diffY = Global.EnergyLayerAntigravityCoef * gCoef * Global.Sign(ldy)
                
                self.stepDiffX += diffX
                self.stepDiffY += diffY
            else:
                Global.Log("Programmer.Error EnergyLayerNode.StepUpdate", "error")
        
        
    def StepUpdateMove(self):
        self.x = self.x + self.stepDiffX
        self.y = self.y + self.stepDiffY
        if self.x < 1: self.x = 1
        if self.y < 1: self.y = 1
        if self.x > self.area.width-1: self.x = self.area.width-1
        if self.y > self.area.height-1: self.y = self.area.height-1 
        self.renderMove()
        self.stepDiffX = 0
        self.stepDiffY = 0
            
    def Train(self, point, effect):
        difX = point.x - self.x
        difY = point.y - self.y
        dist = sqrt(difX**2+difY**2)
        
        gCoef = 1 / max(Global.MinPositiveNumber, dist**2)
        #gCoef = gCoef * (1.0/max(1, self.GetUsage()))
        
        lCoef = Global.EnergyLayerGravityCoef * gCoef * effect
        difX *= min(1, lCoef)
        difY *= min(1, lCoef)

        self.x = self.x + difX
        self.y = self.y + difY
        
        if self.x < 1: self.x = 1
        if self.y < 1: self.y = 1
        if self.x > self.area.width-1: self.x = self.area.width-1
        if self.y > self.area.height-1: self.y = self.area.height-1 
        self.renderMove()
            


class EnergyLayer:
    def __init__(self, area):
        self.area = area
        self.nodes = []
        self.energyPoints = []
        self.energyPointsToDelete = []
        self.mapRenderer = None
        
    def CreateMap(self):
        density = Global.EnergyLayerDensity
        xCount = self.area.width / density
        yCount = self.area.height / density
        for y in range(yCount):
            for x in range(xCount):
                xNoise = randint(-Global.EnergyLayerCreateNoise, Global.EnergyLayerCreateNoise)
                yNoise = randint(-Global.EnergyLayerCreateNoise, Global.EnergyLayerCreateNoise)
                
                node = EnergyLayerNode(self, x*density+density/2+xNoise, y*density+density/2+yNoise)
                self.nodes.append(node)
                node.info = str(x) + "," + str(y) 
        
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
        if diceRoll < Global.EnergyLayerForgetNodeChance:
            chosenNode = choice(self.nodes)
            chosenNode.Delete()
            self.nodes.remove(chosenNode)
        
    def AddNode(self, parentNode):
        xNoise = randint(-Global.EnergyLayerCreateNoise, Global.EnergyLayerCreateNoise)
        yNoise = randint(-Global.EnergyLayerCreateNoise, Global.EnergyLayerCreateNoise)
                
        x = parentNode.x + xNoise
        y = parentNode.y + yNoise
        newNode = EnergyLayerNode(self, x, y)
        self.nodes.append(newNode)
        newNode.info = str(x) + "," + str(y)
        
        newNode.linkToObjects = copy(parentNode.linkToObjects)
        return newNode
    
    def Train(self, memObject, effect):
        ep = EnergyPoint(self, memObject.x, memObject.y, effect * Global.EnergyLayerEnergyPointCreateCoef)
        self.energyPoints.append(ep)
        ep.Render(self.mapRenderer)
        
    def DeleteEneryPoint(self, energyPoint):
        self.energyPointsToDelete.append(energyPoint)
        
    def getNodesAround(self, node, range):
        map = Global.Map
        nodesAround = []
        for n in self.nodes:
            if n == node: continue
            dist = map.DistanceObjs(n, node)
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
