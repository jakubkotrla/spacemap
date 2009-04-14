## @package Agents.EnergyLayer
# Contains implementation of gravity model described in thesis.
#
# EnergyLayer is main class representing "vrstva uzlu".
# EnergyLayerNode is "uzel prostorove mapy", EnergyPoint is "stopa vjemu" and Place is "misto".

from Enviroment.Global import Global
from math import sqrt, fabs, log, e, ceil
from Enviroment.Map import Point
from Enviroment.Objects import WaypointObject
import copy

## Represents "misto", area with higher density of objects and therefore of nodes.
class Place:
    def __init__(self, layer, index, x, y):
        self.layer = layer
        self.index = index
        self.x = x
        self.y = y
        self.range = 0
        self.startRange = 0
        self.parent = None
        self.level = 1
        self.nodes = []
        self.places = []
        ## Described in model as "mnozstvi odpudivosti mista"
        self.AGamount = 0
        self.startTotalAGamount = 0
        self.totalAGamount = 0
        ## Described in model as "intenzita mista"
        self.slowAGamount = 0
    
    ## Saves current state to data file
    def SaveStatus(self):
        status = str(Global.GetStep()) + ";" + str(self.index) + ";%.4f;%.4f;%.4f;%.4f;%.4f;%.4f;%.4f"%(self.x,self.y,self.level,self.range,self.AGamount,self.totalAGamount,self.slowAGamount)
        Global.LogData("place-status", status)
    
    ## Deletes self, aka destructor.
    def Delete(self):
        if self not in self.layer.places:   #probably deleted as child of another deleted place
            return
        for place in self.places:
            place.Delete()
        self.layer.places.remove(self)
    
    ## Calculate current AG, totalAG and slowAG. Updates slowAG.
    def CalculateAG(self):
        self.AGamount = 0
        for node in self.nodes:
            self.AGamount += node.AGamount
        self.totalAGamount = self.calculateAGdeep(self)
        
        self.slowAGamount += self.totalAGamount * (1.0 / max(self.slowAGamount * Global.PlacesAGGrow, 1))
        self.slowAGamount -= Global.PlaceAGFadeOut 
    ## Recursive utility method to calculate AGs of subplaces.    
    def calculateAGdeep(self, placeToProcess):
        sumNodeAGamount = 0
        for node in placeToProcess.nodes:
            sumNodeAGamount += node.AGamount
        for place in placeToProcess.places:
            sumNodeAGamount += self.calculateAGdeep(place)
        return sumNodeAGamount
    
    ## Calculates range by current AGamount
    def CalculateRange(self):
        coef = (0.2 * (self.startTotalAGamount / self.slowAGamount) ) + 0.8
        self.range = self.startRange * coef
    
    ## Update location of Place.
    #
    # Computes weighted centroid if nodes in place.
    # Moves by a small step towards this centroid.
    def UpdateLocation(self):
        (x, y, sumNodeAGamount) = self.updateLocDeep(self)
        self.totalAGamount = sumNodeAGamount
        
        self.totalAGamount = sumNodeAGamount
        if sumNodeAGamount == 0: return
        x = x / sumNodeAGamount
        y = y / sumNodeAGamount
        p = Point(x,y)
        
        coef = min(1, (float(self.startTotalAGamount) / self.slowAGamount)) * Global.PlaceMoveCoef
        dx = (p.x - self.x) * coef
        dy = (p.y - self.y) * coef
        self.x += dx 
        self.y += dy
    # Recursive utility method.
    def updateLocDeep(self, placeToProcess):
        x = 0
        y = 0
        sumNodeAGamount = 0
        for node in placeToProcess.nodes:
            x += node.x * node.AGamount
            y += node.y * node.AGamount
            sumNodeAGamount += node.AGamount
        for place in placeToProcess.places:
            (lx, ly, lsumNodeAGamount) = self.updateLocDeep(place)
            x += lx
            y += ly
            sumNodeAGamount += lsumNodeAGamount
        return (x, y, sumNodeAGamount)
       
