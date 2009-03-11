
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

def plotRemember(fileName):
    portfolio = csv.reader(open(fileName, "rb"), delimiter=";")
    rows = []
    rows.extend(portfolio)
    a = filter(lambda x: x[3]=="12", rows)
    
    step = map(lambda x: x[0], rows)
    trained = map(lambda x: x[1], rows)
    error = map(lambda x: x[2], rows)
    
    errorND = array( error )
    trainedND = array( trained )
    plot(trainedND, errorND, marker=".", color='red', drawstyle="steps", linestyle="None")
    ylabel('Error')
    xlabel('Amount trained')
    title('Error / trained')
    #savefig(fileName+".err-train.png", format="PNG")
    show()

    
def plotRememberTime(fileName):
    plotfile(fileName, (0,1,2), delimiter=";", marker=".", color='red', drawstyle="steps", linestyle="None")
    title('Error and trained in time')
    ylabel('Error')
    xlabel('time (steps)')
    savefig(fileName+".png", format="PNG")
    #show()

plotRemember("data-rememberinfo.txt")
exit()
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
            try:
                plotRememberTime(root + "\\" + fname)
            except:
                pass
            
