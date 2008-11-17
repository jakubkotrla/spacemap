
from Enviroment.Global import Global


class GridLayerNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.linkToObjects = []
        
        self.guiId = None
        
    def Render(self, mapRenderer):
        self.guiId = mapRenderer.PixelC(self, self.x, self.y, "green", 2, "gridlayernode info")
                
    def ToString(self):
        return "GridLayerNode [" + self.x + "," + self.y + "]"
                
    def Train(self, memObject, effect):
        # no training
        pass
            


class GridLayer:
    def __init__(self, area):
        self.area = area
        self.nodes = []
        self.density = 10
        
    def CreateMap(self):
        xCount = self.area.width / self.density
        yCount = self.area.height / self.density
        for y in range(yCount):
            for x in range(xCount):
                node = GridLayerNode(x*self.density+self.density/2, y*self.density+self.density/2)
                self.nodes.append(node)
        
    def PositionToNodes(self, x, y):
        inNodes = []
        closestNode = None
        closestDistance = Global.MaxNumber
        map = Global.Map
        per = Global.GridLayerNodeSize 
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
                nls[node] = self.area.DistanceObj(x,y,node)
            inNodes.sort(lambda a,b: cmp(nls[a],nls[b]))
            return inNodes
        else:
            return [closestNode]
    
    def StepUpdate(self):
        pass
    
    def ObjectNoticed(self, memObject, intensity=1):
        #no training
        pass
    def ObjectFound(self, rObject):
        pass
    def ObjectNotFound(self, rObject):
        pass
    def ObjectUsed(self, rObject):
        pass
    def ObjectUsedUp(self, rObject):
        pass
