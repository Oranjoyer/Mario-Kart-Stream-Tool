from referenceManager import getReference
from referenceMatching import Reference,compareGroup
from raceManager import DummyPlayer
import cv2
from coinCount import NUM_LIST
import numpy as np
import time

DIGIT_START = 1201,67
DIGIT_SIZE = 15,23
DIGIT_GAP = 3
DIGIT_SHIFT = 17
DIGIT_COLOR = np.array([79, 79, 79])
WHITE_DIGIT = np.array([240,240,240])
COLOR_TOLERANCE = 40

# HORI_SEG_COORDS= (1208,(68,77,87))
# VERT_SEG_COORDS= ((1203,1213),(73,82))
# ONE_COORDS=(1208,(73,83))

HORI_SEG_COORDS= (7,(1,10,20))
VERT_SEG_COORDS= ((2,12),(5,15))
ONE_COORDS=(1,(6,16))

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






TAG_DIM = (676,48)
ORIGIN = (552,49)
SHIFT= (0,102)
COUNTRIES = ("USA","Japan","UK","Brazil","Canada","Germany","France","Spain","Mexico")
COUNTRY_REFS = [getReference(c) for c in COUNTRIES]
PLAYER_TAGS = (getReference("TagFFA"),getReference("TagRed"),getReference("TagBlue"))
# CC_REFS = (getReference("50cc"),getReference("100cc"),getReference("150cc"),getReference("Mirror"),getReference("200cc"))




def loadTrackRefs():
    global TRACK_REFS
    for track in TRACKS:
        TRACK_REFS.append(getReference(track))
    # TRACK_REFS=np.array(TRACK_REFS,dtype=Reference)
    TRACK_REFS=tuple(TRACK_REFS)
def checkLoading(img):
    if(LOAD_REF.checkImage(img)[0]):
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