import os
import pickle
import shutil
import sys

import Repo.RepoSpecs as RepoSpecs
import Repo.Search as Search
from Repo.RepoSpecs import pkg
from Repo.RepoSpecs import modlog

def mkRepo(repoLocation):
    if os.path.exists(repoLocation):
        sys.exit("[dmirepo] Directory already exists: " + repoLocation)

    repoLocation = os.path.abspath(repoLocation)
    os.mkdir(repoLocation)

    repospecs = RepoSpecs.repoSpecs(repoLocation)

    writeRepospecs(repospecs, repoLocation)

def addPkg(pkgLocation, repoLocation):
    checkdir(repoLocation)

    pkgObj = pkg.Pkg(pkgLocation)
    shutil.copy(pkgLocation, repoLocation)

    pkgObj.pkgLocation = repoLocation + pkgObj.basename

    repospecs = None
    with open(repoLocation + "/repospecs.p", "rb") as f:
        repospecs = pickle.load(f)

    repospecs.pkgs.append(pkgObj)

    logEntry = modlog.modifcationLogEntry("Added package: " + pkgObj.name)
    repospecs.modificationLog.append(logEntry)
    print(logEntry)

    writeRepospecs(repospecs, repoLocation)

def rmPkg(pkgName, repoLocation):
    checkdir(repoLocation)

    repospecs = None
    with open(repoLocation + "/repospecs.p", "rb") as f:
        repospecs = pickle.load(f)

    pkgInfo = Search.search(pkgName, repoLocation)
    if pkgInfo == None:
        sys.exit("[dmirepo] No such package in given repo")

    pkgs = [x for x in repospecs.pkgs if x.name != pkgName]
    repospecs.pkgs = pkgs

    logEntry = modlog.modifcationLogEntry("Removed package: " + pkgInfo.name)
    repospecs.modificationLog.append(logEntry)
    print(logEntry)

    writeRepospecs(repospecs, repoLocation)
    os.remove(pkgInfo.pkgLocation)


def writeRepospecs(repospecs, repoLocation):
    with open(repoLocation + "/repospecs.p", "wb") as f:
        pickle.dump(repospecs, f)

def checkdir(repoLocation):
    if not os.path.exists(repoLocation):
        sys.exit("[dmirepo] No repository on: " + repoLocation)