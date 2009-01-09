
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
        self.maxAttractivity = 20
         
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
         

class Map:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.points = []
        self.edges = []  
        self.objects = []
        self.agentMoves = []
        self.guiObjectAppeared = None
        
    def CalculateEdges(self):
        lastPoint = self.points[-1]
        for point in self.points:
            edge = Edge(lastPoint, point)
            self.edges.append(edge)
            lastPoint = point
        
    def Render(self, mapRenderer):
        for edge in self.edges:
            mapRenderer.Line(edge.start.x, edge.start.y, edge.end.x, edge.end.y, "#000", "map edge")
    
    def AddObject(self, type, x, y, attractivity = 10, amount=1):
        rObj = RealObject(type, x, y, attractivity, amount)    
        self.objects.append(rObj)
        if self.guiObjectAppeared != None:
            self.guiObjectAppeared(rObj)
    
    def PickUpObject(self, agent, rObject):
        if self.DistanceObjs(agent, rObject) < Global.MapObjectPickupDistance:
            self.objects.remove(rObject)
            return True
        return False 
    
    def SetAgentStart(self, x, y):
        self.agentMoves.append( {"x":x, "y":y} )
    def PlaceAgent(self, agent):
        agent.x = self.agentMoves[0]['x']
        agent.y = self.agentMoves[0]['y']
        
    
    def MoveAgent(self, agent, newX, newY):
        hitPoint = self.CanMove(agent, newX, newY)
        if hitPoint.hit:
            return 0
        else:
            duration = self.Distance(agent.x, agent.y, newX, newY)
            self.agentMoves.append( {"x":agent.x, "y":agent.y} )
            agent.x = newX
            agent.y = newY
            agent.guiMoved()
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
            return Hit(0, 0, False)
        else:
            #we know the point of hit!
            return hitPoint
    
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
 
        
    def GetVisibleObjects(self, centerX, centerY):
        objs = []
        for obj in self.objects:
            if self.DistanceObj(centerX, centerY, obj) < Global.MapVisibility:
                objs.append(obj)
        return objs 
      
    def IsObjectVisibleFrom(self, object, x, y):
        return (self.DistanceObj(x,y,object) < Global.MapVisibility)
      
    def Distance(self, x1,y1,x2,y2):
        return sqrt((x2-x1)**2+(y2-y1)**2)
    def DistanceObj(self, x,y,object):
        return sqrt((x-object.x)**2+(y-object.y)**2)
    def DistanceObjs(self, o1,o2):
        return sqrt((o1.x-o2.x)**2+(o1.y-o2.y)**2)
        
    