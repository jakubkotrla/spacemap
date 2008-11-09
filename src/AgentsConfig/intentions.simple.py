P_Eat               = Process("Eating", [], [Eatability], [Eatability], [], 86400, 1800)
self.processes.AddProcess(P_Eat)

I_Eat           = Intention("Eat", [P_Eat])
self.intentions.AddIntention(I_Eat)
self.intentions.AddHighLevelIntention(I_Eat)


P_Snack               = Process("Snacking", [], [Snackability], [Snackability], [], 86400, 300)
self.processes.AddProcess(P_Snack)

I_Snack           = Intention("Snack", [P_Snack])
self.intentions.AddIntention(I_Snack)
self.intentions.AddHighLevelIntention(I_Snack)


P_Drink               = Process("Drinking", [], [Drinkability], [Drinkability], [], 86400, 60)
self.processes.AddProcess(P_Drink)

I_Drink           = Intention("Drink", [P_Drink])
self.intentions.AddIntention(I_Drink)
self.intentions.AddHighLevelIntention(I_Drink)


P_Smoke               = Process("Smoking", [], [Smokeability], [], [], 86400, 500)
self.processes.AddProcess(P_Smoke)

I_Smoke           = Intention("Smoke", [P_Smoke])
self.intentions.AddIntention(I_Smoke)
self.intentions.AddHighLevelIntention(I_Smoke)


P_Read               = Process("Reading", [], [Zoomability, Readability], [], [], 86400, 4000)
self.processes.AddProcess(P_Read)

I_Read           = Intention("Read", [P_Read])
self.intentions.AddIntention(I_Read)
self.intentions.AddHighLevelIntention(I_Read)


#P_Wash               = Process("Washing", [], [Washability, Wetability], [Wetability], [], 86400, 600)
#self.processes.AddProcess(P_Wash)
#
#I_Wash           = Intention("Wash", [P_Wash])
#self.intentions.AddIntention(I_Wash)
#self.intentions.AddHighLevelIntention(I_Wash)


P_Heat               = Process("Heating", [], [Fireability, Lightability], [Fireability], [], 86400, 1000)
self.processes.AddProcess(P_Heat)

I_Heat           = Intention("Heat", [P_Heat])
self.intentions.AddIntention(I_Heat)
self.intentions.AddHighLevelIntention(I_Heat)


     
S_1 = Scenario()
#S_1.AddIntentionFunction(I_Eat, IF_Eat)

self.scenarios.AddScenario([0,1,2,3,4,5,6], S_1)
