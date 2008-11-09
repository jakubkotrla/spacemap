
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


class MapRenderer:
    def __init__(self, canvas, map, agent):
        self.canvas = canvas
        self.map = map
        self.agent = agent
        self.zoom = 10
        self.agentMHmaxLength = 10
        self.canvas.create_polygon(0,0, self.map.width*self.zoom,0, self.map.width*self.zoom,self.map.height*self.zoom, 0,self.map.height*self.zoom, fill="white")
        
        self.agent.guiMoved = self.agentMoved
        self.agentRect = self.pixel(self.agent.x, self.agent.y, "red")
        self.agentVisibleOval = self.canvas.create_oval((self.agent.x-Global.MapVisibility)*self.zoom, (self.agent.y-Global.MapVisibility)*self.zoom, (self.agent.x+Global.MapVisibility)*self.zoom, (self.agent.y+Global.MapVisibility)*self.zoom, fill="", outline="red")
        self.agentMHlines = []
        
        self.map.guiObjectAppeared = self.objectAppeared
        self.map.guiObjectDisAppeared = self.objectDisAppeared
        self.objectsRects = {}
        for obj in self.map.objects:
            self.objectAppeared(obj)
            
        kml = self.agent.GetSpaceMap().KMLayer
        self.kmlNodes = {}
        for node in kml.nodes:
            nodeId = self.pixelC(node.x, node.y, "green", 2)
            node.guiMoved = self.klmNodeMoved
            lines = []
            for neighbour in node.neighbours:
                if neighbour in self.kmlNodes:
                    lId = self.line(node.x, node.y, neighbour.x, neighbour.y, "green")
                    lines.append(lId)
                    self.kmlNodes[neighbour].lineIds.append(lId)
            self.kmlNodes[node] = KMLNodeGui(node, nodeId, lines)
        
    def pixel(self, cx, cy, color):
        x = cx*self.zoom - round(self.zoom/2) 
        y = cy*self.zoom - round(self.zoom/2)
        return self.canvas.create_rectangle(x,y, x+self.zoom,y+self.zoom, fill=color)
    def pixelC(self, cx, cy, color, coef):
        coef = coef * 2
        x = cx*self.zoom - round(self.zoom/coef) 
        y = cy*self.zoom - round(self.zoom/coef)
        return self.canvas.create_rectangle(x,y, x+round(2*self.zoom/coef),y+round(2*self.zoom/coef), fill=color)
    
    def line(self, x,y,x2,y2, color):
        return self.canvas.create_line(self.zoom*x,self.zoom*y, self.zoom*x2,self.zoom*y2,  fill=color)
    
    
    def klmNodeMoved(self, node):
        self.canvas.delete(self.kmlNodes[node].id)
        for lineId in self.kmlNodes[node].lineIds:
            self.canvas.delete(lineId)
        
        nodeId = self.pixelC(node.x, node.y, "green", 2)
        lines = []
        for neighbour in node.neighbours:
            lId = self.line(node.x, node.y, neighbour.x, neighbour.y, "green")
            lines.append(lId)
            self.kmlNodes[neighbour].lineIds.append(lId)
        self.kmlNodes[node] = KMLNodeGui(node, nodeId, lines)
            
    
    def agentMoved(self):
        oldX = self.map.agentMoves[len(self.map.agentMoves)-1]['x']
        oldY = self.map.agentMoves[len(self.map.agentMoves)-1]['y']
        offsetX = -(oldX - self.agent.x) * self.zoom
        offsetY = -(oldY - self.agent.y) * self.zoom
                
        lId = self.line(oldX, oldY, self.agent.x, self.agent.y, "#faa")
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
    
           
