
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

class Map:
    def __init__(self):
        self.width = 100
        self.height = 100
        self.objects = []
        self.map = [[0 for col in range(self.width)] for row in range(self.height)]
        for i in range(self.width):
            for j in range(self.height):
                self.map[i][j] = None
        self.agentMoves = []
        self.guiObjectAppeared = None
        
    def AddObject(self, type, x, y, attractivity = 10, amount=1):
        rObj = RealObject(type, x, y, attractivity, amount)    
        self.objects.append(rObj)
        self.map[x][y] = rObj
        if self.guiObjectAppeared != None:
            self.guiObjectAppeared(rObj)
    
    def PickUpObject(self, agent, rObject):
        if self.Distance(agent.x, agent.y, rObject) < Global.MapObjectPickupDistance:
            self.objects.remove(rObject)
            return True
        return False 
    
    def PlaceAgent(self, agent, x, y):
        self.agentMoves.append( {"x":agent.x, "y":agent.y} )
        agent.x = x
        agent.y = y
        
    
    def MoveAgent(self, agent, newX, newY):
        #ToDo: check locations, waypoints, impassable things etc.
        
        if (newX < 0 or newY < 0 or newX > self.width/2 or newY > self.height/2):
            return 0
        
        duration = self.Distance(agent.x, agent.y, newX, newY)
        self.agentMoves.append( {"x":agent.x, "y":agent.y} )
        agent.x = newX
        agent.y = newY
        agent.guiMoved()
        return round(duration)
      
    def CanMoveAgent(self, agent, newX, newY):
        #ToDo: check locations, waypoints, impassable things etc.
        if (newX < 0 or newY < 0 or newX > self.width/2 or newY > self.height/2):
            return False
        return True
    
    def GetRealObjectIfThere(self, memObject):
        rObj = self.map[memObject.x][memObject.y]
        if rObj != None and rObj.type == memObject.type:
            return rObj
        else:
            return None
    
    def UseObject(self, excProcess, realObject):
        if realObject.Use():
            self.map[realObject.x][realObject.y] = None
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

map.AddObject(Meal, 20, 25, amount=10)
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
