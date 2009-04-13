## @package Agents.Agent
# Contains Agent - class representing virtual agent.

from Intelligence import Intelligence
from math import pi,atan2
from Enviroment.Global import Global

## Represents one agent field of view.
class ViewCone:
    def __init__(self, intensity, angle, distance):
        ## How much is agent sensitive to objects in this ViewCone.
        self.intensity = intensity
        ## Angle defining half width of ViewCone, max angle to left and right from agent direction, PI means full circle. 
        self.angle = angle
        ## Length of ViewCone, max distance in which object are perceived.
        self.distance = distance  
        

## Represents virtual agent, responsible for its location, movement and other high-level tasks.
#
# Uses class Intelligence to implement full-featured virtual agent.
class Agent:
    def __init__(self, config):
        self.intelligence = Intelligence(self, config)
        self.x = 10
        self.y = 10
        self.newX = self.x
        self.newY = self.y
        self.dirAngle = pi / 4

        ## current text describing state of ProcessArea, used to show best info about its state in GUI.
        self.paText = ' '
        
        self.viewConesNormal = []
        self.viewConesNormal.append( ViewCone(0.1, pi*0.9, 5 ) )
        self.viewConesNormal.append( ViewCone(0.3, pi/2, 20) )
        self.viewConesNormal.append( ViewCone(0.3, pi/4, 30) )
        self.viewConesNormal.append( ViewCone(0.3, pi/8, 50) )
        self.viewConesForExplore = []
        self.viewConesForExplore.append( ViewCone(0.4, pi, 10 ) )
        self.viewConesForExplore.append( ViewCone(0.4, pi, 20 ) )
        self.viewConesForExplore.append( ViewCone(0.4, pi, 30 ) )
        self.viewCones = self.viewConesNormal
        self.viewConeNormalMaxDist = 0
        for vc in self.viewConesNormal:
            self.viewConeNormalMaxDist = max(self.viewConeNormalMaxDist, vc.distance)
        self.viewConeForExploreMaxDist = 0
        for vc in self.viewConesForExplore:
            self.viewConeForExploreMaxDist = max(self.viewConeForExploreMaxDist, vc.distance)
        self.viewConeMaxDist = self.viewConeNormalMaxDist 
    
    ## One step of agent if it is out of the world.
    #
    # Does nothing in virtual world - no movement, perception etc.
    # Only update its SpaceMap. 
    def StepOut(self):
        action = self.intelligence.actionSelector.GetOutAction()
        action.duration = 10
        self.intelligence.memoryArea.Update(action)
        self.paText = 'out'
        Global.Time.AddSeconds(action.duration)
        self.intelligence.spaceMap.StepUpdate(action)
    
    ## One step in agent life.
    #
    # 1. get atomic action from ActionSelector
    # 2. executes atomic action
    # 3. perceive visible objects around
    # 4. updates PerceptionField, MemoryArea
    # 5. updates ProcessArea via call to ActionSelector.ActionDone()
    # 6. updates SpaceMap   
    def Step(self):
        action = self.intelligence.GetAction()
        map = Global.Map
        
        self.x = self.newX
        self.y = self.newY
        self.viewCones = self.viewConesNormal   #fake else-than-Explore/LookForObject-action branch
        self.viewConeMaxDist = self.viewConeNormalMaxDist
                
        #execute action - world/agent-impacting part of atomic process
        if action.process.name == "ExecuteReal":
            action.sources = action.parent.parent.process.sources
            Global.Log("AGENT is doing " + action.data['process'].name + " for " + str(action.duration) + " seconds")
            self.intelligence.UseObjects(action.parent.parent)
            #map.UseObjects(self, action.parent) done in PF.UseObjects
        elif action.process.name == "Execute":
            pass #never happen - done as ExecuteReal or MoveTo(Partial)

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
                Global.Log("AGENT is remembering for " + action.data["affordance"].name + "(nothing in SM/MA) for " + str(action.duration) + " seconds")
            
        elif action.process.name == "LookForObject":
            self.viewCones = self.viewConesForExplore
            self.viewConeMaxDist = self.viewConeForExploreMaxDist
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
            self.viewConeMaxDist = self.viewConeForExploreMaxDist
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
        
        self.intelligence.spaceMap.StepUpdate(action)


    def ToString(self):
        return "Agent"
    ## Returns agents history as was saved by EpisodicMemory. 
    def TellTheStory(self, txt):
        self.intelligence.TellTheStory(txt)
    
