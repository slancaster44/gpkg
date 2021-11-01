import os 
import pickle 

class pkgMetadata:
    def __init__(self, pkgInfoJson, fkRootMap):
        self.fakeRootMap = fkRootMap
        
        self.name = str(pkgInfoJson["name"])
        self.version = str(pkgInfoJson["version"])
        self.description = str(pkgInfoJson["description"])
        self.dependencies = str(pkgInfoJson["dependencies"])
        
    def __str__(self):
        rtrnStr = self.basicInfoAsStr()

        rtrnStr += "-- Associated Files & Directories --\n"
        for i in self.fakeRootMap.files:
            rtrnStr += "[file] " + i + "\n"
        for i in self.fakeRootMap.dirs:
            rtrnStr += "[dir] " + i + "\n"

        return rtrnStr

    def basicInfoAsStr(self):
        rtrnStr = "[Package Info]\n"
        rtrnStr += "Name: " + self.name + "\n"
        rtrnStr += "Version: " + self.version + "\n"
        rtrnStr += "Dependencies: " + self.dependencies + "\n\n"

        rtrnStr += "Description: " + self.description + "\n\n"
        return rtrnStr

def save(pkgdata):
    if not os.path.exists('/var/lib/gpkg'):
        os.mkdir('/var/lib/gpkg')

    with open('/var/lib/gpkg/pkgdata.p', 'ab') as f:
        pickle.dump(pkgdata, f)