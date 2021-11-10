import os
import sys

import List

def remove(pkgName):
    pkgListing = List.findPkg(pkgName)
    if pkgListing == None:
        sys.exit("[Remove] Cannot remove package that is not installed: '" + pkgName + "'")
    
    #Files and dirs sorted by depth
    filesToBeRemoved = sorted(pkgListing.fakeRootMap.files, key=lambda dir: dir.count('/'), reverse=True)
    dirsToBeRemoved = sorted(pkgListing.fakeRootMap.dirs, key=lambda dir: dir.count('/'), reverse=True)


    for i in filesToBeRemoved:
        try:
            print("[Remove] Removing file: " + i)
            os.remove(i)
        except Exception as e:
            print("[Remove]", type(e).__name__, "-->", str(e))   #TODO: MOve to handlefailed     
            handleFailedRemoval(i)
        
    for i in dirsToBeRemoved:
        try:
            print("[Remove] Removing directory: " + i)
            os.rmdir(i)
        except Exception as e:
            print("[Remove]", type(e).__name__, "-->", str(e))        
            handleFailedRemoval(i)

    List.removeListingOn(pkgName)

def handleFailedRemoval(itemName):
    print("[Remove] Could not delete item '" + itemName + "'")
    shouldContinue = input("\tShould removal process continue? [y/N] ")

    if shouldContinue != "y" and shouldContinue != "Y":
        sys.exit(1)

def removeOrphaned():
    orphaned = List.listOrphanedDepends()

    for i in orphaned:
        remove(i)