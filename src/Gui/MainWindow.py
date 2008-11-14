
from Tkinter import *   
from threading import *
import time
from Enviroment.Global import Global
from Enviroment.World import World
from Enviroment.Affordances import Affordances
from Enviroment.Objects import Objects
from Agents.Agent import Agent
from MapRenderer import MapRenderer                           
                                     
class MainWindow(Frame):
    def __init__(self, master=None):                    
        Frame.__init__(self, master)
        tl = self.winfo_toplevel()
        tl.geometry("1000x1000+0+0")
        tl.title("SpaceMap MainWindow")
        self.lock = None
        self.mapRenderer = None
        self.agent = None
        
        self.playbackLock = None
        
        self.wndAffordances = None
        self.wndObjects = None
        self.wndRealObjects = None
        self.wndLog = None
        self.wndPF = None
        self.wndPA = None
        self.wndMA = None
        
        self.pack()  
        self.createWidgets()   
        self.createMenu()
        
        #self.showPAPFMA()
        
    
    def createWidgets(self):
        self.wxCanvas = Canvas(self, width=1000, height=1000)
        self.wxCanvas.grid(row=0, column=0)
        self.wxCanvas.bind('<Button-1>', self.canvasClick)
                                  
    def createMenu(self):
        worldMenu = Menu()
        worldMenu.add_command(label="Show Affordances", command=self.showAffordances)
        worldMenu.add_command(label="Show Object Types", command=self.showObjectTypes)
        worldMenu.add_command(label="Show Objects", command=self.showObjects)
        worldMenu.add_command(label="Show Log", command=self.showLog)
                  
        renderMenu = Menu()
        renderMenu.add_checkbutton(label="Map", command=self.chRenderMap)
        renderMenu.add_checkbutton(label="Objects", command=self.chRenderObjects)
        renderMenu.add_checkbutton(label="Agent", command=self.chRenderAgent)
        renderMenu.add_checkbutton(label="Visible Area", command=self.chRenderVisibleArea)
        renderMenu.add_checkbutton(label="Visible Objects", command=self.chRenderVisibleobjects)
        renderMenu.add_checkbutton(label="SpaceMap", command=self.chRenderSpaceMap)
    
        agentMenu = Menu()
        agentMenu.add_command(label="Show PA-PF-MA", command=self.showPAPFMA)
        agentMenu.add_command(label="Show ProcessArea", command=self.showPA)
        agentMenu.add_command(label="Show PerceptionField", command=self.showPF)
        agentMenu.add_command(label="Show MemoryArea", command=self.showMA)
        agentMenu.add_command(label="Show SpaceMap", command=self.showSM)
                  
        menubar = Menu(self)
        menubar.add_command(label="Start", command=self.startSimulation)
        menubar.add_command(label="Pause", command=self.pauseSimulation)
        menubar.add_command(label="Resume", command=self.resumeSimulation)
        menubar.add_cascade(label="World", menu=worldMenu)
        menubar.add_cascade(label="Agent", menu=agentMenu)
        menubar.add_cascade(label="Render", menu=renderMenu)
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
        
    def chRenderMap(self):
        pass
    def chRenderObjects(self):
        pass
    def chRenderAgent(self):
        pass
    def chRenderVisibleArea(self):
        pass
    def chRenderVisibleobjects(self):
        pass
    def chRenderSpaceMap(self):
        pass
    
    def showPAPFMA(self):
        self.showPA()
        self.showPF()
        self.showMA()
    def showPA(self):
        self.wndPA = Toplevel()
        Global.wndPA = self.wndPA
        self.wndPA.geometry("400x200+820+0")
        self.wndPA.title("SpaceMap - Process Area")
        txt = Listbox(self.wndPA)
        txt.pack(side=LEFT, fill=BOTH, expand=1)
        self.wndPA.txt = txt
        scrollBar = Scrollbar(self.wndPA, orient=VERTICAL, command=txt.yview)
        txt["yscrollcommand"]  =  scrollBar.set
        scrollBar.pack(side=RIGHT, fill=Y)
        if self.agent != None: self.agent.ShowPA(txt)
        
    def showPF(self):
        self.wndPF = Toplevel()
        self.wndPF.geometry("400x200+820+250")
        self.wndPF.title("SpaceMap - Perception Field")
        txt = Listbox(self.wndPF)
        txt.pack(side=LEFT, fill=BOTH, expand=1)
        self.wndPF.txt = txt
        scrollBar = Scrollbar(self.wndPF, orient=VERTICAL, command=txt.yview)
        txt["yscrollcommand"]  =  scrollBar.set
        scrollBar.pack(side=RIGHT, fill=Y)
        if self.agent != None: self.agent.ShowPF(txt)
        
    def showMA(self):
        self.wndMA = Toplevel()
        self.wndMA.geometry("400x200+820+500")
        self.wndMA.title("SpaceMap - Memory Area")
        txt = Listbox(self.wndMA)
        txt.pack(side=LEFT, fill=BOTH, expand=1)
        self.wndMA.txt = txt
        scrollBar = Scrollbar(self.wndMA, orient=VERTICAL, command=txt.yview)
        txt["yscrollcommand"]  =  scrollBar.set
        scrollBar.pack(side=RIGHT, fill=Y)
        if self.agent != None: self.agent.ShowMA(txt)
    def showSM(self):
        pass
    
    def canvasClick(self, event):
        x = int(self.wxCanvas.canvasx(event.x))
        y = int(self.wxCanvas.canvasy(event.y))
        ids = self.wxCanvas.find_overlapping(x,y, x+1,y+1)
        for id in ids:
            tags = self.wxCanvas.gettags(id)
            if "kmlnode" in tags:
                self.showKMLNode(self.mapRenderer.IdToKMLNodeGui(id))
                break
    def showKMLNode(self, guiNode):
        wnd = Toplevel()
        wnd.geometry("400x200+820+500")
        wnd.title("SpaceMap - KMLNode Info")
        txt = Listbox(wnd)
        txt.pack(side=LEFT, fill=BOTH, expand=1)
        txt.insert(0, "Node[" + str(guiNode.node.x) + "," + str(guiNode.node.y) + "]")
        
        

    def startSimulation(self):
        world = World()
        Global.World = world

        self.agent = Agent("agent1", "AgentsConfig\\intentions.simple.py")
        world.SetAgent(self.agent)
        self.mapRenderer = MapRenderer(self.wxCanvas, Global.Map, self.agent, self)
        
        self.lock = Lock()
        self.lock.acquire()
        self.playbackLock = Lock()
        th = Thread(None, self.step, name="steps")
        th.start()     
    
    def step(self):
        world = Global.World
        self.lockBack = Lock()
        self.lockBack.acquire()
        while Global.Time.GetSeconds() < 100000:
            world.Step()
            if self.wndPF != None: self.agent.ShowPF(self.wndPF.txt)
            if self.wndMA != None: self.agent.ShowMA(self.wndMA.txt)
            # PA done in Agent.Step to get more precise data
            time.sleep(0.01)
            if self.lock.acquire(False): break
            
            self.playbackLock.acquire()
            self.playbackLock.release()
            
        self.lockBack.release()
        return
    
    def pauseSimulation(self):
        if self.playbackLock != None:
            self.playbackLock.acquire()
    def resumeSimulation(self):
        if self.playbackLock != None:
            self.playbackLock.release()
    
    def quitSimulation(self):
        #if self.playbackLock != None:
        #   self.playbackLock.release()

        if self.lock != None:
            self.lock.release()
            self.lockBack.acquire()
            self.lockBack.release()
        self.quit()
                 
                     
                                    
