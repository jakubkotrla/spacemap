# -*- coding: UTF-8 -*-

## script to visualize outputted data
#
#  Uses NumPy and Matplotlib to plot CSV file to PNG or EPS files.

from pylab import *
import os
import csv
from numpy import *
from matplotlib.font_manager import fontManager, FontProperties




def addToQueue(visited, queue, point, value):
    hash = str(point[0]) + ";" + str(point[1])
    if hash not in visited and value > 0.1:
        visited[hash] = hash
        queue.append( (point[0], point[1], (value * 0.6)) )
def fill(map, x, y, value):
    visited = {}
    queue = []
    queue.append((x,y, value))
    while len(queue) > 0:
        point = queue.pop(0)
        if point[0] < 0 or point[0] > 100 or point[1] < 0 or point[1] > 100:continue
        map[point[0]][point[1]] += point[2]
        addToQueue(visited, queue, (point[0]-1,point[1]), point[2])
        addToQueue(visited, queue, (point[0]+1,point[1]), point[2])
        addToQueue(visited, queue, (point[0],point[1]-1), point[2])
        addToQueue(visited, queue, (point[0],point[1]+1), point[2])


def plotHeatMap(fileName, titleStr):
    rowsRAW = csv.reader(open(fileName, "rb"), delimiter=";")
    rows = []
    rows.extend(rowsRAW)

    mapa = [None]*101
    for i in range(101):
         mapa[i] = [None] * 101
    for i in range(101):
        for j in range(101):
            mapa[i][j] = 0.0
 
    for row in rows:
        y = int(row[0])
        x = int(row[1])
        value = float(row[2])
        fill(mapa, x, y, value)

    maxValue = 0
    for i in range(101):
        for j in range(101):
            maxValue = max(maxValue, mapa[i][j])
    for i in range(101):
        for j in range(101):
            mapa[i][j] = maxValue - mapa[i][j]
 
    ndA = array(mapa)    
    im = imshow(ndA, cmap=cm.gray, interpolation=None, origin='upper',extent=(0,100,0,100))
    colorbar()
    
    if saveEPS:savefig(fileName+".eps", format="EPS")
    else:
        title(titleStr, family=fontFamily)
        savefig(fileName+".png", format="PNG")
    clf()

def plotRememberOne(fileName, rows):
    trained = map(lambda x: x[1], rows)
    error = map(lambda x: x[2], rows)
    
    errorND = array( error )
    trainedND = array( trained )
    plot(trainedND, errorND, marker=",", color='red', drawstyle="steps", linestyle="None")
    ylabel(u'Chyba', family=fontFamily)
    xlabel(u'Naučenost', family=fontFamily)

    if saveEPS: savefig(fileName+".eps", format="EPS")
    else:
        savefig(fileName+".png", format="PNG")
        title(u'Chyba prostorové mapy v závislosti na naučenosti předmětů', family=fontFamily)
    clf()

def plotRememberTimeOne(fileName, rows, plotTrained=True):
    step = map(lambda x: x[0], rows)
    trained = map(lambda x: x[1], rows)
    error = map(lambda x: x[2], rows)
    
    stepND = array( step )
    errorND = array( error )
    trainedND = array( trained )
    meanError = average(errorND.astype(float))
    
    if plotTrained:
        subplots_adjust(hspace=1)
        subplot(211)
        plot(stepND, trainedND, marker=",", color='red', drawstyle="steps", linestyle="None")
        xlabel(u"čas (kroky)")
        ylabel(u'naučenost')
        title(u'Naučenost v čase')
    
        subplot(212)
    plot(stepND, errorND, marker=",", color='red', drawstyle="steps", linestyle="None")
    ylabel(u'chyba', family=fontFamily)
    xlabel(u"čas (kroky)", family=fontFamily)
    
    if saveEPS: savefig(fileName+".eps", format="EPS")
    else:
        savefig(fileName+".png", format="PNG")
        title(u'Chyba mapy v čase', family=fontFamily)
    clf()
        

def plotRemember(fileName, full=False):
    rowsRAW = csv.reader(open(fileName, "rb"), delimiter=";")
    rows = []
    rows.extend(rowsRAW)
        
    plotRememberOne(fileName, rows)
    plotRememberTimeOne(fileName + ".time", rows, False)
    
    if full:  
        objects = map(lambda x: x[3], rows)
        objects = list(set(objects))
        for obj in objects:
            rowsObj = filter(lambda x: x[3]==obj, rows)
            plotRememberOne(fileName + obj, rowsObj)    
            plotRememberTimeOne(fileName + obj + ".time", rowsObj)
        
