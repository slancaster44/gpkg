
import os
import pickle

def search(pkgName, repoLocation):
    repoLcation = os.path.abspath(repoLocation)

    repospecsLocation = repoLocation + "/repospecs.p"
    repospecsObj = None
    with open(repospecsLocation, "rb") as f:
        repospecsObj = pickle.load(f)

    for i in repospecsObj.pkgs:
        if i.name == pkgName:
            return i

    return None