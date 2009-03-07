
from Tkinter import *  
from threading import *
from shutil import copyfile
import os
import time
import copy
from random import seed
from PIL import ImageGrab, ImageDraw
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
        self.tl = self.winfo_toplevel()
        self.tl.geometry("1500x1020+0+0")
        self.tl.title("SpaceMap MainWindow")
        self.mapRenderer = None
        
        self.testToRunCount = 0
        self.currentTestIndex = 0
        self.testRunStarted = 0
        
        self.lock = None
        self.playbackLock = None
        self.playbackLockLocked = False 
        
        self.wndAffordances = None
        self.wndObjects = None
        self.wndRealObjects = None
        self.wndInfo = None
        
        self.pack()  
        self.createWidgets()   
        self.createMenu()
        
    
    def createWidgets(self):
        self.wxCanvas = Canvas(self, width=1500, height=1020)
        self.wxCanvas.grid(row=0, column=0)
        self.wxCanvas.bind('<Button-1>', self.canvasClick)
        self.wxCanvas.width = 1500
        self.wxCanvas.height = 1020
                                  
    def createMenu(self):
        startMenu = Menu()
        startMenu.add_command(label="Test All", command=self.startAll)
        startMenu.add_separator()
        for config in Config.configs:
             startMenu.add_command(label=config, command= lambda config=config: self.startSimulation(config))
        
        worldMenu = Menu()
        worldMenu.add_command(label="Show Affordances", command=self.showAffordances)
        worldMenu.add_command(label="Show Object Types", command=self.showObjectTypes)
        worldMenu.add_command(label="Show Objects", command=self.showObjects)
        worldMenu.add_checkbutton(label="Show visibility history", command=self.visibilityHistoryCheck)
                  
        menubar = Menu(self)
        menubar.add_cascade(label="Start", menu=startMenu)
        menubar.add_command(label="Pause", command=self.pauseSimulation)
        menubar.add_command(label="Resume", command=self.resumeSimulation)
        menubar.add_command(label="Stop", command=self.stopSimulation)
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
    def visibilityHistoryCheck(self):
        Global.RenderVisibilityHistory = not Global.RenderVisibilityHistory    
    
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
            self.wndInfo.geometry("400x200+50+50")
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

    def startAll(self):
        th = Thread(None, self.simulationTestAllThread, name="simulationTestAllThread")
        th.start()
    def simulationTestAllThread(self):
        #import psyco
        #psyco.full()
        
        settingsToRun = {}
        settings = dir(Global)
        settingsToRunLen = []
        for setting in settings:
            if setting.endswith("TESTSET"):
                a = getattr(Global, setting)
                settingName = setting.split("TESTSET")[0]
                settingsToRun[settingName] = a
                settingsToRunLen.append(len(a))
        #settingsToRun contains all set data to run
        settingsCount = reduce(lambda x,y: x*y, settingsToRunLen)
        self.testToRunCount = settingsCount * len(Config.configs) * len(Global.RandomSeeds)
        self.currentTestIndex = 0
        self.testRunStarted = time.time()
        
        self.simulationTestAllRecursive(settingsToRun)
    
    def simulationTestAllRecursive(self, settingsToRun, settingsText=''):  
        if len(settingsToRun) < 1:  
            self.runOneTestSuite(settingsText)
        else:
            settingsToRunNext = copy.copy(settingsToRun)
            (name, value) = settingsToRunNext.popitem()
            for settings in value:
                setattr(Global, name, settings)
                settingsTextIn = settingsText + "#" + name + "=" + str(settings) + "\n"
                self.simulationTestAllRecursive(settingsToRunNext, settingsTextIn)
        
    def runOneTestSuite(self, settingsText):
        nowTime = time.strftime("%Y-%m-%d--%H-%M-%S")
        configsToTest = Config.configs
        randomSeeds = Global.RandomSeeds
        
        savePath = "../../tests/" + nowTime + "/"
        os.makedirs(savePath)
        copyfile("Enviroment/Global.py", savePath + "Global.py")
        f = open(savePath + "Global.py", "a")
        f.write("\n#real settings of Global.py\n")
        f.write(settingsText)
        f.close()
                
        for randomSeed in randomSeeds:
            for configName in configsToTest:
                self.runOneSimulation(savePath, configName, randomSeed)
        return

    def runOneSimulation(self, savePath, configName, randomSeed):
        savePath = savePath + str(randomSeed) + "-" + configName + "/"
        os.makedirs(savePath)
        Global.LogStart(savePath)   
        Global.Log("Starting new simulation and world for Config: " + configName)
        
        seed(randomSeed)
        config = Config.Get(configName)
        world = World(config)
        Global.World = world

        self.agent = Agent(config)
        world.SetAgent(self.agent)
        self.mapRenderer = MapRenderer(self.wxCanvas, Global.Map, self.agent, self, False)
        
        self.currentTestIndex = self.currentTestIndex + 1
        self.mapRenderer.RenderProgress(self)
        self.mapRenderer.RenderProgressInTest(world.step, Global.MaxTestSteps)
        time.sleep(0.1)
        
        elayer = world.agent.intelligence.spaceMap.Layer
        while world.step < Global.MaxTestSteps:
            world.Step()
            self.mapRenderer.RenderToFile(world, savePath + "PIL" + str(world.step).zfill(6) + ".png")
            self.mapRenderer.RenderProgressInTest(world.step, Global.MaxTestSteps)
            Global.LogData( elayer.Status() )
        
        self.mapRenderer.RenderToFile(world, savePath + "visibilityheatmap.png", ["vh"])
        self.mapRenderer.RenderToFile(world, savePath + "visibilityobjectheatmap.png", ["ovh"])
        self.mapRenderer.RenderELNC(elayer.energyNodesCountHistory, savePath + "spelncount.png")
        
        Global.Log("Stoping simulation...")
        Global.LogEnd()
        Global.Reset()
        self.agent = None
        self.mapRenderer.Clear()
        self.mapRenderer = None

    def startSimulation(self, configName):
        dirList = os.listdir("../../exs/")
        for fname in dirList:
            os.remove("../../exs/" + fname)
        Global.LogStart("../../exs/")
        Global.Log("Starting new simulation and world for Config: " + configName)
        
        seed(Global.RandomSeeds[0])
        config = Config.Get(configName)
        world = World( config )
        Global.World = world

        self.agent = Agent(config)
        world.SetAgent(self.agent)
        self.mapRenderer = MapRenderer(self.wxCanvas, Global.Map, self.agent, self)
         
        self.lock = Lock()
        self.lock.acquire()
        self.playbackLock = Lock()
        th = Thread(None, self.simulationThread, name="simulationThread")
        th.start()     
    
    def simulationThread(self):
        world = Global.World
        self.lockBack = Lock()
        self.lockBack.acquire()
        while True:
            world.Step()
            self.RenderState(world)
            self.mapRenderer.RenderToFile(world, "../../exs/PIL" + str(world.step).zfill(6) + ".png", ["agent", "ov", "eps", "info"])
            
            if self.lock.acquire(False): break
            self.playbackLock.acquire()
            self.playbackLock.release()
  
        self.lockBack.release()
        Global.LogEnd()
        return
    
    def RenderState(self, world):
        self.mapRenderer.RenderObjectVisibility()
        self.mapRenderer.RenderSpaceMap()
        self.mapRenderer.RenderAgent(world.agent)
        if Global.RenderVisibilityHistory:
            self.mapRenderer.RenderVisibilityHistory()
        else:
            self.mapRenderer.HideVisibilityHistory()
        
        self.wxCanvas.delete("infotxt")
        txt =  "Step:  " + str(world.step).zfill(6) + "\nTime:  " + Global.TimeToHumanFormat(True)
        self.txtTime = self.wxCanvas.create_text(1080, 5, text=txt, width=200, anchor=NW, tags="infotxt")
        txt =  "Agent:  " + str(self.agent.x) + "," + str(self.agent.y)
        nc = len(world.agent.intelligence.spaceMap.Layer.nodes)
        txt = txt + "\n EnergyLayer.nodeCount: " + str(nc)
        self.txtAgentInfo = self.wxCanvas.create_text(1300, 5, text=txt, width=200, anchor=NW, tags="infotxt")
        pa = self.agent.intelligence.processArea
        txt = "ProcessArea:\n" + "\n".join(self.agent.paText)
        self.txtPA = self.wxCanvas.create_text(1050, 50, text=txt, width=200, anchor=NW, tags="infotxt")
        ma = self.agent.intelligence.memoryArea
        txt = "MemoryArea:\n  "
        for phantom in ma.memoryPhantoms:
            txt = txt + phantom.ToString() + "\n  "  
        self.txtMA = self.wxCanvas.create_text(1050, 200, text=txt, width=400, anchor=NW, tags="infotxt")
        pf = self.agent.intelligence.perceptionField
        txt = "PerceptionField:\n  "
        for phantom in pf.environmentPhantoms:
            txt = txt + phantom.ToString() + "\n  "
        self.txtPF = self.wxCanvas.create_text(1050, 300, text=txt, width=400, anchor=NW, tags="infotxt")
        txt = "Log:\n  "
        for line in Global.logLines:
            txt = txt + line + "\n  "
        self.txtLog = self.wxCanvas.create_text(1050, 600, text=txt, width=450, anchor=NW, tags="infotxt")
        
        Global.LogData(world.agent.intelligence.spaceMap.Layer.Status())
  
    
    def pauseSimulation(self):
        if self.playbackLock != None and not self.playbackLockLocked:
            self.playbackLock.acquire()
            self.playbackLockLocked = True
    def resumeSimulation(self):
        if self.playbackLock != None and self.playbackLockLocked:
            self.playbackLock.release()
            self.playbackLockLocked = False
    def exitLocks(self):        
        if self.playbackLock != None and self.playbackLockLocked:
            self.playbackLock.release()
        if self.lock != None:
            self.lock.release()
            self.lockBack.acquire()
            self.lockBack.release()
    def stopSimulation(self):
        Global.Log("Stoping simulation...")
        self.exitLocks()
        Global.Reset()
        self.agent = None
        self.mapRenderer.Clear()
        self.mapRenderer = None
        self.lock = None
        
    def quitSimulation(self):
        if self.lock != None:
            self.exitLocks()
        self.quit()
                 
                     
                                    
