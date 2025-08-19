import statistics as stat
import cv2
import numpy as np
from numpy import sqrt
from multiprocessing import Queue, Process, Value, Array
import itertools
import time
import messenger

# Send Message to Logs
def sendMessage(type,content):
    messenger.sendMessage(type, "References",content)

# from math import sqrt
class Pixel:
    def __init__(self,R,G,B,x,y):
        self.R = R
        self.G = G
        self.B = B
        self.RGB = (R,G,B)
        self.BGR = np.array([B,G,R])
        self.x = x
        self.y = y
        self.coords = (x,y)
    # def getDistanceOnImg(self,img):
    #     # print(self.BGR.dtype)
    #     # print((self.BGR-img[self.y][self.x].astype("int64")))
    #     colordists = []
    #     index = 0
    #     for c in range(3):
    #         colordists.append(abs(self.RGB[c]-int(img[self.y][self.x][-(c+1)])))
    #     # distance = np.sum((self.BGR-img[self.y][self.x].astype("int64"))**2)
    #     distance = 0
    #     for dist in colordists:
    #         distance += pow(int(dist),2)
    #     distance = sqrt(distance)
    #     # print(distance)
    #     return int(distance)
    def getDistanceOnImg(self,img):
        distance = np.sum((self.BGR-img[self.y][self.x].astype("int64"))**2)
        distance = sqrt(distance)
        return distance
# def compareGroup(references,img):
#         currentBest = (None, 9999)
#         checkImageFunc = Reference.checkImage

#         index = 0
#         bestIndex = -1

#         for reference in references:

#             currentTest = checkImageFunc(reference,img)
#             # if(currentTest[1]<15):
#             #     return reference, (index)
#             if(currentTest[0] and currentTest[1]<currentBest[1]):
#                 currentBest = (reference, currentTest[1])
#                 bestIndex = index
#             index+=1
#         return currentBest[0], bestIndex
def compareGroup(references,img):
    # checkImageFunc = Reference.checkImage
    refPaired = zip(references,itertools.repeat(img))
    analysis = itertools.starmap(Reference.checkImage,refPaired)
    best = min(enumerate(analysis),key=lambda a: a[1][1])
    if(not best[1][0]):
        return None,-1
    return references[best[0]], best[0]


