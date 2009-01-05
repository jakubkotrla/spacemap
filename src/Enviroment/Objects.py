
from Enviroment.Affordances import *

class Object:
    def __init__(self, name, affs = []):
        self.name = name
        self.affordances = affs
        self.attractivity = 0
    
    def ToString(self):
        strAff = ""
        for aff in self.affordances: strAff = strAff + aff.name + ", "
        return self.name + " (" + strAff + ")" 
        
        
# Configuration part
Meal = Object('Meal', [Eatability])
Sandwich = Object('Sandwich', [Eatability])
Apple = Object('Apple', [Eatability, Throwability])
Orange = Object('Orange', [Eatability, Throwability])

Sink = Object('Sink', [Wetability])
Plate = Object('Plate', [Washability])
Cup = Object('Cup', [Washability])
Fork = Object('Fork', [Washability])
Knife = Object('Knife', [Washability, Cutability])
Cup = Object('Cup', [Washability])
Pot = Object('Pot', [Washability])
Cover = Object('Cover', [Washability])

Book = Object('Book', [Readability])
Journal = Object('Journal', [Readability])
Newspapers = Object('Newspapers', [Readability])
Glasses = Object('Glasses', [Zoomability])

CocaColaCan = Object('CocaColaCan', [Drinkability])
BottleOfWine = Object('BottleOfWine', [Drinkability])

Television = Object('Television', [Watchability])
Painting = Object('Painting', [Watchability])
Photoalbum = Object('Photoalbum', [Watchability])
Video = Object('Video', [Watchability])

Sofa = Object('Sofa', [Restability])
Armchair = Object('Armchair', [Restability])

Table = Object('Table', [Placeability])
Shelf = Object('Shelf', [Placeability])
Box = Object('Box', [Placeability])

Hammer = Object('Hammer', [Hammerability])
Nail = Object('Nail', [Nailability])
Screwdriver = Object('Screwdriver', [Screwability])

Pipe = Object('Pipe', [Smokeability])
Wood = Object('Wood', [Fireability])
Torch = Object('Torch', [Lightability])

#kartacek a pasta


Objects = [
    Meal,
    Sandwich,
    Apple,
    Orange,
    Sink,
    Plate,
    Cup,
    Fork,
    Knife,
    Cup,
    Pot,
    Cover,
    Book,
    Journal,
    Newspapers,
    Glasses,
    CocaColaCan,
    BottleOfWine,
    Television,
    Painting,
    Photoalbum,
    Video,
    Sofa,
    Armchair,
    Table,
    Shelf,
    Box,
    Hammer,
    Nail,
    Screwdriver,
    Pipe,
    Wood,
    Torch
]


