# -*- coding: UTF-8 -*-
## @package Agents.EpisodicMemory
# UNCHANGED, original from Tomas Korenko source code

import Emotion

## UNCHANGED, original from Tomas Korenko source code
#
# Trieda reprezentujúca časový ukazateľ
# - Atribúty triedy:
#   - process ... pointer na proces
#   - _process ... pointer na aktivovaný proces
#   - parentProcessMemoryLink ... pointer na časový ukazateľ rodičovského procesu
#   - nextProcessMemoryLink ... pointer na časový ukazateľ nasledujúceho procesu na rovnakej úrovni
#   - firstSubProcessMemoryLink ... pointer na časový ukazateľ prvého podprocesu
#   - startTime ... čas začiatku vykonávania procesu
#   - endTime ... čas ukončenia vykonávania procesu
#   - iterations ... počet opakovaní vykonania procesu za sebou
#   - location ... lokácia v ktorej sa proces vykonával
#   - successful ... úspešnosť vykonania procesu           
class MemoryLink:
    ## Inicializácia inštancie triedy
    # @param self pointer na časový ukazateľ
    # @param process pointer na proces
    # @param _process pointer na aktivovaný proces
    # @param parentProcessMemoryLink pointer na časový ukazateľ rodičovského procesu
    # @param startTime čas začiatku vykonávania procesu
    def __init__(self, process, _process, parentProcessMemoryLink, startTime):
        self.process                   = process
        self._process                  = _process
        self.parentProcessMemoryLink   = parentProcessMemoryLink
        self.prevProcessMemoryLink     = None
        self.nextProcessMemoryLink     = None
        self.firstSubProcessMemoryLink = None
        self.startTime                 = startTime
        self.endTime                   = None
        self.iterations                = None
        self.location                  = None
        self.successful                = None
        self.importance                = 0
        self.emotion                   = 0
        self.process.AddMemoryLink(self)
    
    def SetPrevProcessMemoryLink(self, processMemoryLink):
        self.prevProcessMemoryLink = processMemoryLink
    ## Funkcia ktorá nastaví pointer na časový ukazateľ nasledujúceho procesu
    # @param self pointer na časový ukazateľ
    # @param processMemoryLink pointer na časový ukazateľ nasledujúceho procesu    
    def SetNextProcessMemoryLink(self, processMemoryLink):
        self.nextProcessMemoryLink = processMemoryLink
    
    ## Funkcia ktorá nastaví pointer na časový ukazateľ prvého podprocesu
    # @param self pointer na časový ukazateľ
    # @param processMemoryLink pointer na časový ukazateľ prvého podprocesu    
    def SetFirstSubProcessMemoryLink(self, processMemoryLink):
        self.firstSubProcessMemoryLink = processMemoryLink
    
    ## Funkcia ktorá uloží časový ukazateľ do epizodickej pamäte
    # @param self pointer na časový ukazateľ
    def Commit(self, emotion):
        self.endTime        = self._process.endTime
        self.iteration      = self._process.iteration
        self.location       = self._process.location
        self.successful     = self._process.successful
        self.process.AddResources(self._process.resources)
        self._process       = None
        if self.successful:
            emotion.SuccessfulProcess()
        else:
            emotion.FailedProcess()
        if self.firstSubProcessMemoryLink != None:
            self.emotion = -1000
            memoryLink = self.firstSubProcessMemoryLink
            while memoryLink != None:
                if memoryLink.emotion > self.emotion:
                    self.emotion = memoryLink.emotion
                memoryLink = memoryLink.nextProcessMemoryLink
        else:
            self.emotion = self.process.pleasure*emotion.pleasure + self.process.intensity*emotion.intensity 
    
    ## Funkce, která vrátí následující časový ukazatel
    # @param self pointer na časový ukazatel
    def GetNextLink(self):
        if self.firstSubProcessMemoryLink != None:
            return self.firstSubProcessMemoryLink
        elif self.nextProcessMemoryLink != None: 
            return self.nextProcessMemoryLink
        else:
            memoryLink = self
            while memoryLink != None and memoryLink.nextProcessMemoryLink == None:
                memoryLink = memoryLink.parentProcessMemoryLink
            if memoryLink != None:
                memoryLink = memoryLink.nextProcessMemoryLink
            return memoryLink
            
    def Subprocess(self, process):
        if self.process == process:
            return True
        elif self.parentProcessMemoryLink == None:
            return False
        else:
            return self.parentProcessMemoryLink.Subprocess(process)
            
    ## Funkce, která vypíše informace o časovém ukazateli
    # @param self pointer na časový ukazatel            
    def Print(self):
        space = ""
        parent = self.parentProcessMemoryLink
        while parent != None:
            space = space + "  "
            parent = parent.parentProcessMemoryLink
        if self.endTime != None:
            print space, self.process.name, self.startTime.ToString(), "-", self.endTime.ToString(), self.emotion, self.importance, self.successful
        else:
            print space, self.process.name, self.startTime.ToString(), "-", self.importance    

