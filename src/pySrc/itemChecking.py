from referenceManager import getReference,loadReferences
from referenceMatching import Reference, compareGroup

ITEM_LIST_PRIME = []
ITEM_LIST_SECOND = []
ITEM_NAMES = ("Empty","Coin","Red Shell","Double Red Shells","Triple Red Shells","Green Shell","Double Green Shells","Triple Green Shells","Mushroom","Double Mushrooms","Triple Mushrooms","Banana","Double Bananas","Triple Bananas","Boomerang","Golden Mushroom","Bullet Bill","Star","Blooper","Lightning","Piranha Plant","Boo","Fire Flower","Blue Shell","Crazy 8")
ITEM_ABBR = ("None","Coin","Red","DoubleRed","TripleRed","Green","DoubleGreen","TripleGreen","Shroom","DoubleShroom","TripleShroom","Banana","DoubleBanana","TripleBanana","Boomerang","GoldShroom","Bullet","Star","Blooper","Shock","Plant","Boo","Fire","Blue","Eight")
ITEM_PAIRS = dict(zip(ITEM_NAMES,ITEM_ABBR))

def getItemRefs():
    for name,item in ITEM_PAIRS.items():
            ref1 = getReference("Prime"+item)
            if(ref1):
                ITEM_LIST_PRIME.append((name,ref1))
            ref2 = getReference("Second"+item)
            if(ref2):
                ITEM_LIST_SECOND.append((name,ref2))
    # print([i[0] for i in ITEM_LIST_PRIME])
    # print(len(ITEM_LIST_PRIME),len(ITEM_LIST_SECOND))
def getItemList():
    return (ITEM_LIST_PRIME,ITEM_LIST_SECOND)

def checkItems(img):

    item1 = checkSlot(img,0)
    if(item1 == 0):
        return ("Unknown","Unknown")
    item2 = checkSlot(img,1)
    slot1 = "Unknown"
    if(item1!=-1):
        slot1 = item1
    slot2 = "Unknown"
    if(item2 != -1):
        slot2 = item2
    return (slot1,slot2)

def checkSlot(img,slot):
    listing = ITEM_LIST_PRIME
    if(slot == 1):
        listing = ITEM_LIST_SECOND
    compared = compareGroup([i[1] for i in listing],img)
    if(compared[0] != None):
        return listing[compared[1]][0]
    return -1
getItemRefs()