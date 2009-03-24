
from Enviroment.Global import Global
from math import sqrt, fabs, log
from Enviroment.Map import Point
import copy


class ELHighNode:
    def __init__(self, layer, index, x, y):
        self.layer = layer
        self.index = index
        self.nodes = {}
        self.x = x
        self.y = y
        self.AGamount = 0
        self.range = 0
        
    def UpdateLocation(self):
        x = 0
        y = 0
        sumAGamount = 0
        for node in self.nodes:
            x += (node.x * self.nodes[node])
            y += (node.y * self.nodes[node])
            sumAGamount += self.nodes[node]
        x = x / sumAGamount
        y = y / sumAGamount
        p = Point(x,y)
        map = Global.Map
        if not map.IsInside(p):  #this should not happen, quick hack - go closer old location
            hit = map.CanMoveEx(self, p.x, p.y)
            if hit.hit:
                p = hit
            else:
                Global.Log("Programmer.Error: ELHLNode: not inside but canMove-not-hit")
        coef = (float(Global.HLAGNeededSum) / self.AGamount)
        dx = (p.x - self.x) * coef
        dy = (p.y - self.y) * coef
        self.x += dx 
        self.y += dy
   
    def StepUpdate(self):
        self.AGamount -=  Global.ELAGFadeOut * max(1, log(len(self.nodes))) 
        
        if self.AGamount < Global.HLAGNeededSum / 2:
            self.Delete()
            return True
        
        self.range = self.layer.GetRangeByAG(self.AGamount)
        
        if len(self.nodes) < 1:
            return False
        
        self.UpdateLocation()
        
        nodesAround = self.layer.getNodesAround(self, self.range)
        map = Global.Map
        nodesToRemove = []
        for node in self.nodes:
            dist = map.DistanceObjs(self, node)
            if dist > self.range:
                s = str(Global.GetStep()) + ";" + ("%.4f,%4f"%(self.x, self.y)) + ";removenode;" + str(node.index) + ";" + ("%.4f,%4f"%(node.x, node.y))
                Global.LogData("hlchanges", s)
                nodesToRemove.append(node)
        for node in nodesToRemove:
            self.AGamount -= self.nodes[node]
            del self.nodes[node]
            del node.hlNodes[self]
        for node in nodesAround:
            if node in self.nodes: continue
            s = str(Global.GetStep()) + ";" + ("%.4f,%4f"%(self.x, self.y)) + ";addnode;" + str(node.index) + ";" + ("%.4f,%4f"%(node.x, node.y))
            Global.LogData("hlchanges", s)
            self.nodes[node] = node.AGamount
            self.AGamount += node.AGamount
            node.hlNodes[self] = 0
            node.AGamount = 0
        s = str(Global.GetStep()) + ";" + str(self.index) + ";" + ("%.4f,%.4f"%(self.x, self.y)) + ";" + str(self.range) + ";" + str(self.AGamount) + ";" + str(len(self.nodes))   
        Global.LogData("hlnodes", s)
        return False
        
    def Delete(self):
        for node in self.nodes:
            del node.hlNodes[self]
    def ToString(self):
        strXY = '%.2f'%(self.x) + ";" + '%.2f'%(self.y)
        return "HLEnergyLayerNode[" + strXY + "].range = " + str(self.range)
        
