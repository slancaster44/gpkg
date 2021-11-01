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

def installPkgFromFkRoot(fkrootLocation):
    os.chdir(fkrootLocation)
    os.system("tar cf - . | (cd / ; tar xf - )")
    