def plotMeanErrorInTime(fileName):
    rowsRAW = csv.reader(open(fileName, "rb"), delimiter=";")
    rows = []
    rows.extend(rowsRAW)
    
    step = map(lambda x: x[0], rows)
    stepND = array( step )
    stepCount = max(stepND.astype(int))
    dataStep = []
    dataME = []
    for step in range(10, stepCount+10, 10):
        rowsSel = filter(lambda x: int(x[0])==step, rows)
        error = map(lambda x: x[2], rowsSel)
        errorND = array( error )
        meanError = average(errorND.astype(float))
        dataStep.append(step)
        dataME.append(meanError)
    
    plot(dataStep, dataME, marker=".", color='red')
    ylabel(u'průměrná chyba', family=fontFamily)
    xlabel(u'čas (kroky)', family=fontFamily)
    
    if saveEPS: savefig(fileName+".meanerror.eps", format="EPS")
    else:
        savefig(fileName+".meanerror.png", format="PNG")
        title(u'Průmerná chyba mapy v čase', family=fontFamily)
    clf()
    
def plotELNodeStats(fileName):
    rowsRAW = csv.reader(open(fileName, "rb"), delimiter=";")
    rows = []
    rows.extend(rowsRAW)
    
    stepND = arange(0, len(rows), 1)
    distMean = map(lambda x: x[1], rows)
    distMin = map(lambda x: x[2], rows)
    distMax = map(lambda x: x[3], rows)
    usageMean = map(lambda x: x[4], rows)
    usageMin = map(lambda x: x[5], rows)
    usageMax = map(lambda x: x[6], rows)
    agMean = map(lambda x: x[7], rows)
    agMin = map(lambda x: x[8], rows)
    agMax = map(lambda x: x[9], rows)
    distMeanND = array( distMean )
    distMinND = array( distMin )
    distMaxND = array( distMax )
    usageMeanND = array( usageMean )
    usageMinND = array( usageMin )
    usageMaxND = array( usageMax )
    agMeanND = array( agMean )
    agMinND = array( agMin )
    agMaxND = array( agMax )
     
    plot(stepND, distMeanND, 'b-', label=u'průměr')
    plot(stepND, distMinND, 'k:', label=u'min')
    plot(stepND, distMaxND, 'k,', label=u'max')
    yscale('log')
    xlabel(u"čas (kroky)", family=fontFamily)
    ylabel(u'změna polohy uzlu', family=fontFamily)
    legend(loc='best', prop=fontObj)
    
    if saveEPS: savefig(fileName+".dist.eps", format="EPS")
    else:
        savefig(fileName+".dist.png", format="PNG")
        title(u'Změna polohy uzlu v čase', family=fontFamily)
    clf()
    
    plot(stepND, usageMeanND, 'b-', label=u'průměr')
    plot(stepND, usageMinND, 'k:', label=u'min')
    plot(stepND, usageMaxND, 'k:', label=u'max')
    xlabel(u"čas (kroky)", family=fontFamily)
    ylabel(u'naplněnost uzlu', family=fontFamily)
    legend(loc='best', prop=fontObj)
    
    if saveEPS: savefig(fileName+".usage.eps", format="EPS")
    else:
        savefig(fileName+".usage.png", format="PNG")
        title(u'Naplněnost uzlů v čase', family=fontFamily)
    clf()
    
    plot(stepND, agMeanND, 'b-', label=u'průměr')
    plot(stepND, agMinND, 'k:', label=u'min')
    plot(stepND, agMaxND, 'k:', label=u'max')
    xlabel(u"čas (kroky)", family=fontFamily)
    ylabel(u'množství odpudivosti', family=fontFamily)
    legend(loc='best', prop=fontObj)
    
    if saveEPS: savefig(fileName+".ag.eps", format="EPS")
    else:
        savefig(fileName+".ag.png", format="PNG")
        title(u'Množství odpudivosti v čase', family=fontFamily)
    clf()
    
def plotPlacesStats(fileName):
    rowsRAW = csv.reader(open(fileName, "rb"), delimiter=";")
    rows = []
    rows.extend(rowsRAW)
    
    stepND = arange(0, len(rows), 1)
    agMean = map(lambda x: x[1], rows)
    agMin = map(lambda x: x[2], rows)
    agMax = map(lambda x: x[3], rows)
    agMeanND = array( agMean )
    agMinND = array( agMin )
    agMaxND = array( agMax )
     
    plot(stepND, agMeanND, 'b-', label=u'průměr')
    plot(stepND, agMinND, 'k:', label='min')
    plot(stepND, agMaxND, 'k:', label='max')
    xlabel(u"čas (kroky)", family=fontFamily)
    ylabel(u'množství odpudivosti', family=fontFamily)
    legend(loc='best', prop=fontObj)
    
    if saveEPS: savefig(fileName+".ag.eps", format="EPS")
    else:
        savefig(fileName+".ag.png", format="PNG")
        title(u'Množství odpudivosti v čase', family=fontFamily)
    clf()

