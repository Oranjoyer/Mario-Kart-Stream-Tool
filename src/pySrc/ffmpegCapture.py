import subprocess
import numpy as np
import threading
import os
import messenger
from cameraSystem import NULL_METHOD,V4L2,DSHOW,FILE
from globals import FFMPEG_BINARY
DEF_PORT = 21732
FLUSH_LIMIT_FAC = 5
CAP_LIST = []
ID_VALUES = 0
#["ffmpeg","-video_size",f"{wid}x{height}","-framerate",f"{framerate}","-i","/dev/video0","-vcodec","rawvideo","-an","-sn","-pix_fmt","bgr24","-f","image2pipe","-","-vcodec","libx264","-f","mpegts","udp://localhost:21623"]
FFMPEG_VAAPI = (("-vaapi_device","/dev/dri/renderD128"),("-vf","format=nv12,hwupload","-vcodec","h264_vaapi"))
FFMPEG_CPU = ((""),("-vcodec","libx264"))

CPU = 0
VAAPI = 1

# Send Message to Logs
def sendMessage(type,content):
    messenger.sendMessage(type, "CaptureManager",content)
def capFromId(id):
    for cap in CAP_LIST:
        if(cap.id == id):
            return cap
def parseArgs(source,sourceType,width,height,framerate,encoder,preset,port):
    args = [FFMPEG_BINARY]
    outputArgs2 = ["-f","mpegts",f"udp://localhost:{port}"]
    if(sourceType==FILE):
        outputArgs2 = ["-r",f"{framerate}","-vf",f"scale={width}:{height}"] + outputArgs2
    if(encoder == VAAPI):
        args += FFMPEG_VAAPI[0]
        outputArgs2 = list(FFMPEG_VAAPI[1]) + ["-preset",preset] + outputArgs2
    else:
        outputArgs2 = list(FFMPEG_CPU[1]) +["-preset",preset] + outputArgs2
    outputArgs1 = ["-vcodec","rawvideo","-an","-sn","-pix_fmt","bgr24","-f","image2pipe","-"]
    if(sourceType==FILE):
        outputArgs1 = ["-r",f"{framerate}","-vf",f"scale={width}:{height}"] + outputArgs1
    sourceArgs = ["-s",f"{width}x{height}", "-framerate",f"{framerate}","-i",source.aliases[0]]
    if(sourceType==FILE):
        sourceArgs = sourceArgs[4:]
    if(sourceType == DSHOW):
        sourceArgs = ["-f","dshow","-s",f"{width}x{height}","-video_device_number",source.aliases[0]] + sourceArgs
        sourceArgs[-1] = f"video=\"{source.name}\""
    elif(sourceType == V4L2):
        sourceArgs[-1] = source.aliases[0]
    args = args + sourceArgs + outputArgs1 + outputArgs2
    return args

class VideoCap:
    def fromCam(camera,width=1280,height=720,framerate=60,preset="ultrafast"):
        # self.name = camera.name
        # self.camera = camera
        # self.height = height
        # self.width = width
        # self.framerate = framerate
        # self.streamCodec = VAAPI
        # self.port = -1
        # self.proc = None
        # self.currentImage = None
        # CAP_LIST.append(self)
        return VideoCap(camera.name,camera,width,height,framerate)
    def __init__(self,name,camera,width,height,framerate,preset="ultrafast",port=-1):
        global ID_VALUES
        self.id = ID_VALUES
        ID_VALUES += 1
        self.name = name
        self.camera = camera
        self.height = height
        self.width = width
        self.preset = preset
        self.framerate = framerate
        self.streamCodec = 0
        self.port = port
        self.proc = None
        self.currentImage = None
        self.currentFrame = 0
        self.active = False
        CAP_LIST.append(self)

    def getArgs(self):
        # if(os.name == "nt"):
        #     return [FFMPEG_BINARY,"-f","dshow","-video-size",f"{self.width}x{self.height}","-framerate",f"{self.framerate}","-i",f"video=\"{self.camera}\"","-vcodec","rawvideo","-an","-sn","-pix_fmt","bgr24","-f","image2pipe","-","-vcodec",f"{libx264}","-f","mpegts",f"udp://localhost:{port}"]
        # return [FFMPEG_BINARY,"-video_size",f"{self.width}x{self.height}","-framerate",f"{self.framerate}","-i",f"{self.camera}","-vcodec","rawvideo","-an","-sn","-pix_fmt","bgr24","-f","image2pipe","-","-vcodec","libx264","-preset", "ultrafast","-f","mpegts",f"udp://localhost:{self.port}"]
        return parseArgs(self.camera,self.camera.method,self.width,self.height,self.framerate,self.streamCodec,self.preset,self.port)
    def isActive(self):
        return self.active
    def activateSource(self,port=-1):
        if(self.proc != None):
            return
        if(port!=-1):
            self.port = port
        elif(self.port==-1):
            global DEF_PORT
            self.port = DEF_PORT
            DEF_PORT+=1
        #stderr=subprocess.DEVNULL,
        self.proc = subprocess.Popen(self.getArgs(),stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,bufsize=10)
        self.active = True
        if(self.camera.method != FILE):
            threading.Thread(target=self.updateSelf).start()
        sendMessage("Info",f"Capture Source \'{self.name}\' activated")
        if(self not in CAP_LIST):
            CAP_LIST.append(self)
    def updateSelf(self):
        while self.active:
            self.updateImage()
    def deactivateSource(self):
        self.active = False
        if(self.proc==None):
            return
        self.proc.terminate()
        self.proc = None
        CAP_LIST.remove(self)
    def updateImage(self):
        if(self.proc == None):
            sendMessage("Error",f"Capture Source \'{self.name}\' deactivated. Unable to update Image")
            return
        raw = self.proc.stdout.read(self.width*self.height*3)
        self.currentFrame+=1
        # self.proc.stdout.flush()
        image = np.frombuffer(raw,dtype='uint8')
        if(image.size==0):
            sendMessage("Warning",f"No video feed in capture source \'{self.name}\' closing stream")
            self.deactivateSource()
            return
        self.currentImage = image.reshape((self.height,self.width,3))
    def dict(self):
        temp = self.__dict__.copy()
        if(self.camera):
            temp["camera"] = self.camera.id
        temp.pop("currentImage")
        return temp
    def getImage(self):
        return self.currentImage

