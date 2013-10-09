# The global variables are used purely for the front end; I can eliminate them
# once I figure out how to work with jQuery's Ajax methods.

from flask import Flask, render_template, flash, redirect, request
from app import app
from forms import InputForm, IndividualForm
import readline, rlcompleter
import pandas as pd
import numpy as np
import urllib2
import datetime
import os

def bclusterlookup(lbattername): 
    bclusterdf = pd.read_csv('listofbatterswithclusters.csv', na_values=[' '])
    ser = (bclusterdf['bname']==lbattername)
    if ser.any():   
        return int(bclusterdf.ix[ser,'bcluster'])
    else:
        return 0

def pclusterlookup(lpitchername):
    pclusterdf = pd.read_csv('listofpitcherswithclusters.csv', na_values=[' '])
    ser = (pclusterdf['pname']==lpitchername)
    if ser.any():   
        return int(pclusterdf.ix[ser,'pcluster'])
    else:
        return 0

def getrating(bcluster, pcluster):
    if bcluster !=0 and pcluster!=0:
        ratingdf = pd.read_csv('scaledopspr.csv', na_values=[' '])
        ratingdfarray = np.array(ratingdf)
        rating = ratingdfarray[bcluster-1, pcluster-1]
        return int(rating * 100)
    else:
        return 0

def todaypitcherlookup(somebatter):
    bclusterdf = pd.read_csv('listofbatterswithclusters.csv', na_values=[' '])
    ser = (bclusterdf['bname']==somebatter)
    if ser.any():
        battingteam = str(bclusterdf.ix[ser, 'Team'])
        battingteam = battingteam[battingteam.find(' ')+4:battingteam.find('Name')-1]
    else:
        return 'Batter not found'
    
    today = pd.read_csv('today.csv', na_values=[' '])
    sertwo = (today['Team']==battingteam)
    if sertwo.any():
        opposingpitcher = str(today.ix[sertwo, 'OtherStarter'])
        opposingpitcher = opposingpitcher[opposingpitcher.find(' ')+4:opposingpitcher.find('Name')-1]
        return opposingpitcher
    else:
        return 'No game today'

def getratingslist(somelist, somenumber):
    ratingslist = []
    for c in range(somenumber):
        bcluster = bclusterlookup(somelist[c])
        pcluster = pclusterlookup(todaypitcherlookup(somelist[c]))
        ratingslist.append(getrating(bcluster, pcluster))
    return ratingslist

def returnbestone(ratingslist, somenumber):
    maxrating = 0
    maxindex = 0
    for c in range(somenumber):
        if ratingslist[c]>maxrating:
            maxrating=ratingslist[c]
            maxindex=c
    return maxindex

def returnbestthree(ratingslist, somenumber):
    threedict = {}
    threelist = []
    for c in range(somenumber):
        threedict[c]=ratingslist[c]
    sorted_list = [(k,v) for v,k in sorted([(v,k) for k,v in threedict.items()])]  
    threelist = [x[0] for x in sorted_list]
    return threelist[somenumber-1], threelist[somenumber-2], threelist[somenumber-3]

def returnbesttwo(listoftherest):
    twodict = {}
    somenumber = len(listoftherest)
    for c in range(somenumber):
        twodict[c]=listoftherest[c]
    sorted_list = [(k,v) for v,k in sorted([(v,k) for k,v in twodict.items()])]  
    twolist = [x[0] for x in sorted_list]
    return twolist[somenumber-1], twolist[somenumber-2], twolist

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    if os.path.exists('tempstore.txt'):
        os.remove("tempstore.txt")
    form = IndividualForm()
    global batternameone
    global pitchernameone
    if form.validate_on_submit():
        batternameone=form.battername.data
        pitchernameone=form.pitchername.data
        return redirect('/matchup1')
    return render_template('index.html', form = form)

