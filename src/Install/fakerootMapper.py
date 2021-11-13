import os
import re
import sys

class FakerootMap:
    def __init__(self):

        self.files = []
        self.dirs = []

def mapFakeroot(location):
    fkmap = FakerootMap()

    for root, dirs, files in os.walk(location):
        dirs = getAbsRootPathsOf(dirs, root, location)
        files = getAbsRootPathsOf(files, root, location)

        fkmap.files += files
        fkmap.dirs += dirs

    return fkmap

def getAbsRootPathsOf(items, root, location):
    items = [root + "/" + x for x in items]
    items = [re.sub(location + "/", "/", x) for x in items]

    returnItems = []
    for i in items:
        if not os.path.exists(i):
            returnItems.append(i)
        else:
            shouldOverwrite = handleExistingItem(i)
            if shouldOverwrite: returnItems.append(i)
        

    return returnItems

def handleExistingItem(item):
    if os.path.isfile(item):
        print("[Fakeroot Mapper] '" + item + "' already exists")
        shouldOverwrite = input("\tShould this item be overwritten during install [Y/n] ")
        if shouldOverwrite == "N" or shouldOverwrite == "n":
            sys.exit(1)
        return True
    else:
        return False


