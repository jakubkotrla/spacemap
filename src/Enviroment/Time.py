## @package Enviroment.Time
# Implements advanced time functions.

import string
import math

## Represents arbitrary time.
class Time:
    def __init__(self, day=0, hour=0, minute=0, second=0, week = 0):
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.week = week

    ## Returns True if self was before given time.
    def Before(self, time):
        if time.day > self.day:
            return True
        elif time.day < self.day:
            return False
        elif time.hour > self.hour:
            return True
        elif time.hour < self.hour:
            return False
        elif time.minute >= self.minute:
            return True
        else:
            return False
    
    ## Adds given count of seconds to self.        
    def AddSeconds(self, seconds):
        self.second += int(math.floor(seconds))
        if self.second > 59:
            self.minute = self.minute + int(math.floor(self.second / 60))
            self.second = self.second % 60
        if self.minute > 59:
            self.hour = self.hour + int(math.floor(self.minute / 60))
            self.minute = self.minute % 60
        if self.hour > 23:
            self.day = self.day + int(math.floor(self.hour / 24))
            self.hour = self.hour % 24
        if self.day > 6:
            self.week = self.week + int(math.floor(self.day / 7))
            self.day = self.day % 7
      
    
    def GetDay(self):
        return self.day
    
    def GetWeek(self):
        return self.week
    
    def ToString(self):
        return str(self.hour)+":"+string.zfill(str(self.minute),2)+":"+string.zfill(str(self.second),2)
        
    def DiffInMinutes(self, timeFrom):
        return ((self.day-timeFrom.day)*24 + self.hour-timeFrom.hour)*60 + self.minute-timeFrom.minute
    
    def ToHours(self):  
        return self.day*24 + self.hour + self.minute/float(60)    
    
    def IsNewDay(self):
        return ((self.hour == 0) and (self.minute == 0) and (self.second == 0))
    
    def GetSecondsInDay(self):
        return self.hour*3600 + self.minute*60 + self.second
    
    ## Returns count of seconds from time zero, lie Unix timeestamp.
    def GetSeconds(self):
        return self.week*3600*24*7 + self.day*3600*24 + self.hour*3600 + self.minute*60 + self.second
    
    ## Formats self to human readable string.
    def TimeToHumanFormat(self, full=False):
        strDay = str(self.week*7 + self.day)
          
        if self.hour < 10: strHours = "0" + str(self.hour)
        else: strHours = str(self.hour)
        if self.minute < 10: strMinute = "0" + str(self.minute)
        else: strMinute = str(self.minute)
        if self.second < 10: strSecs = "0" + str(self.second)
        else: strSecs = str(self.second)
        
        if full:
            return "Week " + str(self.week) + ", Day " + str(self.day) + ", " + strHours + ":" + strMinute + ":" + strSecs
        else:
            return "Day " + strDay + ", " + strHours + ":" + strMinute + ":" + strSecs
        
