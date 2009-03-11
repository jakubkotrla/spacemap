
# simple script to plot outputted data
from pylab import *
import csv

class SKV(csv.excel):
    delimiter = ";"
csv.register_dialect("SKV", SKV)

def plotNC(fileName):
    plotfile(fileName, (0,), delimiter=";", color='green')
    ylabel('EL-nodes count')
    xlabel('time (steps)')
    title('EL-nodes count in time')
    savefig(fileName+".png", format="PNG")
    show()
    
def plotRemember(fileName):
    #plotfile(fileName, (1,2), delimiter=";", marker=".", color='red', drawstyle="steps", linestyle="None")
    #ylabel('Error')
    #xlabel('Amount trained')
    #title('Error / trained')
    #savefig(fileName+".err-train.png", format="PNG")
    #show()
    
    
    plotfile(fileName, (0,3,1,2), delimiter=";", marker=".", color='red', drawstyle="steps", linestyle="None")
    
    title('Error / trained')
    
    ylabel(['Error', 'a'])
    xlabel('time (steps)')
    savefig(fileName+".png", format="PNG")
    show()


#plotNC("data-nc.txt")
plotRemember("data-rememberinfo.txt")
