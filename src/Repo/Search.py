
import os
import sys
import pickle

from Repo.RepoSpecs import repoSpecs

def search(pkgName, repoLocation):
    repoLocation = os.path.abspath(repoLocation)

    repospecsObj = getReposSpecsFrom(repoLocation)
    if repospecsObj == None:
        sys.exit("[Search] Not a valid repository: " + repoLocation)

    pkg = None
    for i in repospecsObj.pkgs:
        if i.name == pkgName:
            pkg = i

    if pkg != None: 
        if not os.path.exists(pkg.pkgLocation):
            sys.exit("[repo_search] Corrupted entry, no package found: " + pkg.pkgLocation)

    return pkg

def getReposSpecsFrom(repoLocation):
    repoLocation = os.path.abspath(repoLocation)

    repospecsLocation = repoLocation + "/repospecs.p"
    if not os.path.exists(repospecsLocation):
        return None

    repospecsObj = None
    with open(repospecsLocation, "rb") as f:
        repospecsObj = pickle.load(f)

    return repospecsObj