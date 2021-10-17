import os
import json

class Package:
    def __init__(self, directory):
        os.chdir(directory)
        self.directoryLocation = directory
        self.pkgContents = os.listdir()

        self.getMustHaves()
        self.getMightHaves()

    def getMustHaves(self):
        self.extractPkgInfo()

        ## Get build.sh ##
        buildShLocation = self.directoryLocation + "/build.sh"

        ## Get tarball ##
        if "tarball.tar.xz" in self.pkgContents:
            self.tarballLocation = self.directoryLocation + "/tarball.tar.xz"
        elif "tarball.tar.gz" in self.pkgContents:
            self.tarballLocation = self.directoryLocation + "/tarball.tar.gz"
        else:
            sys.exit("No tarball found in package")

        print(self.tarballLocation)
        

    def getMightHaves(self):
        ## Get Dependencies ##
        self.extractDependencies()

        ## Get pre.sh ##
        if "pre.sh" in self.pkgContents:
            self.preSh = self.directoryLocation + "/pre.sh"
        else:
            self.preSh = None
        ## Get post.sh ##
        if "post.sh" in self.pkgContents:
            self.postSh = self.directoryLocation + "/post.sh"
        else:
            self.postSh = None

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


class Dependency(Package):
    def __init__(self, parentPkg, dir):
        super.__init__(dir)
        self.parentPkgName = parentPkg
        self.logAsDependency()

    def logAsDependency(self):
        pass

