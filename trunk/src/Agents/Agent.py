
from Intelligence import Intelligence
import random
from math import pi,atan2
from Enviroment.Global import Global
from Enviroment.Map import Point


class ViewCone:
    def __init__(self, intensity, angle, distance):
        self.intensity = intensity
        self.angle = angle
        self.distance = distance  
        
class Agent:
    def __init__(self, config):
        self.intelligence = Intelligence(self, config)
        self.x = 10
        self.y = 10
        self.direction = Point(1,1)
        self.dirAngle = pi / 4
        
        self.paText = ' '
        
        self.viewCones = []
        self.viewCones.append( ViewCone(0.1, pi*0.9, 10 ) )
        self.viewCones.append( ViewCone(0.3, pi/2, 15) )
        self.viewCones.append( ViewCone(0.3, pi/4, 25) )
        self.viewCones.append( ViewCone(0.3, pi/8, 40) )
        
    # does one agent step
    def Step(self):
        action = self.intelligence.GetAction()
        actionDuration = 0
        map = Global.Map
        
        #execute action - world/agent-impacting part of atomic process
        if action.process.name == "Execute":
            actionDuration = action.data['execution-time'] # resp. action.data['process'].durationTime
            Global.Log("Agent doing " + action.data['process'].name + " for " + str(action.data['execution-time']) + " seconds")
            self.intelligence.UseObjects(action.parent)
            #map.UseObjects(self, action.parent) done in PF.UseObjects

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
                Global.Log("Agent remembering for " + action.data["affordance"].name + "(there should be " + action.data["phantom"].object.type.name + " at " + str(action.data["phantom"].object.x) + "," + str(action.data["phantom"].object.y) + ")  for " + str(actionDuration) + " seconds")
            else:
                Global.Log("Agent remembering for " + action.data["affordance"].name + "( nothing :( )  for " + str(actionDuration) + " seconds")
            
        elif action.process.name == "LookForObject":
            actionDuration = random.randint(10,10)
            action.data["object"] = self.intelligence.LookForObject(action.data["phantom"])
            if action.data["object"] != None:
                Global.Log("Agent looking for " + action.data["phantom"].object.type.name + "(Found) for " + str(actionDuration) + " seconds")
            else:
                Global.Log("Agent looking for " + action.data["phantom"].object.type.name + "(NotFound) for " + str(actionDuration) + " seconds")

        elif action.process.name == "MoveTo":
            pass #never happens - done as MoveToPartial
        elif action.process.name == "MoveToPartial":
            dx = action.data['newx'] - self.x
            dy = action.data['newy'] - self.y
            self.direction = Point(dx, dy)
            angle = atan2(dx, dy)
            self.dirAngle = angle
            
            actionDuration = map.MoveAgent(self, action.data['newx'], action.data['newy'])
            self.intelligence.UpdatePhantomsBecauseOfMove()
            Global.Log("Agent moving to " + str(action.data['newx']) + "," + str(action.data['newy']) + " for " + str(actionDuration) + " seconds")
                
        elif action.process.name == "Explore":
            actionDuration = random.randint(30,30)
            visibleObjects = map.GetVisibleObjects(self)
            self.intelligence.NoticeObjectsToPF(visibleObjects)
            Global.Log("Agent exploring for " + action.data['affordance'].name + " for " + str(actionDuration) + " seconds")
        else:
            Global.Log("Agent is a bit CONFUSED doing " + action.process.name + " for " + str(actionDuration) + " seconds")
        
        #sees object around
        #visibleObjects = map.GetVisibleObjects(self)
        #self.intelligence.NoticeObjectsToPF(visibleObjects)
        # some coef to attractivity by cur process and its affs
        
        self.paText = self.intelligence.processesArea.GetText()
        Global.Time.AddSeconds(actionDuration)
        self.intelligence.ActionDone()


    def GetSpaceMap(self):
        return self.intelligence.spaceMap

    def ToString(self):
        return "Agent "
    def TellTheStory(self, txt):
        self.intelligence.TellTheStory(txt)
    
