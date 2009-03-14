
# simple script to plot outputted data
from pylab import *
import os
import csv
from numpy import *

def plotNC(fileName):
    plotfile(fileName, (0,), delimiter=";", color='green')
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
        

def plotRemember(fileName):
    rowsRAW = csv.reader(open(fileName, "rb"), delimiter=";")
    rows = []
    rows.extend(rowsRAW)
        
    plotRememberOne(fileName, rows)
    plotRememberTimeOne(fileName + ".time", rows)
        
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
    
def plotELNode(fileName):
    rowsRAW = csv.reader(open(fileName, "rb"), delimiter=";")
    rows = []
    rows.extend(rowsRAW)
    
    step = map(lambda x: x[0], rows)
    index = map(lambda x: x[1], rows)
    dist = map(lambda x: x[2], rows)
    usage = map(lambda x: x[3], rows)
    ag = map(lambda x: x[4], rows)
    
    stepND = array( step )
    indexND = array( index )
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
    
      
      
      
      
      

for root, dirs, files in os.walk('.'):
    print root
    for fname in files:
        if fname == "data-nc.txt":
            print ("plotNC " + root + "\\" + fname)
            plotNC(root + "\\" + fname)
        elif fname.startswith("data-rememberinfo") and fname.endswith(".txt"):
            print ("plotRem " + root + "\\" + fname)
            plotMeanErrorInTime(root + "\\" + fname)
            plotRemember(root + "\\" + fname)
        elif fname.startswith("data-elnode") and fname.endswith(".txt"):
            print ("plotELNode " + root + "\\" + fname)    
            plotELNode(root + "\\" + fname)

print "*** END ***"          
            
