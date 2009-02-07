
from Tkinter import *   
from threading import *
import time
from random import seed
from PIL import ImageGrab, ImageDraw, ImageFont
from Enviroment.Global import Global
from Enviroment.World import World
from Enviroment.Affordances import Affordances
from Enviroment.Objects import Objects
from Agents.Agent import Agent
from MapRenderer import MapRenderer  
from Config.Config import Config                         
                                     
class MainWindow(Frame):
    def __init__(self, master=None):                    
        Frame.__init__(self, master)
        tl = self.winfo_toplevel()
        tl.geometry("1500x1100+0+0")
        tl.title("SpaceMap MainWindow")
        self.lock = None
        self.mapRenderer = None
        self.agent = None
        
        self.captureScreen = False
        self.saveStep = 0
        self.font = ImageFont.truetype("arial.ttf", 12) 
        
        self.playbackLock = None
        self.playbackLockLocked = False 
        
        self.wndAffordances = None
        self.wndObjects = None
        self.wndRealObjects = None
        self.wndLog = None
        self.wndInfo = None
        
        self.pack()  
        self.createWidgets()   
        self.createMenu()
        
        self.captureScreenCheck()
        
    
    def createWidgets(self):
        self.wxCanvas = Canvas(self, width=1500, height=1100)
        self.wxCanvas.grid(row=0, column=0)
        self.wxCanvas.bind('<Button-1>', self.canvasClick)
        self.wxCanvas.width = 1500
        self.wxCanvas.height = 1100
                                  
    def createMenu(self):
        worldMenu = Menu()
        worldMenu.add_command(label="Show Affordances", command=self.showAffordances)
        worldMenu.add_command(label="Show Object Types", command=self.showObjectTypes)
        worldMenu.add_command(label="Show Objects", command=self.showObjects)
        worldMenu.add_command(label="Show Log", command=self.showLog)
        worldMenu.add_checkbutton(label="Capture screen", command=self.captureScreenCheck)
                  
        menubar = Menu(self)
        menubar.add_command(label="Start", command=self.startSimulation)
        menubar.add_command(label="Pause", command=self.pauseSimulation)
        menubar.add_command(label="Resume", command=self.resumeSimulation)
        menubar.add_cascade(label="World", menu=worldMenu)
        menubar.add_command(label="Quit", command=self.quitSimulation)
        self.winfo_toplevel().config(menu=menubar)
        
    def showAffordances(self):
        wndAffordances = Toplevel()
        wndAffordances.geometry("400x200")
        wndAffordances.title("SpaceMap - List of Affordances")
        txt = Listbox(wndAffordances)
        txt.pack(side=LEFT, fill=BOTH, expand=1)
        scrollBar = Scrollbar(wndAffordances, orient=VERTICAL, command=txt.yview)
        txt["yscrollcommand"]  =  scrollBar.set
        scrollBar.pack(side=RIGHT, fill=Y)
        for aff in Affordances:
            txt.insert("end", aff.name)
    def showObjectTypes(self):
        wndObjects = Toplevel()
        wndObjects.geometry("400x200")
        wndObjects.title("SpaceMap - List of Object Types")
        txt = Listbox(wndObjects)
        txt.pack(side=LEFT, fill=BOTH, expand=1)
        scrollBar = Scrollbar(wndObjects, orient=VERTICAL, command=txt.yview)
        txt["yscrollcommand"]  =  scrollBar.set
        scrollBar.pack(side=RIGHT, fill=Y)
        for obj in Objects:
            txt.insert("end", obj.ToString())
    def showObjects(self):
        wndRealObjects = Toplevel()
        wndRealObjects.geometry("400x200")
        wndRealObjects.title("SpaceMap - List of Object in World")
        wndRealObjects = wndRealObjects
        txt = Listbox(wndRealObjects)
        txt.pack(side=LEFT, fill=BOTH, expand=1)
        scrollBar = Scrollbar(wndRealObjects, orient=VERTICAL, command=txt.yview)
        txt["yscrollcommand"]  =  scrollBar.set
        scrollBar.pack(side=RIGHT, fill=Y)
        map = Global.Map
        for obj in map.objects:
            txt.insert("end", obj.ToString())
    def showLog(self):
        wndLog = Toplevel()
        wndLog.geometry("700x200+0+1000")
        wndLog.title("SpaceMap - Log")
        Global.wndLog = wndLog
        txtLog = Listbox(wndLog)
        txtLog.pack(side=LEFT, fill=BOTH, expand=1)
        Global.wndLog.txtLog = txtLog
        scrollBar = Scrollbar(wndLog, orient=VERTICAL, command=txtLog.yview)
        txtLog["yscrollcommand"]  =  scrollBar.set
        scrollBar.pack(side=RIGHT, fill=Y)
    def captureScreenCheck(self):
        self.captureScreen = not self.captureScreen
        
    
    def canvasClick(self, event):
        x = int(self.wxCanvas.canvasx(event.x))
        y = int(self.wxCanvas.canvasy(event.y))
        ids = self.wxCanvas.find_overlapping(x,y, x+1,y+1)
        if len(ids) < 1: return
        strInfo = []
        for id in ids:
            tags = self.wxCanvas.gettags(id)
            if "info" in tags:
                strInfo.append( self.mapRenderer.GuiIdToObject(id).ToString() )
        if self.wndInfo == None:
            self.wndInfo = Toplevel()
            self.wndInfo.geometry("400x200+1020+500")
            self.wndInfo.title("SpaceMap - Objects Info")
            self.wndInfo.txt = Listbox(self.wndInfo)
            self.wndInfo.txt.pack(side=LEFT, fill=BOTH, expand=1)
            self.wndInfo.bind("<Destroy>", self.wndInfoClosed) 
        else:
            self.wndInfo.txt.delete(0, 100)
        for strI in strInfo:
            if type(strI) is ListType:
                s = strI.pop(0)
                self.wndInfo.txt.insert("end", s)
                for s in strI:
                    self.wndInfo.txt.insert("end", " - " + s)
            else:
                self.wndInfo.txt.insert("end", strI)
    def wndInfoClosed(self, event):
        self.wndInfo = None    

    def startSimulation(self):
        config = Config("Lobby")
        world = World( config )
        Global.World = world
        seed()

        self.agent = Agent("agent1", config)
        world.SetAgent(self.agent)
        self.mapRenderer = MapRenderer(self.wxCanvas, Global.Map, self.agent, self)
        
        self.saveStep = Global.SaveFreq
        
        self.lock = Lock()
        self.lock.acquire()
        self.playbackLock = Lock()
        th = Thread(None, self.step, name="steps")
        th.start()     
    
    def step(self):
        world = Global.World
        self.lockBack = Lock()
        self.lockBack.acquire()
        step = 0
        while True:
            world.Step()
            
            self.RenderState(world);
            
            if self.captureScreen:
                x0 = self.wxCanvas.winfo_rootx()
                y0 = self.wxCanvas.winfo_rooty()
                x1 = x0 + self.wxCanvas.winfo_reqwidth()
                y1 = y0 + self.wxCanvas.winfo_reqheight()

                self.saveStep = self.saveStep + 1
                if self.saveStep > Global.SaveFreq:
                    self.saveStep = 0
                    im = ImageGrab.grab((x0,y0, x1,y1))
                    secs = Global.GetSeconds()
                    draw = ImageDraw.Draw(im)
                    draw.text((5, 1050), str(step) + " steps = " + Global.TimeToHumanFormat(True), font=self.font, fill="black")
                    im.save("../../exs/sp" + str(secs).zfill(10) + ".png", "PNG")
            #end of captureScreen            
            
            time.sleep(0.1)
            step = step + 1
            if self.lock.acquire(False): break
            self.playbackLock.acquire()
            self.playbackLock.release()
            
        self.lockBack.release()
        return
    
    def RenderState(self, world):
        self.wxCanvas.delete("infotxt")
        pa = self.agent.intelligence.processesArea
        txt = "ProcessArea:\n" + self.agent.paText
        self.txtPA = self.wxCanvas.create_text(1020, 10, text=txt, width=230, anchor=NW, tags="infotxt")
        
        ma = self.agent.intelligence.memoryArea
        txt = "MemoraArea:\n "
        for phantom in ma.memoryPhantoms:
            txt = txt + phantom.ToString() + "\n "  
        self.txtMA = self.wxCanvas.create_text(1270, 10, text=txt, width=230, anchor=NW, tags="infotxt")
        
        pf = self.agent.intelligence.perceptionField
        txt = "PerceptionField:\n "
        for phantom in pf.environmentPhantoms:
            txt = txt + phantom.ToString() + "\n "
        self.txtPF = self.wxCanvas.create_text(1270, 110, text=txt, width=230, anchor=NW, tags="infotxt")
        
        
    
    def pauseSimulation(self):
        if self.playbackLock != None and not self.playbackLockLocked:
            self.playbackLock.acquire()
            self.playbackLockLocked = True
    def resumeSimulation(self):
        if self.playbackLock != None and self.playbackLockLocked:
            self.playbackLock.release()
            self.playbackLockLocked = False
    
    def quitSimulation(self):
        if self.playbackLock != None and self.playbackLockLocked:
            self.playbackLock.release()
        if self.lock != None:
            self.lock.release()
            self.lockBack.acquire()
            self.lockBack.release()
        self.quit()
                 
                     
                                    
