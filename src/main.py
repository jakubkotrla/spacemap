#main file

from Enviroment.Global import Global
from Enviroment.World import World
from Agents.Agent import Agent

world= World()
Global.World = world


agent = Agent("agent1", "AgentsConfig\\intentions.simple.py")
world.SetAgent(agent)

while Global.Time.GetSeconds() < 18000:
    world.Step()
    
agent.TellTheStory()