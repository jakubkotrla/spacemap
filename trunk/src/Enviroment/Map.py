
from math import *
from Enviroment.Objects import *
from Enviroment.World import *
from Global import Global
from Agents.ProcessArea import *

class RealObject:
    def __init__(self, type, x, y, attractivity, amount):
        self.type = type
        self.x = x
        self.y = y
        self.onMap = True
        self.amount = amount
        self.attractivity = attractivity
        self.curAttractivity = attractivity #0.0 - 1.0
        self.visibility = 0 #0.0 - 1.0
        self.trainHistory = 0
                
    def Use(self):
        self.amount =- 1
        return (self.amount < 1)
    
    def ToString(self):
        return self.type.name + " at [" + str(self.x) + ";" + str(self.y) + "].trained = " + str(self.trainHistory)
    def IdStr(self):
        return str(self.x) + "," + str(self.y)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def Eq(self, point):
        return fabs(self.x-point.x)<Global.MinPositiveNumber and fabs(self.y - point.y)<Global.MinPositiveNumber
    def ToString(self):
        return str(self.x) + "," + str(self.y)
        
class Hit(Point):
    def __init__(self, x, y, hit):
        Point.__init__(self, x, y)
        self.hit = hit
        self.edge = None  #first edge hit
        self.dist = 0     #distance to first hit, only for Map
        

class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Path:
    def __init__(self, points, dist):
        self.points = []
        self.dist = dist
    def Last(self):
        return self.points[-1]

class Waypoint(Point):
    def __init__(self, x, y):
        Point.__init__(self, x, y)
        self.lastVisited = 0
    def ToString(self):
        return "Waypoint[" + str(self.x) + ", " + str(self.y) + "].lastVisited = " + str(self.lastVisited)

class VisibilityObject(Point):
    def __init__(self, x, y):
        Point.__init__(self, x, y)
        self.visibility = 0
        self.guiId = None
    def ToString(self):
        return "VO[" + str(self.x) + ", " + str(self.y) + "].visibility = " + str(self.visibility)
             
