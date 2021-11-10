import os
import sys
import pickle
import Depends

import Utils
from Depends import installedDepends

#finds package using findPkg()
#and prints info about it
def listPkg(pkgName):
    pkg = findPkg(pkgName)
    if pkg == None:
        print("[List] Package does not exist: '" + pkgName + "'")
    else:
        print(pkg.basicInfoAsStr())

def listDepends(pkgName):
    if not isInstalled(pkgName):
        sys.exit("[List] Cannot list dependencies of package that is not installed: " + pkgName)

    dependsTree = installedDepends.getDependsTree()
    depends = dependsTree.getDependsOf(pkgName)

    print("[List] Dependencies of:", pkgName, "--", depends)

def listAssociated(pkgName):
    pkg = findPkg(pkgName)
    if pkg == None:
        print("[List] Package does not exist: '" + pkgName + "'") 
    else:
        print(pkg)

#Returns None if package does not exist
#returns pkg metadata if it does
def findPkg(pkgName):
    allPkgs = loadAllPkgs()
    
    listOfMatchingPackages = [x for x in allPkgs if x.name == pkgName]
    
    if len(listOfMatchingPackages) == 0:
        return None

    return listOfMatchingPackages[0]

def isInstalled(pkgName):
    pkgInfo = findPkg(pkgName)
    return pkgInfo != None    

def loadAllPkgs():
    if not os.path.exists("/var/lib/dmi/pkgdata.p"):
        return []

    setOfAllPkgs = []
    with open("/var/lib/dmi/pkgdata.p", "rb") as f:
        while True:
            try:
                setOfAllPkgs.append(pickle.load(f))
            except EOFError:
                break

    return setOfAllPkgs

def saveListingOn(pkgdata):
    print("[List] Creating listing for: " + pkgdata.name)
    Utils.ensureLibDmi()

    with open('/var/lib/dmi/pkgdata.p', 'ab') as f:
        pickle.dump(pkgdata, f)

def removeListingOn(pkgName):
    print("[List] Removing listing for: " + pkgName)
    allPkgs = loadAllPkgs()
    pkgsNotIncludingToBeRemoved = [x for x in allPkgs if x.name != pkgName]

    with open("/var/lib/dmi/pkgdata.p", "wb") as f:
        for i in pkgsNotIncludingToBeRemoved:
            pickle.dump(i, f)

def rmAssocItemFromPkg(itemLocation, pkgName):
    absItemLoc = os.path.abspath(itemLocation)

    pkgData = findPkg(pkgName)
    if pkgData == None:
        sys.exit("[List] Cannot remove association from a package that is not installed: " + pkgName)

    if absItemLoc in pkgData.fakeRootMap.dirs:
        pkgData.fakeRootMap.dirs.remove(absItemLoc)
    elif absItemLoc in pkgData.fakeRootMap.files:
        pkgData.fakeRootMap.files.remove(absItemLoc)

    updateListing(pkgData)

def associateNewItemWithPkg(itemLocation, pkgName):
    absItemLoc = os.path.abspath(itemLocation)

    if not os.path.exists(itemLocation):
        sys.exit("[List] Cannot associate non-expkgData.nameistant file: " + absItemLoc)

    pkgData = findPkg(pkgName)
    if pkgData == None:
        sys.exit("[List] Cannot associate with a package that is not installed: " + pkgName)    

    itemType = Utils.pathType(absItemLoc)
    if itemType == "file":
        associateFileWith(absItemLoc, pkgData)
    else:
        associateDirWith(absItemLoc, pkgData)

def associateFileWith(fileLoc, pkgData):
    if fileLoc in pkgData.fakeRootMap.files:
        sys.exit("[List] "+ fileLoc +" is already associated with "+pkgData.name)

    pkgData.fakeRootMap.files.append(fileLoc)
    updateListing(pkgData)

def associateDirWith(fileLoc, pkgData):
    if fileLoc in pkgData.fakeRootMap.dirs:
        sys.exit("[List] "+ fileLoc +" is already associated with "+pkgData.name)

    pkgData.fakeRootMap.dirs.append(fileLoc)
    updateListing(pkgData)

def updateListing(pkgData):
    removeListingOn(pkgData.name)
    saveListingOn(pkgData)

def listOrphanedDepends():
    allInstalled = loadAllPkgs()
    dependsTree = installedDepends.getDependsTree()

    orphanedDepends = []
    for i in allInstalled:
        if not dependsTree.hasKey(i.name):
            orphanedDepends.append(i.name)
    return orphanedDepends