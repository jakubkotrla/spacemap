# -*- coding: UTF-8 -*-

from __future__ import division
from Time import Time
import time

class GlobalVariables:
    def __init__(self):
        self.Time    = Time()
        self.MaxNumber = 9999999
        
        self.gTerrainTypes = { "forest":"#008000", "wood":"#808000", "meadow": "#00b355", 
                "stone_mountain": "#a0a0a0", "iron_mountain": "#ff9f71", "cave": "#996600",
                "house": "#cc6600", "town": "#ffcc99", "road": "#a4a4a4", "default": "#e0e0e0",
                "parcel": "#d2b48c", "room": "#4682b4", "park": "#9acd32", "chamber": "#b8860b" }
        self.WorstEffectivity = 999999999
        self.CutObjects = []
        self.MainCycle = None
        self.World = None
        self.Map = None
        self.MapVisibility = 10
        self.MapObjectPickupDistance = 10
        self.wndLog = None
        self.wndPA = None
        self.Variables = {}
        self.AgentSpeed = 3
        self.MaxResults = 5
        self.objectsList = []
        
        teraz=time.localtime(time.time())
        year, month, day, hour, minute, second, weekday, yearday, daylight = teraz
        datum="%04d-%02d-%02d" % (year, month, day)
        cas="%02d-%02d-%02d" % (hour, minute, second)
        self.gTimeStart = "experiments/"+datum + "_" + cas
        
    def Log(self, msg):
        print msg
        if self.wndLog != None:
            self.wndLog.txtLog.insert("end", msg)
        
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
        
