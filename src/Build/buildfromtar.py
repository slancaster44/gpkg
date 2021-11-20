import os
import sys
import shutil

'''
This file is contains utilities to help a developer
turn a tarball into a '.dmi' file
'''

class unbuiltPkgInfo:
    def __init__(self):
        self.name = self.getName()
        self.version = self.getVersion()
        self.description = self.getDescription()
        self.dependencies = self.getDepends()

        print("[Build] Setting no install_options")
        self.installOpts = []
        print("[Build] Setting envar to 'DESTDIR'")
        self.envar = "DESTDIR"
        print("[Build] Setting 'from_builddir' to False")
        self.frombuilddir = "false"

    def getName(self):
        return input("[Build] Enter the name of the package: ")
    
    def getVersion(self):
        return input("[Build] Enter the version of the package: ")

    def getDescription(self):
        return input("[Build] Enter a description for the package: ")

    def getDepends(self):
        depends = []
        while True:
            hasDependency = input("[Build] Does this package have a dependency? [y/N] ")

            if hasDependency != 'y' and hasDependency != 'Y':
                break
            
            dependency = input("\tWhat is the name of the dependency? ")
            depends.append(dependency)
        return depends

def mkDmipDir(tarballLocation):
    tarAbsPath = os.path.abspath(tarballLocation)
    if not os.path.exists(os.path.abspath(tarballLocation)):
        sys.exit("[Build] Cannot build from non-existant tarball: " + tarAbsPath)
    
    pkgInfo = unbuiltPkgInfo()
    if os.path.exists(pkgInfo.name):
        print("[Build] Directory already exists: " + pkgInfo.name)
        altName = input("\tWhat is an alternative name for the package? ")
        os.mkdir(altName)
        os.chdir(altName)
    else:
        os.mkdir(pkgInfo.name)
        os.chdir(pkgInfo.name)

    defaultCompileSh = getDefaultCompileSh()
    defaultJson = mkDefaultJson(pkgInfo)

    print("[Build] Creating 'pkginfo.json'")
    with open("pkginfo.json", "w") as f:
        f.write(defaultJson)

    print("[Build] Creating 'compile.sh'")
    with open("compile.sh", "w") as f:
        f.write(defaultCompileSh)

    shutil.copy(tarAbsPath, ".")


def getDefaultCompileSh():
    return "#!/bin/bash\n ./configure \n make"

def mkDefaultJson(pkgInfo):
    rtrnVal = "{\n"
    rtrnVal += '\t"name":"' + pkgInfo.name + '",\n'
    rtrnVal += '\t"version":"' + pkgInfo.version + '",\n'
    rtrnVal += '\t"description":"'+ pkgInfo.description + '",\n'
    rtrnVal += '\t"dependencies":'+ str(pkgInfo.dependencies).replace("'", '"') + ',\n'
    rtrnVal += '\t"install_options":' + str(pkgInfo.installOpts) + ',\n'
    rtrnVal += '\t"from_builddir":' + pkgInfo.frombuilddir + ',\n'
    rtrnVal += '\t"envar":"' + pkgInfo.envar + '"\n'

    return rtrnVal + "}"
