import cv2
from statistics import mean
from referenceManager import getReference as getLoadedReference
from coinCount import isSegment
threeHoriCoords = ((128+88,656), (128+88,668), (127+88,682))
LeftVertCoords = ((122+88,663),(119+88,674))
RightVertCoords= ((136+88,663),(133+88,674))
TOLERANCE = 40
MIN_BRIGHT = 205


CoordList = (threeHoriCoords[0],LeftVertCoords[0],threeHoriCoords[1],RightVertCoords[0],LeftVertCoords[1],threeHoriCoords[2],RightVertCoords[1])
# Order of Segments: TopMiddle,TopLeft,Center,TopRight,BottomLeft,BottomMiddle,BottomRight
NUM_LIST = (
(True,True,False,True,True,True,True), #0
(False,False,False,True,False,False,True), #1
(True,False,True,True,True,True,False), #2
(True,False,True,True,False,True,True), #3
(False,True,True,True,False,False,True), #4
(True,True,True,False,False,True,True), #5
(True,True,True,False,True,True,True), #6
(True,False,False,True,False,False,True), #7
(True,True,True,True,True,True,True), #8 #Should never hit this even on baby park
(True,True,True,True,False,True,True), #9
)




def checkLap(img):
    if(img.shape[0:2] != (720,1280)):
            img = cv2.resize(img,(1280,720))
    segList4One = []
    for coord in [(c[0] - 8,c[1]) for c in CoordList]:
        segList4One.append(isSegment(img,coord))
    if(tuple(segList4One) == NUM_LIST[0]):
        return 1
        
    segList = []
    for coord in CoordList:
        segList.append(isSegment(img,coord))
    
    
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
        