import os
import messenger as logManager
import cv2
import csv
import numpy as np
from io import BufferedReader
from zipfile import ZipFile

ASSETS_FOLDER = "assets"
PLACE_TEMPLATE_FOLDER = "placeTemplates"
RACE_PROGRESS_FOLDER = "raceProgress"
RESULT_FOLDER = "result"
DATA_FOLDER = "dataSets"
RACE_DATA_FOLDER = "raceData"


IMAGE_EXTENSIONS=(".jpg",".gif",".png",".tiff",".svg")
CSV_EXT = ".csv"
PLAINTEXT_EXT = (".txt",".json",".ini",".cfg",".js",".htm",".html")
BASE_PATH="./"
ZIP_EXT = ".zip"
fileList = []
# Class That Stores Data associated with a file. Formats as the proper filetype 
class FileContainer:
    def __init__(self,name,file,path,typeOf):
        self.name = name
        self.path = path
        self.fileData = None
        if(type(file)==BufferedReader):
            self.fileData = file.read()
            file.close()
        if(typeOf=="ZIP"):
            self.fileData = ZipFile(path,'r')
        elif(typeOf == "CSV"):
            self.fileData = csv.DictReader(open(path,'r'),delimiter=",")
        elif(file==None):
            self.fileData = open(path, 'r')
        elif((typeOf == "Text")):
            self.fileData = self.fileData.decode("utf-8")
        elif(typeOf == "Image"):
            self.fileData = np.frombuffer(self.fileData,np.uint8)
            self.fileData = cv2.imdecode(self.fileData, cv2.IMREAD_COLOR)
    def __str__(self):
        self.fileData


# Sends Log Message with 'FileService' source
def sendMessage(type,message):
    logManager.sendMessage(type, "FileService", message)

# Loads file into memory or retrieves file from list; returns file
def loadFile(filePath,name):
    # sendMessage("Info", "Checking for preloaded files; disregard 2 potential error messages")
    nameFile = getFileByName(name,True)
    pathFile = getFileByPath(filePath,True)
    fileType = "Bytes"
    for imgExt in IMAGE_EXTENSIONS:
        if(imgExt == filePath[-len(imgExt):]):
            fileType = "Image"
    if(CSV_EXT in filePath[-len(CSV_EXT):]):
            fileType = "CSV"
    for extend in PLAINTEXT_EXT:
        if(extend in filePath[-len(extend):]):
            fileType = "Text"
    if(ZIP_EXT in filePath[-len(ZIP_EXT):]):
            fileType = "ZIP"
    if(nameFile != None):
        sendMessage("Debug",f"File by name \'{name}\' already loaded. Retrieving preloaded file instead")
        return nameFile
        # break
    elif(pathFile != None):
        sendMessage("Debug",f"File at path \'{filePath}\' already loaded. Retrieving preloaded file instead")
        return pathFile
        # break
    elif(not(os.path.isfile(filePath))):
        sendMessage("Error",f"No file at path \'{filePath}\' returning null value instead of loading file")
        return None
        # break
    elif(not(os.access(filePath, os.R_OK))):
        sendMessage("Error",f"Insufficient permissions to load file at path \'{filePath}\' returning null value instead of loading file")
        return None
        # break
    loadedFile = FileContainer(name,open(filePath, "rb"),filePath,fileType)
    sendMessage("Debug",f"Successfuly loaded file \'{name}\' at \'{filePath}\'")
    fileList.append(loadedFile)
    return loadedFile

# Stores file from bytes or retrieves file with desired name
def loadFileFromMemory(fileData,name,fileType):
    # sendMessage("Info", "Checking for preloaded files; disregard 1 potential error messages")
    nameFile = getFileByName(name)
    if(nameFile != None):
        sendMessage("Debug", f"File by name \'{name}\' already loaded. Retrieving preloaded file instead")
        return getFileByName(name)
    fileBytes = fileData
    loadedFile = FileContainer(name,fileBytes,"From Memory",fileType)
    fileList.append(loadedFile)
    return loadedFile

# Retrieves stored file with specific name
def getFileByName(name,*suppress):
    for file in fileList:
        if(file.name == name):
            return file
    if(True not in suppress):
        sendMessage("Error", f"No preloaded file found with name \'{name}\' returning null value instead")
    return None

# Retrieves stored file with specific path
def getFileByPath(path,*suppress):
    for file in fileList:
        if(file.path == path):
            return file
    if(True not in suppress):
        sendMessage("Error", f"No preloaded file found with path \'{path}\' returning null value instead")
    return None

# Retrieves Index value in list of stored file with specific name
def getFileIndexByName(name,*suppress):
    for i in range(len(fileList)):
        if(fileList[i].name==name):
            return i
    if(True not in suppress):
        sendMessage("Error", f"No preloaded file found with name \'{name}\' returning null index instead")
    return -1

# Retrieves Index value in list of stored file with specific path. Add True as arg to suppress errors
def getFileIndexByPath(path,*suppress):
    for i in range(fileList.len()):
        if(fileList[i].path==path):
            return i
    if(True not in suppress):
        sendMessage("Error",f"No preloaded file found with path \'{path}\' returning null index instead")
    return -1