## UNCHANGED, original from Tomas Korenko source code
#      
# Trieda reprezentujúca proces v epizodickej pamäti
# - Atribúty triedy:
#   - name ... meno procesu
#   - sources ... zoznam afordancií potrebných na vykonanie procesu
#   - parent ... pointer na rodičovský proces v hierarchii
#   - hierarchyLevel ... úroveň procesu v hierarchii
#   - memoryLinks ... zoznam časových ukazateľov procesu
#   - resourcesCnt ... slovník počtu použití jednotlivých objektov pri vykonávaní procesu           
class MemoryProcess:
    ## Inicializácia inštancie triedy
    # @param self pointer na proces
    # @param name meno procesu
    # @param sources zoznam afordancií potrebných na vykonanie procesu
    def __init__(self, name, sources, parent, pleasure, intensity):
        self.name           = name
        self.sources        = sources
        if parent != None:
            self.parents    = [parent]
        else:
            self.parents    = []
        self.height         = 1
        self.pleasure       = pleasure
        self.intensity      = intensity
        self.memoryLinks    = []
        self.resourcesCnt   = {}
    
    ## Funkcia ktorá pridáva procesu časový ukazovateľ ktorý na neho ukazuje
    # @param self pointer na proces
    # @param link časový ukazateľ    
    def AddMemoryLink(self, link):
        self.memoryLinks.append(link)
        
    def RemoveMemoryLink(self, link):
        self.memoryLinks.remove(link)
    
    ## Funkcia ktorá pridáva procesu objekty ktoré sa pri jeho vykonaní použili
    # @param self pointer na proces
    # @param resources zoznam použitých objektov
    def AddResources(self, resources):
        for resource in resources:
            if resource in self.resourcesCnt:
                self.resourcesCnt[resource] += 1
            else:
                self.resourcesCnt[resource] = 1
                
    def AddParent(self, parentProcess):
        if parentProcess not in self.parents:
            self.parents.append(parentProcess)

