import os
import pickle

import Utils

class dependsTree:
    def __init__(self):
        self.tree = {}

    ##Inputs should be a pkg name and a list of dependencies
    def addEntry(self, pkg, dependencies):
        self.tree[pkg.name] = dependencies

    def hasKey(self, pkg):
        return pkg.name in self.tree.keys()
    
    def rmKey(self, pkg):
        del self.tree[pkg.name]

    def numberOfPkgsThatDependOn(self, pkg):
        number = 0

        for i in self.tree.values():
            if pkg.name in i:
                number += 1

        return number 


def getDependsTree():
    if not Utils.ensureLibDmi():
        return dependsTree()

    if not os.path.exists("/var/lib/dmi/depends.p"):
        with open("/var/lib/dmi/depends.p", "wb") as f: pass
        return dependsTree()

    with open("/var/lib/dmi/depends.p", "rb") as f:
       return pickle.load(f)

    return None

def writeDependsTree(dependsTree):
    Utils.ensureLibDmi()

    with open("/var/lib/dmi/depends.p", "wb") as f:
        pickle.dumps(dependsTree, f)

def addToDependsTree(pkg, dependencies):
    dependsTree = getDependsTree()

    dependsTree.addEntry(pkg, dependencies)

    writeDependsTree(dependsTree)

def rmFromDependsTree(pkg):
    dependsTree = getDependsTree()

    dependsTree.rmKey(pkg)

    writeDependsTree(dependsTree)