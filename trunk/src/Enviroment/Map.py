
from math import *
from Enviroment.Objects import *
from Enviroment.World import *
from Global import Global
from Agents.ProcessesArea import *

class RealObject:
    def __init__(self, type, x, y, attractivity, amount):
        self.type = type
        self.x = x
        self.y = y
        self.amount = amount
        self.attractivity = attractivity
        self.curAttractivity = attractivity
        self.maxAttractivity = 20
        self.visibility = 0 #0.0 - 1.0
        self.guiId = None
         
        self.memoryPhantom = None
    def Use(self):
        self.amount =- 1
        return (self.amount > 0)
    
    def ToString(self):
        return self.type.name + " at [" + str(self.x) + "," + str(self.y) + "]"

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
    
class VisibilityObject(Point):
    def __init__(self, x, y, visibility):
        Point.__init__(self, x, y)
        self.visibility = visibility
             
class Map:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.points = []
        self.innerPoints = []
        self.edges = []  
        self.objects = []
        self.agentMoves = []
        self.mapRenderer = None
        self.guiObjectAppeared = None
        self.visibilityHistory = []
        
    def CalculateEdges(self):
        lastPoint = self.points[-1]
        for point in self.points:
            edge = Edge(lastPoint, point)
            self.edges.append(edge)
            lastPoint = point
            
        for point in self.points:
            if point.x > 0 and point.y > 0 and point.x < self.width and point.y < self.height:
                self.innerPoints.append(point)
                
        xCount = self.width / 10
        yCount = self.height / 10
        for y in range(yCount):
            for x in range(xCount):
                xx = x*10+5
                yy = y*10+5
                
                if self.IsInside( Point(xx,yy) ):    
                    vObj = VisibilityObject(xx, yy, 0)
                    self.visibilityHistory.append(vObj)
        
    def Render(self, mapRenderer):
        self.mapRenderer = mapRenderer
        for edge in self.edges:
            mapRenderer.Line(edge.start.x, edge.start.y, edge.end.x, edge.end.y, "#000", "map edge")
    
    def AddObject(self, type, x, y, attractivity = 10, amount=1):
        rObj = RealObject(type, x, y, attractivity, amount)    
        self.objects.append(rObj)
        if self.guiObjectAppeared != None:
            self.guiObjectAppeared(rObj)
    
    def SetAgentStart(self, x, y):
        self.agentMoves.append( {"x":x, "y":y} )
    def PlaceAgent(self, agent):
        agent.x = self.agentMoves[0]['x']
        agent.y = self.agentMoves[0]['y']
        
    
    def MoveAgent(self, agent, newX, newY):
        if not self.CanMove(agent, newX, newY):
            Global.Log("Map.MoveAgent Programmer.Error out of map")
            return 0
        else:
            duration = self.Distance(agent.x, agent.y, newX, newY)
            self.agentMoves.append( {"x":agent.x, "y":agent.y} )
            agent.x = newX
            agent.y = newY
            #agent.guiMoved(agent)
        return round(duration)
      
    #start has old position in .x and .y 
    def CanMove(self, start, newX, newY):
        hitPoint = None
        for edge in self.edges:
            hitResult = self.AreIntersecting(edge.start, edge.end, start, Point(newX,newY) )
            if hitResult.hit:
                if hitPoint == None:
                    hitPoint = hitResult
                    hitPoint.dist = self.DistanceObjs(hitResult, start)
                else:
                    dist = self.DistanceObjs(hitResult, start)
                    if dist < hitPoint.dist: hitPoint = hitResult
        if hitPoint == None:
            return True
        else:
            return False
    def CanMoveEx(self, start, newX, newY):
        hitPoint = None
        
        for edge in self.edges:
            hitResult = self.AreIntersecting(edge.start, edge.end, start, Point(newX,newY) )
            if hitResult.hit:
                if hitPoint == None:
                    hitPoint = hitResult
                    hitPoint.dist = self.DistanceObjs(hitResult, start)
                else:
                    dist = self.DistanceObjs(hitResult, start)
                    if dist < hitPoint.dist: hitPoint = hitResult
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
            dividerCount = ceil(dist / Global.MaxAgentMove)
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
        queue.extend(self.innerPoints)
        queue.append(end)
        for point in queue:
            dist[point] = Global.MaxNumber
            previous[point] = None
        
        while len(queue) > 0:
            minPoint = queue[0]
            minPointDist = Global.MaxNumber
            for point in queue:
                if dist[point] < minPointDist:
                    minPoint = point
                    minPointDist = dist[point]
            queue.remove(minPoint)
            for point in queue:
                if self.CanMove(minPoint, point.x, point.y):
                    alt = dist[minPoint] + self.DistanceObjs(minPoint, point)
                    if alt < dist[point]:
                        dist[point] = alt
                        previous[point] = minPoint
        #all set, get data from previous
        path = []
        point = end
        while point != start:
            path.insert(0, point)
            point = previous[point]
        path.insert(0, start)
        return path
    
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
        c = False
        for edge in self.edges:
            if (edge.start.y > point.y) != (edge.end.y > point.y):
                if point.x < (edge.end.x - edge.start.x) * (point.y - edge.start.y) / (edge.end.y - edge.start.y) + edge.start.x:
                    c = not c
        return c 

    def IsVisible(self, start, end):
        hitPoint = self.CanMove(start, end.x, end.y)
        return not hitPoint.hit
    
    def GetArea(self):
        sum = 0
        vertices = copy(self.points)
        vertices.reverse()
        vertices.append(vertices[0])
        for i in range(len(self.points)):
            sum = sum + vertices[i].x * vertices[i+1].y - vertices[i].y * vertices[i+1].x
        return ( sum * 1.0) / 2
    
    def GetRealObjectIfThere(self, memObject):
        for rObj in self.objects:
            if rObj.x == memObject.x and rObj.y == memObject.y and rObj.type == memObject.type:
                return rObj
        return None
    
    def UseObject(self, excProcess, realObject):
        if realObject.Use():
            self.objects.remove(realObject)
            self.guiObjectDisAppeared(realObject)
            Global.Log("Map: agent used object " + realObject.type.name + " at " + str(realObject.y) + "," + str(realObject.x))
 
    def GetVisibleObjects(self, agent):
        objs = []
        for obj in self.objects:
            if obj.visibility > 0:
                objs.append(obj)
        return objs 
      
    def GetVisibility(self, agent, object):
        dist = self.DistanceObjs(agent, object)
        visibility = 0
        if dist == 0:
            for vc in agent.viewCones:
                visibility = visibility + vc.intensity
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
        self.calculateVisibility(agent)
        self.mapRenderer.RenderObjectVisibility()
        agent.guiMoved(agent);
        
    def calculateVisibility(self, agent):
        for obj in self.objects:
            visibility = self.GetVisibility(agent, obj)
            obj.visibility = visibility
        for obj in self.visibilityHistory:
            visibility = self.GetVisibility(agent, obj)
            obj.visibility += visibility
      
    def Distance(self, x1,y1,x2,y2):
        return sqrt((x2-x1)**2+(y2-y1)**2)
    def DistanceObj(self, x,y,object):
        return sqrt((x-object.x)**2+(y-object.y)**2)
    def DistanceObjs(self, o1,o2):
        return sqrt((o1.x-o2.x)**2+(o1.y-o2.y)**2)
        
    