import os
import pickle

import Utils

class dependsTree:
    def __init__(self):
        self.tree = {}

    ##Inputs should be a pkg name and a list of dependencies
    def addEntry(self, pkgName, dependencies):
        self.tree[pkgName] = dependencies

    def hasKey(self, pkgName):
        return pkgName in self.tree.keys()
    
    def rmKey(self, pkgName):
        del self.tree[pkgName]

    def getDependsOf(self, pkgName):
        return self.tree[pkgName]

    def numberOfPkgsThatDependOn(self, pkgName):
        number = 0

        for i in self.tree.values():
            for j in i:
                if pkgName == j: number += 1

        return number 


def getDependsTree():
    if not Utils.ensureLibDmi():
        return dependsTree()

    if not os.path.exists("/var/lib/dmi/depends.p"):
        with open("/var/lib/dmi/depends.p", "wb") as f: pass
        return dependsTree()

    with open("/var/lib/dmi/depends.p", "rb") as f:
        try:
            return pickle.load(f)
        except EOFError:
            return dependsTree()

    return None

def writeDependsTree(dependsTree):
    Utils.ensureLibDmi()

    with open("/var/lib/dmi/depends.p", "wb") as f:
        pickle.dump(dependsTree, f)

def addToDependsTree(pkg, dependencies):
    dependsTree = getDependsTree()

    dependsTree.addEntry(pkg, dependencies)

    writeDependsTree(dependsTree)

def rmFromDependsTree(pkg):
    dependsTree = getDependsTree()
    
    try:
        dependsTree.rmKey(pkg)
    except KeyError:
        pass

    writeDependsTree(dependsTree)

