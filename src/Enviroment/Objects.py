
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

Sink = Object('Sink', [Wetability, Repairability])
Plate = Object('Plate', [Washability])
Cup = Object('Cup', [Washability])
Fork = Object('Fork', [Washability])
Knife = Object('Knife', [Washability, Cutability])
Pot = Object('Pot', [Washability])
Cover = Object('Cover', [Washability])

Book = Object('Book', [Readability])
Journal = Object('Journal', [Readability])
Newspapers = Object('Newspapers', [Readability])
Glasses = Object('Glasses', [Zoomability])

CocaColaCan = Object('CocaColaCan', [Drinkability])
BottleOfWine = Object('BottleOfWine', [Drinkability])

Television = Object('Television', [Watchability, Repairability])
Painting = Object('Painting', [Watchability])
Photoalbum = Object('Photoalbum', [Watchability])
Video = Object('Video', [Watchability, Repairability])
Flower = Object('Flower', [Watchability])

Sofa = Object('Sofa', [Sitability])
Armchair = Object('Armchair', [Sitability])
Chair = Object('Chair', [Sitability])

Table = Object('Table', [Placeability, Repairability])
Shelf = Object('Shelf', [Placeability, Repairability])
Box = Object('Box', [Placeability, Repairability])

Door = Object('Door', [Exitability])

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
    Flower,
    Sofa,
    Armchair,
    Table,
    Shelf,
    Box,
    Door,
    Hammer,
    Nail,
    Screwdriver,
    Pipe,
    Wood,
    Torch
]


