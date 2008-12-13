
P_eat               = Process("Eating", [], [Eatability], [Eatability], [], 600, 10, 20)
self.processes.AddProcess(P_eat)
P_hunt               = Process("Hunting", [], [Killability], [Killability], [Meat], 7200, 120, 1)
self.processes.AddProcess(P_hunt)
P_fish               = Process("Fishing", [], [Fishability], [Fishability], [Meat], 3600, 60, 1)
self.processes.AddProcess(P_fish)
P_slice               = Process("Slicing", [], [Cutability],[],[],300,5,20)
self.processes.AddProcess(P_slice)
P_boil               = Process("Boiling", [], [Fireability, Boilability], [Cookability], [Meal], 2000, 1800, 1)
self.processes.AddProcess(P_boil)

I_eat           = Intention("Eating",[P_eat])
self.intentions.AddIntention(I_eat)
I_fish           = Intention("Fishing",[P_fish])
self.intentions.AddIntention(I_fish)
I_hunt           = Intention("Hunting",[P_hunt])
self.intentions.AddIntention(I_hunt)
I_boil           = Intention("Boiling",[P_boil])
self.intentions.AddIntention(I_boil)
I_slice           = Intention("Slicing",[P_slice])
self.intentions.AddIntention(I_slice)

P_cook               = Process("Cooking", [I_slice, I_boil, I_eat], [], [], [], 10)
self.processes.AddProcess(P_cook)

I_cook           = Intention("Cooking", [P_cook])
self.intentions.AddIntention(I_cook)

P_Fish               = Process("Fishing", [I_fish, I_cook, I_eat], [], [], [], 10)
self.processes.AddProcess(P_Fish)
P_Hunt               = Process("Hunting", [I_hunt, I_cook, I_eat], [], [], [], 10)
self.processes.AddProcess(P_Hunt)

I_Eat           = Intention("Eat", [P_cook, P_Hunt, P_Fish, P_eat])
self.intentions.AddIntention(I_Eat)

def IF_Eat(time):
    if time < 3600:
        return 0
    if time < 8400:
        return 3200
    return 0
     
S_1 = Scenario()
S_1.AddIntentionFunction(I_Eat, IF_Eat)

self.scenarios.AddScenario([0,1,2,3,4,5,6], S_1)