## Represents "stopa vjemu".
class EnergyPoint:
    def __init__(self, layer, memObject, x, y, energy):
        self.layer = layer
        ## Described in model as "pametova stopa predmetu"
        self.memObject = memObject
        self.x = x
        self.y = y
        ## Described in model as "intenzita stopy vjemu"
        self.energy = energy
        
        effect = self.energy / Global.EPCreateEnergy
        self.intenseMemObjToNodes(effect)
        
    def ToString(self):
        strInfo = []
        strXY = '%.2f'%(self.x) + ";" + '%.2f'%(self.y)
        strInfo.append("EnergyPoint[" + strXY + "].energy = " + str(self.energy))
        
    ## One step of simulation of EnergyPoint as described in model
    #
    # 1. check for creating new node, eventually creates one.
    # 2. train EneryLayer by attracting close EnergyLayerNodes.
    # 3. train SpaceMap - links EneryLayerNode-MemoryObject
    # 4. decrease energy and eventually gets deleted
    def StepUpdate(self, nodesAround):
        cost = self.layer.GetNodeCreateCost()
        chanceNew = 100 * float(self.energy - cost) / cost
        diceRoll = Global.DiceRoll()
        if diceRoll < chanceNew:
            self.layer.CreateNode(self, self.memObject)
            self.energy = self.energy - cost
        
        effect = self.energy / Global.EPCreateEnergy
        
        for node in nodesAround:
            node.Train(self, effect)
            
        self.intenseMemObjToNodes(effect)

        self.energy = self.energy * Global.EPFadeCoef
        if self.energy < Global.EPFadeLimit:
            self.layer.DeleteEnergyPoint(self)
            
    ## Trains memoryObject to nodes around.
    def intenseMemObjToNodes(self, effect):
        inNodes = self.layer.PositionToNodes(self.memObject, Global.SMTrainRange)
        if inNodes == None: return  #there are no ELNodes - error paranoid, should not happen anyway
        nodesToIntensity = {}
        sumIntensity = 0
        inc = len(inNodes)
        
        for (node,dist) in inNodes.iteritems():
            # comments below - switch between gauss and 1/max(1,x) norm functions
            #intensity = Global.Gauss( dist / Global.SMNodeAreaDivCoef, Global.SMNodeAreaGaussCoef)
            dist = max(1, dist)
            intensity = 1.0 / dist
            #intensity = Global.SMNodeAreaDivCoef * Global.GaussInverse(intensity, Global.SMNodeAreaGaussCoef)
            intensity = max(Global.MinPositiveNumber, intensity)
            nodesToIntensity[node] = intensity
            sumIntensity = sumIntensity + intensity
        for node in inNodes:
            intensity = effect * nodesToIntensity[node] / sumIntensity
            self.memObject.IntenseToNode(node, intensity)
        
    
