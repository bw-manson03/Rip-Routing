#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: header.py
Authors: Zack Bennett (zbe14), Blake Manson (bma206)
Date: 20/04/2024

Description: A module to create and check headers for RIP packets
"""

# Use RIP Packet format with the following changes:
# Ignore the issue of Network byte order
# 16b Zero field in common header should be the router-id
# Work with router-id instead of ipv4 addresses
# need to have consistancy checks on incoming packets.

def rip_packet_header(router_id):
    """ Common header structure for a RIP packet. """
    packet_header = bytearray(4)
    command = 2 # I think this is the right command value going off of [1]
    version = 2 # As specified in the assignment specification
    packet_header[0] = command
    packet_header[1] = version 
    packet_header[3] = router_id
    return packet_header


def rip_packet_entry(router_id, first_hop, metric):
    """ This function pieces together a routing entry for a RIP packet. """
    rip_entry = bytearray(20)
    rip_entry[7] = router_id
    rip_entry[15] = first_hop
    rip_entry[19] = metric
    return rip_entry


def rip_packet(header, entries):
    """ Takes a created header and a list of formatted entries and combines them all. """
    result = header
    for _ in entries:
        result += _
    result = bytes(result) #
    return result






def checkHeader(recievedHeader):
    """ This is a boolean returning header check for a pakcet that has been recieved. """
    if len(recievedHeader) != 4: # Length of the header  needs to be 4 bytes  long.
        length = len(recievedHeader)
        print(f"Error in Header length. it was {length}.")
        return False
    if recievedHeader[0] != 2:  # Command  should  equal  2
        print("Recieved header has the wrong commmand input.")
        return False
    if recievedHeader[1] != 2:  #  Version  needs to  be 2 as it is a  response message.
        print("Recieved header has the wrong version.")
        return False
    if recievedHeader[3] <= 0 or recievedHeader[3] > 7: # needs to be a router-id within the range of  router -ids for the network of 1-7.
        print("Invalid router id from recieved header.")
        return False
    return True 



def checkEntry(entry):
    """ This function checks an entry for any errors. Returns True if all checks are passed. """
    if entry[7] < 0 or entry[7] > 7: # Makes sure the router id name is within range of the network
        return False
    if entry[15] < 0 or entry[15] > 254: # Makes sure the first hop entry is valid
        return False
    if entry[19] < 0 or entry[19] > 254: # Makes sure the entry of the metric is within range.
        return False
    return True 

# testing 
#header = rip_packet_header(1)
#print(len(header))
