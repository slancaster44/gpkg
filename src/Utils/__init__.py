
import os 

def findTarballsIn(dir):
    contents = os.listdir(dir)
    return [x for x in contents if x.endswith(".tar.gz") or x.endswith(".tar.xz")]

def findCompileScriptsIn(dir):
    contents = os.listdir(dir)
    return [x for x in contents if x == "compile.sh"]

def findPkgInfosIn(dir):
    contents = os.listdir(dir)
    return [x for x in contents if x == "pkginfo.json"]

def pathType(item):
    if os.path.isdir(item): 
        return "dir"
    else:
        return "file"
