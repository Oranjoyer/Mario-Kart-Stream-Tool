import time
from coinCount import checkCoins
from lapCount import checkLap 
from raceChecking import checkPlace, PLACE_NAMES, findPos, isFinished, checkTeam
import messenger
import cv2
from numpy import sqrt
from itemChecking import checkItems

ITEM_STATIC_COUNT = 5
PLACE_STATIC_COUNT = 5

# Send Message to Logs
def sendMessage(type,content):
    messenger.sendMessage(type, "RaceManager",content)

REASONABLE_DIST = 30
class RaceInfo:
    
    MK8DX = 0
    MKW = 1
    CC50 = 0
    CC100 = 1
    CC150 = 2
    CCMM = 3
    CC200 = 4
    OFF = 0
    WW = 1
    PL = 2

    def __init__(self,game,track,engineClass,teamCount,players=[]):
        self.game = game
        self.track = track
        self.engineClass = engineClass
        self.teamCount = teamCount
        self.players = players
        self.type = RaceInfo.OFF
        if(len(players)>0):
            self.type == RaceInfo.WW if max((p.points for p in players)) > 720 else RaceInfo.PL
    def __eq__(self,other):
        selfDict = self.__dict__
        if(type(other) != RaceInfo):
            return False
        for key in selfDict:
            value= selfDict[key]
            if(key == "players"):
                break
            if(value!=other.__dict__[key]):
                return False
        for index in range(len(self.players)):
            if(self.players[index]!=other.players[index]):
                return False
        return True
    def dict(self):
        temp = self.__dict__.copy()
        if(self.players != None):
            temp["players"] = [p.dict() for p in self.players]

        


class DummyPlayer:
    FFA = 0
    RED = 1
    BLUE = 2

    def __init__(self,name,points,country,team):
        self.name = name
        self.points = points
        self.country = country
        self.team = team
    def __eq__(self,other):
        if(other!=DummyPlayer):
            return False
        if(self.name!=other.name):
            return False
        if(self.points!=other.points):
            return False
        if(self.country!=other.country):
            return False
        if(self.team != other.team):
            return False
        return True

class RacePosition:
    def __init__(self,x,y):
        self.coords = (x,y)
        self.time = time.time()
    def getDistance(self,otherPos):
        return sqrt(pow(self.x - otherPos.x,2) + pow(self.y - otherPos.y,2))



class Race:
    def __eq__(self,other):
        if(self.info != None and self.info == other.info):
            return True
        return False
    def __init__(self,player,info):
        self.info = info
        self.playercount= len(info.players) if info else -1
        self.player = player
        self.playerId = player.id
        self.startTime = time.time()
        self.endTime = -1
        self.finishedPlace = 0
        self.lastPlaceCheck = 0
        self.placeStaticCount = 0
        self.team = -1

        self.lastItemCheck = ("Unknown","Unknown")
        self.lastItemFrame = 0
        
        self.character = player.character
        self.kart = player.kart
        self.wheels = player.wheels
        self.glider = player.glider

        self.worldCharacter = player.worldCharacter
        self.worldKart = player.worldKart
        
        self.currentTime = time.time()
        self.lap = -1
        self.coins = -1
        self.place = 0
        self.items = ("Empty","Empty")

        self.hits = 0
        self.positions = []
        self.conditionsOverTime = []
    def printChanges(self):
        if(len(self.conditionsOverTime) == 0):
            return
        playerName = self.player.name
        lastConditions = self.conditionsOverTime[-1]
        if(self.lap != lastConditions.get("lap")):
            sendMessage("Info",f"{playerName} moved to lap {self.lap}")
        if(self.coins != lastConditions.get("coins")):
            sendMessage("Info",f"{playerName} now has {self.coins} coins")
        if(self.hits != lastConditions.get("hits")):
            sendMessage("Info",f"{playerName} was hit")
        if(self.place != lastConditions.get("place")):
            sendMessage("Info",f"{playerName} moved to {PLACE_NAMES[self.place-1]} place")
        if(self.items!=lastConditions.get("items")):
            sendMessage("Info",f"{playerName}'s items changed to {self.items}")
    def updateRace(self,img,frameNum,framerate):
        if(self.team == -1):
            if(self.info and max([p.team for p in self.info.players])==0):
                self.team = 0
            else:
                self.team = checkTeam(img)
                if(self.team !=-1):
                    sendMessage("Info",f"Team Color is {self.team}")
        # cv2.imshow("test",img)
        # cv2.waitKey(1)
        self.currentTime = time.time()
        if(self.player.splitscreenNum!=0):
            sendMessage("Error","Splitscreen Support not implemented")
            return
        if(self.endTime == -1):
            dumpNewCond = False
            tempPlace = checkPlace(img,teamNum=self.team,playercount=self.playercount)
            tempLap = checkLap(img)
            tempCoins = checkCoins(img)
            tempItems= checkItems(img)
            # timeSinceItemChange=(self.player.capture.currentFrame-self.lastItemFrame)/self.player.capture.framerate
            timeSinceItemChange=(frameNum-self.lastItemFrame)/framerate
            if(tempItems==self.items):
                pass
            elif(tempItems!=self.lastItemCheck):
                self.lastItemFrame = frameNum
                self.lastItemCheck = tempItems
            elif(timeSinceItemChange>0.5 and tempItems[0]!="Unknown"):
                temp = tempItems
                if(tempItems[1]=="Unknown"):
                    temp=(tempItems[0],self.items[1])
                self.items = temp
                dumpNewCond=True
            elif(timeSinceItemChange>1.25 and tempItems==("Unknown","Unknown")):
                self.items = ("Empty","Empty")
                dumpNewCond=True

            if(tempPlace!=0 and self.place != tempPlace):
                dumpNewCond = True
                self.place = tempPlace
                self.player.place = tempPlace

            if(tempLap!=-1 and tempLap>self.lap and (abs(tempLap-self.lap)==1 or self.lap==-1)):
                dumpNewCond = True
                self.lap = tempLap

            if(tempCoins != -1 and tempCoins != self.coins):
                if(tempCoins < self.coins):
                    self.hits += 1
                self.coins = tempCoins
                dumpNewCond = True

            if(isFinished(img)):
                self.player.finished = True
                self.endTime = time.time()
            
            if(dumpNewCond):
                newCond = {
                        "time":self.currentTime,
                        "place":self.place,
                        "lap":self.lap,
                        "coins":self.coins,
                        "hits":self.hits,
                        "items":self.items,
                    }
                self.printChanges()
                self.conditionsOverTime.append(newCond)
        else:
            if(self.finishedPlace == 0):
                tempPlace = checkPlace(img,teamNum=self.team,playercount=self.playercount)
                if(tempPlace != 0):
                    self.finishedPlace = tempPlace
                    self.player.place = tempPlace
                    sendMessage("Info",f"{self.player.name} finished in {PLACE_NAMES[tempPlace-1]} place")
                    self.conditionsOverTime.append(
                    {
                        "time":self.endTime,
                        "place":self.finishedPlace,
                        "lap":self.lap,
                        "coins":self.coins,
                        "hits":self.hits,
                        "items":self.items,
                    }
                )
    def dict(self):
        temp = self.__dict__.copy()
        if(self.info!=None):
            temp["info"] = self.info.dict()
        if(self.player!=None):
            temp["player"]= (self.player.name,self.player.id)
        return temp




            


        

