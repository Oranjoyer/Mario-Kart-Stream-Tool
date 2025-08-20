import subprocess
import messenger
import os
CAM_LIST = []
CaptureList = []
AUDIO_LIST =[]

NULL_METHOD = -1
FILE = 0
V4L2 = 1
DSHOW = 2

def sendMessage(type,content):
    messenger.sendMessage(type,"CamSystem",content)

def getCameras(method):
    listing = None
    if(method == V4L2):
        listing = parseCams("v4l2",subprocess.run(["v4l2-ctl", "--list-devices"], capture_output=True).stdout.decode("utf-8"))
    elif(method==DSHOW):
        listing = parseCams("dshow",subprocess.run(["ffmpeg","ffmpeg", "-list_devices", "true", "-f", "dshow"],capture_output=true).stdout.decode("utf-8"))
    return listing
def parseCams(method,str):
    camList = []
    str = str.splitlines()
    str.append("")
    # print(str)
    currentCamera = None
    aliases = []
    for camDetails in str:

        if(camDetails[0:1]=='\t'):
            aliases.append(camDetails[1:])
        else:
            if(currentCamera!=None):
                camList.append(cameraDetails(method,currentCamera,aliases))
                currentCamera = None
                aliases = []
            currentCamera = camDetails[:-1]
    return camList
def initCams():
    global CAM_LIST
    if(os.system == "nt"):
        CAM_LIST = getCameras(DSHOW)
    else:
        CAM_LIST = getCameras(V4L2)
def getListing():
    return CAM_LIST

class cameraDetails:
    def __init__(self,method,name,aliases):
        self.method = method
        self.name = name
        self.aliases = aliases
    def __str__(self):
        return self.name
    def identifier(self):
        id = None
        if(self in CAM_LIST):
            id = CAM_LIST.index(self)
        aliases = self.aliases
        return {"id":id,"aliases":aliases}
    def fromFile(path):
        method=FILE
        name = path
        aliases = [path]
        return cameraDetails(method,name,aliases)
