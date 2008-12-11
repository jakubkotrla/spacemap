
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
        self.width = 100
        self.height = 100
        self.points = [ Point(0,0), Point(100,0), Point(100,100), Point(0,100) ]
        self.edges = []  
        self.objects = []
        self.agentMoves = []
        self.guiObjectAppeared = None
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
    
    def PlaceAgent(self, agent, x, y):
        self.agentMoves.append( {"x":agent.x, "y":agent.y} )
        agent.x = x
        agent.y = y
        
    
    def MoveAgent(self, agent, newX, newY):
        if (newX < 0 or newY < 0 or newX > self.width or newY > self.height):
            return 0
        
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
        
        
# Configuration part
map = Map()

#map.AddObject(Meal, 20, 25, amount=10)
map.AddObject(Snickers, 80, 55)
map.AddObject(CocaColaCan, 50, 35)
#map.AddObject(Glasses, 50, 55)
#map.AddObject(Book, 51, 56)
map.AddObject(Plate, 90, 55)
map.AddObject(Water, 10, 75)
#map.AddObject(Wood, 51, 52)
#map.AddObject(Torch, 50, 52)
map.AddObject(Pipe, 30, 35)

Global.Map = map
