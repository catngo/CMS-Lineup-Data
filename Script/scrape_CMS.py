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

def write_to_csv( list_of_rows, filename ):
    """ write csv takes a list of list and write them out as csv files
    """
    try:
        csvfile = open( filename, "w", newline='' )
        filewriter = csv.writer( csvfile, delimiter=",")
        for row in list_of_rows:
            filewriter.writerow( row )
        csvfile.close()
    except:
        print("File", filename, "could not be opened for writing...")

def readcsv( csv_file_name ):
    """ readcsv takes as
         + input:  csv_file_name, the name of a csv file
        and returns
         + output: a list of lists, each inner list is one row of the csv
           all data items are strings; empty cells are empty strings
    """
    try:
        csvfile = open( csv_file_name, newline='' )  # open for reading
        csvrows = csv.reader( csvfile )              # creates a csvrows object

        all_rows = []                               # we need to read the csv file
        for row in csvrows:                         # into our own Python data structure
            all_rows.append( row )                  # adds only the word to our list

        del csvrows                                  # acknowledge csvrows is gone!
        csvfile.close()                              # and close the file
        return all_rows                              # return the list of lists

    except FileNotFoundError as e:
        print("File not found: ", e)
        return []

def gethtml(link):
    """ Get html file from link
    """
    html = requests.get(link)
    return html

url = ["http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20170224_bycd.xml?view=plays","http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20170225_ra6h.xml?view=plays","http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20170128_dl5k.xml?view=plays"]

def getPlays(url):
    """ Use an html to get all the plays from the string """
    html = gethtml(url)
    soup = BeautifulSoup(html.text,"lxml")
    L = [] #list of list of plays
    s = soup.select('tr.row')
    for tr in s:
        word = tr.text.split()
        L += [word]
    return L

#If CMS is away, first item is name, and last item is score. If home, first item is score, and last item is name.

#structure of dictionary: 
# d['line-up'] = [ 
# [minutes , plus-minus],[ points scored, 
# offensive possessions, turnovers, orebs, 
# opponent def reb, 2pt made, 2pt missed, 
# 3pt made, 3 pt missed, assists, 
# ft attempts],[ points given up, defensive possesions,
#  forced turnovers, orebs given up, team def reb,
#  2pt given up, 2pt missed of opp, 3pt given up, 
# 3 pt missed of op, assists given up, ft attempts given up] ]

# all of this applies to CMS playing at home

#team indicates if CMS is home ("h") or away ("a")

def checkCMS(play,lineup,team):
    """ check if play is CMS's. Team variable is whether CMS is home or away.
    """
    for player in lineup:
        if player in play:
            return True
    try: 
        score = int(play[1])
        if team == "h":
            return True
        else:
            return False
    except ValueError: 
        if team == "h":
            return False        
        else:
            return True

def timeDifference(t1,t2):
    """ Calculate how much minutes a lineup is in
    """
    fmt = "%M:%S"
    d1 = datetime.strptime(t1,fmt)
    d2 = datetime.strptime(t2,fmt)
    return (d1-d2).seconds

#play[0] will always be the time

Ignore = ["Block","Steal","Foul","TIMEOUT"] #we ignore Steals, because TOs reflect that already

def skip(play):
    """ Skip these plays because not important
    """
    for i in Ignore:
        if i in play:
            return True
    return False


#Team: CMS playing home or away

def checkAndOne(lineup,team,identity,L1):
    """ from a made field goal, check if and-one happened. Identity: CMS or not (Boolean value). L1: plays after the made field goal. True: if there is an and-one. False: if there isn't.
    """
    for i in range(len(L1)):
        if "Assist" in L1[i]: 
            if i == (len(L1)-1): return True
            else: continue
        if "Foul" in L1[i]:
            if checkCMS(L1[i],lineup,team) == identity:
                return False
            else:
                return True
        else:
            return False 


