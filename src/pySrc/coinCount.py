import cv2
from statistics import mean
from referenceManager import getReference as getLoadedReference
import numpy as np

threeHoriCoords = ((128,656), (128,670), (127,682))
LeftVertCoords = ((122,663),(119,676))
RightVertCoords= ((136,663),(133,674))
TOLERANCE = 50
MIN_BRIGHT = 205
WHITE_COLOR = np.array([230,230,230])
MAX_COIN_REF = getLoadedReference("10Coin")

CoordList = (threeHoriCoords[0],LeftVertCoords[0],threeHoriCoords[1],RightVertCoords[0],LeftVertCoords[1],threeHoriCoords[2],RightVertCoords[1])
# Order of Segments: TopMiddle,TopLeft,Center,TopRight,BottomLeft,BottomMiddle,BottomRight
NUM_LIST = (
(True,True,False,True,True,True,True), #0
(False,True,False,True,True,False,True), #1
(True,False,True,True,True,True,False), #2
(True,False,True,True,False,True,True), #3
(False,True,True,True,False,False,True), #4
(True,True,True,False,False,True,True), #5
(True,True,True,False,True,True,True), #6
(True,False,False,True,False,False,True), #7
(True,True,True,True,True,True,True), #8
(True,True,True,True,False,True,True), #9
) # I'm Lazy so 10 is just template matching



def checkCoins(img):
    if(img.shape[0:2] != (720,1280)):
            img = cv2.resize(img,(1280,720))
    maxCoinTemplate = MAX_COIN_REF
    if(maxCoinTemplate.checkImage(img)[0]):
        return 10
    return sevSegDecode(img)




def sevSegDecode(img):
    segList = []
    segList4One = []
    for coord in [(c[0] - 8,c[1]) for c in CoordList]:
        segList4One.append(isSegment(img,coord,TOLERANCE))
    if(tuple(segList4One) == NUM_LIST[0]):
        return 1
    for coord in CoordList:
        segList.append(isSegment(img,coord,TOLERANCE))
    
    index = 1
    for num in NUM_LIST[1:]:
        if(tuple(segList)==num):
            return index
        index += 1
    return -1

# def isSegment(img,coords,tolerance):
#     firstColorVal = img[coords[1]][coords[0]][0]
#     if(firstColorVal<MIN_BRIGHT):
#         return False
#     aveBright = mean([int(p) for p in img[coords[1]][coords[0]]])
#     distFirstVal = abs(int(aveBright)-int(firstColorVal))
#     # print(distFirstVal)
#     if(distFirstVal <= tolerance):
#         return True

def isSegment(img,coords,tolerance=TOLERANCE,minbright=MIN_BRIGHT):
    color = img[coords[1]][coords[0]].astype("int64")
    # if(color[0]<minbright):
    #     return False
    dist = np.sqrt(np.sum((color-WHITE_COLOR)**2,axis=0))
    # print(distFirstVal)
    if(dist <= tolerance):
        # print(color)
        return True
    return False