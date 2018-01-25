import requests
import csv
from bs4 import BeautifulSoup
import numpy as np
from datetime import datetime
import time
from tools import *
import os
import os.path
import numpy as np
from fixedPlaybyPlays import *
from scrape_CMS import *
from tools import *


bigDict = np.load("Combined.npy").item()

def ListofPlayers(d):
    """ create list of distinct players in CMS
    """
    L = []
    for keys in d:
        l = chopNames(keys)
        for name in l:
            if name not in L:
                L += [name]
    return L

def addList(L1,L2):
    """ add list togethers
    """
    L = [2*[0],11*[0],11*[0]]
    for entry in range(len(L1)):
        for item in range(len(L1[entry])):
            sum = L1[entry][item]+L2[entry][item]
            L[entry][item] = sum
    return L

def playerPM():
    D = {}
    for player in PLAYERS:
        bigL = [2*[0],11*[0],11*[0]]
        for keys in bigDict:
            lineup = chopNames(keys)
            if player in lineup:
                bigL = addList(bigL,bigDict[keys])
        D[player] = bigL
    np.save("Players_PM.npy",D)
    return D

def pairPM():
    D = {}
    for i1 in range(len(PLAYERS)):
        player1 = PLAYERS[i1]
        if i1 == len(PLAYERS) - 1:
            break
        for i2 in range(i1+1,len(PLAYERS)):
            player2 = PLAYERS[i2]
            bigL = [2*[0],11*[0],11*[0]]
            name = str([player1,player2])
            for keys in bigDict:
                lineup = chopNames(keys)
                if player1 in lineup and player2 in lineup:
                    bigL = addList(bigL,bigDict[keys])
            D[name] = bigL
    np.save("pair_PM.npy",D)
    return D


def dictcsv1(d,name):
    """ from a dictionary of lineups, put out a csv file
    """
    L = [heading1]
    for key in d:
        l = [key]
        LofName = chopNames(key)
        for n in LofName:
            l.append(n)
        for item in d[key]:
            for number in range(len(item)):
                if number == 0 and d[key].index(item) == 0: # for time
                    t = time.strftime("%H:%M:%S",time.gmtime(item[number]))
                    l.append(t)
                else: l.append(item[number])
        L += [l]
    write_to_csv(L,name)

def dictcsv2(d,name):
    """ from a dictionary of lineups, put out a csv file
    """
    L = [heading3]
    for key in d:
        l = []
        LofName = chopNames(key)
        for n in LofName:
            l.append(n)
        for item in d[key]:
            for number in range(len(item)):
                if number == 0 and d[key].index(item) == 0: # for time
                    t = time.strftime("%H:%M:%S",time.gmtime(item[number]))
                    l.append(t)
                else: l.append(item[number])
        L += [l]
    write_to_csv(L,name)

def triplePM():
    D = {}
    for i1 in range(len(PLAYERS)):
        player1 = PLAYERS[i1]
        if i1 == len(PLAYERS) - 2:
            break
        for i2 in range(i1+1,len(PLAYERS)):
            player2 = PLAYERS[i2]
            for i3 in range(i2+1,len(PLAYERS)):
                player3 = PLAYERS[i3]
                bigL = [2*[0],11*[0],11*[0]]
                name = str([player1,player2,player3])
                for keys in bigDict:
                    lineup = chopNames(keys)
                    if player1 in lineup and player2 in lineup and player3 in lineup:
                        bigL = addList(bigL,bigDict[keys])
                D[name] = bigL
    np.save("triple.npy",D)
    return D