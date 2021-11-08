import pickle
import os
import sys

from Repo import Search
import Utils

def addRepo(repoLocation):
    repoLists = getRepos()
    
    repoSpecs = Search.getReposSpecsFrom(repoLocation)
    if repoSpecs == None:
        sys.exit("[Repo] Not a valid repository: " + repoLocation)

    repoLists.append(repoSpecs)
    writeRepoFile(repoLists)

def rmRepo(repoLocation):
    repoLocation = os.path.abspath(repoLocation)

    repos = getRepos()

    outRepos = []
    for i in repos:
        if i.location != repoLocation:
            outRepos.append(i)

    writeRepoFile(outRepos)

def listRepos():
    repos = getRepos()
    for i in repos:
        print(i)

#Note: repos.p will contain a list of repospecs classes
def getRepos():
    Utils.ensureLibDmi()

    if not os.path.exists("/var/lib/dmi/repos.p"):
        return []

    with open("/var/lib/dmi/repos.p", "rb") as f:
        return pickle.load(f)

def writeRepoFile(repos):
    with open("/var/lib/dmi/repos.p", "wb") as f:
        pickle.dump(repos, f)

def update():
    updatedRepoList = []
    oldRepoList = getRepos()

    for i in oldRepoList:
        repoSpecs = Search.getReposSpecsFrom(i.location)
        if repoSpecs != None:
            updatedRepoList.append(repoSpecs)
    
    writeRepoFile(updatedRepoList)

def searchAll(pkgName):
    reposList = getRepos()

    for i in reposList:
        pkg = Search.search(pkgName, i.location)
        if pkg != None: return pkg

    return None