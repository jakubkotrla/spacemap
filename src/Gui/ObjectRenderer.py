
from math import *
from Enviroment.Objects import *
from Enviroment.World import *
from Enviroment.Global import Global


class ObjectRenderer:
    def __init__(self, canvas, map):
        self.canvas = canvas
        self.map = map
        self.zoom = 10
        
        
    def Render(self):
        self.canvas.create_polygon(0,0, self.map.width*self.zoom,0, self.map.width*self.zoom,self.map.height*self.zoom, 0,self.map.height*self.zoom, fill="red")
        self.canvas.update()
        
        for i in range(self.map.width):
            for j in range(self.map.height):
                if self.map.map[i][j] != None:
                    #self.canvas.create_line(i,j,i,j, fill="#000")
                    pass
                