@app.route('/matchup1', methods = ['GET', 'POST'])
def matchup1():
    form = IndividualForm()
    bcluster = bclusterlookup(batternameone)
    pcluster = pclusterlookup(pitchernameone)
    global favratingone
    favratingone = getrating(bcluster, pcluster)

    global zeroone
    zeroone = 0
    global oneone
    oneone = 0
    global twoone
    twoone = 0
    global threeone
    threeone = 0
    global fourone
    fourone = 0
    global fiveone
    fiveone = 0
    global sixone
    sixone = 0
    global sevenone
    sevenone = 0
    global eightone
    eightone = 0
    global nineone
    nineone = 0
    global tenone
    tenone = 0
    if favratingone< 5:
        zeroone = 1
    elif favratingone < 15:
        oneone = 1
    elif favratingone< 25:
        twoone = 1
    elif favratingone< 35:
        threeone = 1
    elif favratingone < 45:
        fourone = 1
    elif favratingone< 55:
        fiveone = 1
    elif favratingone < 65:
        sixone = 1
    elif favratingone < 75:
        sevenone = 1
    elif favratingone< 85:
        eightone = 1
    elif favratingone< 95:
        nineone = 1
    else:
        tenone = 1

    walks = pd.read_csv('walks.csv', na_values=[' '], header=None)
    hits = pd.read_csv('hits.csv', na_values=[' '], header=None)
    hrs = pd.read_csv('hrs.csv', na_values=[' '], header=None)
    plateapps = pd.read_csv('plateapps.csv', na_values=[' '], header=None)
    walks = np.array(walks)
    hits = np.array(hits)
    hrs = np.array(hrs)
    plateapps = np.array(plateapps)
    if plateapps[bcluster-1, pcluster-1] == 0:
        plateapps[bcluster-1, pcluster-1] = 1
    awalkf = walks[bcluster-1, pcluster-1]/plateapps[bcluster-1, pcluster-1] * 100
    global awalkone
    if bcluster == 0 or pcluster == 0:
        awalkone = 0
    else:
        awalkone = int(awalkf)
    ahrf = hrs[bcluster-1, pcluster-1]/plateapps[bcluster-1, pcluster-1] * 100
    global ahrone
    if bcluster == 0 or pcluster == 0:
        ahrone = 0
    else:
        ahrone = int(ahrf)
    ahitf = hits[bcluster-1, pcluster-1]/plateapps[bcluster-1, pcluster-1] * 100
    global ahitone
    if bcluster == 0 or pcluster == 0:
        ahitone = 0
    else:
        ahitone = int(ahitf)

    global batternametwo
    global pitchernametwo
    if form.validate_on_submit():
        batternametwo=form.battername.data
        pitchernametwo=form.pitchername.data
        return redirect('/matchup2')    
    return render_template('matchup1.html', zeroone = zeroone, oneone = oneone, twoone = twoone, threeone = threeone, fourone = fourone,
                           fiveone = fiveone, sixone = sixone, sevenone = sevenone, eightone = eightone, nineone = nineone, tenone = tenone,
                           batternameone = batternameone, pitchernameone = pitchernameone,
                           favratingone = favratingone, awalkone = awalkone, ahitone = ahitone, ahrone = ahrone, form = form)

