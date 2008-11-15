
from math import *
from Enviroment.Objects import *
from Enviroment.World import *
from Enviroment.Global import Global
from Enviroment.Global import Global

class KMLNodeGui:
    def __init__(self, node, id, lineIds):
        self.node = node
        self.id = id
        self.lineIds = lineIds
        
class GLNodeGui:
    def __init__(self, node, id):
        self.node = node
        self.id = id
 


class MapRenderer:
    def __init__(self, canvas, map, agent, mainWindow):
        self.canvas = canvas
        self.map = map
        self.agent = agent
        self.mainWindow = mainWindow
        self.zoom = 10
        self.agentMHmaxLength = 10
        self.canvas.create_polygon(0,0, self.map.width*self.zoom,0, self.map.width*self.zoom,self.map.height*self.zoom, 0,self.map.height*self.zoom, fill="white")
        
        self.agent.guiMoved = self.agentMoved
        self.agentRect = self.pixel(self.agent.x, self.agent.y, "red", "agent")
        self.agentVisibleOval = self.canvas.create_oval((self.agent.x-Global.MapVisibility)*self.zoom, (self.agent.y-Global.MapVisibility)*self.zoom, (self.agent.x+Global.MapVisibility)*self.zoom, (self.agent.y+Global.MapVisibility)*self.zoom, fill="", outline="red", tags="visible")
        self.agentMHlines = []
        
        self.map.guiObjectAppeared = self.objectAppeared
        self.map.guiObjectDisAppeared = self.objectDisAppeared
        self.objectsRects = {}
        for obj in self.map.objects:
            self.objectAppeared(obj)
            
#        kml = self.agent.GetSpaceMap().KMLayer
#        self.kmlNodes = {}
#        self.idToKMLNode = {}
#        for node in kml.nodes:
#            nodeId = self.pixelC(node.x, node.y, "green", 2, "kmlnode")
#            node.guiMoved = self.kmlNodeMoved
#            lines = []
#            for neighbour in node.neighbours:
#                if neighbour in self.kmlNodes:
#                    lId = self.line(node.x, node.y, neighbour.x, neighbour.y, "green", "kmlline")
#                    lines.append(lId)
#                    self.kmlNodes[neighbour].lineIds.append(lId)
#            self.kmlNodes[node] = KMLNodeGui(node, nodeId, lines)
#            self.idToKMLNode[nodeId] = self.kmlNodes[node]
            
#        gl = self.agent.GetSpaceMap().GLayer
#        self.glNodes = {}
#        self.idToGLNode = {}
#        for node in gl.nodes:
#            nodeId = self.pixelC(node.x, node.y, "green", 2, "glnode")
#            node.guiMoved = self.glNodeMoved
#            
#            self.glNodes[node] = GLNodeGui(node, nodeId)
#            self.idToGLNode[nodeId] = self.glNodes[node]

        
            
        
        
    def pixel(self, cx, cy, color, tags="pixel"):
        x = cx*self.zoom - round(self.zoom/2) 
        y = cy*self.zoom - round(self.zoom/2)
        return self.canvas.create_rectangle(x,y, x+self.zoom,y+self.zoom, fill=color, tags=tags)
    def pixelC(self, cx, cy, color, coef, tags="pixelc"):
        coef = coef * 2
        x = cx*self.zoom - round(self.zoom/coef) 
        y = cy*self.zoom - round(self.zoom/coef)
        return self.canvas.create_rectangle(x,y, x+round(2*self.zoom/coef),y+round(2*self.zoom/coef), fill=color, tags=tags)
    
    def line(self, x,y,x2,y2, color, tags="line"):
        return self.canvas.create_line(self.zoom*x,self.zoom*y, self.zoom*x2,self.zoom*y2,  fill=color, tags=tags)
    
    
    def glNodeMoved(self, node):
        self.canvas.delete(self.glNodes[node].id)
        del self.idToGLNode[self.glNodes[node].id]
                    
        nodeId = self.pixelC(node.x, node.y, "green", 2, "glnode")
        self.glNodes[node] = GLNodeGui(node, nodeId)
        self.idToGLNode[nodeId] = self.glNodes[node]
    
    def IdToKMLNodeGui(self, id):
        return self.idToKMLNode[id]
    
    def kmlNodeMoved(self, node):
        self.canvas.delete(self.kmlNodes[node].id)
        del self.idToKMLNode[self.kmlNodes[node].id]
        for lineId in self.kmlNodes[node].lineIds:
            self.canvas.delete(lineId)
                    
        nodeId = self.pixelC(node.x, node.y, "green", 2, "kmlnode")
        lines = []
        for neighbour in node.neighbours:
            lId = self.line(node.x, node.y, neighbour.x, neighbour.y, "green", "kmlline")
            lines.append(lId)
            self.kmlNodes[neighbour].lineIds.append(lId)
        self.kmlNodes[node] = KMLNodeGui(node, nodeId, lines)
        self.idToKMLNode[nodeId] = self.kmlNodes[node]
    
    def agentMoved(self):
        oldX = self.map.agentMoves[len(self.map.agentMoves)-1]['x']
        oldY = self.map.agentMoves[len(self.map.agentMoves)-1]['y']
        offsetX = -(oldX - self.agent.x) * self.zoom
        offsetY = -(oldY - self.agent.y) * self.zoom
                
        lId = self.line(oldX, oldY, self.agent.x, self.agent.y, "#faa", "agenttrail")
        self.agentMHlines.append(lId)
        if len(self.agentMHlines) > self.agentMHmaxLength:
            lId = self.agentMHlines.pop(0)
            self.canvas.delete(lId)
                
        self.canvas.move(self.agentRect, offsetX, offsetY)
        self.canvas.move(self.agentVisibleOval, offsetX, offsetY)


    def objectAppeared(self, object):
        if (object in self.objectsRects.keys()):
            Global.Log("Programmer Error: MapRenderer.objectAppeared")
        else:
            objId = self.pixel(object.x, object.y, "blue")
            self.objectsRects[object] = objId
        
    def objectDisAppeared(self, object):
        if (object in self.objectsRects.keys()):
            objId = self.objectsRects[object]
            self.canvas.delete(objId)
        else:
            Global.Log("Programmer Error: MapRenderer.objectDisAppeared")
    
           
