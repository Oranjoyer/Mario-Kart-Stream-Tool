from referenceMatching import *
import fileService
import json
REF_DIR = "./ReferenceData/"
GAME_DIRS = ("MK8DX","MKW")
SUB_DIRS = ("Tracks","Places","Items")
REF_LIST = []

def loadReferences():
    global REF_LIST
    files = fileService.loadFilesFromQueries(f"{REF_DIR}/MK8DX/",".json")
    for subdir in SUB_DIRS:
        files += fileService.loadFilesFromQueries(f"{REF_DIR}/MK8DX/{subdir}/",".json")
    REF_LIST = [Reference.importFromDict(json.loads(f.fileData)) for f in files]
    # print([ref.name for ref in REF_LIST])
def getReference(name):
    for ref in REF_LIST:
        if(ref.name == name):
            return ref
    return None
loadReferences()
