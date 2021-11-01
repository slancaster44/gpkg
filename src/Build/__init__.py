import os
import sys
import json
import tarfile

import Utils

'''
This file contains the functions for building
a '.gpkg' file from a given folder
'''

def build(dir):
    dir = os.path.abspath(dir)

    if not os.path.isdir(dir):
        sys.exit("[Build] Must build from directory, not file")

    checkContents(dir)
    tarContents(dir)

'''
This function ensures the dir has the
required files to be packaged as a '.gpkg'
-- 'pkginfo.json'
-- 'compile.sh'
-- '<somename>.tar.gz OR <somename>.tar.xz'
'''
def checkContents(dir):

    listOfTarballs = Utils.findTarballsIn(dir)
    if len(listOfTarballs) != 1:
        sys.exit("[Build] Can only build package that contains one tarball")

    listOfCompileScripts = Utils.findCompileScriptsIn(dir)
    if len(listOfCompileScripts) != 1:
        sys.exit("[Build] Can only build package that contains one 'compile.sh'")

    listOfPkgInfoJsons = Utils.findPkgInfosIn(dir)
    if len(listOfPkgInfoJsons) != 1:
        sys.exit("[Build] Can only build package that contains one 'pkginfo.json'")
    else:
        checkJson(dir + "/" + listOfPkgInfoJsons[0])

def checkJson(jsonFileLocation):
    jsonFile = open(jsonFileLocation, 'r')
    try:
        jsonContents = json.load(jsonFile) 
    except:
        sys.exit("[Build] Could not read '" + jsonFileLocation + "'")
    jsonFile.close()

    requiredItems = ['name', 'version', 
    'description', 'dependencies', 
    'install_options', 'envar']

    for i in requiredItems:
        if not i in jsonContents.keys():
            sys.exit("[Build] 'pkginfo.json' must contain key '" + i + "'")

    ##TODO: Test types of install options
    ##Make sure the tarball contains 1 folder

def tarContents(dir):
    nameOfGpkgFile = os.path.basename(dir) + ".gpkg"

    with tarfile.open(nameOfGpkgFile, "w:xz") as tar:
        tar.add(dir, arcname=os.path.basename(dir))