class EnergyPoint:
    def __init__(self, layer, memObject, x, y, energy):
        self.layer = layer
        self.memObject = memObject
        self.x = x
        self.y = y
        self.energy = energy
        
        effect = self.energy / Global.ELEnergyPointCreateEnergy
        self.intenseMemObjToNodes(effect)
        
    def ToString(self):
        strInfo = []
        strXY = '%.2f'%(self.x) + ";" + '%.2f'%(self.y)
        strInfo.append("EnergyPoint[" + strXY + "].energy = " + str(self.energy))
        
    def StepUpdate(self, nodesAround):
        cost = self.layer.GetNodeCreateCost()
        chanceNew = 100 * float(self.energy - cost) / cost
        diceRoll = Global.DiceRoll()
        if diceRoll < chanceNew:
            self.layer.CreateNode(self, self.memObject)
            self.energy = self.energy - cost
        
        effect = self.energy / Global.ELEnergyPointCreateEnergy
        
        self.intenseMemObjToNodes(effect)
        
        for node in nodesAround:
            node.Train(self, effect)

        self.energy = self.energy * Global.ELEnergyFadeCoef
        if self.energy < Global.ELEnergyFadeLimit:
            self.layer.DeleteEnergyPoint(self)
    
    def intenseMemObjToNodes(self, effect):
        inNodes = self.layer.PositionToNodes(self.memObject, Global.SMTrainRange)
        if inNodes == None: return  #there are no ELNodes - error paranoid, should not happen anyway
        nodesToIntensity = {}
        sumIntensity = 0
        inc = len(inNodes)
        
        for (node,dist) in inNodes.iteritems():
            #intensity = Global.Gauss( dist / Global.SMNodeAreaDivCoef, Global.SMNodeAreaGaussCoef)
            dist = max(1, dist)
            intensity = 1.0 / dist
            #inv = Global.SMNodeAreaDivCoef * Global.GaussInverse(intensity, Global.SMNodeAreaGaussCoef)
            intensity = max(Global.MinPositiveNumber, intensity)
            nodesToIntensity[node] = intensity
            sumIntensity = sumIntensity + intensity
        for node in inNodes:
            intensity = effect * nodesToIntensity[node] / sumIntensity
            self.memObject.IntenseToNode(node, intensity)
        
    

