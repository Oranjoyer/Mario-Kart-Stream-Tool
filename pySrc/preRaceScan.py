from referenceManager import getReference
from referenceMatching import Reference,compareGroup
from raceManager import DummyPlayer
import cv2
from coinCount import NUM_LIST
import numpy as np
import cProfile
import time

DIGIT_START = 552,49
DIGIT_SIZE = 19,29
DIGIT_GAP = 3
DIGIT_SHIFT = 22
DIGIT_COLOR = np.array([79, 79, 79])
WHITE_DIGIT = np.array([240,240,240])
COLOR_TOLERANCE = 40

# HORI_SEG_COORDS= (561,(51,64,77))
# VERT_SEG_COORDS= ((555,569),(58,70))
# ONE_COORDS=(562,(58,69))

HORI_SEG_COORDS= (11,(2,15,25))
VERT_SEG_COORDS= ((3,17),(9,21))
ONE_COORDS=(10,(9,20))

HORIZONAL_COORDS = [(HORI_SEG_COORDS[0],v) for v in HORI_SEG_COORDS[1]]
VERT_COORDS = [(v,h) for h in VERT_SEG_COORDS[1] for v in VERT_SEG_COORDS[0]]
#i%3
SEGMENT_COORDS= []
def COORD_CREATE():
    offset=0
    for i in range(len(HORIZONAL_COORDS)+len(VERT_COORDS)):
        if(i==0 or i==2 or i==5):
            SEGMENT_COORDS.append(HORIZONAL_COORDS[int(i/2)])
            offset+=1
        else:
            SEGMENT_COORDS.append(VERT_COORDS[i-offset])
COORD_CREATE()






TAG_DIM = (578,87)
ORIGIN = (62,56)
SHIFT= (580,88)
TRACKS = ("MKS","SSC","WP","TR",
"MC","TH","TM","SGF",
"SA","DS","Ed","MW",
"CC","BDD","BC","RR",
"rMMM","rMC","rCCB","rTT",
"rDDD","rDP3","rRRy","rDKJ",
"rWS","rSL","rMP","rYV",
"rTTC","rPPS","rGV","rRRd",
"dYC","dEA","dDD","dMC",
"dWGM","dRR","dIIO","dHC",
"dBP","dCL","dWW","dAC",
"dNBC","dRiR","dSBS","dBB",
"bPP","bTC","bCMo","bCMa",
"bTB","bSR","bSG","bNH",
"bNYM","bMC3","bKD","bWP",
"bSS","bSL","bMG","bSHS",
"bLL","bBL","bRRM","bMT",
"bBB","bPG","bMM","bRR7",
"bAD","bRP","bDKS","bYI",
"bBR","bMC","bWS","bSS",
"bAtD","bDC","bMH","bSCS",
"bLAL","bSW","bKC","bVV",
"bRA","bDKM","bDC","bPPC",
"bMD","bRIW","bBC3","bRRw")
track_key = [
 'Mario Kart Stadium', 'Water Park', 'Sweet Sweet Canyon', 'Thwomp Ruins',
 'Mario Circuit', 'Toad Harbor', 'Twisted Mansion', 'Shy Guy Falls', 
 'Sunshine Airport', 'Dolphin Shoals', 'Electrodrome', 'Mount Wario', 
 'Cloudtop Cruise', 'Bone-Dry Dunes', "Bowser's Castle", 'Rainbow Road', 
 'Wii Moo Moo Meadows', 'GBA Mario Circuit', 'DS Cheep Cheep Beach', "N64 Toad's Turnpike", 
 'GCN Dry Dry Desert', 'SNES Donut Plains 3', 'N64 Royal Raceway', '3DS DK Jungle', 
 'DS Wario Stadium', 'GCN Sherbet Land', '3DS Music Park', 'N64 Yoshi Valley', 
 'DS Tick-Tock Clock', '3DS Piranha Plant Slide', 'Wii Grumble Volcano', 'N64 Rainbow Road', 
 'GCN Yoshi Circuit', 'Excitebike Arena', 'Dragon Driftway', 'Mute City', 
 "Wii Wario's Gold Mine", 'SNES Rainbow Road', 'Ice Ice Outpost', 'Hyrule Circuit', 
 'GCN Baby Park', 'GBA Cheese Land', 'Wild Woods', 'Animal Crossing', 
 '3DS Neo Bowser City', 'GBA Ribbon Road', 'Super Bell Subway', 'Big Blue', 
 'Tour Paris Promenade', '3DS Toad Circuit', 'N64 Choco Mountain', 'Wii Coconut Mall', 
 'Tour Tokyo Blur', 'DS Shroom Ridge', 'GBA Sky Garden', 'Ninja Hideaway', 'Tour New York Minute', 'SNES Mario Circuit 3', 'N64 Kalimari Desert', 'DS Waluigi Pinball', 'Tour Sydney Sprint', 'GBA Snow Land', 'Wii Mushroom Gorge', 'Sky-High Sundae', 'Tour London Loop', 'GBA Boo Lake', '3DS Rock Rock Mountain', 'Wii Maple Treeway', 'Tour Berlin Byways', 'DS Peach Gardens', 'Merry Mountain', '3DS Rainbow Road', 'Tour Amsterdam Drift', 'GBA Riverside Park', 'Wii DK Summit', "Yoshi's Island", 'Tour Bangkok Rush', 'DS Mario Circuit', 'GCN Waluigi Stadium', 'Tour Singapore Speedway', 'Tour Athens Dash', 'GCN Daisy Cruiser', 'Wii Moonview Highway', 'Squeaky Clean Sprint', 'Tour Los Angeles Laps', 'GBA Sunset Wilds', 'Wii Koopa Cape', 'Tour Vancouver Velocity', 'Tour Rome Avanti', 'GCN DK Mountain', 'Wii Daisy Circuit', 'Piranha Plant Cove', 'Tour Madrid Drive', "3DS Rosalina's Ice World", 'SNES Bowser Castle 3', 'Wii Rainbow Road']
