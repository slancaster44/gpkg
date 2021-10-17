import os
import json
import tarfile

class Package:
    def __init__(self, directory):
        os.chdir(directory)

        self.buildShLocation = None
        self.tarballLocation = None
        self.preShLocation = None
        self.postShLocation = None

        self.pkgInfoLocation = None
        self.pkgInfoJson = None
        self.name = None
        self.version = None
        self.description = None
        self.depends = None
        self.dependsDir = None
        self.dependsPkgs = None

        self.extractedTarballLocation = None

        self.directoryLocation = directory
        self.pkgContents = os.listdir()

        self.getMustHaves()
        self.getMightHaves()

    def getMustHaves(self):
        self.extractPkgInfo()

        ## Get build.sh ##
        self.buildShLocation = self.directoryLocation + "/build.sh"

        ## Get tarball ##
        if "tarball.tar.xz" in self.pkgContents:
            self.tarballLocation = self.directoryLocation + "/tarball.tar.xz"
        elif "tarball.tar.gz" in self.pkgContents:
            self.tarballLocation = self.directoryLocation + "/tarball.tar.gz"
        else:
            sys.exit("No tarball found in package")

    def getMightHaves(self):
        ## Get Dependencies ##
        self.extractDependencies()

        ## Get pre.sh ##
        if "pre.sh" in self.pkgContents:
            self.preShLocation = self.directoryLocation + "/pre.sh"
        ## Get post.sh ##
        if "post.sh" in self.pkgContents:
            self.postShLocation = self.directoryLocation + "/post.sh"

    def extractPkgInfo(self):
        self.pkgInfoLocation = self.directoryLocation + "/pkginfo.json"
        with open(self.pkgInfoLocation) as f:
            self.pkgInfoJson = json.load(f)

        self.name = self.pkgInfoJson["name"]
        self.version = self.pkgInfoJson["version"]
        self.description = self.pkgInfoJson["description"]
        self.depends = self.pkgInfoJson["dependencies"]

    def extractDependencies(self):
        if "dependencies" in self.pkgContents:
            self.dependsDir = self.directoryLocation + "/dependencies"
            self.dependsPkgs = [] ##TODO: Add in support for dependencies
        else:
            self.dependsDir = None
            self.dependsPkgs = []

    def unTar(self):
        dirContentsBefore = os.listdir()

        tar = tarfile.open(name=self.tarballLocation, mode='r')
        tar.extractall(path=".", members=None)

        dirContentsAfter = os.listdir()
        for i in dirContentsAfter:
            if not i in dirContentsBefore:
                self.extractedTarballLocation = i

        tar.close()

    def runPreSh(self):
        pass #TODO: Implement Pre-Sh

class Dependency(Package):
    def __init__(self, parentPkg, dir):
        super.__init__(dir)
        self.parentPkgName = parentPkg
        self.logAsDependency()

    def logAsDependency(self):
        pass

