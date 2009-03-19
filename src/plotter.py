
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
    plot(trainedND, errorND, marker=".", color='red', drawstyle="steps", linestyle="None")
    ylabel('Error')
    xlabel('Amount trained')
    title('Error / trained')
    savefig(fileName+".png", format="PNG")
    clf()

def plotRememberTimeOne(fileName, rows):
    step = map(lambda x: x[0], rows)
    trained = map(lambda x: x[1], rows)
    error = map(lambda x: x[2], rows)
    
    stepND = array( step )
    errorND = array( error )
    trainedND = array( trained )
    meanError = average(errorND.astype(float))
    
    subplots_adjust(hspace=1)
    subplot(211)
    plot(stepND, trainedND, marker=".", color='red', drawstyle="steps", linestyle="None")
    xlabel("Time (steps)")
    ylabel('Amount trained')
    title('Trained in time')
    
    subplot(212)
    plot(stepND, errorND, marker=".", color='red', drawstyle="steps", linestyle="None")
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
    plotRememberTimeOne(fileName + ".time", rows)
    
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
    outFile = open(fileName + ".stats.txt", "w")
        
    step = map(lambda x: x[0], rows)
    stepND = array( step )
    stepCount = max(stepND.astype(int))
    dataStep = []
    dataMeanDist = []
    dataMeanUsage = []
    dataMeanAg = []
    dataMaxAg = []
    for step in range(0, stepCount+1):
        print "plotELNodeStats step " + str(step)
        rowsSel = filter(lambda x: int(x[0])==step, rows)
        
        dist = map(lambda x: x[2], rowsSel)
        usage = map(lambda x: x[3], rowsSel)
        ag = map(lambda x: x[4], rowsSel)
        distND = array( dist )
        usageND = array( usage )
        agND = array( ag )
        
        dataStep.append(step)
        meanDist = average(distND.astype(float))
        dataMeanDist.append(meanDist)
        meanUsage = average(usageND.astype(float))
        dataMeanUsage.append(meanUsage)
        meanAG = average(agND.astype(float))
        dataMeanAg.append(meanAG)
        maxAG = max(agND.astype(float))
        dataMaxAg.append(maxAG)
        
        data = str(step) + ";" + str(meanDist) + ";" + str(meanUsage) + ";" + str(meanAG) + ";" + str(maxAG)  
        outFile.write(data + "\n")
        
    outFile.close()
    subplots_adjust(hspace=1)
    subplot(211)
    plot(dataStep, dataMeanDist, color='blue')
    xlabel("Time (steps)")
    ylabel('Mean distance moved')
    title('Mean distance moved in time')
    
    subplot(212)
    plot(dataStep, dataMeanUsage, color='blue')
    xlabel("Time (steps)")
    ylabel('Mean usage')
    title('Mean usage in time')
    
    savefig(fileName+".stats.png", format="PNG")
    clf()
    
    subplot(211)
    plot(dataStep, dataMeanAg, color='blue')
    xlabel("Time (steps)")
    ylabel('Mean AG amount')
    title('Mean AG amount in time')
    
    subplot(212)
    plot(dataStep, dataMaxAg, color='blue')
    xlabel("Time (steps)")
    ylabel('Max AG amount')
    title('Max AG amount in time')
    
    savefig(fileName+".ag.png", format="PNG")
    clf()
    

def plotELNodeOne(fileName, rows):
    step = map(lambda x: x[0], rows)
    dist = map(lambda x: x[2], rows)
    usage = map(lambda x: x[3], rows)
    ag = map(lambda x: x[4], rows)
    
    stepND = array( step )
    distND = array( dist )
    usageND = array( usage )
    agND = array( ag )
        
    subplots_adjust(hspace=1)
    subplot(311)
    plot(stepND, distND, color='blue')
    xlabel("Time (steps)")
    ylabel('Distance moved')
    title('Distance moved in time')
    
    subplot(312)
    plot(stepND, usageND, color='blue')
    xlabel("Time (steps)")
    ylabel('Usage')
    title('Usage in time')
    
    subplot(313)
    plot(stepND, agND, color='blue')
    xlabel("Time (steps)")
    ylabel('AG amount')
    title('AG amount in time')
    
    savefig(fileName+".png", format="PNG")
    clf()
    
def plotELNode(fileName):
    rowsRAW = csv.reader(open(fileName, "rb"), delimiter=";")
    rows = []
    rows.extend(rowsRAW)
        
    index = map(lambda x: x[1], rows)
    index = list(set(index))
    for i in index:
        rowsObj = filter(lambda x: x[1]==i, rows)
        plotELNodeOne(fileName + i, rowsObj)    

     
full = False   
elnodeStats = False   

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
        elif fname == "data-elnode-status.txt":
            print ("plotELNodeStats " + root + "\\" + fname)
            if elnodeStats: plotELNodeStats(root + "\\" + fname)
            if full:
                print ("plotELNode " + root + "\\" + fname)    
                plotELNode(root + "\\" + fname)

print "*** END ***"          
            
