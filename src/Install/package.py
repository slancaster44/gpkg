import os
import json
import sys

import Utils

class package:
    def __init__(self, directory):
        self.directory = directory

        self.dirContents = os.listdir(self.directory)

        self.pkgInfoLoc = self.getPkgInfoLocation()
        self.compileShLoc = self.getCompileShLocation()
        self.postFakeShLoc = self.getPostFakeShLoc()
        self.postInstallShLoc = self.getPostInstallShLoc()
        self.tarballLocation = self.getTarballLocation()

        self.pkgInfoContents = self.getPkgInfoContents()

        self.name = self.getName()
        self.version = self.getVersion()
        self.description = self.getDescription()
        self.installOpts = self.getInstallOpts()
        self.envar = self.getEnvar()
        self.dependencies = self.getDependencies()
        self.installFromBuildDir = self.getInstallFromBuildDir()

        self.extractedContents = []

    def getPkgInfoLocation(self):
        return self.directory + "/pkginfo.json"

    def getCompileShLocation(self):
        if not "compile.sh" in self.dirContents:
            return None
        else:
            return self.directory + "/" + "compile.sh"

    def getPostFakeShLoc(self):
        if not "postfake.sh" in self.dirContents:
            return None
        else:
            return self.directory + "/" + "postfake.sh"

    def getPostInstallShLoc(self):
        if not "postinstall.sh" in self.dirContents:
            return None
        else:
            return self.directory + "/" + "postinstall.sh"

    def getTarballLocation(self):
        tarballName = Utils.findTarballsIn(self.directory)[0]
        return self.directory + "/" + tarballName 
    
    def getPkgInfoContents(self):
        retVal = None
        with open(self.pkgInfoLoc, 'r') as f:
            try:
                retVal = json.load(f)
            except:
                sys.exit("[Package] Cannot load json: " + self.pkgInfoLoc)
        return retVal
        

    def getName(self):
        return self.pkgInfoContents["name"]

    def getVersion(self):
        return self.pkgInfoContents["version"]

    def getDescription(self):
        return self.pkgInfoContents["description"]

    def getInstallOpts(self):
        return self.pkgInfoContents["install_options"]

    def getDependencies(self):
        return self.pkgInfoContents["dependencies"]

    def getEnvar(self):
        return self.pkgInfoContents["envar"]

    def getInstallFromBuildDir(self):
        return self.pkgInfoContents["from_builddir"]