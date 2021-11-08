import os 
import pickle 
import sys

class pkgMetadata:
    def __init__(self, pkgInfoJson, fkRootMap):
        self.fakeRootMap = fkRootMap
        
        self.name = str(pkgInfoJson["name"])
        self.version = str(pkgInfoJson["version"])
        self.description = str(pkgInfoJson["description"])
        self.dependencies = pkgInfoJson["dependencies"]
        
    def __str__(self):
        rtrnStr = self.basicInfoAsStr()

        rtrnStr += "\n-- Associated Files & Directories --\n"
        for i in self.fakeRootMap.files:
            rtrnStr += "[file] " + i + "\n"
        for i in self.fakeRootMap.dirs:
            rtrnStr += "[dir] " + i + "\n"

        return rtrnStr

    def basicInfoAsStr(self):
        rtrnStr = "[Package Info]\n"
        rtrnStr += "Name: " + self.name + "\n"
        rtrnStr += "Version: " + self.version + "\n"
        rtrnStr += "Dependencies: " + str(self.dependencies) + "\n"

        rtrnStr += "Description: " + self.description 
        return rtrnStr