TRACK_REFS = []
COUNTRIES = ("USA","Japan","UK","Brazil","Canada","Germany","France","Spain","Mexico")
COUNTRY_REFS = [getReference(c) for c in COUNTRIES]
PLAYER_TAGS = (getReference("TagFFA"),getReference("TagRed"),getReference("TagBlue"))
CC_REFS = (getReference("50cc"),getReference("100cc"),getReference("150cc"),getReference("Mirror"),getReference("200cc"))
LOADING_REF = getReference("Loading")


def checkLoading(img):
    return LOADING_REF.checkImage(img)[0]
def loadTrackRefs():
    global TRACK_REFS
    for track in TRACKS:
        TRACK_REFS.append(getReference(track))
    # TRACK_REFS=np.array(TRACK_REFS,dtype=Reference)
    TRACK_REFS=tuple(TRACK_REFS)
def checkLoading(img):
    if(LOADING_REF.checkImage(img)[0]):
        return True
    return False
def checkTrack(img):
    compare, index = compareGroup(TRACK_REFS,img)
    if(compare == None):
        return
    return track_key[index]
def checkCountry(img):
    for ref in COUNTRY_REFS:
        if(ref!=None and ref.checkImage(img)[0]):
            return ref.name
    return "Unknown"
# 35 363
def scanPlayers(img):
    players = []
    img = img[ORIGIN[1]:,ORIGIN[0]:]
    count = 0
    breakSig = False
    teamCount = 0
    for c in range(2):
        if(breakSig): break
        for r in range(6):
            crop = img[int(SHIFT[1]*r):int(SHIFT[1]*r+TAG_DIM[1]),int(SHIFT[0]*c):int(SHIFT[0]*c+TAG_DIM[0])]
            
            index = 0
            playerTeam = -1
            for tagType in PLAYER_TAGS:
                if(tagType.checkImage(crop)[0]):
                    playerTeam = index
                    break
                index+=1
            count+=1
            if(playerTeam==-1):
                breakSig = True
                break
            country = checkCountry(crop)
            points = getPoints(crop,playerTeam>0)

            if(playerTeam!=0):
                teamCount = 2
            players.append(DummyPlayer(f"Player{count}",points,country,playerTeam))
    return teamCount,players
def getPoints(img,teamGame):
    points = 0
    for i in range(5):
        numCoord = ((DIGIT_START[1]),(DIGIT_START[1]+DIGIT_SIZE[1])),(DIGIT_START[0]-DIGIT_SHIFT*i,DIGIT_START[0]+DIGIT_SIZE[0]-DIGIT_SHIFT*i)
        number = getNumber(img[numCoord[0][0]:numCoord[0][1],numCoord[1][0]:numCoord[1][1]],teamGame)
        if(number == -1):
            break
        points += 10**i * number
    return points

def getNumber(img,teamGame):
    if(isSegment(img[ONE_COORDS[1][0]][ONE_COORDS[0]],teamGame) and isSegment(img[ONE_COORDS[1][1]][ONE_COORDS[0]],teamGame)):
        return 1
    segmentList = tuple(makeSegmentList(img,teamGame))
    for i,number in enumerate(NUM_LIST):
        if(i==1):
            continue
        if(number == segmentList):
            return i
    return -1

def makeSegmentList(img,teamGame):
    return [isSegment(img[coord[1]][coord[0]],teamGame) for coord in SEGMENT_COORDS]

def isSegment(color,teamGame):
    colorArr = DIGIT_COLOR
    if(teamGame):
        colorArr = WHITE_DIGIT
    if(type(color) != np.array):
        np.array(color)
    dist = np.sqrt(np.sum((color-colorArr)**2,axis=0))
    if(dist<=COLOR_TOLERANCE):
        return True
    return False

def checkCC(img):
    index = 0
    for ref in CC_REFS:
        if(ref.checkImage(img)[0]):
            return index
        index += 1
loadTrackRefs()