@app.route('/matchup2', methods = ['GET', 'POST'])
def matchup2():
    xoneed = 1
    if os.path.exists('tempstore.txt'):
        with open('tempstore.txt', 'r') as f:
            read_data = f.read()
            f.closed
        read_data = list(read_data)
        if '1' in read_data:
            xoneed = 0
        
    form = IndividualForm()
    bcluster = bclusterlookup(batternametwo)
    pcluster = pclusterlookup(pitchernametwo)
    global favratingtwo
    favratingtwo = getrating(bcluster, pcluster)

    global zerotwo
    zerotwo = 0
    global onetwo
    onetwo = 0
    global twotwo
    twotwo = 0
    global threetwo
    threetwo = 0
    global fourtwo
    fourtwo = 0
    global fivetwo
    fivetwo = 0
    global sixtwo
    sixtwo = 0
    global seventwo
    seventwo = 0
    global eighttwo
    eighttwo = 0
    global ninetwo
    ninetwo = 0
    global tentwo
    tentwo = 0
    if favratingtwo< 5:
        zerotwo = 1
    elif favratingtwo < 15:
        onetwo = 1
    elif favratingtwo< 25:
        twotwo = 1
    elif favratingtwo< 35:
        threetwo = 1
    elif favratingtwo < 45:
        fourtwo = 1
    elif favratingtwo< 55:
        fivetwo = 1
    elif favratingtwo < 65:
        sixtwo = 1
    elif favratingtwo < 75:
        seventwo = 1
    elif favratingtwo< 85:
        eighttwo = 1
    elif favratingtwo< 95:
        ninetwo = 1
    else:
        tentwo = 1

    walks = pd.read_csv('walks.csv', na_values=[' '], header=None)
    hits = pd.read_csv('hits.csv', na_values=[' '], header=None)
    hrs = pd.read_csv('hrs.csv', na_values=[' '], header=None)
    plateapps = pd.read_csv('plateapps.csv', na_values=[' '], header=None)
    walks = np.array(walks)
    hits = np.array(hits)
    hrs = np.array(hrs)
    plateapps = np.array(plateapps)
    if plateapps[bcluster-1, pcluster-1] == 0:
        plateapps[bcluster-1, pcluster-1] = 1
    awalkf = walks[bcluster-1, pcluster-1]/plateapps[bcluster-1, pcluster-1] * 100
    global awalktwo
    if bcluster == 0 or pcluster == 0:
        awalktwo = 0
    else:
        awalktwo = int(awalkf)
    ahrf = hrs[bcluster-1, pcluster-1]/plateapps[bcluster-1, pcluster-1] * 100
    global ahrtwo
    if bcluster == 0 or pcluster == 0 :
        ahrtwo = 0
    else:
        ahrtwo = int(ahrf)
    ahitf = hits[bcluster-1, pcluster-1]/plateapps[bcluster-1, pcluster-1] * 100
    global ahittwo
    if bcluster == 0 or pcluster == 0:
        ahittwo = 0
    else:
        ahittwo = int(ahitf)

    global batternamethree
    global pitchernamethree
    if form.validate_on_submit():
        batternamethree=form.battername.data
        pitchernamethree=form.pitchername.data
        return redirect('/matchup3')
    return render_template('matchup2.html', zeroone = zeroone, oneone = oneone, twoone = twoone, threeone = threeone, fourone = fourone,
                           fiveone = fiveone, sixone = sixone, sevenone = sevenone, eightone = eightone, nineone = nineone, tenone = tenone,
                           batternameone = batternameone, pitchernameone = pitchernameone,
                           favratingone = favratingone, awalkone = awalkone, ahitone = ahitone, ahrone = ahrone,
                           zerotwo = zerotwo, onetwo = onetwo, twotwo = twotwo, threetwo = threetwo, fourtwo = fourtwo,
                           fivetwo = fivetwo, sixtwo = sixtwo, seventwo = seventwo, eighttwo = eighttwo, ninetwo = ninetwo, tentwo = tentwo,
                           batternametwo = batternametwo, pitchernametwo = pitchernametwo,
                           favratingtwo = favratingtwo, awalktwo = awalktwo, ahittwo = ahittwo, ahrtwo = ahrtwo,
                           xoneed = xoneed, form = form)