## Represents "uzel prostorove mapy".
class EnergyLayerNode:
    def __init__(self, layer, x, y, index):
        self.layer = layer
        ## Pointer to Map.
        self.area = layer.area
        self.x = x
        self.y = y
        self.linkToObjects = []
        self.index = index
        ## Described in model as "naplnenost uzlu".
        self.usage = 0
        ## Described in model as "mnozstvi odpudivosti".
        self.AGamount = 0
        self.place = None
        
        ## Used to correctly simulate antigravity.
        self.stepDiffX = 0
        ## Used to correctly simulate antigravity.
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
    
    ## Deletes self, aka destructor.
    def Delete(self):
        for link in self.linkToObjects:
            link.NodeDeleted()
        if Global.CreatePlaces:
            self.place.nodes.remove(self)
    
    ## Increases self-intensity, called from memoryObject.IntenseToNode().
    def Intense(self, intensity):
        self.usage += intensity
    
    ## One step of simulation of node. Calculates anti-gravity and AGamount.      
    def StepUpdate(self, nodesAround, normalStep=True):
        for node in nodesAround:
            ldx = (self.x - node.x) 
            ldy = (self.y - node.y)
            dist2 = ldx*ldx+ldy*ldy
            dist = sqrt(dist2)

            if normalStep:
                self.AGamount += ((1.0/ max(1, dist)) * Global.ELAGAddCoef) * (1 / max(self.AGamount, 1))
            
            gDiffCoef = dist2 * max(Global.ELAGUsageCoef, self.usage) * max(Global.ELAGUsageCoef,node.usage)
            gDiffCoef = float(Global.ELAntigravityCoef) / max(Global.ELAGUsageCoef2, gDiffCoef)
            
            dist = max(Global.MinPositiveNumber, dist)
            self.stepDiffX += ldx * (gDiffCoef / dist)
            self.stepDiffY += ldy * (gDiffCoef / dist)
    
    ## Moves node by calculated anti-gravity stepsDiffXY    
    def StepUpdateMove(self, normalStep=True):
        massCoef = 1.0/max(1, self.usage)

        dx = self.stepDiffX * massCoef
        dy = self.stepDiffY * massCoef
        
        distToMove2 = dx*dx + dy*dy
        maxDif = Global.MaxELNodeMove
        if distToMove2 > (maxDif * maxDif):
            distToMove = sqrt(distToMove2)
            coef = maxDif / distToMove 
            dx = dx * coef
            dy = dy * coef
            
        newX = self.x + dx
        newY = self.y + dy
        hit = self.area.CanMoveEx(self, newX, newY)
        if hit.hit:
            newX = hit.x
            newY = hit.y
            
            ldx = newX - self.x
            ldy = newY - self.y
            distToMove2 = ldx*ldx + ldy*ldy
            if distToMove2 < 0.0001:
                newX = self.x
                newY = self.y 
        
        if normalStep and Global.SaveELNodesStatus:
            ldx = newX - self.x
            ldy = newY - self.y
            distToMove = sqrt(ldx*ldx + ldy*ldy)
        
        if self.area.IsInside(Point(newX, newY)):
            self.x = newX
            self.y = newY
        self.stepDiffX = self.stepDiffY = 0

        if normalStep:
            self.usage -= Global.ELNodeUsageFadeOut
            if self.usage < 0: self.usage = 0
            self.AGamount -= Global.ELAGFadeOut
        
        if normalStep and Global.SaveELNodesStatus:
            status = str(Global.GetStep()) + ";" + str(self.index) + ";%.4f;%.4f;%.4f"%(distToMove,self.usage,self.AGamount)
            Global.LogData("elnode-status", status)
    
    ## Trains node, move it slightly to location of EnergyPoint regarding effect.       
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
            

