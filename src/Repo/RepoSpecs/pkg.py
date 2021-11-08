import json
import tarfile
import os
import sys

import List

class Pkg:
    def __init__(self, location):
        self.pkgLocation = os.path.abspath(location)
        if not os.path.exists(self.pkgLocation):
            sys.exit("[repospecs] No such package: " + self.pkgLocation)

        self.basename = os.path.basename(location)

        self.pkgInfoJson = self.getPkgInfoJson()

        self.name = str(self.pkgInfoJson["name"])
        self.version = str(self.pkgInfoJson["version"])
        self.description = str(self.pkgInfoJson["description"])
        self.dependencies = self.pkgInfoJson["dependencies"]
        self.envar = str(self.pkgInfoJson["envar"])
        self.installOpts = str(self.pkgInfoJson["install_options"])

    def isInstalled(self): 
        return List.isInstalled(self.name)
    
    def getPkgInfoJson(self):
        tmpDir = "/tmp/dmir" + str(os.getpid())

        jsonFile = None
        with tarfile.open(self.pkgLocation, "r") as f:
            jsonFileInfo = [x for x in f.getmembers() if os.path.basename(x.name) == "pkginfo.json"][0]
            jsonFile = f.extractfile(jsonFileInfo.name).read().decode("utf-8")

        return json.loads(jsonFile)

    def __str__(self):
        rtrnStr = "[Package Info]\n"
        rtrnStr += "Name: " + self.name + "\n"
        rtrnStr += "Version: " + self.version + "\n"
        rtrnStr += "Dependencies: " + str(self.dependencies) + "\n"
        rtrnStr += "Description: " + self.description + "\n"
        rtrnStr += "Location: " + self.pkgLocation + "\n"
        rtrnStr += "Installation Status: " + str(self.isInstalled()) 
        return rtrnStr
