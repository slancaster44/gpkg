import os
import sys
import shutil
import json

def mkPkgFrom(name, directory):
    pkgBuilder = PackageBuilder(name, directory)
    pkgBuilder.buildPkg()

class PackageBuilder:
    def __init__(self, name, directory):
        self.name = name
        self.directory = directory

    def buildPkg(self):
        self.checkDirectory()
        self.zipPkg()

    ## Must Contain ##
    # build.sh
    # pkginfo.json
    # *.tar*
    ## Can Contain ##
    # pre.sh
    # post.sh
    def checkDirectory(self):
        os.chdir(self.directory)
        filesOfDir = os.listdir()

        if 'build.sh' not in filesOfDir:
            sys.exit("Package must contain 'build.sh' before building")
        elif 'pkginfo.json' not in filesOfDir:
            sys.exit("Package must contain 'pkginfo.json' before building")
        elif 'tarball.tar.xz' not in filesOfDir and 'tarball.tar.gz' not in filesOfDir:
            sys.exit("Package must contain 'taball.tar.*' before building")

        self.checkJson()
        os.chdir("..")

    def zipPkg(self):
        shutil.make_archive(self.name + ".gpkg", "zip", self.directory)
        os.rename(self.name + ".gpkg.zip", self.name + ".gpkg")

    def checkJson(self):
        jsonfile = open("./pkginfo.json")
        try:
            self.jsonContents = json.load(jsonfile)
        except ValueError as e:
            print("Must have valid json in 'pkginfo.json': %s" % e)
            sys.exit(1)

        requiredValues = ["name", "version", "description", "dependencies"]
        for value in requiredValues:
            if not value in self.jsonContents:
                sys.exit("Required value missing from 'pkginfo.json: " + value)
            else:
                continue
