import cv2
import sys
import apiService
import cameraSystem
from cameraSystem import initCams, getListing, cameraDetails
from playerManager import Player
import playerManager
import ffmpegCapture
from ffmpegCapture import CAP_LIST
import threading
import time
import messenger
import os
import signal


last_pulse = -1
THREAD_LIST=[]
PORT_OPT = "port="
PORT = 52402
PLAYERS = []
CAPTURE_SOURCES=[]
MAX_UPDATE_RATE=-1
GLOBAL_SIGNAL=threading.Event()
GLOBAL_SIGNAL.set()
def setStartOption():
    if(len(sys.argv) <= 1):
        return
    for option in sys.argv:
        if(option[:len(PORT_OPT)]==PORT_OPT):
            global PORT 
            PORT = option[len(PORT_OPT):]
def startThread(target,args=[]):
        thread = threading.Thread(target=target,args=args)
        THREAD_LIST.append(thread)
        thread.start()
def startProcessing():
        GLOBAL_SIGNAL.set()
        threading.Thread(target=lambda: apiService.startApi(PLAYERS,CAPTURE_SOURCES,GLOBAL_SIGNAL)).start()
        startThread(target=capLoop)
        startThread(target=playerLoop)
def mainInit():
        initCams()
def main():
        sendMessage("Info","System Controller Starting")
        setStartOption()
        mainInit()
        startProcessing()
def playerLoop():
    while GLOBAL_SIGNAL.is_set():
        # sendMessage("Debug",PLAYERS)
        start = time.time()
        updatePlayers(PLAYERS)
        if(MAX_UPDATE_RATE>0):
            time.sleep(max(0,1/(MAX_UPDATE_RATE)-(time.time()-start)))
        framerate = 1/(time.time()-start+0.0001)
def capLoop():
    while GLOBAL_SIGNAL.is_set():
        if(len(CAP_LIST)==0):
            continue
        maxFPS = max([cap.framerate for cap in CAP_LIST])
        start = time.time()
        for cap in CAP_LIST:
            if(not (cap.camera.method == 0 and playerManager.SELF_UPDATE)):
                cap.updateImage()
        time.sleep(max(0,1/(maxFPS+1)-(time.time()-start)))
        framerate = 1/(time.time()-start+0.0001)
        # print(int(framerate))
def stopProcessing():
    GLOBAL_SIGNAL.clear()
def sendMessage(type,content):
    messenger.sendMessage(type,"SystemController",content)


def capFromId(id):
        return ffmpegCapture.capFromId(id)

def camFromId(id):
    cams = getListing()
    if(id>len(cams)or id<0):
        return
    return cams[id]
def getCams():
    return [c.name for c in getListing()]
def loadPlayer(capture,playerFile):
    if(type(capture)!= ffmpegCapture.VideoCap):
        capture=ffmpegCapture.capFromId(capture)
    player = Player.fromFile(capture)
    PLAYERS.append(player)
    return player

def createPlayer(name,capture=None):
    if(type(capture)!= ffmpegCapture.VideoCap):
        capture=ffmpegCapture.capFromId(capture)
    player = Player(name,capture)
    PLAYERS.append(player)
    if(capture):
        sendMessage("Info",f"Player \'{name}\' created on capture \'{capture.name}\'")
    else:
        sendMessage("Info",f"Player \'{name}\' created without assigned capture device")
    return player

def removePlayer(id):
    return PLAYERS.pop(id)
def getPlayer(id):
    if(id >=0 and id<len(PLAYERS)):
        return PLAYERS[id]
    return None
def modifyPlayer(id,attrDict):
    player = getPlayer(id)
    if(not player):
        return
    for key, value in attrDict.items():
        if(not hasattr(player,key)):
            continue
        if(key == "capture" and type(value)!=ffmpegCapture.VideoCap):
            value = capFromId(value)
        setattr(player,key,value)
def createCapture(camera,width=1280,height=720,framerate=60,preset="ultrafast"):
    sendMessage("Info",type(camera))
    if(type(camera)==cameraDetails):
        pass
    elif(type(camera)==str):
        camera = cameraDetails.fromFile(camera)
    elif(type(camera)==int):
        camera = camFromId(camera)
    if(camera):
        return ffmpegCapture.VideoCap.fromCam(camera,width,height,framerate,preset)
def modifyCapture(id,attrDict):
    cap = capFromId(id)
    if(not cap):
        return
    cap.deactivateSource()
    for key, value in attrDict.items():
        if(not hasattr(cap,key)):
            continue
        if(key == "camera" and type(value)!=cameraDetails):
            value = getListing()[value]
        setattr(player,key,value)
    cap.activateSource()

def setUpdateRate(rate):
        global MAX_UPDATE_RATE
        MAX_UPDATE_RATE = rate

def updatePlayers(players=PLAYERS):
        # return map(Player.updateStatus,players)
        # [Player.updateStatus(p) for p in players]
        [p.updateStatus() for p in PLAYERS]

def setPlayerCapture(player,capture):
    if(type(capture)!= ffmpegCapture.VideoCap):
        capture=ffmpegCapture.capFromId(capture)
    player.changeCaptureSource(capture)


def pulse():
    global last_pulse
    last_pulse = time.time()

def getpid():
    return os.getpid()
def stop():
    stopProcessing()
    apiService.eventLoop.stop()
    sys.exit()
def heartbeat(args="Test"):
    print("Is On")
    return args
def pulseCheck(limit):
    while GLOBAL_SIGNAL.is_set():
        sendMessage("Debug",f"Time since last pulse is \'{time.time()-last_pulse}\'")
        if(last_pulse!=-1 and time.time()-last_pulse>limit):
            stop()
            return
        time.sleep(limit)
def foo():
    return
def getCapImage(capture):
    return cv2.imencode(".png",capFromId(capture).currentImage)[1]

main()

    
