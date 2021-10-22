import Listing
import UserMgmt

import shutil
import os


def parentDirHasBeenRemoved(removedDirs, item):
    for dir in removedDirs:
        lengthOfDirName = len(dir)
        if lengthOfDirName > len(item):
            continue
        elif item[:len(dir)] == dir:
            return True
    return False



def remove(pkgName):
    pkgListing = Listing.getInfoFor(pkgName)

    ## Remove Associated Files ##
    print("[Removal] Removing associated files")
    removedDirectories = []
    for item in pkgListing.installedFiles:
        ##If Parent Directory of file or dir has been removed,
        ##Then we should continue to the next item
        if parentDirHasBeenRemoved(removedDirectories, item):
            continue

        if os.path.isfile(item):
            os.remove(item)
        else:
            shutil.rmtree(item)
            removedDirectories.append(item)

    ## Delete Associated User ##
    UserMgmt.rmUser(pkgListing.name)