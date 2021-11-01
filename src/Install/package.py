import os
import json
import tarfile
import shutil
import stat
import subprocess

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

        self.extractedContents = []

    def getPkgInfoLocation(self):
        return self.directory + "/" + "pkginfo.json"

    def getCompileShLocation(self):
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
        with open(self.pkgInfoLoc, 'r') as f:
            return json.load(f)

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

    def openTarball(self):
        oldContents = self.dirContents

        with tarfile.open(self.tarballLocation, 'r') as f:
            f.extractall(path=self.directory)

        ## Determine what was just extracted
        self.dirContents = os.listdir(self.directory)
        self.extractedContents = os.listdir(self.directory) #Put everything in extracted
        for i in oldContents:
            self.extractedContents.remove(i) #Remove old stuff from extracted
                                             #This ensures that if a new file
                                             #have the same name as an old one,
                                             #it gets counted as an extracted item
        
    def runCompileSh(self):
        
        firstExtractedItem = self.directory + "/" + self.extractedContents[0]
        
        os.chdir(firstExtractedItem)
        shutil.copyfile(self.compileShLoc, firstExtractedItem + "/compile.gpkg.sh")
        self.compileShLoc = firstExtractedItem + "/compile.gpkg.sh"
        
        os.chmod(self.compileShLoc, stat.S_IEXEC)
        os.system(self.compileShLoc)

    def installToFakeRoot(self, location):
        cmd = ["make"]
        
        if self.installOpts != None:
            cmd += self.installOpts
        
        cmd += [self.envar+"="+location, "install"]
        subprocess.run(cmd)
