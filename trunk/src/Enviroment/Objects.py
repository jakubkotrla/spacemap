
from Enviroment.Affordances import *

class Object:
    def __init__(self,name):
        self.name = name
        self.affordances = []
        self.attractivity = 0
    
    def ToString(self):
        strAff = ""
        for aff in self.affordances: strAff = strAff + aff.name + ", "
        return self.name + " (" + strAff + ")" 
        
        
# Configuration part
Meal = Object('Meal')
Meal.affordances = [Eatability]

Snickers = Object('Snickers')
Snickers.affordances = [Snackability]

CocaColaCan = Object('CocaColaCan')
CocaColaCan.affordances = [Drinkability]

Pipe = Object('Pipe')
Pipe.affordances = [Smokeability]

Glasses = Object('Glasses')
Glasses.affordances = [Zoomability]

Book = Object('Book')
Book.affordances = [Readability]

Plate = Object('Plate')
Plate.affordances = [Washability]

Water = Object('Water')
Water.affordances = [Wetability]

Wood = Object('Wood')
Wood.affordances = [Fireability]

Torch = Object('Torch')
Torch.affordances = [Lightability]

Objects = [Meal,Snickers,CocaColaCan,Pipe,Glasses,Book,Plate,Water,Wood,Torch]