class EnergyLayerNode:
    def __init__(self, layer, x, y, index):
        self.layer = layer
        self.area = layer.area
        self.x = x
        self.y = y
        self.linkToObjects = []
        self.index = index
        self.usage = 0
        self.AGamount = 0
        self.hlNodes = {}
                
        self.stepDiffX = 0
        self.stepDiffY = 0

    def ToString(self):
        strInfo = []
        strXY = '%.2f'%(self.x) + ";" + '%.2f'%(self.y)
        usageStr = '%.4f'%( self.usage )
        AGstr = '%.4f'%( self.AGamount )
        strInfo.append("EnergyLayerNode" + str(self.index) + "[" + strXY + "].usage = " + usageStr + "; AG = " + AGstr)
        for link in self.linkToObjects:
            strInfo.append(link.ToString())        
        return strInfo

    def Delete(self):
        for link in self.linkToObjects:
            link.NodeDeleted()
        for hlNode in self.hlNodes:
            hlNode.AGamount -= hlNode.nodes[self]
            del hlNode.nodes[self]
    
    def Intense(self, intensity):
        self.usage += intensity
                
    def StepUpdate(self, nodesAround):
        for node in nodesAround:
            ldx = (self.x - node.x) 
            ldy = (self.y - node.y)
            dist2 = ldx*ldx+ldy*ldy
            dist = sqrt(dist2)

            self.AGamount += (1.0/ max(1, dist)) * Global.ELAGAddCoef
            
            gDiffCoef = dist2 * max(0.8, self.usage) * max(0.8,node.usage)
            gDiffCoef = float(Global.ELAntigravityCoef) / max(0.64, gDiffCoef)
            
            dist = max(Global.MinPositiveNumber, dist)
            self.stepDiffX += ldx * (gDiffCoef / dist) #Global.Sign(ldx)
            self.stepDiffY += ldy * (gDiffCoef / dist) #Global.Sign(ldy)
        
    def StepUpdateMove(self, saveStatus=True):
        massCoef = 1.0/max(1, self.usage)# * self.usage)

        dx = self.stepDiffX * massCoef
        dy = self.stepDiffY * massCoef
        maxDif = Global.MaxELNodeMove
        if fabs(dx) > maxDif:
            Global.Log("ELNode.StepUpdateMove: MaxELNodeMove reached: " + str(fabs(dx)))
            coef = maxDif / fabs(dx)
            dx = dx * coef
            dy = dy * coef
        if fabs(dy) > maxDif:
            Global.Log("ELNode.StepUpdateMove: MaxELNodeMove reached: " + str(fabs(dy)))
            coef = maxDif / fabs(dy)
            dx = dx * coef
            dy = dy * coef
            
        newX = self.x + dx
        newY = self.y + dy
        
        hit = self.area.CanMoveEx(self, newX, newY)
        if hit.hit:
            newX = hit.x
            newY = hit.y
        
        if saveStatus and Global.SaveELNodesStatus:
            ldx = newX - self.x
            ldy = newY - self.y
            distToMove = sqrt(ldx*ldx + ldy*ldy)
                     
        self.x = newX
        self.y = newY
        self.stepDiffX = self.stepDiffY = 0

        self.usage -= Global.ELNodeUsageFadeOut
        if self.usage < 0: self.usage = 0
        
        if len(self.hlNodes) > 0 and self.AGamount > 0:
            AGamountPart = self.AGamount / len(self.hlNodes)
            for hlNode in self.hlNodes:
                hlNode.AGamount += AGamountPart
                hlNode.nodes[self] += AGamountPart
            self.AGamount = 0  
        else: 
            self.AGamount -= Global.ELAGFadeOut
        
        if saveStatus and Global.SaveELNodesStatus:
            status = str(Global.GetStep()) + ";" + str(self.index) + ";%.4f;%.4f;%.4f"%(distToMove,self.usage,self.AGamount)
            Global.LogData("elnode-status", status)
           
    def Train(self, point, effect):
        diffX = point.x - self.x
        diffY = point.y - self.y
        if diffX == diffY == 0: return
        
        gCoef = 1.0 / (diffX*diffX+diffY*diffY)
        gCoef = gCoef * (1.0/max(0.1, self.usage))
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
        self.hlNodes = []
        self.energyPoints = []
        self.energyPointsToDelete = []
        self.forgetEnergy = 0
        self.nodeIndex = 1
        self.hlNodeIndex = 1
        self.desiredNodeCount = 0
        self.minimalDesiredNodeCount = 0
        self.maximalDesiredNodeCount = 0
        
        self.stepEPCreated = 0
        self.stepELNodesCreated = 0
        
    def CreateMap(self):
        areaArea = self.area.GetArea()
        nodeCount = areaArea / Global.ELDensity ** 2
        self.desiredNodeCount = nodeCount * 2
        self.minimalDesiredNodeCount = self.desiredNodeCount / 5
        self.maximalDesiredNodeCount = self.desiredNodeCount
        
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
        
    def PositionToNodes(self, center, per):
        inNodes = {}
        closestNode = None
        closestDistance = Global.MaxNumber
        map = Global.Map
        for node in self.nodes:
            if not self.area.CanMove(center, node.x, node.y): continue
            
            distance = map.DistanceObjs(center, node)
            if distance < closestDistance:
                closestNode = node
                closestDistance = distance
            if distance < per:
                inNodes[node] = distance
        if len(inNodes) > 0:
            return inNodes
        else:
            if closestNode != None:
                return {closestNode : closestDistance}
            else:
                return None
    
    def StepUpdate(self):
        for ep in self.energyPoints:
            ep.StepUpdate(self.getNodesAround(ep, Global.ELGravityRange))
        for node in self.nodes:
            node.StepUpdate(self.getNodesAround(node, Global.ELAntigravityRange))
        for node in self.nodes:
            node.StepUpdateMove()
        hlNodesToDelete = []
        for hlNode in self.hlNodes:
            if hlNode.StepUpdate():
                hlNodesToDelete.append(hlNode)
        for hlNode in hlNodesToDelete:
            self.hlNodes.remove(hlNode)
        
        for ep in self.energyPointsToDelete:
            self.energyPoints.remove(ep)
        self.energyPointsToDelete = []

        self.forgetEnergy = self.forgetEnergy + Global.ELForgetNodeRate
        cost = self.GetNodeDeleteCost()
        chanceForget = 100 * float(self.forgetEnergy - cost) / cost
        
        diceRoll = Global.DiceRoll()
        if diceRoll < chanceForget:
            self.forgetEnergy = self.forgetEnergy - cost
            self.DeleteNode(Global.Choice(self.nodes))

