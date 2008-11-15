#main file

from Enviroment.Global import Global
from Enviroment.World import World
from Agents.Agent import Agent

from sets import *

s = set('abc')
s.add("a")
s.add(1)
s.add(1)

print s

#world= World()
#Global.World = world
#
#
#agent = Agent("agent1", "AgentsConfig\\intentions.simple.py")
#world.SetAgent(agent)
#
#while Global.Time.GetSecondsInDay() < 18000:
#    world.Step()
#    
#agent.TellTheStory()