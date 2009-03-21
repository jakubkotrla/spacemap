
# simple script to plot outputted data
from pylab import *
import os
import csv
from numpy import *


def addToQueue(visited, queue, point, value):
    hash = str(point[0]) + ";" + str(point[1])
    if hash not in visited and value > 0.1:
        visited[hash] = hash
        queue.append( (point[0], point[1], (value/2)) )
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


def plotHeatMap(fileName, titleStr, defValue=None):
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
        if defValue != None:
            fill(mapa, x, y, defValue)
        else:
            fill(mapa, x, y, value)

    ndA = array(mapa)    
    im = imshow(ndA, cmap=cm.gray, interpolation=None, origin='upper',extent=(0,100,0,100))
    colorbar()
    title(titleStr)
    savefig(fileName+".png", format="PNG")
    clf()

    for i in range(101):
        for j in range(101):
            mapa[i][j] = sqrt(mapa[i][j])

    ndA = array(mapa)    
    im = imshow(ndA, cmap=cm.gray, interpolation='bilinear', origin='upper',extent=(0,100,0,100))
    colorbar()
    title(titleStr + " sqrt")
    savefig(fileName+"sqrt.png", format="PNG")
    clf()



def plotNC(fileName):
    rowsRAW = csv.reader(open(fileName, "rb"), delimiter=";")
    rows = []
    rows.extend(rowsRAW)
    
    stepsND = arange(0, len(rows), 1)
    ncCount = map(lambda x: x[0], rows)
    desiredCount = map(lambda x: x[3], rows)
    objsCount = map(lambda x: x[4], rows)
    
    ncCountND = array( ncCount )
    desiredCountND = array( desiredCount )
    objsCountND = array( objsCount )
    figure()
    plot(stepsND, ncCountND, 'g-', label='El-node count')
    plot(stepsND, desiredCountND, 'k:', label='desired EL-node count')
    plot(stepsND, objsCountND, 'b:', label='Object count')
    legend(loc='lower right')
    
    ylabel('EL-nodes count')
    xlabel('time (steps)')
    title('EL-nodes count in time')
    savefig(fileName+".png", format="PNG")
    clf()

def plotRememberOne(fileName, rows):
    trained = map(lambda x: x[1], rows)
    error = map(lambda x: x[2], rows)
    
    errorND = array( error )
    trainedND = array( trained )
    plot(trainedND, errorND, marker=",", color='red', drawstyle="steps", linestyle="None")
    ylabel('Error')
    xlabel('Amount trained')
    title('Error / trained')
    savefig(fileName+".png", format="PNG")
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
        xlabel("Time (steps)")
        ylabel('Amount trained')
        title('Trained in time')
    
        subplot(212)
    plot(stepND, errorND, marker=",", color='red', drawstyle="steps", linestyle="None")
    ylabel('Error')
    xlabel("Time (steps)")
    title('Error in time - mean: %.2f'%meanError)
    savefig(fileName+".png", format="PNG")
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
    ylabel('Mean error')
    xlabel('Time (steps)')
    title('Mean error in time')
    savefig(fileName+".meanerror.png", format="PNG")
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
     
    plot(stepND, distMeanND, 'b-', label='mean')
    plot(stepND, distMinND, 'k:', label='min')
    plot(stepND, distMaxND, 'k,', label='max')
    #plot(stepND, distMaxND, marker=",", color='red', drawstyle="steps", linestyle="None", label="max")
    yscale('log')
    xlabel("Time (steps)")
    ylabel('Distance moved')
    title('Distance moved in time')
    legend(loc='upper left')
    savefig(fileName+".dist.png", format="PNG")
    clf()
    
    plot(stepND, usageMeanND, 'b-', label='mean')
    plot(stepND, usageMinND, 'k:', label='min')
    plot(stepND, usageMaxND, 'k:', label='max')
    xlabel("Time (steps)")
    ylabel('Node usage')
    title('Node usage in time')
    legend(loc='upper left')
    savefig(fileName+".usage.png", format="PNG")
    clf()
    
    plot(stepND, agMeanND, 'b-', label='mean')
    plot(stepND, agMinND, 'k:', label='min')
    plot(stepND, agMaxND, 'k:', label='max')
    xlabel("Time (steps)")
    ylabel('AG amount')
    title('AG amount in time')
    legend(loc='upper left')
    savefig(fileName+".ag.png", format="PNG")
    clf()
    
def plotHist():
    rowsRAW = csv.reader(open("p.txt", "rb"), delimiter=";")
    rows = []
    rows.extend(rowsRAW)
    rows = map(lambda x: x[2], rows)
    rowsND = array(rows)
    hist(rowsND.astype(float), bins=20)
    savefig("p.png", format="PNG")

    
     
full = False   

for root, dirs, files in os.walk('.'):
    print root
    for fname in files:
        if fname == "data-objheatmap.txt":
            print ("plotHeatMapObj " + root + "\\" + fname)
            plotHeatMap(root + "\\" + fname, "Object HeatMap")
        elif fname == "data-elnodeheatmap.txt":
            print ("plotHeatMapELNode " + root + "\\" + fname)
            plotHeatMap(root + "\\" + fname, "ELNodes HeatMap")
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
            

print "*** END ***"          
            
