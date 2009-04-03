
import time
from math import *
from Enviroment.Objects import *
from Enviroment.World import *
from Enviroment.Global import Global
from Enviroment.Map import Point
from PIL import Image, ImageDraw, ImageFont, ImageColor
from Tkinter import NW
from Enviroment.Time import Time 


class MapRenderer:
    def __init__(self, canvas, map, agent, mainWindow, renderAtStart=True):
        self.canvas = canvas
        self.map = map
        self.agent = agent
        self.mainWindow = mainWindow
        self.zoom = 10
        self.guiIdsToObjects = {}
        
        self.font = ImageFont.truetype("arial.ttf", 12)
        
        self.Clear()
        if renderAtStart:
            self.mapEdges = self.map.Render(self)
        
            self.agentRect = self.Pixel(agent, self.agent.x, self.agent.y, "red", "agent")
            self.agentMHlines = []
        
            self.objectsRects = []
            for obj in self.map.objects:
                objId = self.Pixel(obj, obj.x, obj.y, "blue", tags="info object")
      
    def Clear(self):
        self.canvas.addtag_all("2del")
        self.canvas.delete("2del")
        self.canvas.create_polygon(0,0, self.canvas.width, 0, self.canvas.width, self.canvas.height, 0, self.canvas.height, fill="white")
        
    def GuiIdToObject(self, id):
        return self.guiIdsToObjects[id]  
        
    def Pixel(self, object, cx, cy, color, tags="pixel"):
        x = cx*self.zoom - round(self.zoom/2) 
        y = cy*self.zoom - round(self.zoom/2)
        id = self.canvas.create_rectangle(x+10,y+10, x+self.zoom+10,y+self.zoom+10, fill=color, outline="", tags=tags)
        self.guiIdsToObjects[id] = object
        return id 
    def PixelC(self, object, cx, cy, color, coef, tags="pixelc", outline=""):
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
                self.canvas.itemconfigure(obj.guiId, fill="#6496ff")
            else:
                self.canvas.itemconfigure(obj.guiId, fill="#0000ff")
    
    def RenderVisibilityHistory(self):
        for vObj in self.map.visibilityHistory:
            intensity = 255 - int(255 * vObj.visibility*1.0 / self.map.visibilityMaxEver)
            color = str(hex(intensity*65536 + intensity*256 + intensity)[2:])
            color = "#" + color.zfill(6)
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
            
    def RenderSpaceMap(self):
        energyPoints = self.agent.intelligence.spaceMap.Layer.energyPoints
        self.canvas.delete("energylayerpoint")
        for ep in energyPoints:
            self.PointC(ep, ep.x, ep.y, "#00c800", 0.5, "energylayerpoint info")
        
        hlNodes = self.agent.intelligence.spaceMap.Layer.hlNodes
        self.canvas.delete("energylayerHLnode")
        for hlNode in hlNodes:
            self.PixelC(hlNode, hlNode.x, hlNode.y, None, 1, "energylayerHLnode info", outline="#00a800")
            self.CircleC(hlNode, hlNode.x, hlNode.y, hlNode.range, "#00a800", "energylayerHLnode info")
            for node in hlNode.nodes:
                self.Line(hlNode.x, hlNode.y, node.x, node.y, "#00c900", "energylayerHLnode")
        
        elnodes = self.agent.intelligence.spaceMap.Layer.nodes
        self.canvas.delete("energylayernode")
        for node in elnodes:
            self.PixelC(node, node.x, node.y, "#00b500", 2, "energylayernode info")
            
        self.canvas.delete("energylayerPlace")
        places = self.agent.intelligence.spaceMap.Layer.places
        for place in places:
            if place.parent == None: continue
            self.PixelC(place, place.x, place.y, None, 1, "energylayerPlace info", outline="#0000aa")
            self.CircleC(place, place.x, place.y, place.range, "#0000aa", "energylayerPlace info")
            for node in place.nodes:
                 self.Line(place.x, place.y, node.x, node.y, "#0000aa", "energylayerPlace")
         
    
    def RenderProgress(self, progressObject, configName):
        txt = "Progress:\n\n\n"
        txt = txt + " Total test to run: "
        txt = txt + str(progressObject.testToRunCount) + "\n\n"
        txt = txt + " Current test running: "
        txt = txt + str(progressObject.currentTestIndex) + "  (" + configName + ")" + "\n\n"
        txt = txt + " Time passed: "
        secs = time.time() - progressObject.testRunStarted
        timePassed = Time()
        timePassed.AddSeconds(secs)
        txt = txt + timePassed.TimeToHumanFormat(True) + "\n\n"
        txt = txt + " Percentage done: "
        per = (100.0*(progressObject.currentTestIndex-1) / progressObject.testToRunCount)
        txt = txt +  '%.3f'%(per) + "%\n\n"
        txt = txt + " Time left: "
        secs = float(100-per)*secs / max(Global.MinPositiveNumber, per)
        timeLeft = Time()
        timeLeft.AddSeconds(secs)
        txt = txt + timeLeft.TimeToHumanFormat(True) + "\n\n"
        self.canvas.create_text(10, 10, text=txt, width=500, anchor=NW, tags="progress")
    def RenderProgressInTest(self, step, stepCount):
        self.canvas.delete("progresstest")
        txt = "Test: " + str(step) + "/" + str(stepCount)
        self.canvas.create_text(10, 200, text=txt, width=500, anchor=NW, tags="progresstest")
        
    
    #layers full: [agent, eps(energyPoints), ov(object.visibility), vh(visibilityHistory), objvh(objectVisibilityHistory), info(text info, log, etc.), wp(waypoint)]
    def RenderToFile(self, world, filename, layers=[]):
        if "info" in layers:
            im = Image.new("RGB", (1500, 1020), (255, 2555, 255))
        else:
            im = Image.new("RGB", (1100, 1100), (255, 2555, 255))
        draw = ImageDraw.Draw(im)
        
        if "vh" in layers:
            for vObj in self.map.visibilityHistory:
                intensity = 255 - int(255 * vObj.visibility*1.0 / self.map.visibilityMaxEver)
                color = (intensity, intensity, intensity)
                x = (vObj.x - Global.VisibilityHistoryArea/2) *self.zoom + 10
                y = (vObj.y - Global.VisibilityHistoryArea/2) *self.zoom + 10
                length = Global.VisibilityHistoryArea * self.zoom
                draw.rectangle([x,y, x+length,y+length], fill=color, outline=None)
        
        for edge in self.map.edges:
            draw.line( [self.zoom*edge.start.x+10, self.zoom*edge.start.y+10, self.zoom*edge.end.x+10, self.zoom*edge.end.y+10], fill=(0,0,0))
        if "wp" in layers:
            for wayPoint in self.map.wayPoints:
                x = wayPoint.x*self.zoom - 2 + 10
                y = wayPoint.y*self.zoom - 2 + 10
                draw.rectangle([x,y, x+4,y+4], fill=(0,0,0), outline=None)
        
        if "agent" in layers:
            lastPoint = self.map.agentMoves[0]
            points = self.map.agentMoves[1:]
            points.append( Point(self.agent.newX, self.agent.newY) )
            for point in points:
                draw.line( [self.zoom*lastPoint.x+10, self.zoom*lastPoint.y+10, self.zoom*point.x+10, self.zoom*point.y+10], fill=(255, 200, 200))
                lastPoint = point
            x = self.agent.x*self.zoom - 5 + 10
            y = self.agent.y*self.zoom - 5 + 10
            draw.rectangle([x,y, x+10,y+10], fill=(255, 0, 0), outline=None)
            agStart = (self.agent.dirAngle - pi/2)
            for vc in self.agent.viewCones:
                if vc.angle == pi:
                    x = self.agent.x*self.zoom - round(vc.distance*self.zoom) + 10
                    y = self.agent.y*self.zoom - round(vc.distance*self.zoom) + 10
                    draw.ellipse([x,y, x+round(2*vc.distance*self.zoom),y+round(2*vc.distance*self.zoom)], outline=(255, 0, 0))
                else:
                    start = agStart + vc.angle
                    if start < 0: start = 2*pi + start
                    if start > 2*pi: start = start - 2*pi
                    start = int(360 - (180.0 * start / pi))
                    end = agStart - vc.angle
                    if end < 0: end = 2*pi + end
                    end = int(360 - (180.0 * end / pi))
                    x = int(self.agent.x*self.zoom - round(vc.distance*self.zoom) + 10)
                    y = int(self.agent.y*self.zoom - round(vc.distance*self.zoom) + 10)
                    draw.pieslice([x,y, x+int(2*vc.distance*self.zoom),y+int(2*vc.distance*self.zoom)], start, end, outline=(255, 0, 0))
        
        spaceMap = self.agent.intelligence.spaceMap
        elayer = spaceMap.Layer
        if "eps" in layers:
            for ep in elayer.energyPoints:
                x = ep.x*self.zoom #- 10 + 10
                y = ep.y*self.zoom #- 10 + 10
                draw.ellipse([x,y, x+20,y+20], fill=None, outline=(0, 200, 0))
        if "ovh" in layers:    
            for obj in self.map.objects:
                x = obj.x*self.zoom - 5 + 10
                y = obj.y*self.zoom - 5 + 10
                intensity = 255 - int(255 * obj.trainHistory*1.0 / max(Global.MinPositiveNumber, spaceMap.maxTrained))
                color = (intensity, intensity, intensity)
                draw.rectangle([x,y, x+10,y+10], fill=color, outline=(0, 0, 0))        
        elif "ov" in layers:
            for obj in self.map.objects:
                x = obj.x*self.zoom - 5 + 10
                y = obj.y*self.zoom - 5 + 10
                if obj.visibility > 0:
                    draw.rectangle([x,y, x+10,y+10], fill=(100, 150, 255), outline=None)
                else:
                    draw.rectangle([x,y, x+10,y+10], fill=(0, 0, 255), outline=None)
        else:
            for obj in self.map.objects:
                x = obj.x*self.zoom - 5 + 10
                y = obj.y*self.zoom - 5 + 10
                draw.rectangle([x,y, x+10,y+10], fill=(0, 0, 255), outline=None)
        
        
        for hlNode in elayer.hlNodes:
            x = (hlNode.x-hlNode.range)*self.zoom + 10
            y = (hlNode.y-hlNode.range)*self.zoom + 10
            x2 = (hlNode.x+hlNode.range)*self.zoom + 10
            y2 = (hlNode.y+hlNode.range)*self.zoom + 10
            draw.ellipse([x,y, x2,y2], fill=None, outline=(0, 128, 0))
            x = hlNode.x*self.zoom - 5 + 10
            y = hlNode.y*self.zoom - 5 + 10
            draw.rectangle([x,y, x+10,y+10], fill=None, outline=(0, 128, 0))
            for node in hlNode.nodes:
                draw.line( [x+5, y+5, self.zoom*node.x+10, self.zoom*node.y+10], fill=(0, 222, 0))
        for place in elayer.places:
            if place.parent == None: continue
            x = (place.x-place.range)*self.zoom + 10
            y = (place.y-place.range)*self.zoom + 10
            x2 = (place.x+place.range)*self.zoom + 10
            y2 = (place.y+place.range)*self.zoom + 10
            draw.ellipse([x,y, x2,y2], fill=None, outline=(0, 0, 128))
            x = place.x*self.zoom - 5 + 10
            y = place.y*self.zoom - 5 + 10
            draw.rectangle([x,y, x+10,y+10], fill=None, outline=(0, 0, 128))
            for node in place.nodes:
                draw.line( [x+5, y+5, self.zoom*node.x+10, self.zoom*node.y+10], fill=(0, 0, 128))
        
        for node in elayer.nodes:    
            x = node.x*self.zoom - 2 + 10
            y = node.y*self.zoom - 2 + 10
            draw.rectangle([x,y, x+4,y+4], fill=(0, 180, 0), outline=None)
        
        if "ovh" in layers:    
            for obj in self.map.objects:
                x = obj.x*self.zoom - 5 + 10
                y = obj.y*self.zoom - 5 + 10
                draw.text([x+5,y+10], str(obj.trainHistory), font=self.font, fill=(0, 0, 0))
                
        if "info" in layers:
            draw.text([1080,5], "Step:  " + str(world.step).zfill(6), font=self.font, fill=(0, 0, 0))
            draw.text([1080,20], "Time:  " + Global.TimeToHumanFormat(True), font=self.font, fill=(0, 0, 0))
            strXY = "%.4f,%.4f" % (self.agent.x, self.agent.y)
            draw.text([1300,5], "Agent:  " + strXY, font=self.font, fill=(0, 0, 0))
            draw.text([1300,20], "EnergyLayer.nodeCount: " + str(len(elayer.nodes)), font=self.font, fill=(0, 0, 0))
            txt = self.agent.paText
            draw.text([1050,50], "ProcessArea:", font=self.font, fill=(0, 0, 0))
            ypos = 50
            for t in txt:
                ypos = ypos + 14
                draw.text([1050,ypos], t, font=self.font, fill=(0, 0, 0))
            ma = self.agent.intelligence.memoryArea
            draw.text([1050,200], "MemoryArea:", font=self.font, fill=(0, 0, 0))
            ypos = 200
            for phantom in ma.memoryPhantoms:
                ypos = ypos + 15
                draw.text([1050,ypos], " " + phantom.ToString(), font=self.font, fill=(0, 0, 0))
            pf = self.agent.intelligence.perceptionField
            draw.text([1050,300], "PerceptionField:", font=self.font, fill=(0, 0, 0))
            ypos = 300
            for phantom in pf.environmentPhantoms:
                ypos = ypos + 15
                draw.text([1050,ypos], " " + phantom.ToString(), font=self.font, fill=(0, 0, 0))
            draw.text([1050,500], "Log:", font=self.font, fill=(0, 0, 0))
            ypos = 500
            for line in Global.logLines:
                ypos = ypos + 15
                draw.text([1050,ypos], "  " + line, font=self.font, fill=(0, 0, 0))
        else:
            draw.text([10,1020], "Step: " + str(world.step).zfill(6), font=self.font, fill=(0, 0, 0))
            draw.text([400,1020], "Time: " + Global.TimeToHumanFormat(True), font=self.font, fill=(0, 0, 0))
         
        im.save(filename, "PNG")