#        if self.stepEPCreated < 1 and self.desiredNodeCount > self.minimalDesiredNodeCount:
#            self.desiredNodeCount -= 0.5
#        else:
#            if self.desiredNodeCount < self.maximalDesiredNodeCount:
#                self.desiredNodeCount += 1
        Global.LogData("nc", self.Status())
        
    def StepUpdateBig(self):
        self.nodes.sort(lambda b,a: cmp(a.AGamount,b.AGamount))
        for node in self.nodes:
            if node.AGamount > Global.HLAGNeeded:
                if self.createHLNode(node):
                    Global.Log("EL: HighLevel node created at " + str(node.x) + ";" + str(node.y))

    def createHLNode(self, startNode):
        nodeDists = self.getAllNodesDist(startNode)
        nodes = self.nodes[:]
        nodes.remove(startNode)
        nodes.sort(lambda a,b: cmp(nodeDists[a],nodeDists[b]))
        
        hlNode = ELHighNode(self, self.hlNodeIndex, startNode.x, startNode.y)
        hlNode.nodes[startNode] = startNode.AGamount
        startNode.hlNodes[hlNode] = 0
        hlNode.AGamount = startNode.AGamount
        hlNode.range = self.GetRangeByAG(hlNode.AGamount)
        
        for node in nodes:
            if nodeDists[node] > hlNode.range: break
            
            hlNode.nodes[node] = node.AGamount
            node.hlNodes[hlNode] = 0
            hlNode.AGamount += node.AGamount            
            
            hlNode.UpdateLocation()
            hlNode.range = self.GetRangeByAG(hlNode.AGamount)
        
        if hlNode.AGamount > Global.HLAGNeededSum:
            for n in hlNode.nodes:
                n.AGamount = 0
            self.hlNodes.append(hlNode)
            self.hlNodeIndex += 1
            return True
        else:
            hlNode.Delete()
            return False
    def GetRangeByAG(self, AGEnergy):
        #return sqrt(AGEnergy / 1000)/2 + 2
        return log(AGEnergy / 1000) + 1
     
    def DeleteNode(self, node):
        node.Delete()
        self.nodes.remove(node)
        nodesToRun = nodes = self.getNodesAround(node, Global.ELDeleteNodeReTrainRange) 
        for i in range(Global.ELDeleteNodeReTrainCount):
            for n in nodesToRun:
                n.StepUpdate(self.getNodesAround(n, Global.ELAntigravityRange))
                n.StepUpdateMove(False)
        
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
        
        for hlNode in self.hlNodes:
            dist = self.area.DistanceObjs(newNode, hlNode)
            if dist < hlNode.range:
                hlNode.nodes[newNode] = 0
                newNode.hlNodes[hlNode] = 0
        
        memObject.AddLinkToNode(newNode)
        memObject.IntenseToNode(newNode, Global.MemObjIntenseToNewNode)
        self.stepELNodesCreated = self.stepELNodesCreated + 1
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
        self.stepEPCreated += effect * Global.ELEnergyPointCreateEnergy
        
    def DeleteEnergyPoint(self, energyPoint):
        self.energyPointsToDelete.append(energyPoint)
    
    def Status(self):
        strObjs = str(len(self.area.objects))
        s = str(len(self.nodes)) + ";" + str(self.stepEPCreated) + ";" + str(self.stepELNodesCreated) + ";" + str(self.desiredNodeCount) + ";" + strObjs
        self.stepEPCreated = 0
        self.stepELNodesCreated = 0
        return s
    
    def SaveHeatMap(self):
        for n in self.nodes:
            nStr = "%d;%d;%.4f;%.4f" % (int(n.x), int(n.y), n.usage, n.AGamount)
            Global.LogData("elnodeheatmap", nStr)
        
    def GetNodeCreateCost(self):
        x = 50 * float(len(self.nodes) - self.desiredNodeCount) / self.desiredNodeCount
        cost = 100 * (3 ** (float(x)/50))
        return cost
    def GetNodeDeleteCost(self):
        x = 50 * float(len(self.nodes) - self.desiredNodeCount) / self.desiredNodeCount
        cost = 100 * (3 ** (float(-x)/50))
        return cost

    def getNodesAround(self, node, range):
        nodesAround = []
        range = range * range
        for n in self.nodes:
            if n == node: continue
            ldx = n.x-node.x
            ldy = n.y-node.y
            dist = ldx*ldx + ldy*ldy
            if dist < range:
                #if self.area.CanMove(node, n.x, n.y):
                nodesAround.append(n)
        return nodesAround
    
    def getAllNodesDist(self, node):
        nodesAround = {}
        for n in self.nodes:
            if n == node: continue
            ldx = n.x-node.x
            ldy = n.y-node.y
            dist = ldx*ldx + ldy*ldy
            nodesAround[n] = sqrt(dist)
        return nodesAround

 
