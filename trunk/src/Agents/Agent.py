
from Intelligence import Intelligence
from math import pi,atan2
from Enviroment.Global import Global


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
        self.newX = self.x
        self.newY = self.y
        self.dirAngle = pi / 4
        
        self.paText = ' '
        
        self.viewConesNormal = []
        self.viewConesNormal.append( ViewCone(0.1, pi*0.9, 7 ) )
        self.viewConesNormal.append( ViewCone(0.3, pi/2, 15) )
        self.viewConesNormal.append( ViewCone(0.3, pi/4, 25) )
        self.viewConesNormal.append( ViewCone(0.3, pi/8, 40) )
        self.viewConesForExplore = []
        self.viewConesForExplore.append( ViewCone(0.5, pi, 10 ) )
        self.viewConesForExplore.append( ViewCone(0.5, pi, 20 ) )
        self.viewCones = self.viewConesNormal
        
    def Step(self):
        action = self.intelligence.GetAction()
        map = Global.Map
        
        self.x = self.newX
        self.y = self.newY
        self.viewCones = self.viewConesNormal   #fake else-than-Explore-action branch
                
        #execute action - world/agent-impacting part of atomic process
        if action.process.name == "Execute":
            action.sources = action.parent.process.sources
            Global.Log("AGENT is doing " + action.data['process'].name + " for " + str(action.duration) + " seconds")
            self.intelligence.UseObjects(action.parent)
            #map.UseObjects(self, action.parent) done in PF.UseObjects

        elif action.process.name == "SearchRandom":
            pass #never happens - done as MoveTo or Explore child process
        elif action.process.name == "LookUpInMemory":
            pass #never happens - done as Remember, MoveTo or LookForObject child process
            
        elif action.process.name == "Remember":
            action.duration = Global.Randint(1,10)
            action.data["phantom"] = self.intelligence.RememberObjectsFor(action.data["affordance"])
            if action.data["phantom"] != None:
                Global.Log("AGENT is remembering for " + action.data["affordance"].name + "(there should be " + action.data["phantom"].object.type.name + " at " + str(action.data["phantom"].object.x) + "," + str(action.data["phantom"].object.y) + ")  for " + str(action.duration) + " seconds")
            else:
                Global.Log("AGENT is remembering for " + action.data["affordance"].name + "( nothing in SM/MA )  for " + str(action.duration) + " seconds")
            
        elif action.process.name == "LookForObject":
            action.duration = Global.Randint(1,5)
            action.data["object"] = self.intelligence.LookForObject(action.data["phantom"])
            if action.data["object"] != None:
                Global.Log("AGENT is looking for " + action.data["phantom"].object.type.name + "(Found) for " + str(action.duration) + " seconds")
            else:
                Global.Log("AGENT is looking for " + action.data["phantom"].object.type.name + "(NotFound) for " + str(action.duration) + " seconds")

        elif action.process.name == "MoveTo":
            pass #never happens - done as MoveToPartial
        elif action.process.name == "MoveToPartial":
            dx = action.data['newx'] - self.newX
            dy = action.data['newy'] - self.newY
            angle = atan2(dx, dy)
            self.dirAngle = angle
            
            action.duration = map.MoveAgent(self, action.data['newx'], action.data['newy'])
            self.intelligence.UpdatePhantomsBecauseOfMove()
            Global.Log("AGENT is moving to " + str(action.data['newx']) + "," + str(action.data['newy']) + " for " + str(action.duration) + " seconds")
                
        elif action.process.name == "Explore":
            self.viewCones = self.viewConesForExplore
            action.duration = Global.Randint(5,20)
            action.sources = [action.data['affordance']]
            Global.Log("AGENT is exploring for " + action.data['affordance'].name + " for " + str(action.duration) + " seconds")
        else:
            Global.Log("AGENT is a bit CONFUSED doing " + action.process.name)
        
        #sees object around
        visibleObjects = map.GetVisibleObjects(self)
        self.intelligence.NoticeObjects(visibleObjects, action)
        self.intelligence.perceptionField.Update(action)
        self.intelligence.memoryArea.Update(action)
        
        self.paText = self.intelligence.processArea.GetText()
        Global.Time.AddSeconds(action.duration)
        self.intelligence.ActionDone()


    def ToString(self):
        return "Agent"
    def TellTheStory(self, txt):
        self.intelligence.TellTheStory(txt)
    