import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import urllib2
import csv

dbbdteams = ['ari', 'atl', 'bal', 'bos', 'chc', 'chw', 'cle', 'cin', 'col', 'det', 'hou',
             'kc','laa', 'lad', 'mia', 'mil', 'min', 'nym', 'nyy', 'oak', 'phi',
             'pit', 'stl', 'sd', 'sf', 'sea', 'tb', 'tex', 'tor', 'wsh']

brefteams = ['ARI', 'ATL', 'BAL', 'BOS', 'CHC', 'CHW', 'CLE', 'CIN', 'COL', 'DET', 'HOU',
             'KCR', 'LAA', 'LAD', 'MIA', 'MIL', 'MIN', 'NYM', 'NYY', 'OAK', 'PHI',
             'PIT', 'STL', 'SDP', 'SFG', 'SEA', 'TBR', 'TEX', 'TOR', 'WSN']

url="http://dailybaseballdata.com/cgi-bin/dailyhit.pl"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read())
soup = str(soup)

todaysmatchup = pd.read_csv('C:/Users/Shanshan/Desktop/gettodaysmatchups/todaytemplate.csv', na_values=[' '], header=False)
todaysmatchup = np.array(todaysmatchup)

k = 1

for c in range(0, 30):
    tempindex = soup.find('('+dbbdteams[c]+')')
    if tempindex!= -1:
        if dbbdteams[c] == 'kc' or dbbdteams[c] == 'sd' or dbbdteams[c] == 'sf' or dbbdteams[c] == 'tb':
            if soup[tempindex+18] == ' ':
                tempstring = soup[tempindex-40: tempindex+22]
            else:
                tempstring = soup[tempindex-40: tempindex+23]
        else:
            if soup[tempindex+19] == ' ':
                tempstring = soup[tempindex-40: tempindex+23]
            else:
                tempstring = soup[tempindex-40: tempindex+24]
    
        if tempstring[-3:-1] == 'kc' or tempstring[-3:-1] == 'sd' or tempstring[-3:-1] == 'sf' or tempstring[-3:-1] == 'tb':
            tempopp = tempstring[-3:-1]
        else:
            tempopp = tempstring[-3:]

        oppindex = dbbdteams.index(tempopp)
        s = tempstring.find('blank')
        t = tempstring.find(dbbdteams[c])

        opppitcherindex = soup.find('('+tempopp+')')
        opppitcherstring = soup[opppitcherindex-36: opppitcherindex+23]
        sopp = opppitcherstring.find('blank')
        topp = opppitcherstring.find(tempopp)
        
        todaysmatchup[k, 0] = brefteams[c]
        todaysmatchup[k, 1] = tempstring[s+7: t-6]
        todaysmatchup[k, 2] = brefteams[oppindex]
        todaysmatchup[k, 3] = opppitcherstring[sopp+7: topp-6]    
    
        k = k+1

b = open("C:/Users/Shanshan/Desktop/gettodaysmatchups/today.csv", 'wb')
a = csv.writer(b)
a.writerows(todaysmatchup)
b.close()

