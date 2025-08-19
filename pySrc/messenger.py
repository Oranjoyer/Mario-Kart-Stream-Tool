import time
import sys
APP_Mode = False
logLine = []
LOG_LEVELS=("NONE","Error","Warning","Info","Debug","ALL")
LOG_LEVEL = 3

class Message:
    def __init__(self,type,source,content):
        self.type = type
        self.source = source
        self.content = content
        self.time = time.ctime()
    def __str__(self):
        return f" {self.time} :: {self.type} | {self.source} : {self.content}"

def sendMessage(type,source,content):
    mess = Message(type,source,content)
    logLine.append(mess)
    # sys.stdout.flush()
    printMessage(mess)

def printMessage(message):
    if(checkLogLevel(message.type)):
        print(message,file=sys.stderr)

def getLogLevel(level):
    index = 0
    for type in LOG_LEVELS:
        if(level == type):
            return index
        index += 1
    return index
def checkLogLevel(level):
    return getLogLevel(level) <= LOG_LEVEL

def formatLog():
    logStr = ""
    for mess in logLine:
        logStr += f"{mess}\n"
    return logStr
