
# simple script to plot outputted data
from pylab import *
import os
import csv

def plotNC(fileName):
    plotfile(fileName, (0,), delimiter=";", color='green')
    ylabel('EL-nodes count')
    xlabel('time (steps)')
    title('EL-nodes count in time')
    savefig(fileName+".png", format="PNG")
    #show()

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
    title('Error in time')
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

for root, dirs, files in os.walk('.'):
    print root
    for fname in files:
        if fname == "data-nc.txt":
            print ("plotNC" + root + "\\" + fname)
            try:
                plotNC(root + "\\" + fname)
            except:
                pass
        if fname.startswith("data-rememberinfo") and fname.endswith(".txt"):
            print ("plotRem" + root + "\\" + fname)
            try:
                plotRemember(root + "\\" + fname)
            except:
                pass
            
            
