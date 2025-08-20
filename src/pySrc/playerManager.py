from raceChecking import findPos,isStart
from raceManager import Race, RaceInfo
from preRaceScan import checkTrack, scanPlayers, checkLoading
from ffmpegCapture import VideoCap
import ffmpegCapture
import messenger
import cv2

def sendMessage(type,content):
    messenger.sendMessage(type,"PlayerManager",content)

SELF_UPDATE = 1
ID_VALUES = 0
class Player:
    def __init__(self,name,capture=None):
        global ID_VALUES
        self.id = ID_VALUES
        ID_VALUES += 1
        self.name = name
        self.capture = capture
        if(capture):
            self.capture.activateSource(-1)
        self.splitscreenNum = 0

        self.character = "Mario"
        self.kart = "Standard Kart"
        self.wheels = "Standard"
        self.glider = "Super Glider"

        self.worldCharacter = "Mario"
        self.worldKart = "Standard Kart"

        self.lastPlayerCheck = 0, None
        self.currentActivity = None
        self.preRaceInfo = None
        self.currentRace = None
        self.raceHistory = []
        self.finished = False
        self.place = 0

        # Color info for overlays HSL
        
        self.colorAdj = {"H":0,"S":0,"L":200}
    def changeCaptureSource(self,capture):
        self.lastPlayerCheck = 0,None
        self.currentActivity = None
        self.preRaceInfo = None
        self.currentRace = None
        self.capture.activateSource()
    
    def updateStatus(self):
        if(type(self.capture) != ffmpegCapture.VideoCap):
            return
        if(SELF_UPDATE and self.capture.camera.method == 0):
            self.capture.updateImage()
        if(not self.capture.isActive()):
            sendMessage("Error",f"Capture device \'{self.capture.name}\' is not activated for player \'{self.name}\'")
        currentImg = self.capture.currentImage
        frameNum = self.capture.currentFrame
        framerate = self.capture.framerate
        if(type(currentImg) == type(None)):
            return
        if(currentImg.shape[0:2]!=(720,1280)):
            currentImg = cv2.resize(currentImg,(1280,720))
        # cv2.imshow("Test",currentImg)
        # cv2.waitKey(1)
        # findPos(currentImg)        
        cv2.imshow(f"{self.name}",currentImg)
        cv2.waitKey(1)
        if(self.currentActivity == "Race"):
            self.currentRace.updateRace(currentImg,frameNum,framerate)
            if(self.currentRace.finishedPlace != 0):
                self.raceHistory.append(self.currentRace)
                self.currentRace = None
                self.currentActivity = None
        elif(isStart(currentImg)):
            self.finished = False
            self.currentRace = Race(self,self.preRaceInfo)
            print("Race Started")
            self.preRaceInfo = None
            self.currentActivity = "Race"
        elif self.preRaceInfo == None and checkLoading(currentImg):
            trackCheck = checkTrack(currentImg)
            # print(trackCheck)
            if(trackCheck==None):
                return
            self.finished = False
            teamCount,players = scanPlayers(currentImg)
            if(len(players)<=1):
                return
            if((frameNum-self.lastPlayerCheck[0])/framerate>.5 and self.lastPlayerCheck[1] == len(players)):
                print(f"Racing on {trackCheck}")
                print([(player.points,player.team) for player in players])
                self.preRaceInfo = RaceInfo(RaceInfo.MK8DX,trackCheck,RaceInfo.CC150,teamCount,players)
                self.lastPlayerCheck = 0,None
            elif(len(players)!=self.lastPlayerCheck[1]):
                self.lastPlayerCheck = frameNum, len(players)
    # def exportData(self):
    #     return {
    #         "id": self.id,
    #         "capture": self.capture.id,
    #         "name": self.name,
    #         "splitNum": self.splitscreenNum,
    #         "character": self.character,
    #         "kart": self.kart,
    #         "wheels":self.wheels,
    #         "glider": self.glider,
    #         "worldChar": self.worldCharacter,
    #         "worldKart": self.worldKart,
    #         "activity": self.currentActivity,
    #         "preRaceInfo": isExportable(self.preRaceInfo),
    #         "currentRace": isExportable(self.currentRace),
    #         "colorAdj": self.colorAdj,
    #         "finished": self.finished,
    #         "place": self.place
    #     }
    def exportData(self):
        toExport = self.__dict__.copy()
        if(self.capture):
            toExport["capture"] = self.capture.id
        if(self.preRaceInfo):
            toExport["preRaceInfo"] = isExportable(self.preRaceInfo)
        if(self.currentRace):
            toExport["currentRace"] = isExportable(self.currentRace)
        return toExport
    def dict(self):
        return self.exportData()
    def exportToFile(self,path="./"):
        pass
def isExportable(obj):
    try:
        if(obj):
            return obj.exportInfo()
    except:
        return None
        