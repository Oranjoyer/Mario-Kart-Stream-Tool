# import interfaceLink
import sys
import json
import base64
import controller
import threading
import messenger
import time
import traceback
import queue
MAX_UPDATE_RATE = -1
def sendMessage(type="Info",content=""):
    messenger.sendMessage(type,"ApplicationLink",content)

inputQueue=queue.Queue()
dataStart = ":CMDSTART:"
dataEnd = ":CMDEND:"
def main():
    controller.startThread(controller.pulseCheck,[5])
    isReady()
    while (__name__=="__main__") or controller.GLOBAL_SIGNAL.is_set():
        # for line in sys.stdin:
        line = sys.stdin.readline()
        [inputQueue.put(st) for st in line.split("\n")]
        while not inputQueue.empty():
            input = inputQueue.get()
            try:
                readData(input)
            except Exception as e:
                sendMessage("Error",f"Invalid Request Made Error\nException: {e}\nTraceback: {traceback.format_exc()}")
        start = time.time()
        if(MAX_UPDATE_RATE!=-1):
            time.sleep(max(0,1/(MAX_UPDATE_RATE)-(time.time()-start)))
        framerate = 1/(time.time()-start+0.0001)
        
def receiveData():
    return sys.stdin.readline()
def readData(data=None):
    data = parseData(data)
    if(not data):
        return
    cmdReturn = receiveRequest(data.get("functionName"),data.get("args"),data.get("requestId"))

def getDataArea(data):
    startLen = len(dataStart)
    endLen = len(dataEnd)

    start = data.find(dataStart)
    end = data.find(dataEnd)
    if(start ==-1 or end == -1):
        return
    return data[start+startLen:end]


def parseData(data=None):
    if(not data):
        data = receiveData()
    if(len(data)==0):
        return None
    data = getDataArea(data)
    if(data):
        data = base64.b64decode(data).decode("utf-8")
    sendMessage(type="Debug",content=data)
    if(not data):
        return None
    try:
        parsed = json.loads(data)
        return parsed
    except(ValueError, json.JSONDecodeError):
        return None
def writeData(data):
    data = base64.b64encode(bytes(data,"utf-8")).decode("utf-8")
    print(f"{dataStart}{data}{dataEnd}")
    sys.stdout.flush()
def writeResponse(requestId,returnData):
    
    toWrite=json.dumps({"requestId":requestId,"response":str(returnData)})
    try:
        toWrite=json.dumps({"requestId":requestId,"response":returnData})
    except(TypeError):
        pass

    writeData(toWrite)
def receiveRequest(function,args=[],requestId=-1):
    returnVal = runCommand(function,args)
    if(requestId==-1):
        return
    writeResponse(requestId,returnVal)

def commandData(jData):
    data = json.loads(jData)
    return runCommand(data.get("function"),data.get("args"))
def runCommand(functionName,args=[]):
    func = getattr(controller,functionName)
    if(not args):
        args=[]
    return func(*args)
def isReady():
    sendMessage(content="Ready to go")
    sendMessage("Info",getFunctions())
    writeResponse(-3,getFunctions())
    # writeResponse(-3,None)
def getFunctions():
    return [m for m in dir(controller) if callable(getattr(controller,m))]
try:
    main()
except(KeyboardInterrupt):
    controller.stop()
    sendMessage("Info","Shutting Down")