def checkPossession(L1,L2):
    """ from a free throw, decide if this free throw is an end of a possession, or even a possession at all. L1: plays before the free throws. L2: plays after the free throw.
    """
    for i in reversed(range(len(L1))):
        if "Technical" in L1[i]: #account for technical foul and timeouts
            return False
        elif "free" in L1[i]:
            continue
        else: break
    for i in range(len(L2)):
        if "enters" in L2[i] or "goes" in L2[i] or "TIMEOUT" in L2[i] or "deadball" in L2[i]:
            if i == (len(L2)-2):
                return True
            else: continue
        else:
            if "free" in L2[i]:
                return False
            else:
                return True
    

line = ["PRESIDENT,MILES","SCARLETT,MICHAEL","HALL,RILEY","LYNDS,SCOTT","MORRIS,KENDRICK"]#against PP on 2/24/17

#remember that offensive rebounds EXTEND a possesion, not add to it.

def analyze(L,starters,team): #made for CMS home game
    """ take in a list of plays and throw out the dictionaries of line-up. Team is whether CMS is "h" or "a" """
    d = {}
    d[str(sorted(starters))] = [2*[0],11*[0],11*[0]] #first list is minutes and plus minus. second list is offensive. third is defensive.
    index = 0
    op = 0
    dp = 0
    s = starters #keep this constant
    lineup = list(starters)
    randomshit = []
    changehalf = 0
    time = "20:00"
    while index < len(L):
        play = L[index]
        if sorted(lineup) == sorted(line):
            print(lineup)
            print(play)
            # print(d[str(sorted(lineup))])
            # print("\n")
        # if abs(op-dp) >= 2:
        #     randomshit += [[L[index-1],op,dp]]
        if index == 0:
            previousplay = "start"
        else: previousplay = L[index-1]
        try: nextplay = L[index+1]
        except IndexError:
            nextplay = "end"
        if play[0] > previousplay[0]: #change of half
            lineup = list(s)
            # print("SPECIAL")
            # print(play)
            if changehalf == 0:
                time = "20:00" #represent at start of half
            else:
                time = "5:00" #for OT
            changehalf += 1
        index += 1
        name = str(sorted(lineup)) #appropriate for dictionary
        if play[0] < nextplay[0]: #represent end of half and any number < e in Python
            timechange = "00:00"
            # print(play)
            # print(lineup)
            if len(lineup) == 5:
                d[name][0][0] += timeDifference(time,timechange)
        if skip(play): continue
        if "deadball" in play: #check for deadballs
            if "free" in previousplay: continue
            else:
                afterplays = L[index:]
                identity = checkCMS(previousplay,lineup,team)
                if nextplay[0] > play[0]: #change of half
                    if identity == 1: # of CMS
                        d[name][1][1] += 1
                    else:
                        d[name][2][1] += 1
                    continue
                for p in afterplays:
                    if "enters" in p or "goes" in p or "Foul" in p or "TIMEOUT" in p:
                        continue
                    else:
                        idNextPlay = checkCMS(p,lineup,team)
                        break
                if identity == idNextPlay:
                    continue
                else:
                    if identity == 1: #change from CMS to opp
                        d[name][1][1] += 1
                    else:
                        d[name][2][1] += 1
                    continue
        if checkCMS(play,lineup,team): #for CMS plays!
            if "made" in play:
                identity = checkCMS(play,lineup,team)
                i = play.index("made")
                if play[i+1] in ["layup","jump","tip-in","dunk"]: #2 pt
                    d[name][1][5] += 1 #changing 2 pt made
                    d[name][1][0] += 2 #changing points scored
                    d[name][0][1] += 2 #changing plus-minus
                elif play[i+1] == "3-pt.":
                    d[name][1][7] += 1 #changing 3 pt made
                    d[name][1][0] += 3 #changing points scored
                    d[name][0][1] += 3 #changing plus-minus
                elif "free" in play: #for free throw
                    d[name][1][10] += 1 #changing free throw attempt
                    d[name][1][0] += 1 #changing points scored
                    d[name][0][1] += 1 #changing plus-minus
                if nextplay == "end": #check for possession
                    d[name][1][1] += 1 
                    op += 1
                elif "free" in play:
                    if checkPossession(L[:index-1],L[index:]): #L[index] here is already next play
                            d[name][1][1] += 1
                else:
                    if checkAndOne(lineup,team,identity,L[index:]) == False:
                        d[name][1][1] += 1 
                        op += 1
            elif "missed" in play:
                i = play.index("missed")
                if "defensive" in nextplay: #possesion ends in an opp's defensive rebounds
                    d[name][1][1] += 1
                    op += 1
                    d[name][1][4] += 1 #update opp's defensive rebound
                if play[i+1] in ["layup","jump","tip-in","dunk"]: #2 pt
                    d[name][1][6] += 1 #changing 2 pt missed
                elif play[i+1] == "3-pt.":
                    d[name][1][8] += 1 #changing 3 pt missed
                elif "free" in play: #for free throw
                    d[name][1][10] += 1 #changing free throw attempt
            elif "Assist"  in play:
                d[name][1][9] += 1
            elif "Turnover" in play:
                d[name][1][1] += 1 #update offensive possession
                op += 1
                d[name][1][2] += 1 #update turnover
            elif "offensive" in play:
                d[name][1][3] += 1 #update offensive rebound 
            elif "defensive" in play:
                if "Block" in previousplay: #check for blocks for the previous plays and we already cover this case of defensive rebound off opp's miss shots under opp's missed shot
                    d[name][2][4] += 1
                    d[name][2][1] += 1
                    dp += 1
            elif "enters" in play:
                timechange = play[0]
                if len(lineup) == 5 and name in d:
                    d[name][0][0] += timeDifference(time,timechange) #mark how many minutes the lineup played together
                time = timechange
                i = play.index("enters")
                player = play[i-1]
                lineup.append(player)
                # print("JUST ADD. AND LINEUP IS:",lineup,"\n")
            elif "goes" in play:
                i = play.index("goes")
                player = play[i-1]
                print(play)
                print(player)
                print(lineup)
                lineup.remove(player)
                # print(lineup)
                # print("\n")
                if checkCMS(nextplay,lineup,team):
                    if "goes" not in nextplay and "enters" not in nextplay and str(sorted(lineup)) not in d and len(lineup) == 5:
                        d[str(sorted(lineup))] = [2*[0],11*[0],11*[0]]
                else:
                    if str(sorted(lineup)) not in d and len(lineup) == 5:
                        d[str(sorted(lineup))] = [2*[0],11*[0],11*[0]]
                if nextplay == "end" and len(lineup) == 5: #end of game
                    timechange = "00:00"
                    d[str(sorted(lineup))][0][0] += timeDifference(time,timechange)
            else: randomshit += [play]
        else: # for non-CMS plays!
            if "enters" in play or "goes" in play:
                continue
            elif "made" in play:
                i = play.index("made")
                identity = checkCMS(play,lineup,team)
                if play[i+1] in ["layup","jump","tip-in","dunk"]: #2 pt
                    d[name][2][5] += 1 #changing 2 pt given up
                    d[name][2][0] += 2 #changing points given up
                    d[name][0][1] -= 2 #changing plus-minus
                elif play[i+1] == "3-pt.":
                    d[name][2][7] += 1 #changing 3 pt made
                    d[name][2][0] += 3 #changing points given
                    d[name][0][1] -= 3 #changing plus-minus
                elif "free" in play: #for free throw
                    d[name][2][10] += 1 #changing free throw attempt
                    d[name][2][0] += 1 #changing points given up
                    d[name][0][1] -= 1 #changing plus-minus
                if nextplay == "end":
                    d[name][2][1] += 1 
                    dp += 1
                elif "free" in play:
                    if checkPossession(L[:index-1],L[index:]):
                        d[name][2][1] += 1 
                        dp += 1
                else:
                    if checkAndOne(lineup,team,identity,L[index:]) == False:
                        d[name][2][1] += 1 
                        dp += 1
            elif "missed" in play:
                i = play.index("missed")
                if "defensive" in nextplay: #possesion ends in an CMS defensive rebounds
                    d[name][2][1] += 1
                    dp += 1
                    d[name][2][4] += 1
                if play[i+1] in ["layup","jump","tip-in","dunk"]: #2 pt
                    d[name][2][6] += 1 #changing 2 pt missed
                elif play[i+1] == "3-pt.":
                    d[name][2][8] += 1 #changing 3 pt missed
                elif "free" in play: #for free throw
                    d[name][2][10] += 1 #changing free throw attempt
            elif "Assist"  in play:
                d[name][2][9] += 1
            elif "Turnover" in play:
                d[name][2][1] += 1 #update defensive possession
                dp += 1
                d[name][2][2] += 1 #update turnover forced
            elif "offensive" in play:
                d[name][2][3] += 1 #update opp's offensive rebound 
            elif "defensive" in play:
                if "Block" in previousplay: #check for blocks for the previous plays
                    d[name][1][4] += 1 #update defensive rebound
                    d[name][1][1] += 1
                    op += 1
            else:
                randomshit += [play]
    return d,randomshit



