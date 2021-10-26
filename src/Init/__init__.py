import sys
import os
import UserMgmt

def mkUsrShareDir():
    os.mkdir('/usr/share/gpkg')
    with open('/usr/share/gpkg/dependencies.p', 'wb') as _:
        pass

def initGpkg():
    
    shouldContinue = input("This may only be executed upon first run of gpkg. Continue? (y/N) ")
    if shouldContinue != "y" and shouldContinue != "Y":
        sys.exit(1)

    UserMgmt.addInstallGroup()
    mkUsrShareDir()
