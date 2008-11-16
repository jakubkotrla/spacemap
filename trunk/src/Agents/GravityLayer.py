
from Enviroment.Global import Global
from math import sqrt
from random import randint

class GravityLayerNode:
    def __init__(self, area, x, y):
        self.area = area
        self.x = x
        self.y = y
        self.linkToObjects = []
        
        self.info = ""
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
        strInfo.append("GravityLayerNode(" + self.info + ") [" + str(self.x) + "," + str(self.y) + "]")
        for link in self.linkToObjects:
            strInfo.append(link.ToString())        
        return strInfo

    def GetUsage(self):
        usage = 0
        for link in self.linkToObjects:
            usage = usage + link.intensity
        return usage
                
    def StepUpdate(self, nodesAround):
        difX = 0
        difY = 0
        for node in nodesAround:
            ldx = (self.x - node.x) 
            ldy = (self.y - node.y)
            dist = sqrt(ldx**2+ldy**2)
            if dist < Global.GravLayerAntigravityRange:
                
                if Global.GravLayerUseGauss: gCoef = Global.Gauss(dist * Global.GravLayerDistanceCoef)
                else: gCoef = 1 / dist**2
                
                #anti-gravity is based on node usage
                usageCoef = Global.GravLayerNodeUsageMax / max(1, self.GetUsage()+node.GetUsage())
                gCoef = gCoef * usageCoef
                Global.Log("GLN.StepUpdate usageCoef=" + str(usageCoef), "grav") 
                
                difX += ldx * Global.GravLayerAntigravityCoef * gCoef
                difY += ldy * Global.GravLayerAntigravityCoef * gCoef
            else:
                Global.Log("Programmer.Error GravityLayerNode.StepUpdate", "error")
        self.x = self.x + difX
        self.y = self.y + difY
        
        if self.x < 1: self.x = 1
        if self.y < 1: self.y = 1
        if self.x > self.area.width-1: self.x = self.area.width-1
        if self.y > self.area.height-1: self.y = self.area.height-1 
        self.renderMove()
        
            
    def Train(self, memObject, effect, nodesAround):
        difX = memObject.x - self.x
        difY = memObject.y - self.y
        dist = sqrt(difX**2+difY**2)
        
        if Global.GravLayerUseGauss: gCoef = Global.Gauss(dist * Global.GravLayerDistanceCoef)
        else: gCoef = 1 / dist**2
        Global.Log("GLN.Train gCoef=" + str(gCoef), "grav")
        
        
        lCoef = Global.GravLayerGravityCoef * gCoef * effect #ToDo * memObject.attractivity*1.0/memObject.maxAttractivity
        difX *= lCoef
        difY *= lCoef
        
        for node in nodesAround:
            ldx = (self.x - node.x) 
            ldy = (self.y - node.y)
            dist = sqrt(ldx**2+ldy**2)
            if dist < Global.GravLayerAntigravityRange:
                
                if Global.GravLayerUseGauss: gCoef = Global.Gauss(dist * Global.GravLayerDistanceCoef)
                else: gCoef = 1 / dist**2
                
                #anti-gravity is based on node usage
                usageCoef = Global.GravLayerNodeUsageMax / max(1, self.GetUsage()+node.GetUsage())
                #gCoef = gCoef * usageCoef
                Global.Log("GLN.Train usageCoef=" + str(usageCoef), "grav") 
                
                difX += ldx * Global.GravLayerAntigravityCoef * gCoef
                difY += ldy * Global.GravLayerAntigravityCoef * gCoef
            else:
                Global.Log("Programmer.Error GravityLayerNode.Train", "error")
        self.x = self.x + difX
        self.y = self.y + difY
        
        if self.x < 1: self.x = 1
        if self.y < 1: self.y = 1
        if self.x > self.area.width-1: self.x = self.area.width-1
        if self.y > self.area.height-1: self.y = self.area.height-1 
        self.renderMove()
            


class GravityLayer:
    def __init__(self, area):
        self.area = area
        self.nodes = []
        
    def CreateMap(self):
        density = Global.GravLayerDensity
        xCount = self.area.width / density
        yCount = self.area.height / density
        for y in range(yCount):
            for x in range(xCount):
                xNoise = randint(-Global.GravLayerNoise, Global.GravLayerNoise)
                yNoise = randint(-Global.GravLayerNoise, Global.GravLayerNoise)
                
                node = GravityLayerNode(self.area, x*density+density/2+xNoise, y*density+density/2+yNoise)
                self.nodes.append(node)
                node.info = str(x) + "," + str(y) 
        
    def PositionToNodes(self, x, y):
        inNodes = []
        closestNode = None
        closestDistance = Global.MaxNumber
        per = Global.GravLayerGravityRange
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
        if not Global.GravLayerAntigravityEveryStep: return
        map = Global.Map
        for node in self.nodes:
            nodesAround = []
            for n in self.nodes:
                if n == node: continue
                dist = map.DistanceObjs(n, node)
                if dist < Global.GravLayerAntigravityRange:
                    nodesAround.append(n)
            node.StepUpdate(nodesAround)
        
    
    def Train(self, node, memObject, effect):
        map = Global.Map
        nodesAround = []
        if not Global.GravLayerAntigravityEveryStep:
            for n in self.nodes:
                if n == node: continue
                dist = map.DistanceObjs(n, node)
                if dist < Global.GravLayerAntigravityRange:
                    nodesAround.append(n)
        node.Train(memObject, effect, nodesAround)
            
        
    
    def ObjectNoticed(self, memObject, intensity=1):
        inNodes = self.PositionToNodes(memObject.x, memObject.y)
        for node in inNodes:
            self.Train(node, memObject, Global.TrainEffectNotice)
    
    def ObjectFound(self, rObject):
        pass
    
    def ObjectNotFound(self, rObject):
        pass
    
    def ObjectUsed(self, rObject):
        pass
    
    def ObjectUsedUp(self, rObject):
        pass
