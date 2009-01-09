
from Agents.Intentions import Intentions, Intention
from Enviroment.Affordances import *
from Enviroment.Objects import *
from Agents.Processes import Processes, Process
from Agents.Scenarios import Scenarios, Scenario
from Enviroment.Global import Global
from Enviroment.Map import Map, Point
from BaseConfig import BaseConfig

class CrazyRoom(BaseConfig):
    def __init__(self):
        BaseConfig.__init__(self)
        
       
    def prepareMap(self, map):
        map.points = [ Point(0,0), Point(30,0), Point(30,20), Point(50,10), Point(70,20), Point(100,0), Point(70,80), Point(100,80), Point(100,100), Point(0,100), Point(0,80), Point(40,50), Point(20,40), Point(0,40)]
        map.width = 100
        map.height = 100
        map.SetAgentStart(50, 50)
        
        map.AddObject(Painting, 5, 20)
         
        map.AddObject(Flower, 51, 14)
        map.AddObject(Apple, 48, 21)
        map.AddObject(Pipe, 46, 20)
         
        map.AddObject(Sofa, 80, 20)
        map.AddObject(Table, 88, 12)
        map.AddObject(Armchair, 93, 6)
        
        map.AddObject(Newspapers, 10, 92)
        map.AddObject(Journal, 5, 98)
        map.AddObject(Glasses, 14, 88)
        map.AddObject(Book, 15, 93)
        map.AddObject(BottleOfWine, 20, 79)
        map.AddObject(Television, 17, 95)
        
        map.AddObject(Pot, 81, 95)
        map.AddObject(Orange, 87, 91)
        map.AddObject(Knife, 93, 84)
        map.AddObject(Cover, 95, 92)
        
        map.AddObject(CocaColaCan, 51, 92)
        map.AddObject(Photoalbum, 57, 97)
        
        map.AddObject(Plate, 60, 68)
        map.AddObject(Sink, 62, 50)
        map.AddObject(Cup, 40, 30)
        map.AddObject(Fork, 44, 32)
        map.AddObject(Screwdriver, 60, 42)
   
     
  
        
        