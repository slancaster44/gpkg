
import os
import pickle

def search(pkgName, repoLocation):
    repoLocation = os.path.abspath(repoLocation)

    repospecsLocation = repoLocation + "/repospecs.p"
    repospecsObj = None
    with open(repospecsLocation, "rb") as f:
        repospecsObj = pickle.load(f)

    pkg = None
    for i in repospecsObj.pkgs:
        if i.name == pkgName:
            pkg = i

    if pkg != None: 
        if not os.path.exists(pkg.pkgLocation):
            sys.exit("[repo_search] Corrupted entry, no package found: " + pkg.pkgLocation)

    return pkg