@app.route('/matchup3', methods = ['GET', 'POST'])
def matchup3():
    xoneed = 1
    xtwoed = 1
    if os.path.exists('tempstore.txt'):
        with open('tempstore.txt', 'r') as f:
            read_data = f.read()
            f.closed
        read_data = list(read_data)
        if '1' in read_data:
            xoneed = 0
        if '2' in read_data:
            xtwoed = 0
    
    form = IndividualForm()
    bcluster = bclusterlookup(batternamethree)
    pcluster = pclusterlookup(pitchernamethree)

    global favratingthree
    favratingthree = getrating(bcluster, pcluster)

    global zerothree
    zerothree = 0
    global onethree
    onethree = 0
    global twothree
    twothree = 0
    global threethree
    threethree = 0
    global fourthree
    fourthree = 0
    global fivethree
    fivethree = 0
    global sixthree
    sixthree = 0
    global seventhree
    seventhree = 0
    global eightthree
    eightthree = 0
    global ninethree
    ninethree = 0
    global tenthree
    tenthree = 0
    if favratingthree< 5:
        zerothree = 1
    elif favratingthree < 15:
        onethree = 1
    elif favratingthree< 25:
        twothree = 1
    elif favratingthree< 35:
        threethree = 1
    elif favratingthree < 45:
        fourthree = 1
    elif favratingthree< 55:
        fivethree = 1
    elif favratingthree < 65:
        sixthree = 1
    elif favratingthree < 75:
        seventhree = 1
    elif favratingthree< 85:
        eightthree = 1
    elif favratingthree< 95:
        ninethree = 1
    else:
        tenthree = 1

    walks = pd.read_csv('walks.csv', na_values=[' '], header=None)
    hits = pd.read_csv('hits.csv', na_values=[' '], header=None)
    hrs = pd.read_csv('hrs.csv', na_values=[' '], header=None)
    plateapps = pd.read_csv('plateapps.csv', na_values=[' '], header=None)
    walks = np.array(walks)
    hits = np.array(hits)
    hrs = np.array(hrs)
    plateapps = np.array(plateapps)
    if plateapps[bcluster-1, pcluster-1] == 0:
        plateapps[bcluster-1, pcluster-1] = 1
    awalkf = walks[bcluster-1, pcluster-1]/plateapps[bcluster-1, pcluster-1] * 100
    global awalkthree
    if bcluster == 0 or pcluster == 0:
        awalkthree = 0
    else:
        awalkthree = int(awalkf)
    ahrf = hrs[bcluster-1, pcluster-1]/plateapps[bcluster-1, pcluster-1] * 100
    global ahrthree
    if bcluster == 0 or pcluster == 0:
        ahrthree = 0
    else:
        ahrthree = int(ahrf)
    ahitf = hits[bcluster-1, pcluster-1]/plateapps[bcluster-1, pcluster-1] * 100
    global ahitthree
    if bcluster == 0 or pcluster == 0:
        ahitthree = 0
    else:
        ahitthree = int(ahitf)

    global batternamefour
    global pitchernamefour
    if form.validate_on_submit():
        batternamefour=form.battername.data
        pitchernamefour=form.pitchername.data
        return redirect('/matchup4')

    return render_template('matchup3.html', zeroone = zeroone, oneone = oneone, twoone = twoone, threeone = threeone, fourone = fourone,
                           fiveone = fiveone, sixone = sixone, sevenone = sevenone, eightone = eightone, nineone = nineone, tenone = tenone,
                           batternameone = batternameone, pitchernameone = pitchernameone,
                           favratingone = favratingone, awalkone = awalkone, ahitone = ahitone, ahrone = ahrone,
                           zerotwo = zerotwo, onetwo = onetwo, twotwo = twotwo, threetwo = threetwo, fourtwo = fourtwo,
                           fivetwo = fivetwo, sixtwo = sixtwo, seventwo = seventwo, eighttwo = eighttwo, ninetwo = ninetwo, tentwo = tentwo,
                           batternametwo = batternametwo, pitchernametwo = pitchernametwo,
                           favratingtwo = favratingtwo, awalktwo = awalktwo, ahittwo = ahittwo, ahrtwo = ahrtwo,
                           zerothree = zerothree, onethree = onethree, twothree = twothree, threethree = threethree, fourthree = fourthree,
                           fivethree = fivethree, sixthree = sixthree, seventhree = seventhree, eightthree = eightthree, ninethree = ninethree, tenthree = tenthree,
                           batternamethree = batternamethree, pitchernamethree = pitchernamethree,
                           favratingthree = favratingthree, awalkthree = awalkthree, ahitthree = ahitthree, ahrthree = ahrthree,
                           xoneed = xoneed, xtwoed = xtwoed, form = form)

