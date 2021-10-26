import os
import shutil
import subprocess
from zipfile import ZipFile
import tarfile
import sys

import Installation.Pkg as Pkg
import UserMgmt
import Listing



uniqueID = "gpkg" + str(os.getpid())
tmpLocation = "/tmp/" + uniqueID
tmpPkgLoc = tmpLocation + "/Pkg.gpkg"

def createTmpEnv(pkgLocation):
    os.mkdir(tmpLocation)
    os.chdir(tmpLocation)


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

def ensureScriptHasRunProperly(pkgName, script):
    confirmation = input("[Install] Has " + script + " been run properly (y/N)? ")
    if confirmation != "y" and confirmation != "Y":
        failOut(pkgName, "[Install] Failing out of installation")

def install(pkgLocation):
    if os.path.isfile(pkgLocation) and pkgLocation[-5:] == ".gpkg":
        installGpkg(pkgLocation)
    elif os.path.isdir(pkgLocation):
        shutil.copytree(pkgLocation, tmpLocation)
        os.chdir(tmpLocation)
        installDirectory()
    else:
        sys.exit("[Install] File is not gpkg")

def installGpkg(pkgLocation):
    createTmpEnv(pkgLocation)
    shutil.copyfile(pkgLocation, tmpPkgLoc)

    unzipPkg()
    installDirectory()

def installDirectory():
    pkgObj = getPkgAsObj()

    print("[Install] Decompressing package tarball... ")
    pkgObj.unTar()
    print("\tDone")

    os.chdir(pkgObj.extractedTarballLocation)
    pkgObj.checkDepends()

    if UserMgmt.doesUserExist(pkgObj.name):
        removeTmpEnv()
        print("[Install] Cannot create pkg-specific user for: " + pkgObj.name)
        sys.exit("\tNote: User already exists")

    UserMgmt.mkUser(pkgObj.name)
    UserMgmt.givePermissionToUser(pkgObj.name, pkgObj.directoryLocation)

    if pkgObj.preShLocation != None:
        print("[Install] Running pre-installation script")
        pkgObj.runPreSh()
        ensureScriptHasRunProperly(pkgObj.name, "pre.sh")

    print("[Install] Running build script")
    pkgObj.runBuildSh()
    ensureScriptHasRunProperly(pkgObj.name, "build.sh")

    if pkgObj.postShLocation != None:
        print("[Install] Running post-installation script")
        pkgObj.runPostSh()
        ensureScriptHasRunProperly(pkgObj.name, "post.sh")

    saveLocation = "/home/"+pkgObj.name+"/installation_files"
    print("[Install] Saving pkg files to:", saveLocation)
    shutil.copytree(tmpLocation, saveLocation)
        
    pkgObj.logDepends()

    removeTmpEnv()