def plotPlace(fileName):
    rowsRAW = csv.reader(open(fileName, "rb"), delimiter=";")
    rows = []
    rows.extend(rowsRAW)
    
    steps = map(lambda x: x[0], rows)
    agC = map(lambda x: x[6], rows)
    agT = map(lambda x: x[7], rows)
    agS = map(lambda x: x[8], rows)
    stepND = array( steps )
    agCND = array( agC )
    agTND = array( agT )
    agSND = array( agS )
    
    plot(stepND, agCND, 'k-', label=u'množství odpudivosti')
    plot(stepND, agTND, 'g-', label=u'celkové množství odpudivosti')
    plot(stepND, agSND, 'b-', label=u'intenzita')
    xlabel(u"čas (kroky)", family=fontFamily)
    ylabel(u'množství odpudivosti a intenzita', family=fontFamily)
    legend(loc='best', prop=fontObj)
    
    if saveEPS: savefig(fileName+".ags.eps", format="EPS")
    else:
        savefig(fileName+".ags.png", format="PNG")
        title(u'Množství odpudivosti a intenzita v čase', family=fontFamily)
    clf()

def plotNC(fileName):
    rowsRAW = csv.reader(open(fileName, "rb"), delimiter=";")
    rows = []
    rows.extend(rowsRAW)

    stepsND = arange(0, len(rows), 1)
    stepsND = array(map(lambda x: x[0], rows))
    ncCount = map(lambda x: x[1], rows)
    desiredCount = map(lambda x: x[4], rows)
    objsCount = map(lambda x: x[5], rows)

    ncCountND = array( ncCount )
    desiredCountND = array( desiredCount )
    objsCountND = array( objsCount )
    figure()
    plot(stepsND, ncCountND, 'g-', label=u'počet uzlů')
    plot(stepsND, desiredCountND, 'k:', label=u'chtěný počet uzlů')
    plot(stepsND, objsCountND, 'b:', label=u'počet předmětů')
    legend(loc='best', prop=fontObj)
    ylabel(u'počet', family=fontFamily)
    xlabel(u'čas (kroky)', family=fontFamily)
    
    if saveEPS: savefig(fileName+".eps", format="EPS")
    else:
        savefig(fileName+".png", format="PNG")
        title(ur'Počet uzlů v čase', family=fontFamily)
    clf()


fontFamily = 'Arial'
fontObj = FontProperties(family=fontFamily);
## if True, app will plot remember data (mean/min/max/trained) error for every object
full = False   
## if True, app will save all output as EPS without title  
saveEPS = True

for root, dirs, files in os.walk('.'):
    print root
    for fname in files:
        if fname == "data-objheatmap.txt":
            print ("plotHeatMapObj " + root + "\\" + fname)
            plotHeatMap(root + "\\" + fname, u"Mapa naučenosti předmětů")
        elif fname == "data-elnodeheatmap.txt":
            print ("plotHeatMapELNode " + root + "\\" + fname)
            plotHeatMap(root + "\\" + fname, u"Mapa naplněnosti uzlů prostorové mapy")
        elif fname == "data-elnodeheatmapag.txt":
            print ("plotHeatMapELNodeAG " + root + "\\" + fname)
            plotHeatMap(root + "\\" + fname, u"Mapa množství AG uzlů prostorové mapy")
        elif fname == "data-nc.txt":
            print ("plotNC " + root + "\\" + fname)
            plotNC(root + "\\" + fname)
        elif fname.startswith("data-rememberinfo") and fname.endswith(".txt"):
            print ("plotRem " + root + "\\" + fname)
            plotMeanErrorInTime(root + "\\" + fname)
            plotRemember(root + "\\" + fname, full)
        elif fname == "data-elnode-status.stats.txt":
            print ("plotELNodeStats " + root + "\\" + fname)
            plotELNodeStats(root + "\\" + fname)
        elif fname == "data-places-status.stats.txt":
            print ("plotPlacesStats " + root + "\\" + fname)
            plotPlacesStats(root + "\\" + fname)
        elif fname.startswith("place-") and fname.endswith(".txt"):
            print ("plotPlaces " + root + "\\" + fname)
            plotPlace(root + "\\" + fname)

print "*** END ***"          
            