def calcPoss(fga,fta,orb,to):
    return fga+0.475*fta-orb+to

def checkStats(d):
    seconds = 0; pm = 0; pts = 0; offposs = 0; defrebgiven = 0; tos = 0 ;offreb = 0; two = 0; twoattempt = 0; three = 0; threeattempt = 0; assists = 0;FTA = 0 ; ptsgiven = 0;defposs = 0;tosforced = 0;offrebgiven = 0 ;defreb = 0; twogiven = 0; twoattemptgiven = 0;threegiven = 0;threeattemptgiven = 0; assistsgiven = 0;FTAgiven = 0
    for key in d:
        seconds += d[key][0][0]
        pm += d[key][0][1]
        pts += d[key][1][0]
        offposs += d[key][1][1]
        tos += d[key][1][2]
        offreb += d[key][1][3]
        defrebgiven += d[key][1][4]
        two += d[key][1][5]
        twoattempt += (d[key][1][5] + d[key][1][6])
        three += d[key][1][7]
        threeattempt += (d[key][1][8] + d[key][1][7])
        assists += d[key][1][9]
        FTA += d[key] [1][10]
        ptsgiven += d[key][2][0]
        defposs += d[key][2][1]
        tosforced += d[key][2][2]
        offrebgiven += d[key][2][3] 
        defreb += d[key][2][4]
        twogiven += d[key][2][5]
        twoattemptgiven += (d[key][2][5]+d[key][2][6])
        threegiven += d[key][2][7]
        threeattemptgiven += (d[key][2][7]+d[key][2][8])
        assistsgiven += d[key][2][9]
        FTAgiven += d[key][2][10]
    L = ["seconds","pm","pts","offposs","defrebgiven","tos","offreb","two","twoattempt","three","threeattempt","assists","FTA","ptsgiven","defposs","tosforced","offrebgiven","defreb","twogiven","twoattemptgiven","threegiven","threeattemptgiven","assistsgiven","FTAgiven"]
    S = [seconds,pm,pts, offposs,defrebgiven,tos,offreb,two, twoattempt,three,threeattempt,assists,FTA,ptsgiven,defposs,tosforced,offrebgiven,defreb,twogiven,twoattemptgiven,threegiven,threeattemptgiven,assistsgiven,FTAgiven]
    for i in range(len(L)):
        print(L[i]+":",S[i])
    ExpOPoss = calcPoss(twoattempt+threeattempt,FTA,offreb,tos)
    ExpDPoss = calcPoss(twoattemptgiven+threeattemptgiven,FTAgiven,offrebgiven,tosforced)
    print("Expected Offensive Possession:",ExpOPoss)
    print("Expected Defensive Possession:",ExpDPoss)

