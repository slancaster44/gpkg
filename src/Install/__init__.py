import os
import shutil
import tarfile
import subprocess

from Install import package
from Install import fakerootMapper
import PkgMetadata
'''
A unique temporary folder must be 
created for pre-installation procedures
to take place in
'''
tmpDir = "/tmp/gpkg" + str(os.getpid())

def install(pkgLocation):
    pkgLocation = os.path.abspath(pkgLocation)

    os.mkdir(tmpDir)
    unTarPkg(pkgLocation)

    pkgObj = package.package(getPkgDirLocation())

    pkgObj.openTarball()
    pkgObj.runCompileSh()

    fakeRootLoc = mkFakeroot(pkgObj)
    pkgObj.installToFakeRoot(fakeRootLoc)

    fkrtMap = fakerootMapper.mapFakeroot(fakeRootLoc)
    installPkgFromFkRoot(fkrtMap, fakeRootLoc)

    pkgData = PkgMetadata.pkgMetadata(pkgObj.pkgInfoContents, fkrtMap)
    PkgMetadata.save(pkgData)

    shutil.rmtree(tmpDir)

def unTarPkg(pkgLocation):
    pkgFileName = tmpDir + "/" + os.path.basename(pkgLocation)
    shutil.copy(pkgLocation, tmpDir)

    with tarfile.open(pkgFileName, 'r') as f:
        f.extractall(path=tmpDir)

def getPkgDirLocation():
    for i in os.listdir(tmpDir):
        if os.path.isdir(tmpDir + "/" + i):
            return tmpDir + "/" + i

def mkFakeroot(pkgObj):
    fakeRootLoc = tmpDir + "/" + pkgObj.name + "_fakeroot"
    os.mkdir(fakeRootLoc)
    return fakeRootLoc

def installPkgFromFkRoot(fkrtMap, fkrtLocation):
    #This sorts the directories into the order they need to be created, by 
    #sorting them by depth in the root ('/') heirarchy. We figure out the depth
    #by counting the number of '/' in the name of the directory
    dirsSortedByHeirachy = sorted(fkrtMap.dirs, key=lambda dir: dir.count('/'))

    #Create the necessary directories:
    for i in dirsSortedByHeirachy:
       os.mkdir(i)

    #Move the files to the directories:
    for i in fkrtMap.files:
        locationInFkrt = fkrtLocation + i
        shutil.copyfile(locationInFkrt, i)
    