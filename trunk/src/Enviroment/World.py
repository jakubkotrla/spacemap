

from Map import Map
from Global import Global
from Objects import Objects

class WorldEvent:
    def __init__(self, step, object, action):
        self.step = step
        self.object = object
        self.action = action
        
    def ToString(self):
        return str(self.step) + ";" + self.action + ";" + self.object.ToString()  

class World:
    def __init__(self, config):
        self.step = 0
        self.agent = None
        Global.Map = config.SetUpMap()
        self.events = config.GetWorldEvents()
        if Global.WorldDynamic > 0:
            self.events.extend(self.generateWorldEvents())
        for event in self.events:
            Global.LogData("worldevents", event.ToString())
        Global.LogEnd("worldevents")

    def generateWorldEvents(self):
        map = Global.Map
        eventCount = 2 * float(Global.MaxTestSteps) / 50
        events = []
        curObjects = map.objects[:]
        for i in range(1, eventCount):
            step = i * 50
            if Global.DiceRoll() < Global.WorldDynamic and len(curObjects) > 0:
                objToRemove = Global.Choice(curObjects)
                curObjects.remove(objToRemove)
                events.append(WorldEvent(step, objToRemove, "remove"))
            if Global.DiceRoll() < Global.WorldDynamic:
                objType = Global.Choice(Objects)
                p = map.GetRandomLocation()
                objToCreate = map.CreateObject(objType, p.x, p.y)
                curObjects.append(objToCreate)
                events.append(WorldEvent(step, objToCreate, "add"))
        return events
            
    def runEvents(self):
        map = Global.Map
        for event in self.events:
            if event.step == self.step:
                if event.action == "remove":
                    map.RemoveExistingObject(event.object)
                    Global.Log("World.Event: removing " + event.object.ToString())
                elif event.action == "add":
                    map.AddExistingObject(event.object)
                    Global.Log("World.Event: adding " + event.object.ToString())
                else:
                    Global.Log("Programmer.Error: unknown action in world event")

    def SetAgent(self, agent):
        self.agent = agent
        map = Global.Map
        map.PlaceAgent(agent)

    def Step(self):
        Global.Log("------------------------------ Step " + str(self.step).zfill(5) + " --- " + str(Global.TimeToHumanFormat()) + " ----------")
        self.agent.Step()
        if len(self.events) > 0:
            self.runEvents()
        map = Global.Map
        map.Step(self.agent)
        self.step = self.step + 1
        
        