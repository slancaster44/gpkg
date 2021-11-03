import os
import sys
import pickle

#finds package using findPkg()
#and prints info about it
def listPkg(pkgName):
    pkg = findPkg(pkgName)
    if pkg == None:
        print("[List] Package does not exist: '" + pkgName + "'")
    else:
        print(pkg.basicInfoAsStr())

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
    if not os.path.exists("/var/lib/gpkg/pkgdata.p"):
        sys.exit("[List] No packages installed")

    setOfAllPkgs = []
    with open("/var/lib/gpkg/pkgdata.p", "rb") as f:
        while True:
            try:
                setOfAllPkgs.append(pickle.load(f))
            except EOFError:
                break

    return setOfAllPkgs

def saveListingOn(pkgdata):
    if not os.path.exists('/var/lib/gpkg'):
        os.mkdir('/var/lib/gpkg')

    with open('/var/lib/gpkg/pkgdata.p', 'ab') as f:
        pickle.dump(pkgdata, f)

def removeListingOn(pkgName):
    allPkgs = loadAllPkgs()
    pkgsNotIncludingToBeRemoved = [x for x in allPkgs if x.name != pkgName]

    with open("/var/lib/gpkg/pkgdata.p", "wb") as f:
        for i in pkgsNotIncludingToBeRemoved:
            pickle.dump(i, f)