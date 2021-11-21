import os
import sys
import json
import tarfile

import Utils

'''
This file contains the functions for building
a '.dmi' file from a given folder
'''

def build(dir):
    dir = os.path.abspath(dir)

    if not os.path.isdir(dir):
        sys.exit("[Build] Must build from directory, not file")

    checkContents(dir)
    tarContents(dir)

'''
This function ensures the dir has the
required files to be packaged as a '.dmi'
-- 'pkginfo.json'
-- 'compile.sh'
-- '<somename>.tar.gz OR <somename>.tar.xz'
'''
def checkContents(dir):

    listOfTarballs = Utils.findTarballsIn(dir)
    if len(listOfTarballs) != 1:
        sys.exit("[Build] Can only build package that contains one tarball")
    checkTarball(dir + "/" + listOfTarballs[0])

    listOfCompileScripts = Utils.findCompileScriptsIn(dir)
    if len(listOfCompileScripts) > 1:
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

    ##Make sure the items required in pkginfo.json are there
    requiredItems = ['name', 'version', 
    'description', 'dependencies', 
    'install_options', 'envar', 'from_builddir']

    for i in requiredItems:
        if not i in jsonContents.keys():
            sys.exit("[Build] 'pkginfo.json' must contain key '" + i + "'")

    itemsThatShouldBeStrings = ['name', 'version', 'description', 'envar']
    itemsThatShouldBeLists = ['install_options', 'dependencies']
    itemsThatShouldBeBools = ['from_builddir']

    ## Type check items in 'pkginfo.json'
    for i in itemsThatShouldBeStrings:
        item = jsonContents[i]
        if not isinstance(item, str):
            sys.exit("[Build] Variable in 'pkginfo.json' must be stored as string: " + i)

    for i in itemsThatShouldBeLists:
        item = jsonContents[i]
        if not isinstance(item, list) and item != None:
            sys.exit("[Build] Variable in 'pkginfo.json' must be stored as list: " + i)

    for i in itemsThatShouldBeBools:
        item = jsonContents[i]
        if not isinstance(item, bool) and item != None:
            sys.exit("[Build] Variable in 'pkginfo.json' must be stored as list: " + i)
    
    ##If the envar is an option in the install_opts
    ##The install to the fakeroot will fail;
    envar = jsonContents['envar']
    for i in jsonContents['install_options']:
        if envar in i:
            sys.exit("[Build] Cannot set envar in install_options")

def checkTarball(tarball):
    ##Ensure that tarball contains 1 upper level directory
    with tarfile.open(tarball, "r") as f:
        members = f.getmembers()
        
        if len(members) == 0:
            sys.exit("[Build] Empty tarball: " + tarball)

        upperLevelMembers = [x for x in members if not "/" in x.name[:-1]]
        
        if len(upperLevelMembers) > 1:
            sys.exit("[Build] You must have one upper level directory in tarball: " + tarball)

        allMembersWithSameUpperLevel = [x for x in members if x.name.split('/')[0] == members[0].name.split('/')[0]]
        if len(allMembersWithSameUpperLevel) < len(members):
            sys.exit("[Build] You must have one upper level directory in tarball: " + tarball)

def tarContents(dir):
    nameOfDMIFile = os.path.basename(dir) + ".dmi"

    with tarfile.open(nameOfDMIFile, "w:xz") as tar:
        tar.add(dir, arcname=os.path.basename(dir))

