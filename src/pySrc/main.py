import sys
from cameraSystem import initCams, getListing, cameraDetails
from playerManager import Player
import ffmpegCapture
from ffmpegCapture import CAP_LIST
import threading
from multiprocessing import Pool
import time
import cv2

PORT_OPT = "port="
PORT = 52402
PLAYERS = []
MAX_UPDATE_RATE=20

def main():
    setStartOption()
    mainInit()
    # if(__name__== "__main__"):
    #     threading.Thread(target=lambda: flaskService.flaskRun()).start()
    # mainCap = ffmpegCapture.VideoCap.fromCam("Main",getListing()[0],1920,1080,60)
    mainCap = ffmpegCapture.VideoCap.fromCam(cameraDetails.fromFile("mkVid.mkv"),1280,720,60)
    size = 1
    players = []
    for i in range(size):
        players.append(Player(f"Player{i+1}",mainCap))
    global PLAYERS
    PLAYERS = players
    # player = Player(mainCap,"Grant")
    threading.Thread(target=mainLoop).start()
    while(len(CAP_LIST)>0):
    # for i in range(1):
        start = time.time()
        # playerThreads = [threading.Thread(target=updatePlayer,args=[player]) for player in players]
        updatePlayers(players)
            # threading.Thread(target=updatePlayer,args=[player]).start()
        #     # print(player.__dict__)
        # cv2.waitKey(int(max(0.001,1/MAX_UPDATE_RATE-(time.time()-start))*1000))
        # cv2.waitKey(1)
        # time.sleep(max(0,1/MAX_UPDATE_RATE-(time.time()-start)))
        framerate = 1/(time.time()-start+0.0001)
        # if(framerate<MAX_UPDATE_RATE-1):
        #   print(int(framerate))
def updatePlayers(players):
        # return map(Player.updateStatus,players)
        [Player.updateStatus(p) for p in players]
def mainInit():
    initCams()

def mainLoop():
    while True:
        if(len(CAP_LIST)==0):
            continue
        maxFPS = max([cap.framerate for cap in CAP_LIST])
        start = time.time()
        for cap in CAP_LIST:
            if(cap.camera.method != 0):
                cap.updateImage()
        time.sleep(max(0,1/(maxFPS+1)-(time.time()-start)))
        framerate = 1/(time.time()-start+0.0001)
        # print(int(framerate))
    
    


def setStartOption():
    if(len(sys.argv) <= 1):
        return
    for option in sys.argv:
        if(option[:len(PORT_OPT)]==PORT_OPT):
            global PORT 
            PORT = option[len(PORT_OPT):]

main()

    
