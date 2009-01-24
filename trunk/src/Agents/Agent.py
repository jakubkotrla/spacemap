
from Intelligence import Intelligence
import random
from Enviroment.Global import Global
from Enviroment.Map import Point

class Agent:
    def __init__(self, name, config):
        self.name   = name
        self.intelligence = Intelligence(self, config)
        self.pocket = []    # list of RealObjects
        self.x = 10
        self.y = 10
        self.direction = Point(1,1)
        
    # does one agent step, returns number of seconds step took
    def Step(self):
        action = self.intelligence.GetAction()
        actionDuration = 0
        map = Global.Map
        
        #execute action - world/agent-impacting part of atomic process
        if action.process.name == "Execute":
            actionDuration = action.data['execution-time'] # resp. action.data['process'].durationTime
            Global.Log("Agent " + self.name + " doing " + action.data['process'].name + " for " + str(action.data['execution-time']) + " seconds")
            self.intelligence.UseObjects(action.parent)
            #map.UseObjects(self, action.parent) done in PF.UseObjects - ok?
            
#        elif action.process.name == "PickUp":
#            rObj = action.data["object"]
#            map = Global.Map
#            if map.PickUpObject(self, rObj):
#                self.pocket.append(rObj)
#                self.intelligence.PickUpObject(rObj)
#            actionDuration = random.randint(1,10)

        elif action.process.name == "SearchRandom":
            pass #never happens - done as MoveTo or Explore child process
        elif action.process.name == "LookUpInMemory":
            pass #never happens - done as Remember, MoveTo or LookForObject child process
        elif action.process.name == "Walk":
            pass #never happens - done as MoveTo
        elif action.process.name == "Rest":
            pass #never happens - done as Explore
            
        elif action.process.name == "Remember":
            actionDuration = random.randint(30,30)
            action.data["phantom"] = self.intelligence.RememberObjectsFor(action.data["affordance"])
            if action.data["phantom"] != None:
                Global.Log("Agent " + self.name + " remembering for " + action.data["affordance"].name + "(there should be " + action.data["phantom"].object.type.name + " at " + str(action.data["phantom"].object.x) + "," + str(action.data["phantom"].object.y) + ")  for " + str(actionDuration) + " seconds")
            else:
                Global.Log("Agent " + self.name + " remembering for " + action.data["affordance"].name + "( nothing :( )  for " + str(actionDuration) + " seconds")
            
        elif action.process.name == "LookForObject":
            actionDuration = random.randint(10,10)
            action.data["object"] = self.intelligence.LookForObject(action.data["phantom"])
            if action.data["object"] != None:
                Global.Log("Agent " + self.name + " looking for " + action.data["phantom"].object.type.name + "(Found) for " + str(actionDuration) + " seconds")
            else:
                Global.Log("Agent " + self.name + " looking for " + action.data["phantom"].object.type.name + "(NotFound) for " + str(actionDuration) + " seconds")

        elif action.process.name == "MoveTo":
            pass #never happens - done as MoveToPartial
        elif action.process.name == "MoveToPartial":
            dx = action.data['newx'] - self.x
            dy = action.data['newy'] - self.y
            self.direction = Point(dx, dy)
            actionDuration = map.MoveAgent(self, action.data['newx'], action.data['newy'])
            self.intelligence.UpdatePhantomsBecauseOfMove()
            Global.Log("Agent " + self.name + " moving to " + str(action.data['newx']) + "," + str(action.data['newy']) + " for " + str(actionDuration) + " seconds")
                
        elif action.process.name == "Explore":
            actionDuration = random.randint(33,33)
            visibleObjects = map.GetVisibleObjects(self)
            self.intelligence.NoticeObjectsToPF(visibleObjects)
            Global.Log("Agent " + self.name + " exploring for " + action.data['affordance'].name + " for " + str(actionDuration) + " seconds")
        else:
            Global.Log("Agent " + self.name + " is a bit CONFUSED doing " + action.process.name + " for " + str(actionDuration) + " seconds")
        
        
        wndPA = Global.wndPA
        if wndPA != None: self.ShowPA(wndPA.txt)
        
        Global.Time.AddSeconds(actionDuration)
        
        self.intelligence.ActionDone()

    
    def ShowPF(self, txt):
        self.intelligence.ShowPF(txt)
    def ShowPA(self, txt):
        self.intelligence.ShowPA(txt)
    def ShowMA(self, txt):
        self.intelligence.ShowMA(txt)
    def GetSpaceMap(self):
        return self.intelligence.spaceMap

    def ToString(self):
        return "Agent " + self.name
    def TellTheStory(self, txt):
        self.intelligence.TellTheStory(txt)
    