## Represents "gravitacni model vrstvy uzlu".
class EnergyLayer:
    def __init__(self, area):
        ## Pointer to Map.
        self.area = area
        self.nodes = []
        self.energyPoints = []
        self.energyPointsToDelete = []
        ## Described in model as "energie na zapominani".
        self.forgetEnergy = 0
        self.nodeIndex = 1
        self.places = []
        self.placeIndex = 0
        ## Described in model as "chteny pocet uzlu".
        self.desiredNodeCount = 0
        
        ## Only for saving state to data files
        self.stepEPCreated = 0
        ## Only for saving state to data files
        self.stepELNodesCreated = 0
    
    ## Creates initial nodes.
    def CreateMap(self):
        areaArea = self.area.GetArea()
        nodeCount = areaArea / Global.ELDensity ** 2
        self.desiredNodeCount = nodeCount * 2
        self.minimalDesiredNodeCount = self.desiredNodeCount / 5
        self.maximalDesiredNodeCount = self.desiredNodeCount
        
        x = self.area.points[0].x
        y = self.area.points[0].y
        if Global.CreatePlaces:
            rootPlace = Place(self, self.placeIndex, self.area.width/2 + x, self.area.height/2 + y)
            rootPlace.range = max(x + self.area.width, y + self.area.height) * sqrt(2) / 2
            rootPlace.range = ceil(rootPlace.range)
            rootPlace.startRange = rootPlace.range
            self.places.append(rootPlace)
        
        if Global.ELCreateNoise == -1:  #completely random distribution of nodes
            while len(self.nodes) < nodeCount:
                x = float(Global.Randint(0, self.area.width-1))
                y = float(Global.Randint(0, self.area.height-1))
                
                if self.area.IsInside( Point(x,y) ):                
                    node = EnergyLayerNode(self, x, y, self.nodeIndex)
                    self.nodeIndex = self.nodeIndex + 1
                    self.nodes.append(node)
                    if Global.CreatePlaces:
                        node.place = rootPlace
                        rootPlace.nodes.append(node)
        else:
            xCount = self.area.width / Global.ELDensity
            yCount = self.area.height / Global.ELDensity
            density = Global.ELDensity
            for y in range(yCount):
                for x in range(xCount):
                    xNoise = Global.Randint(-Global.ELCreateNoise, Global.ELCreateNoise)
                    yNoise = Global.Randint(-Global.ELCreateNoise, Global.ELCreateNoise)
                    xx = float(x*density+density/2+xNoise)
                    yy = float(y*density+density/2+yNoise)
                    
                    if self.area.IsInside( Point(xx,yy) ):    
                        node = EnergyLayerNode(self, xx, yy, self.nodeIndex)
                        self.nodeIndex = self.nodeIndex + 1
                        self.nodes.append(node)
                        if Global.CreatePlaces:
                            node.place = rootPlace
                            rootPlace.nodes.append(node)
     
    ## Returns list of nodes around given center closer than given per, returns at least one node, the closest one even if is outside of per.
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
    ## One step of simulation for EnergyLayer.
    #
    # 1. updates EnergyPoints, EnergyLayerNodes, Places
    # 2. forgets nodes
    # 3. saves current state - node count etc.
    def StepUpdate(self):
        for ep in self.energyPoints:
            ep.StepUpdate(self.getNodesAround(ep, Global.ELGravityRange))
        for node in self.nodes:
            node.StepUpdate(self.getNodesAround(node, Global.ELAntigravityRange))
        for node in self.nodes:
            node.StepUpdateMove()
        
        if Global.CreatePlaces:
            placesToDelete = []
            for place in self.places:
                place.CalculateAG()
                if place.slowAGamount < Global.PlacesAGMin * (place.level-1):
                    placesToDelete.append(place)
                    continue
                
                if place.AGamount > Global.PlacesAGNeeded * (2**(place.level) - 1):
                    self.createPlaces(place)
                
                if place.parent != None:
                    place.UpdateLocation()
                    place.CalculateRange()
                place.SaveStatus()
                
            for place in placesToDelete:
                place.Delete()
                
            for node in self.nodes:
                p = self.GetPlaceForNode(node)
                if p != node.place:
                    node.place.nodes.remove(node)
                    node.place = p
                    p.nodes.append(node)
        
        for ep in self.energyPointsToDelete:
            self.energyPoints.remove(ep)
        self.energyPointsToDelete = []

        self.forgetEnergy = self.forgetEnergy + Global.ELForgetNodeRate
        cost = self.GetNodeDeleteCost()
        chanceForget = 100 * float(self.forgetEnergy - cost) / cost
        
        diceRoll = Global.DiceRoll()
        if diceRoll < chanceForget and len(self.nodes) > 0:
            node = Global.Choice(self.nodes)
            self.forgetEnergy = self.forgetEnergy - (cost * log(max(2,node.usage), 2))
            self.DeleteNode(node)

        Global.LogData("nc", self.Status())

    ## Divides one place to subplaces.    
    def createPlaces(self, placeToSplit):
        startAG = placeToSplit.AGamount
        
        while placeToSplit.AGamount > (startAG / 2):
            nodesPlace = placeToSplit.nodes
            nodesPlace.sort(lambda b,a: cmp(a.AGamount,b.AGamount))
            placeCreated = self.createSubPlace(placeToSplit, nodesPlace)
            if not placeCreated: break
            placeToSplit.CalculateAG()
        
    ## Creates one subplace.
    #
    # Returns False if new Place has AGamount lower than required limit.    
    def createSubPlace(self, placeToSplit, nodesPlace):
        startNode = nodesPlace[0]
        nodes = nodesPlace[:]
        nodes.remove(startNode)
        nodeDists = self.getAllNodesDist(startNode, nodes)
        nodes.sort(lambda a,b: cmp(nodeDists[a],nodeDists[b]))
                
        nodesInNewPlace = [startNode]
        newPlaceAGamount = 0
        newPlaceRange = placeToSplit.range / 2
        newPlaceLevel = placeToSplit.level + 1
        for n in nodes:
            if nodeDists[n] > newPlaceRange: break
            nodesInNewPlace.append(n)
        for node in nodesInNewPlace:
            newPlaceAGamount += node.AGamount
        if newPlaceAGamount < (Global.PlacesAGMin * newPlaceLevel):
            return False
        
        self.placeIndex += 1
        newPlace = Place(self, self.placeIndex, startNode.x, startNode.y)
        newPlace.range = newPlaceRange
        newPlace.startRange = newPlace.range
        newPlace.level = newPlaceLevel
        newPlace.parent = placeToSplit
        placeToSplit.places.append(newPlace)
        self.places.append(newPlace)
        
        newPlace.nodes = nodesInNewPlace
        for n in nodesInNewPlace:
            n.place.nodes.remove(n)
            n.place = newPlace
            
        newPlace.AGamount = newPlaceAGamount
        newPlace.totalAGamount = newPlaceAGamount
        newPlace.startTotalAGamount = newPlace.AGamount
        newPlace.slowAGamount = newPlace.AGamount
        newPlace.CalculateRange() 
        newPlace.UpdateLocation()
        return True
        

    ## Returns Place to which given node belongs, based on node location, Places' range and location. 
    def GetPlaceForNode(self, node):
        self.places.sort(lambda a,b: cmp(a.range,b.range))
        for place in self.places:
            dist = self.area.DistanceObjs(node, place)
            if dist < place.range:
                return place
    ## Returns Place to which given node belongs, based only on node location.
    def GetAllPlacesForNode(self, node):
        places = []
        for place in self.places:
            dist = self.area.DistanceObjs(node, place)
            if dist < place.range:
                places.append(place)
        return places
    
    ## Deletes self aka destuctor
    def DeleteNode(self, node):
        node.Delete()
        self.nodes.remove(node)
        nodesToRun = nodes = self.getNodesAround(node, Global.ELDeleteNodeReTrainRange) 
        for i in range(Global.ELDeleteNodeReTrainCount):
            for n in nodesToRun:
                n.StepUpdate(self.getNodesAround(n, Global.ELAntigravityRange), False)
                n.StepUpdateMove(False)
    
    ## Creates new node during simulation.
    #
    # Sets new node location based on EnergyPoint location and noise.
    # Set-ups correct links to MemoryObject and Place    
    def CreateNode(self, point, memObject):
        xNoise = Global.Randint(-Global.ELNodeAddNoise, Global.ELNodeAddNoise)
        yNoise = Global.Randint(-Global.ELNodeAddNoise, Global.ELNodeAddNoise)
        x = float(point.x + xNoise)
        y = float(point.y + yNoise)
        
        while not self.area.IsInside( Point(x,y) ):
            xNoise = Global.Randint(-Global.ELNodeAddNoise, Global.ELNodeAddNoise)
            yNoise = Global.Randint(-Global.ELNodeAddNoise, Global.ELNodeAddNoise)
            x = float(point.x + xNoise)
            y = float(point.y + yNoise)
            
        newNode = EnergyLayerNode(self, x, y, self.nodeIndex)
        self.nodeIndex = self.nodeIndex + 1
        self.nodes.append(newNode)

        if Global.CreatePlaces:
            place = self.GetPlaceForNode(newNode)
            place.nodes.append(newNode)
            newNode.place = place
        
        memObject.AddLinkToNode(newNode)
        memObject.IntenseToNode(newNode, Global.MemObjIntenseToNewNode)
        self.stepELNodesCreated = self.stepELNodesCreated + 1
        return newNode
    
    ## Trains EnergyLayer to input, entry method. Creates EneryPoint at given location of MemoryObject.
    def Train(self, memObject, effect):
        foundEP = None
        for ep in self.energyPoints:
            if ep.x == memObject.x and ep.y == memObject.y:
                foundEP = ep
                break
        if foundEP != None:
            foundEP.energy = foundEP.energy + effect * Global.EPCreateEnergy
        else:                
            ep = EnergyPoint(self, memObject, memObject.x, memObject.y, effect * Global.EPCreateEnergy)
            self.energyPoints.append(ep)
        self.stepEPCreated += effect * Global.EPCreateEnergy
        
    def DeleteEnergyPoint(self, energyPoint):
        self.energyPointsToDelete.append(energyPoint)
    
    ## Returns current status as line to be saved to CSV file.
    def Status(self):
        strObjs = str(len(self.area.objects))
        s = str(Global.GetStep()) + ';' + str(len(self.nodes)) + ";" + str(self.stepEPCreated) + ";" + str(self.stepELNodesCreated) + ";" + str(self.desiredNodeCount) + ";" + strObjs
        self.stepEPCreated = 0
        self.stepELNodesCreated = 0
        return s
    
    ## Saves current nodes.usage heatmap
    def SaveHeatMap(self):
        for n in self.nodes:
            nStr = "%d;%d;%.4f" % (int(n.x), int(n.y), n.usage)
            Global.LogData("elnodeheatmap", nStr)
        for n in self.nodes:
            nStr = "%d;%d;%.4f" % (int(n.x), int(n.y), n.AGamount)
            Global.LogData("elnodeheatmapag", nStr)
    
    ## Returns current create cost of new node as described in model.    
    def GetNodeCreateCost(self):
        x = 50 * float(len(self.nodes) - self.desiredNodeCount) / self.desiredNodeCount
        cost = 100 * (3 ** (float(x)/50))
        xf = 1100 * float(len(self.nodes) - self.desiredNodeCount) / self.desiredNodeCount
        costf = 0.0001 * (3 ** (float(xf)/50))
        return (cost + costf)
    
    ## Returns current forget cost of new node as described in model.
    def GetNodeDeleteCost(self):
        x = 50 * float(len(self.nodes) - self.desiredNodeCount) / self.desiredNodeCount
        cost = 100 * (3 ** (float(-x)/50))
        xf = 1100 * float(len(self.nodes) - self.desiredNodeCount) / self.desiredNodeCount
        costf = 0.0001 * (3 ** (float(-xf)/50))
        return (cost + costf)
    
    ## Returns list of nodes around given center closer than given per, returns empty list [] if no nodes around.
    def getNodesAround(self, node, range):
        nodesAround = []
        range = range * range
        for n in self.nodes:
            if n == node: continue
            ldx = n.x-node.x
            ldy = n.y-node.y
            dist = ldx*ldx + ldy*ldy
            if dist < range:
                nodesAround.append(n)
        return nodesAround
    
    ## Returns dist {nodes:distances} of distance od nodes from given node. 
    def getAllNodesDist(self, node, nodes = None):
        nodesAround = {}
        if nodes == None: nodes = self.nodes 
        for n in nodes:
            if n == node: continue
            ldx = n.x-node.x
            ldy = n.y-node.y
            dist = ldx*ldx + ldy*ldy
            nodesAround[n] = sqrt(dist)
        return nodesAround
    

 
