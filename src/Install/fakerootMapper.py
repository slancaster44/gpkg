import os
import re
import sys

class FakerootMap:
    def __init__(self):

        self.files = []
        self.dirs = []

    def __str__(self):
        out = "--Files to Be Installed--"
        for i in self.files:
            out += i + "\n"

        print("--Directories to Be Created--")
        for i in self.dirs:
            out += i + "\n"

        return out

def mapFakeroot(location):
    fkmap = FakerootMap()

    for root, dirs, files in os.walk(location):
        dirs = getAbsRootPathsOf(dirs, root, location)
        dirs = [x for x in dirs if not os.path.exists(x)]
        files = getAbsRootPathsOf(files, root, location)

        fkmap.files += files
        fkmap.dirs += dirs

    return fkmap

def getAbsRootPathsOf(items, root, location):
    items = [root + "/" + x for x in items]
    items = [re.sub(location + "/", "/", x) for x in items]

    return items


