# -*- coding: UTF-8 -*-

from __future__ import division
from Time import Time
import time
from math import exp

class GlobalVariables:
    def __init__(self):
        self.Time    = Time()
        self.MaxNumber = 9999999
        
        self.World = None
        self.Map = None
        
        self.wndLog = None
        self.wndPA = None
        self.AgentMoveHistoryLength = 10
        
        self.MapVisibility = 10
        self.MapObjectPickupDistance = 10
        
        self.GridLayerNodeSize = 20 
        
        
        
        
        # OLD !!!
        self.WorstEffectivity = 999999999
        self.CutObjects = []
        self.MainCycle = None
        self.Variables = {}
        self.AgentSpeed = 3
        self.MaxResults = 5
        self.objectsList = []
        self.gTerrainTypes = { "forest":"#008000", "wood":"#808000", "meadow": "#00b355", 
                "stone_mountain": "#a0a0a0", "iron_mountain": "#ff9f71", "cave": "#996600",
                "house": "#cc6600", "town": "#ffcc99", "road": "#a4a4a4", "default": "#e0e0e0",
                "parcel": "#d2b48c", "room": "#4682b4", "park": "#9acd32", "chamber": "#b8860b" }
        
        
        
    def Log(self, msg):
        print msg
        if self.wndLog != None:
            self.wndLog.txtLog.insert("end", msg)
        
    def Gauss(self, x, c=1):
        return exp( - ((x)**2) / 2*(c**2) )
        
    def TimeToHumanFormat(self):
        return self.Time.TimeToHumanFormat()
    
    
       
        
        
    def Explode(self,string,delimiter):
        result = []
        substring = ""
        for char in string:
            if char != delimiter:
                substring = substring + char
            else:
                result.append(substring)
                substring = ""
        if substring != "":
            result.append(substring)
        return result
    def PrintList(self,list):
        result = "[ \"" + list.pop(0) +"\""
        for item in list:
            result = result + ", \"" + item + "\""
        result = result + " ]"
        return result
    
        
        

Global = GlobalVariables()
        
