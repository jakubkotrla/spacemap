## @package Enviroment.Affordances
# Contains list of affordances available for worlds.

## Represents affordance, has name.
class Affordance:

    def __init__(self, name):
        self.name = name


# Configuration part    

Cutability = Affordance('Cutability')
Eatability = Affordance('Eatability')
Washability = Affordance('Washability')
Drinkability = Affordance('Drinkability')
Smokeability = Affordance('Smokeability')
Lightability = Affordance('Lightability')
Wetability = Affordance('Wetability')
Readability = Affordance('Readability')
Zoomability = Affordance('Zoomability')

Throwability = Affordance('Throwability')
Watchability = Affordance('Watchability')
Playability = Affordance('Playability')
Sitability = Affordance('Sitability')
Hammerability = Affordance('Hammerability')
Nailability = Affordance('Nailability')

Placeability = Affordance('Placeability')
Exitability = Affordance('Exitability')

Fireability = Affordance('Fireability')
Repairability = Affordance('Repairability')
Screwability = Affordance('Screwability')
Sewability = Affordance('Sewability')

## List of all available affordances.
Affordances = [
    Cutability,
    Eatability,
    Washability,
    Drinkability,
    Smokeability,
    Lightability,
    Wetability,
    Readability,
    Zoomability,
    Throwability,
    Watchability,
    Playability,
    Sitability,
    Hammerability,
    Nailability,
    Placeability,
    Exitability,
    Fireability,
    Repairability,
    Screwability,
    Sewability
]

