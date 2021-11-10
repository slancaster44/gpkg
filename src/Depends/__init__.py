import sys

import Repo
import List
'''
Should return a list ordered by how
packages should be installed
'''
def resolveFor(pkgInfo):
    pkg = pkgWithAllDependencies(pkgInfo)
    dependencyOrder = orderedDependsOf(pkg)

    return [x.name for x in dependencyOrder]


class Pkg:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.depends = []
    
    def addDepends(self, pkg):
        self.depends.append(pkg)

    def __str__(self):
        rtrnVal = self.name + ": "
        for i in self.depends:
            rtrnVal += i.name + " "
        return rtrnVal

def pkgWithAllDependencies(pkgInfo):
    pkg = Pkg(pkgInfo.name, pkgInfo.pkgLocation)

    for i in pkgInfo.dependencies:
        if List.isInstalled(i):
            print("[Depends] Dependency already installed, skipping: " + i)
            continue 

        dependencyInfo = Repo.searchAll(i)
        if dependencyInfo == None:
            sys.exit("[Depends] Cannot resolve dependency for: " + i)

        
        pkgWithDepends = pkgWithAllDependencies(dependencyInfo)
        pkg.addDepends(pkgWithDepends)

    return pkg

def orderedDependsOf(pkg):
    return orderedDependsOfHelper(pkg, [], [])

def orderedDependsOfHelper(pkg, seen, resolved):
    for dependency in pkg.depends:
        if dependency not in resolved:
            if dependency in seen:
                return None 
            seen.append(dependency)
            rtrnVal = orderedDependsOfHelper(dependency, seen, resolved)
            if rtrnVal == None:
                return None

    resolved.append(pkg)
    return resolved