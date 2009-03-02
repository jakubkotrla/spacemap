
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
        self.amount = amount
        self.attractivity = attractivity
        self.curAttractivity = attractivity #0.0 - 1.0
        self.visibility = 0 #0.0 - 1.0
        self.guiId = None
        self.trainHistory = 0
        
    def Use(self):
        self.amount =- 1
        return (self.amount < 1)
    
    def ToString(self):
        return self.type.name + " at [" + str(self.x) + "," + str(self.y) + "] trained: " + str(self.trainHistory)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class Hit(Point):
    def __init__(self, x, y, hit):
        Point.__init__(self, x, y)
        self.hit = hit

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

class VisibilityObject(Point):
    def __init__(self, x, y):
        Point.__init__(self, x, y)
        self.visibility = 0
        self.guiId = None
    def ToString(self):
        return "VO(" + str(self.x) + ", " + str(self.y) + ").visibility = " + str(self.visibility)
             
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
        self.guiObjectAppeared = None
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
        rObj = RealObject(type, x, y, attractivity, amount)    
        self.objects.append(rObj)
        if self.guiObjectAppeared != None:
            self.guiObjectAppeared(rObj)
    
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
            agent.newX = int(newX)
            agent.newY = int(newY)
        return round(duration)
      
    #start has old position in .x and .y 
    def CanMove(self, start, newX, newY):
        hitPoint = None
        for edge in self.edges:
            hitResult = self.AreIntersecting(edge.start, edge.end, start, Point(newX,newY) )
            if hitResult.hit:
                if hitResult.x == newX and hitResult.y == newY:
                    pass
                elif hitResult.x == start.x and hitResult.y == start.y:
                    pass
                else:
                    return False
        return True
    def CanMoveEx(self, start, newX, newY):
        hitPoint = None
        hitDist = Global.MaxNumber
        
        newPos = Point(newX,newY)
        for edge in self.edges:
            hitResult = self.AreIntersecting(edge.start, edge.end, start, newPos)
            if hitResult.hit:
                if hitPoint == None:
                    hitPoint = hitResult
                    hitDist = self.DistanceObjs(hitResult, start)
                else:
                    dist = self.DistanceObjs(hitResult, start)
                    if dist < hitDist:
                        hitPoint = hitResult
                        hitDist = dist
        if hitPoint == None:
            return Hit(0, 0, False)
        else:
            return hitPoint
    
    def GetPath(self, start, newX, newY):
        if self.CanMove(start, newX, newY):
            return self.dividePath([start, Point(newX, newY)])
        else:
            path = self.findPath(start, Point(newX, newY))
            path = self.dividePath(path)
            return path
    
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
        
        lx1 = min(edge1point1.x, edge1point2.x) - 0.1
        rx1 = max(edge1point1.x, edge1point2.x) + 0.1
        if not lx1 <= x <= rx1: return Hit(x,y, False)
        ly1 = min(edge1point1.y, edge1point2.y) - 0.1
        ry1 = max(edge1point1.y, edge1point2.y) + 0.1
        if not ly1 <= y <= ry1: return Hit(x,y, False)
        
        lx2 = min(edge2point1.x, edge2point2.x) - 0.1
        rx2 = max(edge2point1.x, edge2point2.x) + 0.1
        if not lx2 <= x <= rx2: return Hit(x,y, False)
        ly2 = min(edge2point1.y, edge2point2.y) - 0.1
        ry2 = max(edge2point1.y, edge2point2.y) + 0.1
        if not ly2 <= y <= ry2: return Hit(x,y, False)
        
        return Hit(x,y, True)       
   
    
    def IsInside(self, point):
        count = 0
        endPoint = Point(self.width+1, point.y)
        
        for edge in self.edges:
            hitResult = self.AreIntersecting(edge.start, edge.end, point, endPoint)
            if hitResult.hit:
                count = count + 1
        return ((count % 2) == 1)
        
    #from http://local.wasp.uwa.edu.au/~pbourke/geometry/polyarea/
    def GetArea(self):
        sum = 0
        vertices = copy(self.points)
        vertices.reverse()
        vertices.append(vertices[0])
        for i in range(len(self.points)):
            sum = sum + vertices[i].x * vertices[i+1].y - vertices[i].y * vertices[i+1].x
        return fabs( sum * 0.5)
    
    def GetRealObjectIfThere(self, memObject):
        for rObj in self.objects:
            if rObj.x == memObject.x and rObj.y == memObject.y and rObj.type == memObject.type:
                return rObj
        return None
    
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
            
      
    def Distance(self, x1,y1,x2,y2):
        return sqrt((x2-x1)**2+(y2-y1)**2)
    def DistanceObj(self, x,y,object):
        return sqrt((x-object.x)**2+(y-object.y)**2)
    def DistanceObjs(self, o1,o2):
        return sqrt((o1.x-o2.x)**2+(o1.y-o2.y)**2)
        
    