@app.route('/matchup4', methods = ['GET', 'POST'])
def matchup4():
    xoneed = 1
    xtwoed = 1
    xthreeed = 1
    if os.path.exists('tempstore.txt'):
        with open('tempstore.txt', 'r') as f:
            read_data = f.read()
            f.closed
        read_data = list(read_data)
        if '1' in read_data:
            xoneed = 0
        if '2' in read_data:
            xtwoed = 0
        if '3' in read_data:
            xthreeed = 0
    
    form = IndividualForm()
    bcluster = bclusterlookup(batternamefour)
    pcluster = pclusterlookup(pitchernamefour)
    global favratingfour
    favratingfour = getrating(bcluster, pcluster)

    global zerofour
    zerofour = 0
    global onefour
    onefour = 0
    global twofour
    twofour = 0
    global threefour
    threefour = 0
    global fourfour
    fourfour = 0
    global fivefour
    fivefour = 0
    global sixfour
    sixfour = 0
    global sevenfour
    sevenfour = 0
    global eightfour
    eightfour = 0
    global ninefour
    ninefour = 0
    global tenfour
    tenfour = 0
    if favratingfour< 5:
        zerofour = 1
    elif favratingfour < 15:
        onefour = 1
    elif favratingfour< 25:
        twofour = 1
    elif favratingfour< 35:
        threefour = 1
    elif favratingfour < 45:
        fourfour = 1
    elif favratingfour< 55:
        fivefour = 1
    elif favratingfour < 65:
        sixfour = 1
    elif favratingfour < 75:
        sevenfour = 1
    elif favratingfour< 85:
        eightfour = 1
    elif favratingfour< 95:
        ninefour = 1
    else:
        tenfour = 1

    walks = pd.read_csv('walks.csv', na_values=[' '], header=None)
    hits = pd.read_csv('hits.csv', na_values=[' '], header=None)
    hrs = pd.read_csv('hrs.csv', na_values=[' '], header=None)
    plateapps = pd.read_csv('plateapps.csv', na_values=[' '], header=None)
    walks = np.array(walks)
    hits = np.array(hits)
    hrs = np.array(hrs)
    plateapps = np.array(plateapps)
    if plateapps[bcluster-1, pcluster-1] == 0:
        plateapps[bcluster-1, pcluster-1] = 1
    awalkf = walks[bcluster-1, pcluster-1]/plateapps[bcluster-1, pcluster-1] * 100
    global awalkfour
    if bcluster == 0 or pcluster == 0:
        awalkfour = 0
    else:
        awalkfour = int(awalkf)
    ahrf = hrs[bcluster-1, pcluster-1]/plateapps[bcluster-1, pcluster-1] * 100
    global ahrfour
    if bcluster == 0 or pcluster == 0:
        ahrfour = 0
    else:
        ahrfour = int(ahrf)
    ahitf = hits[bcluster-1, pcluster-1]/plateapps[bcluster-1, pcluster-1] * 100
    global ahitfour
    if bcluster == 0 or pcluster == 0:
        ahitfour = 0
    else:
        ahitfour = int(ahitf)

    if form.validate_on_submit():
        return redirect('/index')

    return render_template('matchup4.html', zeroone = zeroone, oneone = oneone, twoone = twoone, threeone = threeone, fourone = fourone,
                           fiveone = fiveone, sixone = sixone, sevenone = sevenone, eightone = eightone, nineone = nineone, tenone = tenone,
                           batternameone = batternameone, pitchernameone = pitchernameone,
                           favratingone = favratingone, awalkone = awalkone, ahitone = ahitone, ahrone = ahrone,
                           zerotwo = zerotwo, onetwo = onetwo, twotwo = twotwo, threetwo = threetwo, fourtwo = fourtwo,
                           fivetwo = fivetwo, sixtwo = sixtwo, seventwo = seventwo, eighttwo = eighttwo, ninetwo = ninetwo, tentwo = tentwo,
                           batternametwo = batternametwo, pitchernametwo = pitchernametwo,
                           favratingtwo = favratingtwo, awalktwo = awalktwo, ahittwo = ahittwo, ahrtwo = ahrtwo,
                           zerothree = zerothree, onethree = onethree, twothree = twothree, threethree = threethree, fourthree = fourthree,
                           fivethree = fivethree, sixthree = sixthree, seventhree = seventhree, eightthree = eightthree, ninethree = ninethree, tenthree = tenthree,
                           batternamethree = batternamethree, pitchernamethree = pitchernamethree,
                           favratingthree = favratingthree, awalkthree = awalkthree, ahitthree = ahitthree, ahrthree = ahrthree,
                           zerofour = zerofour, onefour = onefour, twofour = twofour, threefour = threefour, fourfour = fourfour,
                           fivefour = fivefour, sixfour = sixfour, sevenfour = sevenfour, eightfour = eightfour, ninefour = ninefour, tenfour = tenfour,
                           batternamefour = batternamefour, pitchernamefour = pitchernamefour,
                           favratingfour = favratingfour, awalkfour = awalkfour, ahitfour = ahitfour, ahrfour = ahrfour,
                           xoneed = xoneed, xtwoed = xtwoed, xthreeed = xthreeed, form = form)