def unloadFilesFromNameList(*fileNames):
    sendMessage("Debug",f"Removing Files With Names: {fileNames}")
    for name in fileNames:
        unloadFileByName(name)

# Unloads file with specific name from memory
def unloadFileByName(name):
    fileIndex = getFileIndexByName(name)
    if(fileIndex == -1):
        sendMessage("Error",f"No preloaded file found with name \'{name}\' removing no files from memory")
        return
    fileList[fileIndex].file.close()
    fileList.pop(fileIndex)
    sendMessage("Debug",f"Successfully removed file with name \'{name}\' from memory")
    return

# Removes file with specific path from memory
def unloadFileByPath(path):
    fileIndex = getFileIndexByPath(path)
    if(fileIndex == -1):
        sendMessage("Error",f"No preloaded file found with path \'{path}\' removing no files from memory")
        return
    fileList[fileIndex].file.close()
    fileList.pop(fileIndex)
    sendMessage("Debug",f"Successfully removed file with path \'{path}\' from memory")
    return

# Finds Files in Directory based on Query list. Including a '!' as the first character and then the query wrapped in quotes marks exclusion
def listFilesInDir(dir,queries):
    if(not os.path.exists(dir)):
        sendMessage("Error",f"Path \'{dir}\' doesn't exist")
        return []
    allInDir = os.listdir(dir)
    # files = [f for f in allInDir if(os.path.isfile(formatStringsAsPath(dir,f)))]
    files = []
    for f in allInDir:
        filePath = formatStringsAsPath(dir)+f
        sendMessage("ExInfo",f"Checking if path \'{filePath}\' is a file")
        if(os.path.isfile(filePath)):
            files.append(f)
            sendMessage("ExInfo",f"\'{f}\' is a file")

    for q in queries:
        if(q == "endSearch"):
            break
        sendMessage("ExInfo",f"Current Amount of applicable entries before filtering for \'{q}\': {len(files)}")
        removeString = False
        currentQuery = q

        # Check for Exclusion Parameter
        if q[0]=='!':
            removeString = True
            currentQuery = stringInQuotes(q[1:])
        
        # Check If Remaining Files Apply to Query
        if(removeString):
            files = [f for f in files if currentQuery not in f]
        else:
            files = [f for f in files if currentQuery in f]
        # for f in files:
        #     queryApplicable=not(checkStringForQuery(f,currentQuery,not(removeString)))
        #     sendMessage("ExInfo",f"Checking File \'{f}\' for query \'{q}\' |\t Remove: {queryApplicable}")
        #     if(queryApplicable):
        #         files.remove(f)
    return files

# Loads Files from Directory into the FileService based on Query list. Including a '!' as the first character and then the query wrapped in quotes marks exclusion
def loadFilesFromList(dir, fileList):
    returnedList = []
    if (dir[-1]!= "/") | (dir[-1] != "\\"):
        dir + "/"
    for f in fileList:
        temp = loadFile(dir+f,f)
        if(type(temp)==FileContainer):
            returnedList.append(temp)
    if(len(returnedList) == 0):
        sendMessage("Warning",f"No Files Found with names \'{fileList}\' in directory \'{dir}\'")
    return returnedList

# Loads All Files in a Directory based on Query List. Including a '!' as the first character and then the query wrapped in quotes marks exclusion 
def loadFilesFromQueries(dir,queries):
    sendMessage("Debug",f"Loading all files found in directory \'{dir}\' based on queries: {queries}")
    return loadFilesFromList(dir,listFilesInDir(dir,queries))

# Formats Multiple Strings as proper Path
def formatStringsAsPath(*str):
    path = ""
    for s in str:
        if (len(s)!=0):
            path +=s
        if(s[-1]!="/"):
            path += "/"
    return path

# Checks whether string has or doesn't have a query based on whether it is desired
def checkStringForQuery(str,query,desired):
    if(query in str):
        return desired
    return not(desired)

# Returns all the characters contained in quotes within a string as a list of groups. If String does not contain quotes, the function will return the passed string
def stringInQuotes(unfStr):
    strList = []
    currentString = ""
    startQuote = False
    quoteType = ''
    if ("\'" not in unfStr) & ("\"" not in unfStr):
        sendMessage("Warning",f"String \'{unfStr}\' passed into \'stringInQuotes\' function without any quotes. Returning string as is")
        return unfStr
    elif(totalQuotes(unfStr)%2!=0):
        sendMessage("Warning",f"String \'{unfStr}\' passed into \'stringInQuotes\' function with odd number of quotes. String may not format properly. Avoid adding extra quotes in String")
    for letter in unfStr:
        if((letter == '\'' | letter == '\"') & startQuote == False):
            startQuote = True
            quoteType = letter
            sendMessage("ExInfo", f"QuoteType is set to \'{letter}\'")
        elif((letter == '\'' | letter == '\"') & letter != quoteType):
            sendMessage("Warning",f"Non-Matching Quotes Present in String \'{unfStr}\'. Avoid Adding Extra Quotes in String")
        elif(letter == quoteType):
            startQuote = False
            strList.append(currentString)
        else:
            currentString += letter
    return strList

# Counts total number of quotes in string
def totalQuotes(str):
    return str.count("\'")+str.count("\"")