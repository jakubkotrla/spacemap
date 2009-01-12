
from Enviroment.Global import Global
from math import sqrt
from Enviroment.Map import Point, Map

class PathFinderNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = []
        
        self.guiId = None
        self.mapRenderer = None
        
        
    def Render(self, mapRenderer):
        self.guiId = mapRenderer.CircleC(self, self.x, self.y, "darkgreen", 0.5, "energylayerpoint info")
        self.mapRenderer = mapRenderer
    def ToString(self):
        strInfo = []
        strXY = '%.4f'%(self.x) + "," + '%.4f'%(self.y)
        strInfo.append("PathFinderNode [" + strXY + "]")
        

class PathFinder:
    def __init__(self, area):
        self.area = area
        self.nodes = []
        self.mapRenderer = None
        
    def CreateMap(self):
        areaArea = self.area.GetArea()
        nodeCount = areaArea / Global.PFDensity ** 2

        xCount = self.area.width / Global.PFDensity
        yCount = self.area.height / Global.PFDensity
        density = Global.PFDensity
        for y in range(yCount):
            for x in range(xCount):
                xx = x*density+density/2
                yy = y*density+density/2
                
                if self.area.IsInside( Point(xx,yy) ):    
                    node = PathFinderNode(self, xx, yy, self.nodeIndex)
                    self.nodes.append(node)
        #calculate edges to have graph
        
        
    #returns list of points to move through
    def FindWay(self, start, end):
        way = []
        return way
        
    def positionToNode(self, x, y):
        inNodes = []
        closestNode = None
        closestDistance = Global.MaxNumber
        map = Global.Map
        for node in self.nodes:
            distance = map.DistanceObj(x, y, node)
            if distance < closestDistance:
                closestNode = node
                closestDistance = distance
        return closestNode
    
        
    def getNodesAround(self, node, range):
        nodesAround = []
        range = range ** 2
        for n in self.nodes:
            if n == node: continue
            dist = (n.x-node.x)**2+(n.y-node.y)**2
            if dist < range:
                nodesAround.append(n)
        return nodesAround

 
