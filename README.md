# RIPv2 Project

## Name
RIP Routing Simulator

## Description
Assignment Submission for COSC364 Assignment 1: RIP Routing.
Grade Achieved: 57% (Probably should've fixed it using the whole damn CPU)

This software takes in a number of config files with an ID, a list of available connections to other routers, and a list of ports to listen on for other routers, and creates a RIPv2 routing daemon for each. The daemons will launch in their own terminal and display all current connections and their cost, closest hop, time since the last recieved packet from this router, and the ID of the router in a table. This will update periodically with any changes to connections.

This program has quite a few bugs:
. Uses 100% of the CPU due to listening not timing out correctly.
. Takes too long to converge to the correct connections, could be due to split horizon not working as intended.
. Routers loop connections due to bad poisoned reverse, displaying old router connections.

Will try to fix these problems if I can be bothered later.

## Installation
Download and extract the folder, and launch the "run.sh" file. run.sh is initially set up to launch 7 routers using the included Test-2 config files. To change the routers, just follow the same format as the included config files and update the run.sh file.

This program will only work on Linux devices with Python installed, with the module Tabulate.

## Authors and acknowledgment
Blake Manson (bma206), Zack Bennett (zbe14) - University of Canterbury.
