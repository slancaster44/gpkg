import os
import shutil
import subprocess
from zipfile import ZipFile
import tarfile

import Pkg
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
    createTmpEnv(pkgLocation)
    unzipPkg()


    pkgObj = getPkgAsObj()

    print("Decompressing package tarball... ")
    pkgObj.unTar()
    print("\tDone")

    os.chdir(pkgObj.extractedTarballLocation)
    print(os.listdir())

    if pkgObj.preShLocation != None:
        pkgObj.runPreSh()

    removeTmpEnv()