@app.route('/kittensone', methods = ['GET', 'POST'])
def kittensone():
	text_file = open("tempstore.txt", "a")
        text_file.write("1")
        text_file.close()
        return 'some response'

@app.route('/kittenstwo', methods = ['GET', 'POST'])
def kittenstwo():
	text_file = open("tempstore.txt", "a")
        text_file.write("2")
        text_file.close()
        return 'some response'

@app.route('/kittensthree', methods = ['GET', 'POST'])
def kittensthree():
	text_file = open("tempstore.txt", "a")
        text_file.write("3")
        text_file.close()
        return 'some response'

@app.route('/team', methods = ['GET', 'POST'])
def team():
    form = InputForm()
    global catcher
    catcher = 'empty'
    global firstb
    firstb = 'empty'
    global secondb
    secondb = 'empty'
    global thirdb
    thirdb = 'empty'
    global ss
    ss = 'empty'
    global outfieldone
    outfieldone = 'empty'
    global outfieldtwo
    outfieldtwo = 'empty'
    global outfieldthree
    outfieldthree = 'empty'
    global utilone
    utilone = 'empty'
    global utiltwo
    utiltwo = 'empty'
    global benchone
    benchone = 'empty'
    global benchtwo
    benchtwo = 'empty'
    global benchthree
    benchthree = 'empty'

    listofcatchers = []
    listoffbasemen = []
    listofsbasemen = []
    listofss = []
    listoftbasemen = []
    listofoutfielders = []
    if form.validate_on_submit():
        stringofcatchers = form.catchernames.data
        numberofcatchers = stringofcatchers.count(',')+1
        listofcatchers = stringofcatchers.split(', ')
        try:
            catchersratingslist = getratingslist(listofcatchers, numberofcatchers)
        except:
            return redirect('/inputerror')
        catchersmaxindex = returnbestone(catchersratingslist, numberofcatchers)
        catcher = listofcatchers[catchersmaxindex]
        
        stringoffbasemen = form.firstbnames.data
        numberoffbasemen = stringoffbasemen.count(',')+1
        listoffbasemen = stringoffbasemen.split(', ')
        try:
            fbasemenratingslist = getratingslist(listoffbasemen, numberoffbasemen)
        except:
            return redirect('/inputerror')
        fbasemenmaxindex = returnbestone(fbasemenratingslist, numberoffbasemen)
        firstb = listoffbasemen[fbasemenmaxindex]
        
        stringofsbasemen = form.secondbnames.data
        numberofsbasemen = stringofsbasemen.count(',')+1
        listofsbasemen = stringofsbasemen.split(', ')
        try:
            sbasemenratingslist = getratingslist(listofsbasemen, numberofsbasemen)
        except:
            return redirect('/inputerror')
        sbasemenmaxindex = returnbestone(fbasemenratingslist, numberofsbasemen)
        secondb = listofsbasemen[sbasemenmaxindex]

        stringofss = form.ssnames.data
        numberofss = stringofss.count(',')+1
        listofss = stringofss.split(', ')
        try:
            ssratingslist = getratingslist(listofss, numberofss)
        except:
            return redirect('/inputerror')
        ssmaxindex = returnbestone(ssratingslist, numberofss)
        ss = listofss[ssmaxindex]

        stringoftbasemen = form.thirdbnames.data
        numberoftbasemen = stringoftbasemen.count(',')+1
        listoftbasemen = stringoftbasemen.split(', ')
        try:
            tbasemenratingslist = getratingslist(listoftbasemen, numberoftbasemen)
        except:
            return redirect('/inputerror')
        tbasemenmaxindex = returnbestone(tbasemenratingslist, numberoftbasemen)
        thirdb = listoftbasemen[tbasemenmaxindex]

        stringofoutfielders = form.outfieldnames.data
        numberofoutfielders = stringofoutfielders.count(',')+1
        if numberofoutfielders < 3:
            return redirect('/inputerror')        
        listofoutfielders = stringofoutfielders.split(', ')
        try:
            outfieldersratingslist = getratingslist(listofoutfielders, numberofoutfielders)
        except:
            return redirect('/inputerror')
        ofmaxindexone, ofmaxindextwo, ofmaxindexthree = returnbestthree(outfieldersratingslist, numberofoutfielders)
        outfieldone = listofoutfielders[ofmaxindexone]
        outfieldtwo = listofoutfielders[ofmaxindextwo]
        outfieldthree = listofoutfielders[ofmaxindexthree]

        total = numberofcatchers + numberoffbasemen + numberofsbasemen + numberofss + numberoftbasemen + numberofoutfielders
        if total < 10 or total > 13:
            return redirect('/inputerror')

        listoftherest = []
        ratingsoftherest = []
        posoftherest = []
        for c in range(0, numberofcatchers):
            if c != catchersmaxindex:
                listoftherest.append(listofcatchers[c])
                ratingsoftherest.append(catchersratingslist[c])
                posoftherest.append('C ')
        for c in range(0, numberoffbasemen):
            if c != fbasemenmaxindex:
                listoftherest.append(listoffbasemen[c])
                ratingsoftherest.append(fbasemenratingslist[c])
                posoftherest.append('1B')
        for c in range(0, numberofsbasemen):
            if c != sbasemenmaxindex:
                listoftherest.append(listofsbasemen[c])
                ratingsoftherest.append(sbasemenratingslist[c])
                posoftherest.append('2B')
        for c in range(0, numberofss):
            if c != ssmaxindex:
                listoftherest.append(listofss[c])
                ratingsoftherest.append(ssratingslist[c])
                posoftherest.append('SS')
        for c in range(0, numberoftbasemen):
            if c != tbasemenmaxindex:
                listoftherest.append(listoftbasemen[c])
                ratingsoftherest.append(tbasemenratingslist[c])
                posoftherest.append('3B')
        for c in range(0, numberofoutfielders):
            if (c != ofmaxindexone and c != ofmaxindextwo and c!=ofmaxindexthree):
                listoftherest.append(listofoutfielders[c])
                ratingsoftherest.append(outfieldersratingslist[c])
                posoftherest.append('OF')
 
        utilmaxindexone, utilmaxindextwo, restoftherestindices = returnbesttwo(ratingsoftherest)
        utilone = posoftherest[utilmaxindexone] + ': ' + listoftherest[utilmaxindexone]
        utiltwo = posoftherest[utilmaxindextwo] + ': ' + listoftherest[utilmaxindextwo]

        if len(restoftherestindices)==5:
            if restoftherestindices[2] is not None:
                benchone = posoftherest[restoftherestindices[2]] + ': ' + listoftherest[restoftherestindices[2]]
            if restoftherestindices[1] is not None:
                benchtwo = posoftherest[restoftherestindices[1]] + ': ' + listoftherest[restoftherestindices[1]]
            if restoftherestindices[0] is not None:
                benchthree = posoftherest[restoftherestindices[0]] + ': ' + listoftherest[restoftherestindices[0]]
        elif len(restoftherestindices)==4:
            if restoftherestindices[1] is not None:
                benchtwo = posoftherest[restoftherestindices[1]] + ': ' + listoftherest[restoftherestindices[1]]
            if restoftherestindices[0] is not None:
                benchthree = posoftherest[restoftherestindices[0]] + ': ' + listoftherest[restoftherestindices[0]]
        elif len(restoftherestindices)==3:
            if restoftherestindices[0] is not None:
                benchthree = posoftherest[restoftherestindices[0]] + ': ' + listoftherest[restoftherestindices[0]]
                
        return redirect('/lineup')

    return render_template('team.html', form=form)

