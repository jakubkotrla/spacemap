
from math import *
from Enviroment.Objects import *
from Enviroment.World import *
from Enviroment.Global import Global
from Enviroment.Global import Global


class MapRenderer:
    def __init__(self, canvas, map, agent, mainWindow):
        self.canvas = canvas
        self.map = map
        self.agent = agent
        self.mainWindow = mainWindow
        self.zoom = 10
        self.guiIdsToObjects = {}
        
        self.Clear()
        self.mapEdges = self.map.Render(self)
        
        self.agentRect = self.Pixel(agent, self.agent.x, self.agent.y, "red", "agent")
        self.agentMHlines = []
        
        self.map.guiObjectAppeared = self.objectAppeared
        self.map.guiObjectDisAppeared = self.objectDisAppeared
        self.objectsRects = []
        for obj in self.map.objects:
            self.objectAppeared(obj)
          
        layer = self.agent.GetSpaceMap().Layer
        layer.mapRenderer = self
        for node in layer.nodes:
            node.Render(self)
      
      
    def Clear(self):
        self.canvas.create_polygon(0,0, self.canvas.width, 0, self.canvas.width, self.canvas.height, 0, self.canvas.height, fill="white")
        
    def GuiIdToObject(self, id):
        return self.guiIdsToObjects[id]  
        
    def Pixel(self, object, cx, cy, color, tags="pixel"):
        x = cx*self.zoom - round(self.zoom/2) 
        y = cy*self.zoom - round(self.zoom/2)
        id = self.canvas.create_rectangle(x+10,y+10, x+self.zoom+10,y+self.zoom+10, fill=color, tags=tags)
        self.guiIdsToObjects[id] = object
        return id 
    def PixelC(self, object, cx, cy, color, coef, tags="pixelc", outline="black"):
        coef = coef * 2
        x = cx*self.zoom - round(self.zoom/coef) 
        y = cy*self.zoom - round(self.zoom/coef)
        id = self.canvas.create_rectangle(x+10,y+10, x+round(2*self.zoom/coef)+10,y+round(2*self.zoom/coef)+10, fill=color, outline=outline, tags=tags)
        self.guiIdsToObjects[id] = object
        return id
    def Rectangle(self, object, cx, cy, w, h, color, tags="rectangle", outline=""):
        x = cx*self.zoom
        y = cy*self.zoom
        x2 = x+w*self.zoom
        y2 = y+h*self.zoom
        id = self.canvas.create_rectangle(x+10,y+10, x2+10,y2+10, fill=color, outline=outline, tags=tags)
        self.guiIdsToObjects[id] = object
        return id
    def CircleC(self, object, cx, cy, diameter, color, tags="ovalc"):
        x = cx*self.zoom - round(diameter*self.zoom) 
        y = cy*self.zoom - round(diameter*self.zoom)
        id = self.canvas.create_oval(x+10,y+10, x+round(2*diameter*self.zoom)+10,y+round(2*diameter*self.zoom)+10, fill="", outline=color, tags=tags)
        self.guiIdsToObjects[id] = object
        return id
    def PointC(self, object, cx, cy, color, coef, tags="pointc"):
        coef = coef * 2
        x = cx*self.zoom - round(self.zoom/coef) 
        y = cy*self.zoom - round(self.zoom/coef)
        id = self.canvas.create_oval(x+10,y+10, x+round(2*self.zoom/coef)+10,y+round(2*self.zoom/coef)+10, fill="", outline=color, tags=tags)
        self.guiIdsToObjects[id] = object
        return id
    def Pie(self, object, x0, y0, x1, y1, start, width, color, tags="pie"):
        id = self.canvas.create_arc(x0*self.zoom+10, y0*self.zoom+10, x1*self.zoom+10, y1*self.zoom+10, start=start, extent=width, style="pieslice", fill="", outline=color, tags=tags)
        self.guiIdsToObjects[id] = object
        return id
    
    def Line(self, x,y,x2,y2, color, tags="line"):
        return self.canvas.create_line(self.zoom*x+10,self.zoom*y+10, self.zoom*x2+10,self.zoom*y2+10, fill=color, tags=tags)
    
    def DeleteGuiObject(self, id):
        self.canvas.delete(id)
        if id in self.guiIdsToObjects:
            del self.guiIdsToObjects[id]
    
    
    def RenderAgent(self, agent):
        lId = self.Line(self.agent.x, self.agent.y, self.agent.newX, self.agent.newY, "#fcc", "agenttrail")
        self.agentMHlines.append(lId)
        if len(self.agentMHlines) > Global.AgentMoveHistoryLength:
            lId = self.agentMHlines.pop(0)
            self.canvas.delete(lId)
                
        self.canvas.delete(self.agentRect)
        agentx = agent.x
        agenty = agent.y
        self.agentRect = self.Pixel(agent, agentx, agenty, "red", "agent")
        
        self.canvas.delete("vcone")
        agStart = (agent.dirAngle - pi/2)
        for vc in agent.viewCones:
            if vc.angle == pi:
                self.CircleC(agent, agentx, agenty, vc.distance, "red", "vcone")
            else:
                angle = 180.0 * vc.angle / pi
                start = agStart - vc.angle
                if start < 0: start = 2*pi + start 
                start = 180.0 * start / pi
                x0 = agentx - vc.distance
                y0 = agenty - vc.distance
                x1 = agentx + vc.distance
                y1 = agenty + vc.distance
                self.Pie(vc, x0, y0, x1, y1, start, 2*angle, "red", tags="vcone")
        
    def RenderObjectVisibility(self):
        for obj in self.objectsRects:
            if obj.visibility > 0:
                self.canvas.itemconfigure(obj.guiId, fill="LightSkyBlue1")
            else:
                self.canvas.itemconfigure(obj.guiId, fill="blue")
    
    def RenderVisibilityHistory(self):
        for vObj in self.map.visibilityHistory:
            intensity = 255 - int(255 * vObj.visibility*1.0 / self.map.visibilityMaxEver)
            color = "#" + str(hex(intensity)[2:]) + str(hex(intensity)[2:]) + str(hex(intensity)[2:])
            if vObj.guiId == None:
                x = vObj.x - Global.VisibilityHistoryArea/2
                y = vObj.y - Global.VisibilityHistoryArea/2
                vObj.guiId = self.Rectangle(vObj, x, y, Global.VisibilityHistoryArea, Global.VisibilityHistoryArea, color, "visibilityobject info")
                self.canvas.tag_lower(vObj.guiId, self.mapEdges)
            else:
                self.canvas.itemconfigure(vObj.guiId, fill=color)
                
    def HideVisibilityHistory(self):
        self.canvas.delete("visibilityobject")
        for vObj in self.map.visibilityHistory:
            vObj.guiId = None
    
    def objectAppeared(self, object):
        if (object in self.objectsRects):
            Global.Log("Programmer.Error: MapRenderer.objectAppeared")
        else:
            if object.type.name == "InternalLearningObj":
                objId = self.PixelC(object, object.x, object.y, "darkgreen", 3, tags="info internalobject")
            else:
                objId = self.Pixel(object, object.x, object.y, "blue", tags="info object")
            self.objectsRects.append(object)
            object.guiId = objId
        
    def objectDisAppeared(self, object):
        pass
        #if (object in self.objectsRects.keys()):
        #    objId = self.objectsRects[object]
        #    self.canvas.delete(objId)
        #else:
        #    Global.Log("Programmer.Error: MapRenderer.objectDisAppeared")
    
           
