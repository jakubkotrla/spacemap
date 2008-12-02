

class Affordance:

    def __init__(self, name):
        self.name = name
        self.attractivity = 0  



# Configuration part    
InternalLearningAff = Affordance('InternalLearningAff')

NothingSpecial = Affordance('NothingSpecial')
Cutability = Affordance('Cutability')
Flushability = Affordance('Flushability')
Eatability = Affordance('Eatability')
Killability = Affordance('Killability')
Fishability = Affordance('Fishability')
Washability = Affordance('Washability')
Stickability = Affordance('Stickability')
Fireability = Affordance('Fireability')
Drinkability = Affordance('Drinkability')
Protectability = Affordance('Protectability')
Sliceability = Affordance('Sliceability')
Cookability = Affordance('Cookability')
Repairability = Affordance('Repairability')
Boilability = Affordance('Boilability')
Screwability = Affordance('Screwability')
Sewability = Affordance('Sewability')
Smokeability = Affordance('Smokeability')
Lightability = Affordance('Lightability')
Wetability = Affordance('Wetability')
Readability = Affordance('Readability')
Zoomability = Affordance('Zoomability')
Snackability = Affordance('Snackability')


Affordances = [InternalLearningAff,Cutability,Flushability,Eatability,Killability,Fishability,Washability,Stickability,Fireability,Drinkability,Protectability,
               Sliceability,Cookability,Repairability,Boilability,Screwability,Sewability,Smokeability,Lightability,Wetability,Readability,Zoomability,Snackability]