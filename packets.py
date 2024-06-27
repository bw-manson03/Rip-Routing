#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: packets.py
Authors: Zack Bennett (zbe14), Blake Manson (bma206)
Date: 20/04/2024

Description: A module to send and recieve packets, and process into routing table entries
"""

import select

import header
from routing import Router

LOCALHOST = "127.0.0.1"

def sendMessage(output, routerID, routingTable):
    """Creates the update message to send to a connected router, then sends the message"""
    entries = []
    messageHeader = header.rip_packet_header(routerID)
    entry = header.rip_packet_entry(routerID, routerID, output.metric)
    entries.append(entry)
    for router in routingTable.entries.values():
        if output.routerID != router.routerID:
            if output.routerID != router.firstHop:
                entry = header.rip_packet_entry(router.routerID, routerID, router.metric)
                entries.append(entry)
            else:
                entry = header.rip_packet_entry(router.routerID, routerID, 32)
                entries.append(entry)
    packet = header.rip_packet(messageHeader, entries)
    output.socket.sendto(packet, (LOCALHOST, output.port))

def sendToAll(outputs, routerID, routingTable):
    """function to send packets to all routers from the given output list"""
    for output in outputs:
        sendMessage(output, routerID, routingTable)

def recieveMessages(inputSockets, timeout, routingTable, routerID):
    """Receieves incoming messages"""
    updated = False
    readable, writable, exceptional = select.select(inputSockets, [], [], timeout)
    for socket in readable:
        packet = socket.recvfrom(2048)
        updated = processMessage(packet, routingTable, routerID)
    if not updated:
        for entry in routingTable.entries.values():
            entry.updateTimeSince()
            routingTable.entries[entry.routerID] = entry
    return updated

def processMessage(message, routingTable, routerID):
    """ Recieves a message from a router and processes it. """
    updatedEntries = list()
    # check packet length
    messageByteArray, address = message
    message  =  bytearray(messageByteArray)  #
    num_entries = (len(message) - 4) // 20
    receivedHeader = message[0:4]
    senderID = receivedHeader[3]
    if header.checkHeader(receivedHeader):
        i = 4
        for _ in range(num_entries):
            entry = message[i:i + 20]
            if header.checkEntry(entry):
                # pull the contents of the entry
                peerRouterID = int(entry[7])
                firstHop = int(entry[15])
                metric = int(entry[19])
                router = Router(peerRouterID, firstHop, metric)
                updated = routingTable.updateEntry(router, routerID, senderID)
                if updated:
                    updatedEntries.append(router.routerID)
            i += 20

        # the first 4 bytes of the packet should be the header
        # the 20 bytes afterwards are each entry in the routers routing table.
        #get the entries out of packet
    for entry in routingTable.entries.values():
        if entry.routerID in updatedEntries:
            entry.updateTime()
        entry.updateTimeSince()
        routingTable.entries[entry.routerID] = entry
    return updated