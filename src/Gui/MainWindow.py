## @package Gui.MainWindow
# Main GUI file, uses TkInter to create window and other GUI elements and runs the whole application.

from Tkinter import *  
from threading import *
from shutil import copyfile
import os
import time
import copy
import traceback
from random import seed
from Enviroment.Global import Global
from Enviroment.World import World
from Enviroment.Affordances import Affordances
from Enviroment.Objects import Objects
from Agents.Agent import Agent
from MapRenderer import MapRenderer  
from Config.Config import Config                         

## Main GUI class. Handles all GUI interaction, threading etc.                                  
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
        
        ## Locks used to control Pause/Resume/Quit in two theards enviroment.
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
        
    ## Creates Canvas GUI element.
    def createWidgets(self):
        self.wxCanvas = Canvas(self, width=1500, height=1020)
        self.wxCanvas.grid(row=0, column=0)
        self.wxCanvas.bind('<Button-1>', self.canvasClick)
        self.wxCanvas.width = 1500
        self.wxCanvas.height = 1020
    
    ## Creates Menu GUI elements.                              
    def createMenu(self):
        startMenu = Menu()
        startMenu.add_command(label="Test All", command=self.startAll)
        startMenu.add_separator()
        configs = Config.GetConfigs()
        for config in configs:
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
    
    ## Creates new window showing affordances in world.   
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
            
    ## Creates new window showing object types in world.
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
            
    ## Creates new window showing objects in world.
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
        if Global.CalculateVisibilityHistory:
            Global.RenderVisibilityHistory = not Global.RenderVisibilityHistory    
    
    ## Creates new window showing information about objects below mouse cursor.
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
    
    
    ## Starts TestAll mode in separate thread.
    def startAll(self):
        th = Thread(None, self.simulationTestAllThread, name="simulationTestAllThread")
        th.start()
        
    ## Does TestAll, runs in separate thread.
    #
    # Constructs all test suites to run, using reflection to get settings in Global with name parametrTESTSET.
    def simulationTestAllThread(self):
        self.lock = Lock()
        
        import psyco
        psyco.full()
        
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
        if len(settingsToRunLen) < 1:
            settingsCount = 1
        else:
            settingsCount = reduce(lambda x,y: x*y, settingsToRunLen)
        self.testToRunCount = settingsCount * len(Config.GetConfigs()) * len(Global.RandomSeeds)
        self.currentTestIndex = 0
        self.testRunStarted = time.time()
        
        self.simulationTestAllRecursive(settingsToRun)
    
    ## Recursively gets to one test suite/settings to run.
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
        
    ## Runs one test suite - all worlds and random seeds with one settings.
    def runOneTestSuite(self, settingsText):
        nowTime = time.strftime("%Y-%m-%d--%H-%M-%S")
        configsToTest = Config.GetConfigs()
        randomSeeds = Global.RandomSeeds
        
        savePath = "../../tests/" + nowTime + "/"
        os.makedirs(savePath)
                
        if Global.SafeMode:
            for randomSeed in randomSeeds:
                for configName in configsToTest:
                    try:
                        self.runOneSimulation(savePath, configName, randomSeed)
                    except:
                        e = sys.exc_info()[1]
                        if type(e) == TclError: raise SystemExit
                        print e
                        time.sleep(1)
        else:
            for randomSeed in randomSeeds:
                for configName in configsToTest:
                    self.runOneSimulation(savePath, configName, randomSeed)
        
        copyfile("Enviroment/Global.py", savePath + "Global.py")
        copyfile("plotter.py", "../../tests/plotter.py")
        copyfile("../statter.exe", "../../tests/statter.exe")
        copyfile("../LumenWorks.Framework.IO.dll", "../../tests/LumenWorks.Framework.IO.dll")
        f = open(savePath + "Global.py", "a")
        f.write("\n#real settings of Global.py\n")
        f.write(settingsText)
        f.close()
        #run statter and plotter ?
            
    ## Runs one simulation - one world and one random seed.
    def runOneSimulation(self, savePath, configName, randomSeed):
        savePath = savePath + str(randomSeed) + "-" + configName + "/"
        os.makedirs(savePath)
        Global.LogStart(savePath)   
        Global.Log("Starting new simulation and world for Config: " + configName)
        try:
            seed(randomSeed)
            config = Config.Get(configName)
            world = World(config)
            Global.World = world
    
            self.agent = Agent(config)
            world.SetAgent(self.agent)
            self.mapRenderer = MapRenderer(self.wxCanvas, Global.Map, self.agent, self, False)
            
            self.currentTestIndex = self.currentTestIndex + 1
            self.mapRenderer.RenderProgress(self, configName)
            self.mapRenderer.RenderProgressInTest(world.step, Global.MaxTestSteps)
            time.sleep(0.1)
            
            elayer = world.agent.intelligence.spaceMap.Layer
            while world.step < Global.MaxTestSteps:
                world.Step()
                self.mapRenderer.RenderToFile(world, savePath + "PIL" + str(world.step).zfill(6) + ".png")
                self.mapRenderer.RenderProgressInTest(world.step, Global.MaxTestSteps)
        
            world.SendAgentOut()
            while world.step < Global.MaxTestSteps + Global.MaxTestStepAfter:
                world.Step()
                self.mapRenderer.RenderToFile(world, savePath + "PIL" + str(world.step).zfill(6) + ".png")
                self.mapRenderer.RenderProgressInTest(world.step, Global.MaxTestSteps)
                    
            if Global.CalculateVisibilityHistory:
                self.mapRenderer.RenderToFile(world, savePath + "visibilityheatmap.png", ["vh"])
            self.mapRenderer.RenderToFile(world, savePath + "visibilityobjectheatmap.png", ["ovh"])
            map = Global.Map
            map.SaveHeatMap()
            self.agent.intelligence.spaceMap.Layer.SaveHeatMap()
        except:
            Global.Log("FATAL ERROR occured: ")
            ss = traceback.format_exc()
            Global.Log(ss)
            time.sleep(1)
            raise
        finally:        
            Global.Log("Stoping simulation...")
            Global.LogEnd()
            Global.Reset()
            self.agent = None
            self.mapRenderer.Clear()
            self.mapRenderer = None

    ## Starts simulation in interactive mode in separate thread.
    def startSimulation(self, configName):
        if not os.path.exists("../../exs/"): os.makedirs("../../exs/")
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
    
    ## Does simulation in interactive mode, runs in separate thread.
    def simulationThread(self):
        world = Global.World
        self.lockBack = Lock()
        self.lockBack.acquire()
        while True:
            world.Step()
            self.RenderState(world)
            self.mapRenderer.RenderToFile(world, "../../exs/PIL" + str(world.step).zfill(6) + ".png", ["agent", "ov", "eps", "info"])
            
            # used only to get EPS of test rooms
            #p=self.wxCanvas.postscript(width="1020",height="1020")
            #f=open("image" + str(world.step) + ".eps", "wb")
            #f.write(p)
            #f.close()
            
            if self.lock.acquire(False): break
            self.playbackLock.acquire()
            self.playbackLock.release()
  
        self.lockBack.release()
        Global.LogEnd()
        return
    
    ## Renders curent state of world, agent and SpaceMap on screen.
    def RenderState(self, world):
        self.mapRenderer.RenderObjectVisibility()
        self.mapRenderer.RenderSpaceMap()
        self.mapRenderer.RenderAgent(world.agent)
        #self.mapRenderer.RenderObjects() - only for dynamic worlds
        if Global.RenderVisibilityHistory:
            self.mapRenderer.RenderVisibilityHistory()
        else:
            self.mapRenderer.HideVisibilityHistory()
        
        self.wxCanvas.delete("infotxt")
        txt =  "Step:  " + str(world.step).zfill(6) + "\nTime:  " + Global.TimeToHumanFormat(True)
        self.txtTime = self.wxCanvas.create_text(1080, 5, text=txt, width=200, anchor=NW, tags="infotxt")
        strXY = "%.4f,%.4f" % (self.agent.x, self.agent.y)
        txt =  "Agent:  " + strXY
        nc = len(world.agent.intelligence.spaceMap.Layer.nodes)
        txt = txt + "\nEnergyLayer.nodeCount: " + str(nc)
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
        self.txtLog = self.wxCanvas.create_text(1050, 550, text=txt, width=450, anchor=NW, tags="infotxt")
        
        Global.LogData("nc", world.agent.intelligence.spaceMap.Layer.Status())
  
    ## Pauses simulation using locks.
    def pauseSimulation(self):
        if self.playbackLock != None and not self.playbackLockLocked:
            self.playbackLock.acquire()
            self.playbackLockLocked = True
    ## Resumes simulation by releasing locks.
    def resumeSimulation(self):
        if self.playbackLock != None and self.playbackLockLocked:
            self.playbackLock.release()
            self.playbackLockLocked = False
    ## Exits and releases all locks to properly exit application.
    def exitLocks(self):        
        if self.playbackLock != None and self.playbackLockLocked:
            self.playbackLock.release()
        if self.lock != None:
            self.lock.release()
            self.lockBack.acquire()
            self.lockBack.release()
    ## Stops interactive mode. Another simulation can be runned, even TestAll.
    def stopSimulation(self):
        Global.Log("Stoping simulation...")
        self.exitLocks()
        Global.Reset()
        self.agent = None
        self.mapRenderer.Clear()
        self.mapRenderer = None
        self.lock = None
    
    ## Quits application.    
    def quitSimulation(self):
        if self.lock != None:
            self.exitLocks()
            self.lock = None
        self.quit()
                 
                     
                                    