class Map:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.points = []
        self.wayPoints = []
        self.edges = []  
        self.objects = []
        self.agentMoves = []
        self.mapRenderer = None
        self.visibilityHistory = []
        self.visibilityMaxEver = 0
        
    def CalculateEdges(self):
        lastPoint = self.points[-1]
        for point in self.points:
            edge = Edge(lastPoint, point)
            self.edges.append(edge)
            lastPoint = point
                
        xCount = self.width / Global.VisibilityHistoryArea
        yCount = self.height / Global.VisibilityHistoryArea
        for y in range(yCount):
            for x in range(xCount):
                xx = x*Global.VisibilityHistoryArea + Global.VisibilityHistoryArea/2
                yy = y*Global.VisibilityHistoryArea + Global.VisibilityHistoryArea/2
                
                if self.IsInside( Point(xx,yy) ):    
                    vObj = VisibilityObject(xx, yy)
                    self.visibilityHistory.append(vObj)
        
    def Render(self, mapRenderer):
        self.mapRenderer = mapRenderer
        firstLine = None
        for edge in self.edges:
            guiId = mapRenderer.Line(edge.start.x, edge.start.y, edge.end.x, edge.end.y, "#000", "map edge")
            if firstLine == None:
                firstLine = guiId
        for wayPoint in self.wayPoints:
            mapRenderer.PixelC(wayPoint, wayPoint.x, wayPoint.y, "#000", 2, "waypoint")
        return firstLine
    
    def AddObject(self, type, x, y, attractivity = Global.ObjDefaultAttractivity, amount=1):
        rObject = RealObject(type, x, y, attractivity, amount)    
        self.objects.append(rObject)
        return rObject
    def CreateObject(self, type, x, y, attractivity = Global.ObjDefaultAttractivity, amount=1):
        rObject = RealObject(type, x, y, attractivity, amount)
        rObject.onMap = False
        return rObject    
    def AddExistingObject(self, rObject):
        self.objects.append(rObject)
        rObject.onMap = True
    def RemoveExistingObject(self, rObject):
        self.objects.remove(rObject)
        rObject.onMap = False
    
    def SetAgentStart(self, x, y):
        self.agentMoves.append( Point(x, y) )
    def PlaceAgent(self, agent):
        agent.newX = agent.x = self.agentMoves[0].x
        agent.newY = agent.y = self.agentMoves[0].y
        self.calculateVisibility(agent)
        
    
    def MoveAgent(self, agent, newX, newY):
        if not self.CanMove(agent, newX, newY):
            Global.Log("Programmer.Error: Map.MoveAgent out of map")
            return 0
        else:
            duration = self.DistanceObj(newX, newY, agent)
            self.agentMoves.append( Point(agent.x, agent.y) )
            if len(self.agentMoves) > Global.AgentMoveHistoryLength:
                self.agentMoves.pop(0)
            #agent.x = agent.newX - done in Agent.step
            #agent.y = agent.newY - done in Agent.step
            agent.newX = newX
            agent.newY = newY
        return round(duration)
      
    #start has old position in .x and .y 
    def CanMove(self, start, newX, newY):
        hitPoint = None
        newPos = Point(newX,newY)
        for edge in self.edges:
            hitResult = self.AreIntersecting(edge.start, edge.end, start, newPos)
            if hitResult.hit:
                if fabs(hitResult.x-newX)<Global.MinPositiveNumber and fabs(hitResult.y - newY)<Global.MinPositiveNumber:
                    pass
                elif hitResult.Eq(start):
                    if self.IsInside(newPos):
                        pass
                    else:
                        return False    #hit at start - start on edge and move out
                else:
                    return False
        return True
    def CanMoveEx(self, start, newX, newY):
        newPos = Point(newX, newY)
        hitPoint = self.canMoveExInner(start, newPos)
        
        if (hitPoint.hit):
            if fabs(hitPoint.x-start.x)<Global.MinPositiveNumber and fabs(hitPoint.y - start.y)<Global.MinPositiveNumber:
                newPos = self.moveAlongEdge(hitPoint.edge, start, newPos)
                newHit = self.canMoveExInner(start, newPos)
                if newHit.hit:
                    hitPoint = newHit
                else:
                    hitPoint.x = newPos.x
                    hitPoint.y = newPos.y
            else:
                return hitPoint
        return hitPoint
        
    def canMoveExInner(self, start, end):
        hitPoint = None
        
        for edge in self.edges:
            hitResult = self.AreIntersecting(edge.start, edge.end, start, end)
            if hitResult.hit:
                if hitResult.Eq(end):
                    pass
                elif hitResult.Eq(start) and self.IsInside(end):
                    pass
                else: #real hit
                    if hitPoint == None:
                        hitPoint = hitResult
                        hitPoint.edge = edge
                        hitPoint.dist = self.DistanceObjs(hitResult, start)
                    else:
                        dist = self.DistanceObjs(hitResult, start)
                        if dist < hitPoint.dist:
                            hitPoint = hitResult
                            hitPoint.edge = edge
                            hitPoint.dist = dist
        #end for edge
        if hitPoint == None:
            return Hit(0, 0, False)
        else:
            return hitPoint
    
    def moveAlongEdge(self, edge, start, newPos):
        edx = edge.end.x - edge.start.x
        edy = edge.end.y - edge.start.y
       
        if edx == 0:
            xx = start.x
            yy = newPos.y
            return Point(xx, yy)
        elif edy == 0:
            yy = start.y
            xx = newPos.x
            return Point(xx, yy)
        else:
            y1 = 200
            x1 = (edx*newPos.x - edy*(y1-newPos.y)) / edx
            y2 = -200
            x2 = (edx*newPos.x - edy*(y2-newPos.y)) / edx   
            return self.AreIntersecting(edge.start, edge.end, Point(x2,y2), Point(x1, y1))    
    
    def GetPath(self, start, newX, newY):
        if self.CanMove(start, newX, newY):
            return self.dividePath([start, Point(newX, newY)])
        else:
            if self.IsInside( Point(newX, newY) ):
                path = self.findPath(start, Point(newX, newY))
                path = self.dividePath(path)
                return path
            else:
                return None
    
    def dividePath(self, path):
        last = path[0]
        path2 = path[1:]
        newPath = [last]
        for part in path2:
            points = self.dividePathPart(last, part)
            if points != None:
                for point in points:
                    newPath.append(point)
            newPath.append(part)
            last = part
        return newPath
    
    def dividePathPart(self, start, end):
        dist = self.DistanceObjs(start, end)
        if dist > Global.MaxAgentMove:
            dividerCount = int(ceil(dist / Global.MaxAgentMove))
            dividerLength = dist *1.0 / dividerCount
            dividerCoef = dividerLength *1.0 / dist
            dx = end.x - start.x
            dy = end.y - start.y
            
            dividers = []
            sx = start.x
            sy = start.y
            for i in range(dividerCount-1):
                px = round(sx + dx * dividerCoef)   #round leads to zigzag movement.. like human
                py = round(sy + dy * dividerCoef)
                divider = Point(px, py)
                dividers.append(divider)
                sx = sx + dx * dividerCoef
                sy = sy + dy * dividerCoef
                
            return dividers
        else:
            return None
    
    #using inner points as in http://alienryderflex.com/shortest_path/
    def findPath(self, start, end):
        dist = {}
        previous = {}
        dist[start] = 0
        queue = [start]
        allPoints = [end]
        allPoints.extend(self.wayPoints)
        donePoints = []
        for point in allPoints:
            dist[point] = Global.MaxNumber
            previous[point] = None
        
        while len(queue) > 0:
            curPoint = queue.pop(0)
            donePoints.append(curPoint)
            neighbours = self.getNeighbours(curPoint, end)
            for point in neighbours:
                alt = dist[curPoint] + self.DistanceObjs(curPoint, point)
                if alt < dist[point]:
                    dist[point] = alt
                    previous[point] = curPoint
                if point not in donePoints:
                    queue.append(point)
            
        #all set, get data from previous
        path = []
        point = end
        while point != start:
            path.insert(0, point)
            if point == None:
                Global.Log("Map.findPath: pointNone start: " + str(start.x) + "," + str(start.y))
                Global.Log("Map.findPath: pointNone end: " + str(end.x) + "," + str(end.y))
            point = previous[point]
        path.insert(0, start)
        return path
    def getNeighbours(self, point, end):
        neighbours = []
        for p in self.wayPoints:
            if p == point: continue
            if self.CanMove(point, p.x, p.y):
                neighbours.append(p)
        if point != end:
            if self.CanMove(point, end.x, end.y):
                neighbours.append(end)
        return neighbours
    
    def AreIntersecting(self, edge1point1, edge1point2, edge2point1, edge2point2):
        # 0 = ax + by + c
        a1 = edge1point2.y - edge1point1.y
        b1 = edge1point1.x - edge1point2.x
        c1 = edge1point2.x*edge1point1.y - edge1point1.x*edge1point2.y

        a2 = edge2point2.y - edge2point1.y
        b2 = edge2point1.x - edge2point2.x
        c2 = edge2point2.x*edge2point1.y - edge2point1.x*edge2point2.y

        denom = a1*b2 - a2*b1;
        if denom == 0:
            return Hit(0,0, False)
        x =(b1*c2 - b2*c1)/denom;
        y =(a2*c1 - a1*c2)/denom;
        
        lx1 = min(edge1point1.x, edge1point2.x) - Global.MinPositiveNumber
        rx1 = max(edge1point1.x, edge1point2.x) + Global.MinPositiveNumber
        if not lx1 <= x <= rx1: return Hit(x,y, False)
        ly1 = min(edge1point1.y, edge1point2.y) - Global.MinPositiveNumber
        ry1 = max(edge1point1.y, edge1point2.y) + Global.MinPositiveNumber
        if not ly1 <= y <= ry1: return Hit(x,y, False)
        
        lx2 = min(edge2point1.x, edge2point2.x) - Global.MinPositiveNumber
        rx2 = max(edge2point1.x, edge2point2.x) + Global.MinPositiveNumber
        if not lx2 <= x <= rx2: return Hit(x,y, False)
        ly2 = min(edge2point1.y, edge2point2.y) - Global.MinPositiveNumber
        ry2 = max(edge2point1.y, edge2point2.y) + Global.MinPositiveNumber
        if not ly2 <= y <= ry2: return Hit(x,y, False)
        
        return Hit(x,y, True)       
   
    #from http://alienryderflex.com/polygon/
    #more at http://tog.acm.org/editors/erich/ptinpoly/
    def IsInside(self, point):
        for p in self.points:
            if point.Eq(p): return True
        countX = 0
        countY = 0
        endPointX = Point(self.width+1, point.y)
        endPointY = Point(point.x, self.height+1)
        
        for edge in self.edges:
            hitResult = self.AreIntersecting(edge.start, edge.end, point, endPointX)
            if hitResult.hit:
                if hitResult.Eq(point): return True
                if hitResult.Eq(edge.start) and edge.end.y <= point.y:   pass
                elif hitResult.Eq(edge.end) and edge.start.y <= point.y: pass
                else: countX = countX + 1
            
            hitResult = self.AreIntersecting(edge.start, edge.end, point, endPointY)
            if hitResult.hit:
                if hitResult.Eq(point): return True
                if hitResult.Eq(edge.start) and edge.end.x <= point.x:   pass
                elif hitResult.Eq(edge.end) and edge.start.x <= point.x: pass
                else: countY = countY + 1
        countX = ((countX % 2) == 1)
        countY = ((countY % 2) == 1)
        if countX != countY:
            Global.Log("Programmer.Error: IsInside countX!=countY for: " + point.ToString())
        return (countX or countY)
    
    #from http://local.wasp.uwa.edu.au/~pbourke/geometry/polyarea/
    def GetArea(self):
        sum = 0
        vertices = copy(self.points)
        vertices.reverse()
        vertices.append(vertices[0])
        for i in range(len(self.points)):
            sum = sum + vertices[i].x * vertices[i+1].y - vertices[i].y * vertices[i+1].x
        return fabs( sum * 0.5)
    
    def GetRandomLocation(self):
        x = Global.Randint(0, self.width) 
        y = Global.Randint(0, self.height)
        p = Point(x,y)
        while not self.IsInside( p ):                
            x = Global.Randint(0, self.width) 
            y = Global.Randint(0, self.height)
            p = Point(x,y)    
        return p
    
    def UseObject(self, excProcess, realObject):
        if realObject.Use():
            self.objects.remove(realObject)
            Global.Log("Map.UseObject: agent used up object " + realObject.type.name + " at " + str(realObject.y) + "," + str(realObject.x))
            return True
        return False    
 
    def GetVisibleObjects(self, agent):
        self.calculateVisibility(agent)
        objs = []
        for obj in self.objects:
            if obj.visibility > 0:
                objs.append(obj)
        return objs 
      
    def GetVisibility(self, agent, object):
        dist = self.DistanceObjs(agent, object)
        if dist > agent.viewConeMaxDist: return 0
        if not self.CanMove(agent, object.x, object.y): return 0
        
        visibility = 0
        if dist == 0:
            for vc in agent.viewCones: visibility = visibility + vc.intensity
            return visibility
        odx = object.x - agent.x
        ody = object.y - agent.y
        oangle = atan2(odx, ody)
        dangle = agent.dirAngle
        angle = abs(oangle - dangle)
        if oangle * dangle < 0 and angle > pi:
            angle = 2*pi - angle 
        
        visibility = 0
        for vc in agent.viewCones:
            if angle < vc.angle and dist < vc.distance:
                visibility = visibility + vc.intensity
        return visibility
      
    def IsObjectVisible(self, agent, object):
        object.visibility = self.GetVisibility(agent, object)
        return (object.visibility > 0)
    
    def Step(self, agent):
        self.calculateWayPointsVisited(agent)
        if Global.CalculateVisibilityHistory:
            self.calculateVisibilityHistory(agent)
    
    def calculateWayPointsVisited(self, agent):
        for wayPoint in self.wayPoints:
            if self.DistanceObjs(wayPoint, agent) < Global.WayPointArea:
                wayPoint.lastVisited = Global.GetSeconds()
            
    def calculateVisibility(self, agent):
        for obj in self.objects:
            visibility = self.GetVisibility(agent, obj)
            obj.visibility = visibility
            
    def calculateVisibilityHistory(self, agent):
        for obj in self.visibilityHistory:
            visibility = self.GetVisibility(agent, obj)
            obj.visibility += visibility
            if obj.visibility > self.visibilityMaxEver:
                self.visibilityMaxEver = obj.visibility
      
    def SaveHeatMap(self):
        for obj in self.objects:
            objStr = str(obj.x) + ";" + str(obj.y) + ";%.4f"%(obj.trainHistory)
            Global.LogData("objheatmap", objStr)
      
    def Distance(self, x1,y1,x2,y2):
        ldx = x2-x1
        ldy = y2-y1
        return sqrt(ldx*ldx+ldy*ldy)
    def DistanceObj(self, x,y,object):
        ldx = x-object.x
        ldy = y-object.y
        return sqrt(ldx*ldx+ldy*ldy)
    def DistanceObjs(self, o1,o2):
        ldx = o1.x-o2.x
        ldy = o1.y-o2.y
        return sqrt(ldx*ldx+ldy*ldy)
        
    