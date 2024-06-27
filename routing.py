#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: routing.py
Authors: Zack Bennett (zbe14), Blake Manson (bma206)
Date: 18/04/2024

Description: A module to create and manage routing tables and their entries
"""

from tabulate import tabulate
from time import time

INFINITY = 32

class Router(object):
    """Router object, a class describing a router that is communicating with the daemon"""
    def __init__(self, routerID, firstHop, metric, time = time()):
        self.routerID = routerID
        self.firstHop = firstHop
        self.metric = metric
        self.time = time
        self.isGarbage = False
        self.updateTimeSince()

    def updateTime(self):
        """Updates the time when updated"""
        self.time = time()
    
    def updateTimeSince(self):
        """updates time since last update"""
        self.timeSince = time() - self.time

    def setToInfinity(self):
        """Sets the metric to infinity to show the router is disconnected or for first hops"""
        self.metric = INFINITY

class RoutingTable(object):
    """Routing table object, a class that stores all information about all other routers using router objects"""
    def __init__(self, routerID):
        self.entries = dict()
        self.routerID = routerID

    def __repr__(self):
        rstr = str(self.entries)
        return rstr
    
    def __str__(self):
        rstr = f"Router ID: {self.routerID}\n"
        headers = ["Router", "Metric", "First Hop", "Time Since Update"]
        routerTableOutput = []
        for _ in self.entries.values():
            timeStamp = f"{_.timeSince:.2f}"
            routerTableOutput.append([_.routerID, _.metric, _.firstHop, timeStamp])
        table_str = tabulate(sorted(routerTableOutput), headers=headers, tablefmt="grid")
        rstr += table_str
        return rstr

    def getEntry(self, routerID):
        """Returns a single entry of a router object by its ID"""
        return self.entries.get(routerID)

    def updateEntry(self, entry, routerID, senderID):
        """Adds a router to the routing table if applicable"""

        updated = False

        previousEntry = self.getEntry(entry.routerID)

        sender = self.getEntry(senderID)
        if sender == None or entry.routerID == senderID: # This means we are initialising the senders' entry so dont need to add cost
            linkCost = 0
        else:
            linkCost = sender.metric
        totalCost = linkCost + entry.metric

        if previousEntry == None and totalCost < INFINITY: #If the route is not in the table yet
            entry.metric = totalCost
            self.entries[entry.routerID] = entry
            updated = True

        elif previousEntry != None:
            
            if totalCost < previousEntry.metric:
                entry.metric = totalCost
                self.entries[entry.routerID] = entry
                updated = True
            
            elif entry.firstHop == previousEntry.firstHop:
                if previousEntry.isGarbage:
                    return False
            
                elif totalCost > previousEntry.metric:
                    if totalCost >= INFINITY:
                        entry.isGarbage = True
                        entry.metric = INFINITY
                    else:
                        entry.metric = totalCost # If the new metric from same hop is worse, we must use it
                    updated = True
                    self.entries[entry.routerID] = entry

                elif totalCost == previousEntry.metric:
                    updated = True
        return updated

    def removeEntry(self, routerID):
        """Removes a router from the routing table"""
        if (self.entries.get(routerID)):
            return self.entries.pop(routerID)
        else:
            return None