@app.route('/lineup', methods = ['GET', 'POST'])
def lineup():
    now = datetime.datetime.now()

    catcherp = todaypitcherlookup(catcher)
    firstbp = todaypitcherlookup(firstb)
    secondbp = todaypitcherlookup(secondb)
    thirdbp = todaypitcherlookup(thirdb)
    ssp = todaypitcherlookup(ss)
    outfieldonep = todaypitcherlookup(outfieldone)
    outfieldtwop = todaypitcherlookup(outfieldtwo) 
    outfieldthreep = todaypitcherlookup(outfieldthree)
    utilonep = todaypitcherlookup(utilone[4:])
    utiltwop = todaypitcherlookup(utiltwo[4:])
    benchonep = todaypitcherlookup(benchone[4:])
    benchtwop = todaypitcherlookup(benchtwo[4:])
    benchthreep = todaypitcherlookup(benchthree[4:])
    
    return render_template('lineup.html', catcher=catcher,
                           firstb=firstb, secondb=secondb, thirdb=thirdb,
                           ss=ss, outfieldone=outfieldone, outfieldtwo=outfieldtwo,
                           outfieldthree=outfieldthree, utilone=utilone,
                           utiltwo=utiltwo, benchone=benchone, benchtwo=benchtwo,
                           benchthree=benchthree,
                           catcherp = catcherp,
                           catchermfi = getrating(bclusterlookup(catcher), pclusterlookup(catcherp)),
                           firstbp = firstbp,
                           firstbmfi = getrating(bclusterlookup(firstb), pclusterlookup(firstbp)),
                           secondbp = secondbp,
                           secondbmfi = getrating(bclusterlookup(secondb), pclusterlookup(secondbp)),
                           thirdbp = thirdbp,
                           thirdbmfi = getrating(bclusterlookup(thirdb), pclusterlookup(thirdbp)),
                           ssp = ssp,
                           ssmfi = getrating(bclusterlookup(ss), pclusterlookup(ssp)),
                           outfieldonep = outfieldonep,
                           outfieldonemfi = getrating(bclusterlookup(outfieldone), pclusterlookup(outfieldonep)),
                           outfieldtwop = outfieldtwop,
                           outfieldtwomfi = getrating(bclusterlookup(outfieldtwo), pclusterlookup(outfieldtwop)),
                           outfieldthreep = outfieldthreep,
                           outfieldthreemfi = getrating(bclusterlookup(outfieldthree), pclusterlookup(outfieldthreep)),
                           utilonep = utilonep,
                           utilonemfi = getrating(bclusterlookup(utilone[4:]), pclusterlookup(utilonep)),
                           utiltwop = utiltwop,
                           utiltwomfi = getrating(bclusterlookup(utiltwo[4:]), pclusterlookup(utiltwop)),
                           benchonep = benchonep,
                           benchonemfi = getrating(bclusterlookup(benchone[4:]), pclusterlookup(benchonep)),
                           benchtwop = benchtwop,
                           benchtwomfi = getrating(bclusterlookup(benchtwo[4:]), pclusterlookup(benchtwop)),
                           benchthreep = benchthreep,
                           benchthreemfi = getrating(bclusterlookup(benchthree[4:]), pclusterlookup(benchthreep)),
                           month=9, day=29, year=2013)

@app.route('/inputerror')
def inputerror():
     return render_template('inputerror.html')

@app.route('/about')
def about():
     return render_template('about.html')
