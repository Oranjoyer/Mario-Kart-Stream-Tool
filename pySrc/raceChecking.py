from referenceManager import getReference
from referenceMatching import Reference, compareGroup
PLACE_NAMES = ("1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th","11th","12th")
PLACE_REFS = []
TEAM_REFS = []

TEAM_COLORS=(
    getReference("NoTeam"),
    getReference("RedTeam"),
    getReference("BlueTeam")
)

GO_REF = getReference("Go!")
FIN_REF = getReference("Finish")
MAP_REF = getReference("MinimapIcon")

LAP_BOX_COORD=(0,0)

def loadPlaceRef():
    global PLACE_REFS
    PLACE_REFS = [getReference(pn) for pn in PLACE_NAMES]
    global TEAM_REFS
    TEAM_REFS = ([getReference(f"{pn}Red") for pn in PLACE_NAMES],[getReference(f"{pn}Blue") for pn in PLACE_NAMES])


def checkPlace(img,teamNum=-1,playercount=12):
    refs=PLACE_REFS[:playercount]
    if(teamNum == -1):
        return max((checkPlace(img,i,playercount) for i in range(3)))
    elif(teamNum!=0):
        refs = TEAM_REFS[teamNum-1][:playercount]
    compared = compareGroup(refs,img)
    # print(compared)
    if(compared[0] != None):
        return compared[1]+1
    return 0
def checkTeam(img):
    return compareGroup(TEAM_COLORS,img)[1]
def checkProg(img,raceGoing="False"):
    goCheck = GO_REF.checkImage(img)
    if(goCheck[0]):
        return 1
    
    if(raceGoing):
        return 0
    
    finCheck = FIN_REF.checkImage(img)
    if(finCheck[0]):
        return 2
    # print(goCheck)
    # print(goCheck)

    return 0
def isFinished(img):
    if(FIN_REF.checkImage(img)[0]):
        return True
    return False
def isStart(img):
    if(GO_REF.checkImage(img)[0]):
        return True
    return False
def findPos(img):
    MAP_REF.scanImage(img)

loadPlaceRef()