def dictcsv(d,name):
    """ from a dictionary of lineups, put out a csv file
    """
    L = [heading]
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

def combinedict(d1,d2):
    """ Combined two dictionaries to get
    """
    d = {}
    for key in d1:
        d[key] = d1[key]
        if key in d2:
            for entry in range(len(d[key])):
                for number in range(len(d[key][entry])):
                    d[key][entry][number] += d2[key][entry][number]
    for key in d2:
        if key not in d1:
            d[key] = d2[key]
    return d

def chopNames(string):
    """ from a string of 5 players to list of strings"""
    L = []
    string = string[1:-1] #get rid of square brackets
    name = ""
    comma = 0
    for index in range(len(string)):
        letter = string[index]
        if letter == " " or letter == "'":
            if index == len(string) - 1:#last letter
                L += [name]
            else: continue
        if letter != ",":
            name += letter
        else:
            if comma % 2 == 0: #every second comma
                name += letter
            else:
                L += [name]
                name = ""
            comma += 1
    return L


def write(url,starters,team):
    """ From a url to a csv file
    """
    P = getPlays(url)
    d,L = analyze(P,starters,team)
    od = collections.OrderedDict(sorted(d.items()))
    name = url[62:64]+"-"+url[64:66]+"-"+url[58:62] +".csv"#just the name
    dictcsv(od,name)
    return d,L

