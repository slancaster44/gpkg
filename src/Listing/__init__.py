import pwd
import grp
import os
import json
import subprocess
import sys
import pickle

def getPkgUsers():
    listOfUsers = []
    for p in pwd.getpwall():
        userName = p[0]
        groupName = grp.getgrgid(p[3])[0]

        if groupName == "install":
            listOfUsers.append(p)

    return listOfUsers

def findPkgUserFor(pkg):
    listOfUsers = getPkgUsers()

    for i in listOfUsers:
        if i.pw_name == pkg:
            return i

    return None

class PkgInfo:
    def __init__(self, pkgUser):
        self.name = pkgUser.pw_name
        self.home = pkgUser.pw_dir

        self.pkgInfoLocation = None
        self.getJsonFile()

        self.installedFiles = []
        self.getFiles()
        
        self.parentPkgs = []
        self.getParentPkgs()

        self.version = None
        self.description = None
        self.pkgInfoJson = None
        self.dependends = []
        self.extractJsonInfo()


    def __str__(self):
        out = "[Package Listing]\n"
        out += "Name: " + str(self.name) +"\n"
        out += "Version: " + str(self.version )+ "\n"
        out += "Description: " + str(self.description) + "\n"
        out += "Dependencies: " + str(self.depends) + "\n"
        out += "Parent Packages: " + str(self.parentPkgs) + "\n\n"

        out += "## Associated Files & Directories ##\n"
        for i in self.installedFiles:
            out += "|- " + i + "\n"

        return out[:-1]

    def getFiles(self):
        #Get Files Owned By User
        output = subprocess.run(["find", "/", "-user", self.name],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.DEVNULL).stdout
        #Filter out whitespace
        outputNoWhite = output.decode().split("\n")

        #Filter out files in '/home'
        outputNoHomeFiles = []
        for filename in outputNoWhite:
            if filename[:6] != "/home/" and filename != '':
                outputNoHomeFiles.append(filename)

        #Filter out files 'No Such File or dir'
        finallyCleanOutput = []
        for filename in outputNoHomeFiles:
            if not "No such file or directory" in filename:
                self.installedFiles.append(filename)

    def getJsonFile(self):
        for root, dirNames, fileNames in os.walk(self.home + "/installation_files"):
            for file in fileNames:
                if file == "pkginfo.json":
                    self.pkgInfoLocation = self.home + "/installation_files/" + file

    def extractJsonInfo(self):
        if self.pkgInfoLocation == None:
            print("[Listing] Unable to find pkginfo.json")
            return

        with open(self.pkgInfoLocation) as f:
            self.pkgInfoJson = json.load(f)

            self.version = self.pkgInfoJson["version"]
            self.description = self.pkgInfoJson["description"]
            self.depends = self.pkgInfoJson["dependencies"]
            
    def getParentPkgs(self):
        with open("/usr/share/gpkg/dependencies.p", "rb") as f:
           while True:
                try:
                   item = pickle.load(f)
                   if item["dependency"] == self.name and \
                       not item["parentPkg"] in self.parentPkgs: 
                       self.parentPkgs.append(item["parentPkg"])
                except EOFError:
                    break
                
    def hasParentPkgs(self):
        return self.parentPkgs != []
        

def getInfoFor(pkg):
    print("[Listing] Collecting info for " + pkg)

    pkgUser = findPkgUserFor(pkg)
    if pkgUser == None:
        sys.exit("[Listing] No such package installed: " + pkg)

    return PkgInfo(pkgUser)

