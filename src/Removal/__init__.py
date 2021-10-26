import Listing
import UserMgmt

import shutil
import os
import sys
import pickle

def parentDirHasBeenRemoved(removedDirs, item):
    for dir in removedDirs:
        lengthOfDirName = len(dir)
        if lengthOfDirName > len(item):
            continue
        elif item[:len(dir)] == dir:
            return True
    return False

def rmAssociatedFiles(pkgListing):
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
            
def rmDependencyListings(pkgListing):
    f = open("/usr/share/gpkg/dependencies.p", "rb")
    
    dependencyListingsNotRemoved = []
    while True:
        try:
            item = pickle.load(f)
            if item["parentPkg"] != pkgListing.name:
                dependencyListingsNotRemoved.append(item)
        except EOFError:
            break
    
    f.close
    with open("/usr/share/gpkg/dependencies.p", "wb") as f:
        for i in dependencyListingsNotRemoved:
            pickle.dump(i, f)

def remove(pkgName):
    pkgListing = Listing.getInfoFor(pkgName)
    
    if pkgListing.hasParentPkgs():
        sys.exit("[Removal] Cannot remove this package, packages depend on it: " + str(pkgListing.parentPkgs))

    rmAssociatedFiles(pkgListing)
    rmDependencyListings(pkgListing)
    UserMgmt.rmUser(pkgListing.name)