class address:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

# Davis sub out Lynds on 2/4 (index 8) for HOME URLs. 1/28 (index 7) for Away URLs.
# Ely sub out Davis on 2/18 (index 12) for home URLs. 2/20 (index 10) for Away URLs.

def scrapeHome():
    """ Scrape up all home games
    """
    BigList = []
    with address("/Users/CatNgo/Dropbox/CMS/Home"):
        for i in range(len(Home_URLs)):
            if i < 8:
                starters = STARTERS[0]
            elif 8 <= i < 12:
                starters = STARTERS[1]
            else:
                starters = STARTERS[2]
            if i == 0:
                d,L = write(Home_URLs[i],starters,"h")
            else:
                d1,L = write(Home_URLs[i],starters,"h")
                d = combinedict(d,d1)
            print("Done with home game",i)
            BigList += [L]
        od = collections.OrderedDict(sorted(d.items()))
        np.save('AllHome.npy',od)
        dictcsv(od,"AllHome.csv")
    return BigList

badPlays = ["01-28-2017.npy"]

def scrapeAway(start):
    """ Scrape all away games
    """
    BigList = []
    with address("/Users/CatNgo/Dropbox/CMS/Away"):
        for i in range(start,len(Away_URLs)):
            if i < 7:
                starters = STARTERS[0]
            elif 7 <= i < 10:
                starters = STARTERS[1]
            else:
                starters = STARTERS[2]
            if i == start:
                try:
                    d,L = write(Away_URLs[i],starters,"a")
                except:
                    print("Something's wrong with Away game",i)
                    d = {}
                    L = []
            else:
                try:
                    d1,L = write(Away_URLs[i],starters,"a")
                    d = combinedict(d,d1)
                except:
                    print("Something's wrong with Away game",i)
                    d1 = {}
                    d = combinedict(d,d1)
                    L = []
            
            print("Done with away game",i)
            BigList += [L]
        for dict in badPlays:
            D = np.load(dict).item()
            d = combinedict(d,D)
        od = collections.OrderedDict(sorted(d.items()))
        np.save('AllAway.npy',od)
        dictcsv(od,"AllAway.csv")
    return L

def writeSHIT(d,name):
    """ from broken play by play to dictionary and csv, also update AllAway.npy
    """
    with address("/Users/CatNgo/Dropbox/CMS/Away"):
        dictcsv(d,name+".csv")
        np.save(name,d)
        bigDict = np.load('AllAway.npy').item()
        bigDict = combinedict(bigDict,d)
        np.save('AllAway.npy',bigDict)
        dictcsv(bigDict,'AllAway.csv')

def updateCombined():
    with address("/Users/CatNgo/Dropbox/CMS/Away"):
        dictaway = np.load('AllAway.npy').item()
    with address("/Users/CatNgo/Dropbox/CMS/Home"):
        dicthome = np.load('AllHome.npy').item()
    d = combinedict(dictaway,dicthome)
    np.save("Combined.npy",d)
    dictcsv(d,"Combined.csv")

#For away games, game 0,1,3,6,7 are broken. Game 0 cannot be fixed. Game 3, 6 and 7 are fixed. (Game 1 is not necessary anymore, because we're scraping from December till end of season`)