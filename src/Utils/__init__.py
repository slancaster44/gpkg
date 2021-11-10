
import os 
import sys

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

def ensureLibDmi():
    if os.getuid() != 0:
        sys.exit("Can only run this operation as root")

    if not os.path.exists("/var/lib/dmi"):
        os.mkdir("/var/lib/dmi")
        return False

    return True