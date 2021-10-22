import os
import shutil
import subprocess
from zipfile import ZipFile
import tarfile
import sys

import Installation.Pkg as Pkg
import UserMgmt



uniqueID = "gpkg" + str(os.getpid())
tmpLocation = "/tmp/" + uniqueID
tmpPkgLoc = tmpLocation + "/Pkg.gpkg"

def createTmpEnv(pkgLocation):
    os.mkdir(tmpLocation)
    os.chdir(tmpLocation)

    shutil.copyfile(pkgLocation, tmpPkgLoc)

def removeTmpEnv():
    subprocess.run(["rm", "-r", tmpLocation])

def unzipPkg():
    zip = ZipFile(tmpPkgLoc, 'r')
    zip.extractall()

def getPkgAsObj():
    return Pkg.Package(tmpLocation)

def failOut(pkgName, message):
    removeTmpEnv()
    UserMgmt.rmUser(pkgName)
    sys.exit(message)

def install(pkgLocation):
    if not os.path.isfile(pkgLocation) and \
        pkgLocation[:-5] != ".gpkg":
        sys.exit("[Install] File is not gpkg")

    createTmpEnv(pkgLocation)
    unzipPkg()


    pkgObj = getPkgAsObj()

    print("[Install] Decompressing package tarball... ")
    pkgObj.unTar()
    print("\tDone")

    os.chdir(pkgObj.extractedTarballLocation)

    if UserMgmt.doesUserExist(pkgObj.name):
        removeTmpEnv()
        print("[Install] Cannot create pkg-specific user for: " + pkgObj.name)
        sys.exit("\tNote: User already exists")

    UserMgmt.mkUser(pkgObj.name)
    UserMgmt.givePermissionToUser(pkgObj.name, pkgObj.directoryLocation)

    if pkgObj.preShLocation != None:
        print("[Install] Running pre-installation script")
        pkgObj.runPreSh()

    print("[Install] Running build script")
    pkgObj.runBuildSh()

    if pkgObj.postShLocation != None:
        print("[Install] Running post-installation script")
        pkgObj.runPostSh()

    saveLocation = "/home/"+pkgObj.name+"/installation_files"
    print("[Install] Saving pkg files to:", saveLocation)
    shutil.copytree(tmpLocation, saveLocation)

    removeTmpEnv()