## UNCHANGED, original from Tomas Korenko source code
#   
# Trieda reprezentujúca epizodickú pamäť agenta
# - Atribúty triedy:
#   - processes ... slovník použitých procesov
#   - days ... slovník prvých procesov jednotlivých dní
#   - lastProcessMemoryLink ... posledný vložený časový ukazateľ
class EpisodicMemory:
    ## Inicializácia inštancie triedy
    # @param self pointer na epizodickú pamäť
    def __init__(self):
        self.processes = {}
        self.days = {}
        self.lastProcessMemoryLink = None
    
    ## Funkcia ktorá uloží proces do epizodickej pamäte
    # @param self pointer na epizodickú pamäť
    # @param executedProcess vykonávaný proces        
    def StoreProcess(self, executedProcess, emotion):
        if executedProcess.process.name not in self.processes:
        # Aktuálne vykonávaný proces je vykonávaný prvýkrát
            if executedProcess.parent == None:
                self.processes[executedProcess.process.name] = MemoryProcess(executedProcess.process.name, executedProcess.process.sources, None, executedProcess.process.pleasure, executedProcess.process.intensity)
            else:                
                self.processes[executedProcess.process.name] = MemoryProcess(executedProcess.process.name, executedProcess.process.sources, self.processes[executedProcess.parent.process.name], executedProcess.process.pleasure, executedProcess.process.intensity)
            # Pridáme ho do zoznamu vykonaných procesov                
        memoryProcess = self.processes[executedProcess.process.name]
        if executedProcess.parent != None:
            memoryProcess.AddParent(self.processes[executedProcess.parent.process.name])
        
        if self.lastProcessMemoryLink == None:
        # Aktuálne vykonávaný proces je prvým procesom vôbec    
            # Vytvoríme nový MemoryLink
            newMemoryLink = MemoryLink(memoryProcess, executedProcess, None, executedProcess.startTime)
            self.lastProcessMemoryLink = newMemoryLink
        elif self.lastProcessMemoryLink._process == executedProcess.parent:
        # Aktuálne vykonávaný proces je prvým podprocesom posledne vykonávaného procesu
            # Vytvoríme nový MemoryLink
            newMemoryLink = MemoryLink(memoryProcess, executedProcess, self.lastProcessMemoryLink, executedProcess.startTime)
            self.lastProcessMemoryLink.SetFirstSubProcessMemoryLink(newMemoryLink)
            self.lastProcessMemoryLink = newMemoryLink            
        elif self.lastProcessMemoryLink._process.parent == executedProcess.parent:
        # Aktuálne vykonávanému procesu predchádza proces na rovnakej úrovni
            # Vytvoríme nový MemoryLink
            newMemoryLink = MemoryLink(memoryProcess, executedProcess, self.lastProcessMemoryLink.parentProcessMemoryLink, executedProcess.startTime)
            newMemoryLink.SetPrevProcessMemoryLink(self.lastProcessMemoryLink)               
            self.lastProcessMemoryLink.SetNextProcessMemoryLink(newMemoryLink)
            self.lastProcessMemoryLink.Commit(emotion)
            self.UpdateDays(self.lastProcessMemoryLink)
            self.lastProcessMemoryLink = newMemoryLink
        else:
        # Aktuálne vykonávaný proces je patrí do inej vetvy procesného stromu
            # Ukončíme vykonanú vetvu procesného stromu kým nenájdeme spoločného predka
            self.TerminateActualProcessTree(executedProcess.parent, emotion)
            # Vytvoríme nový MemoryLink
            newMemoryLink = MemoryLink(memoryProcess, executedProcess, self.lastProcessMemoryLink.parentProcessMemoryLink, executedProcess.startTime)
            newMemoryLink.SetPrevProcessMemoryLink(self.lastProcessMemoryLink)
            self.lastProcessMemoryLink.SetNextProcessMemoryLink(newMemoryLink)
            self.lastProcessMemoryLink.Commit(emotion)
            self.UpdateDays(self.lastProcessMemoryLink)
            self.lastProcessMemoryLink = newMemoryLink        
    
    ## Funkcia ktorá ukončí vetvu procesov a uloží ju do pamäte
    # @param self pointer na epizodickú pamäť
    # @param parentProcess proces ktorého vetvy ukončujeme     
    def TerminateActualProcessTree(self, parentProcess,emotion):
        while self.lastProcessMemoryLink._process.parent != parentProcess:
            self.lastProcessMemoryLink.Commit(emotion)
            self.lastProcessMemoryLink = self.lastProcessMemoryLink.parentProcessMemoryLink
    
    def UpdateDays(self, processMemoryLink):
        day = processMemoryLink.endTime.day
        if day not in self.days:
        # Do zoznamu prvých procesov dní pridáme najstaršieho predka aktuálneho procesu
            while processMemoryLink.parentProcessMemoryLink != None:
                processMemoryLink = processMemoryLink.parentProcessMemoryLink
            self.days[day] = processMemoryLink
            
    ## Funkce, která vypíše činnosti, vykonané v daném časovém rozmezí. Je možné omezit počet vypsaných činností a činnost, jejíž vykonání nás zajímá.
    # @param self pointer na epizodickou paměť
    # @param timeFrom počáteční čas
    # @param timeTo koncový čas
    # @param sentences počet činností, které chceme vypsat
    # @param proces, jehož podprocesy (včetně jeho samotného) chceme vypsat
    def WhatDidYouDo(self, timeFrom, timeTo, timeNow, sentences, process):
        # Najdeme první link daného dne, který zasahuje do daného času
        if timeFrom.day in self.days:
            memoryLink = self.days[timeFrom.day]
        else:
            return
        while memoryLink != None and ((memoryLink.endTime == None and timeNow.Before(timeFrom)) or memoryLink.endTime.Before(timeFrom)):
            memoryLink = memoryLink.GetNextLink()
        if sentences == 0:
            while memoryLink != None and memoryLink.startTime.Before(timeTo):
                if (memoryLink.endTime == None and timeFrom.Before(timeNow)) or timeFrom.Before(memoryLink.endTime):
                    if process == None or memoryLink.Subprocess(self.processes[process]):
                        memoryLink.Print()
                memoryLink = memoryLink.GetNextLink()
        else:
            self.UpdateHeights()
            toplist = []
            minLink = None
            length = 0
            while memoryLink != None and memoryLink.startTime.Before(timeTo):
                if (memoryLink.endTime == None and timeFrom.Before(timeNow)) or timeFrom.Before(memoryLink.endTime):
                    if process == None or memoryLink.Subprocess(self.processes[process]):
                        memoryLink.importance = memoryLink.process.height*parameters.height_imp + memoryLink.emotion*parameters.emotion_imp
                        if minLink == None:
                            minLink = memoryLink
                            toplist.append(memoryLink)
                            length = 1
                        elif length < sentences:
                            if minLink.importance > memoryLink.importance:
                                minLink = memoryLink
                            toplist.append(memoryLink)
                            length += 1
                        elif minLink.importance <= memoryLink.importance:
                            toplist.remove(minLink)
                            toplist.append(memoryLink)
                            minLink = FindMinLink(toplist)
                memoryLink = memoryLink.GetNextLink()
            for l in toplist:
                l.Print()
    
    def UpdateHeights(self):
        changed = True
        height = 1
        while changed:
            changed = False
            for p in self.processes.keys():
                process = self.processes[p]
                if process.height == height:
                    for parent in process.parents:
                        if parent.height <= height:
                            parent.height = height + 1
                            changed = True
            height += 1
        
    ## Funkcia na textový výpis stavu epizodickej pamäte
    # @param self pointer na epizodickú pamäť            
    def Print(self):
        print "Episodic Memory"
        print "  Known Processes:"
        for process in self.processes.keys():
            print "    " + process
        print "  FirstDayEpisodes:"
        for episode in self.days.keys():
            print "    " + self.days[episode].process.name
        memoryLink = self.days[0]
        while memoryLink != None:
            memoryLink.Print()
            memoryLink = memoryLink.GetNextLink()
    
    def Forget(self, remain, time):
        self.UpdateHeights()
        minImpTot = 1000
        minImp    = 1000
        maxImpTot = -1000
        minLink = None
        linkCount = 0
        memoryLink = self.days[0]
        while memoryLink != None:
            if memoryLink.endTime != None:
                memoryLink.importance = memoryLink.process.height*parameters.height_imp - time.DiffInMinutes(memoryLink.endTime)*parameters.time_imp + memoryLink.emotion*parameters.emotion_imp
            else:
                memoryLink.importance = memoryLink.process.height*parameters.height_imp
            if memoryLink.importance < minImpTot:
                minImpTot = memoryLink.importance
            if memoryLink.importance < minImp and memoryLink.endTime != None:
                minImp = memoryLink.importance
                minLink = memoryLink
            if memoryLink.importance > maxImpTot:
                maxImpTot = memoryLink.importance
            linkCount += 1
            memoryLink = memoryLink.GetNextLink()
        self.Print()
        self.Draw(minImpTot,maxImpTot,'before')
        while linkCount > remain:
            if minLink.prevProcessMemoryLink != None:
                minLink.prevProcessMemoryLink.SetNextProcessMemoryLink(minLink.nextProcessMemoryLink)
            if minLink.nextProcessMemoryLink != None:
                minLink.nextProcessMemoryLink.SetPrevProcessMemoryLink(minLink.prevProcessMemoryLink)
            if minLink.parentProcessMemoryLink != None and minLink.parentProcessMemoryLink.firstSubProcessMemoryLink == minLink:
                minLink.parentProcessMemoryLink.SetFirstSubProcessMemoryLink(minLink.nextProcessMemoryLink)
            if minLink.parentProcessMemoryLink == None:
                for d in self.days:
                    if self.days[d] == minLink:
                        self.days[d] = minLink.GetNextLink()
                        if self.days[d] == None:
                            del self.days[d]
            minLink.process.RemoveMemoryLink(minLink)
            del minLink
            linkCount -=1
            minImp = 1000
            minLink = None
            memoryLink = self.days[0]
            while memoryLink != None:
                if memoryLink.importance < minImp and memoryLink.endTime != None:
                    minImp = memoryLink.importance
                    minLink = memoryLink
                memoryLink = memoryLink.GetNextLink()
        self.Draw(minImpTot,maxImpTot,'after')

        """
    def Draw(self,mini,maxi,state):
        clf()
        figure(figsize=(12,4))
        xlabel('time (hours)')
        ylabel('level of memory')
        grid(False)
        memoryLink = self.days[0]
        day = len(self.days)
        while memoryLink != None:
            red = (maxi-memoryLink.importance)/float(maxi-mini)
            green = (memoryLink.importance - mini)/float(maxi-mini)
            if memoryLink.endTime != None:
                plot([memoryLink.startTime.ToHours(), memoryLink.endTime.ToHours()], [memoryLink.process.height,memoryLink.process.height], color=(red, green, 0), linestyle='-', solid_capstyle='butt', lw=3, marker='|', mfc='black', mec='black', ms=10)
            else:
                plot([memoryLink.startTime.ToHours(), (day+1)*24], [memoryLink.process.height,memoryLink.process.height], color=(red, green, 0), linestyle='--', dash_capstyle='butt', lw=3, marker='|', mfc='black', mec='black', ms=10)
            if memoryLink.parentProcessMemoryLink != None:
                if memoryLink.prevProcessMemoryLink == None:
                    plot([memoryLink.startTime.ToHours(), memoryLink.startTime.ToHours()], [memoryLink.process.height, memoryLink.parentProcessMemoryLink.process.height], color='gray', linestyle=':', lw=1)
                if memoryLink.nextProcessMemoryLink == None and memoryLink.endTime != None:
                    plot([memoryLink.endTime.ToHours(), memoryLink.endTime.ToHours()], [memoryLink.process.height, memoryLink.parentProcessMemoryLink.process.height], color='gray', linestyle=':', lw=1
                    )
            memoryLink = memoryLink.GetNextLink()
        
        for day in self.days:
            memoryLink = self.days[day]
            plot([memoryLink.startTime.ToHours(),memoryLink.startTime.ToHours()], [memoryLink.process.height,memoryLink.process.height], color='blue', linestyle='--', marker='o',mfc='blue')        
        axis([0,(day+1)*24,0,6])
        savefig('day'+str(day+1)+state)  
        """                                   
    
def FindMinLink(list):
    minimp = 1000
    link = None
    for l in list:
        if l.importance < minimp:
            minimp = l.importance
            link = l
    return link
