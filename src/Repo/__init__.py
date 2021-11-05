import os
import pickle
import shutil

import Repo.RepoSpecs as RepoSpecs
from Repo.RepoSpecs import pkg
from Repo.RepoSpecs import modlog

def mkRepo(repoLocation):
    repoLocation = os.path.abspath(repoLocation)
    os.mkdir(repoLocation)

    repospecs = RepoSpecs.repoSpecs()

    with open(repoLocation + "/repospecs.p", "wb") as f:
        pickle.dump(repospecs, f)

def addPkg(pkgLocation, repoLocation):
    pkgObj = pkg.Pkg(pkgLocation)
    shutil.copy(pkgLocation, repoLocation)

    pkgObj.pkgLocation = repoLocation + "/" + pkgObj.basename

    repospecs = None
    with open(repoLocation + "/repospecs.p", "rb") as f:
        repospecs = pickle.load(f)

    repospecs.pkgs.append(pkgObj)

    logEntry = modlog.modifcationLogEntry("Added package: " + pkgObj.name)
    repospecs.modificationLog.append(logEntry)
    print(logEntry)

    with open(repoLocation + "/repospecs.p", "wb") as f:
        pickle.dump(repospecs, f)

def rmPkg(pkgName, repoLocation):
    pass