#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: runProgramLinux.py
Authors: Zack Bennett (zbe14), Blake Manson (bma206)
Date: 20/04/2024

Description: A program to create and run a RIPv2 Routing Daemon based off a given config
file, that displaysthe connections in the form of a routing table printed to the terminal.

This program is made to run on Linux machines
"""

import sys
import socket as s
from time import time, sleep
from random import randint

from routing import RoutingTable
from packets import recieveMessages, sendToAll

# GLOBAL VARIABLES
CONFIGFILE = sys.argv[1]
LOCALHOST = "127.0.0.1"


def createInputSockets(inputPorts):
    """Tries to create sockets for each input port, and adds the sockets to the open sockets list"""
    inputSockets = list()
    for port in inputPorts:
        try:
            sock = s.socket(s.AF_INET, s.SOCK_DGRAM)
            sock.bind((LOCALHOST, port))
            inputSockets.append(sock)
        except:
            print("Port " + str(port) + " failed to open, try again")
    return inputSockets

def closeSockets(inputSockets, outputs):
    """Closes all open sockets listed in the openSockets list"""
    for s in inputSockets:
        s.close()
    for output in outputs:
        output.socket.close()
    print("All sockets have been closed\n")

def garbageHandler(garbageTimer, outputs, routingTable, routerID):
    """Takes a list of routers and removes the ones exceeding the garbage timer"""
    expiredRouters = list()
    for router in routingTable.entries.values():
        if router.isGarbage and router.timeSince >= garbageTimer:
            expiredRouters.append(router)
        elif router.isGarbage == False and router.timeSince >= garbageTimer:
            router.setToInfinity()
            routingTable.entries[router.routerID] = router
            router.isGarbage = True
    sendToAll(outputs, routerID, routingTable)
    for router in expiredRouters:
        routingTable.removeEntry(router.routerID)
    
class Output(object):
    """Class defining each part of an output"""
    def __init__(self, string):
        """Takes a string of format port-metric-routerID"""
        parts = string.split("-")

        self.port = int(parts[0])
        self.metric = int(parts[1])
        self.routerID = int(parts[2])
        self.createOutputSocket()

    def createOutputSocket(self):
        """Creates the socket to output from"""
        try:
            sock = s.socket(s.AF_INET, s.SOCK_DGRAM)
            self.socket = sock
        except:
            print("Port " + str(self.port) + " failed to open, try again")
    
def createDaemon(config):
    """returns the ID, input ports and outputs of the daemon"""
    lines = config.readlines()

    routerID = int(lines[0].strip("router-id "))
    strInputPorts = list(lines[1].strip("input-ports ").strip("\n").split(" "))
    inputPorts = list()
    for i in strInputPorts:
        inputPorts.append(int(i))
    outputs = list()
    for element in lines[2].strip("outputs ").split(" "):
        output = Output(element)
        outputs.append(output)
    return routerID, inputPorts, outputs 

def main():
    """initialisation"""
    print("\nInput config file name: " + CONFIGFILE)
    config = open(CONFIGFILE, 'r')
    routerID, inputPorts, outputs = createDaemon(config)
    config.close()
    print("Daemon started (Ctrl + C to quit)")
    inputSockets = createInputSockets(inputPorts)
    routingTable = RoutingTable(routerID)

    """set random periodic time to prevent overlaps"""
    #updateTimer = random.randint(16, 25) #for demonstration
    updateTimer = randint(2, 12) #for testing
    print(f"Update timer is {updateTimer} seconds")
    garbageTimer = 6*updateTimer
    garbageCounter = 0

    try:
        while True:
            currentTime = int(time())
            if currentTime % updateTimer == 0:
                sleep(1) # to stop multiple updates in 1s

                sendToAll(outputs, routerID, routingTable)
                updated = recieveMessages(inputSockets, 2, routingTable, routerID)
                if updated:
                    sendToAll(outputs, routerID, routingTable)
                print(str(routingTable) + "\n")
                garbageCounter += 1

            if garbageCounter == 6:
                garbageHandler(garbageTimer, outputs, routingTable, routerID)
                print("Removing unresponsive routers")
                garbageCounter = 0

    except KeyboardInterrupt:
        closeSockets(inputSockets, outputs)
        print("Closing software")
        exit(0)

if (__name__ == "__main__"):
    main()