class Reference:
    def __init__(self,name,pixels,tolerance,referenceRes):
        self.name = name
        self.pixels = pixels
        self.tolerance = tolerance
        self.referenceRes = referenceRes
        self.discrete = True
        self.subRes = referenceRes
        self.bounds = None
    def checkImage(self,img):
        if(self.discrete and img.shape[0:2]!=(self.referenceRes[1],self.referenceRes[0])):
            sendMessage("Warning","Image plugged into comparison function with non-standard resolution")
            img = cv2.resize(img,self.referenceRes)
        # pixelDists = []
        # for pixel in self.pixels:
        #     pixelDists.append(Pixel.getDistanceOnImg(pixel,img))
        # pixelDists = (pixel.getDistanceOnImg(img) for pixel in self.pixels)
        pixelDists = itertools.starmap(Pixel.getDistanceOnImg,zip(self.pixels,itertools.repeat(img)))
        meanDist = stat.mean(pixelDists)
        # print(meanDist)
        # if(self.name == "bWP"):
        #     print(meanDist)
        if(meanDist<=self.tolerance):
            return True, meanDist
        return False, meanDist
    
    # def scanImage(self,img): # Fun lil experiment, might try to make work later
    #     lowestDist = -1
    #     if(self.discrete):
    #         return False, (0,0)
    #     if(img.shape[0:2]!=(self.referenceRes[1],self.referenceRes[2])):
    #         img = cv2.resize(img,self.referenceRes)
    #     for i in range((self.bounds[1][1] - self.bounds[0][1]) - self.subRes[1]):
    #         y = i + self.bounds[0][1]
    #         y2 = y + self.subRes[1]
    #         for j in range((self.bounds[1][0] - self.bounds[0][0]) - self.subRes[0]):
    #             x = j + self.bounds[0][0]
    #             x2 = x + self.subRes[0]
    #             checked = self.checkImage(img[y:y2,x:x2])
    #             if(lowestDist == -1 or checked[1]<lowestDist):
    #                 lowestDist = checked[1]
    #             if(checked[0]):
    #                 print(checked[1])
    #                 cv2.imshow("Test",img[y:y2,x:x2])
    #                 cv2.imshow("Test2",img[self.bounds[0][1]:self.bounds[1][1],self.bounds[0][0]:self.bounds[1][0]])
    #                 cv2.waitKey(1)
    #                 return (x,y)
    #     print(lowestDist)
    #     return (None,None)

        
        
    
    def exportAsDict(self):
        selfDict = {
            "Name": self.name,
            "ReferenceResolution":self.referenceRes,
            "Tolerance":self.tolerance,
            "Points": [[int(i) for i in p.coords] for p in self.pixels],
            "Colors": [[int(i) for i in p.RGB] for p in self.pixels],
            "Discrete": self.discrete,
            "Bounds": self.bounds,
            "SubRes": self.subRes
        }
        return selfDict
    def dict(self):
        return self.exportAsDict()
    def importFromDict(data):
        tolerance = data.get("Tolerance")
        colorList = data.get("Colors")
        pointList = data.get("Points")
        name = data.get("Name")
        refRes = data["ReferenceResolution"]
        subRes = data.get("SubRes")
        bounds = data.get("Bounds")
        discrete = data.get("Discrete")
        if(discrete == None):
            discrete = True
        pixelList = []
        for i in range(len(pointList)):
            tempPix = Pixel(colorList[i][0],colorList[i][1],colorList[i][2],pointList[i][0],pointList[i][1])
            pixelList.append(tempPix)
        temp = Reference(name,pixelList,tolerance,refRes)
        temp.subRes = subRes
        temp.bounds = bounds
        temp.discrete = discrete
        return temp

# class multiProcScan:
#     def __init__(self,procNum):
#         self.procNum = procNum
#         self.refQueues = [Queue() for i in range(procNum)]
#         self.imgQueue = Queue()
#         self.returnQueue = Queue()
#         self.run = Value('i')
#         self.run.value = 1
#         self.hasImage = Array('i',procNum)
#         args = (self.returnQueue,self.imgQueue,self.run,self.hasImage)
#         self.procs = [Process(target=multiProcScan.refProc,args=[self.refQueues[i]]+list(args) + [i]) for i in range(procNum)]
#         for proc in self.procs:
#             proc.start()
    
#     def refProc(refQueue,returnQueue,imgQueue,runValue,imgStatus,index):
#         currentImg = None
#         while(runValue.value==1):
#             if(imgStatus[index]==0 and not imgQueue.empty()):
#                 currentImg = imgQueue.get()
#                 imgStatus[index]=1
#             if not refQueue.empty(): 
#                 ref = refQueue.get()
#                 # print(ref[0].name)
#                 while(imgStatus[index]==0):
#                     if(not imgQueue.empty()):
#                         currentImg = imgQueue.get()
#                         imgStatus[index]=1
#                 test = Reference.checkImage(ref[0],currentImg)
#                 returnQueue.put((test[0],test[1],ref[1]))
#     def compareGroup(self,references,img):
#         self.sendImg(img)
#         refLen = len(references)
#         i=0
#         while i < refLen:
#             for refQueue in self.refQueues:
#                 refQueue.put((references[i],i))
#                 i+=1
#         results = []
#         while len(results)<refLen:
#             if(not self.returnQueue.empty()):
#                 results.append(self.returnQueue.get())
#         minTrio = min(results,key=lambda trio : trio[1])
#         if(minTrio[0]):
#             return minTrio[0],minTrio[2]
#         return None,-1 
#     def sendImg(self,img):
#         # while(not self.imgQueue.empty()):
#         #     self.imgQueue.get()
#         for i in range(self.procNum):
#             self.imgQueue.put(img) 
#         for i in range(self.procNum):
#             self.hasImage[i] = 0 
#         while(min(self.hasImage)==0):
#             pass
        

        
    

# MAIN_PROC = multiProcScan(2)



