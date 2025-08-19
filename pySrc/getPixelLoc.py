import cv2
import json
import fileService
import frameAverage
import referenceMatching
import sys
import numpy as np
from statistics import mode
coordList = []
TEMPLATE_LOC = "./TemplateData"

def checkDict(infoJson):
    if(type(infoJson)==str):
        infoJson = json.loads(infoJson)
    if("TemplateInfo" not in infoJson):
        return None
    # print(infoJson)
    refDir = infoJson.get("GAME")
    referenceResolution = infoJson.get("RefRes")
    cropPoint = infoJson.get("CropPoint")
    refList = []
    queries = infoJson.get("Query")
    for template in infoJson.get("Templates"):
        queries = template.get("Query") if template.get("Query") else queries
        print(template)
        print(template.get("Query"))
        queried = [f.fileData for f in fileService.loadFilesFromQueries(f"{TEMPLATE_LOC}/{refDir}/",queries)]
        templateImg = frameAverage.getAverageFrameColor(queried)
        if(cropPoint!=None):
            templateImg = templateImg[cropPoint[0][1]:cropPoint[1][1],cropPoint[0][0]:cropPoint[1][0]]
        cv2.imshow("Template",templateImg)
        cv2.setMouseCallback("Template",addToCoordList)
        # print([int(np.mean(templateImg[:,:,i])) for i in range(3)])
        cv2.waitKey(0)
        # for i in range(3):
        #     cv2.imshow("Template",templateImg[:,:,i]) 
        #     cv2.waitKey(1)
        dumpCoordList()
        cv2.waitKey(0)

def addToCoordList(event,x,y,flags,param):
    if(event == cv2.EVENT_LBUTTONDBLCLK):
        print((x,y))
        coordList.append((x,y))

def dumpCoordList():
    global coordList
    print(json.dumps(coordList))
    coordList = []

filePaths = sys.argv[1:]
# filePath = "MK8DX/placeInfo.json"     
for filePath in filePaths:
    with open(filePath) as f:
        
        checkDict(f.read())