import os
import shutil
import tarfile
import subprocess
import stat
import sys

from Install import package
from Install import fakerootMapper
import List.packageMetadata as PkgMetadata
import List
import Repo
import Depends
from Depends import installedDepends

'''
A unique temporary folder must be 
created for pre-installation procedures
to take place in
'''
tmpDir = "/tmp/dmi" + str(os.getpid())

def install(pkgIdentifier):
    pkg = Repo.searchAll(pkgIdentifier)
    if pkg != None:
        installFromFile(pkg.pkgLocation)
    elif os.path.exists(pkgIdentifier):
       installFromFile(pkgIdentifier)
    else:
        sys.exit("[Install] No such package " + pkgIdentifier)

def installFromFile(pkgLocation):
    print("[Install] Installing '" + pkgLocation + "'...")
    pkgLocation = os.path.abspath(pkgLocation)

    if not os.path.exists(pkgLocation):
        sys.exit("[Install] Cannot install package, file does not exist: " + pkgLocation)

    print("[Install] Creating temporary build environment")
    os.mkdir(tmpDir)

    print("[Install] Opening '.dmi' file")
    unTarPkg(pkgLocation)

    pkgObj = package.package(getPkgDirLocation())
    if List.findPkg(pkgObj.name) != None:
        sys.exit("[Install] Package is already installed: " + pkgObj.name)

    print("[Install] Opening source code tarball")
    openPkgTarball(pkgObj)

    print("[Install] Running 'compile.sh'")
    runPkgCompileSh(pkgObj)

    print("[Install] Installing to fakeroot")
    fakeRootLoc = mkFakeroot(pkgObj)
    installPkgToFakeRoot(pkgObj, fakeRootLoc)

    print("[Install] Mapping fakeroot")
    fkrtMap = fakerootMapper.mapFakeroot(fakeRootLoc)

    print("[Install] Running postfake.sh")
    runPkgPostFakeSh(pkgObj)
    
    print("[Install] Installing to trueroot")
    installPkgFromFkRoot(fkrtMap, fakeRootLoc)

    pkgData = PkgMetadata.pkgMetadata(pkgObj.pkgInfoContents, fkrtMap)
    List.saveListingOn(pkgData)

    print("[Install] Running 'postinstall.sh'")
    runPkgPostInstallSh(pkgObj)

    print("[Install] Removing temporary build environment")
    shutil.rmtree(tmpDir)

def unTarPkg(pkgLocation):
    pkgFileName = tmpDir + "/" + os.path.basename(pkgLocation)
    shutil.copy(pkgLocation, tmpDir)
        
    with tarfile.open(pkgFileName, 'r') as f:
        f.extractall(path=tmpDir)

def getPkgDirLocation():
    for i in os.listdir(tmpDir):
        if os.path.isdir(tmpDir + "/" + i):
            return tmpDir + "/" + i

def mkFakeroot(pkgObj):
    fakeRootLoc = tmpDir + "/" + pkgObj.name + "_fakeroot"
    os.mkdir(fakeRootLoc)
    return fakeRootLoc

def installPkgFromFkRoot(fkrtMap, fkrtLocation):
    #This sorts the directories into the order they need to be created, by 
    #sorting them by depth in the root ('/') heirarchy. We figure out the depth
    #by counting the number of '/' in the name of the directory
    dirsSortedByHeirachy = sorted(fkrtMap.dirs, key=lambda dir: dir.count('/'))

    #Create the necessary directories:
    for i in dirsSortedByHeirachy:
        print("[Install] Making directory: " + i)
        os.mkdir(i)

    #Move the files to the directories:
    for i in fkrtMap.files:
        print("[Install] Installing file: " + i)
        locationInFkrt = fkrtLocation + i
        shutil.copyfile(locationInFkrt, i)

#TODO: Does build accept the envar as install opt? It shouldn't
def installPkgToFakeRoot(pkg, location):
        cmd = ["make"]
        
        if pkg.installOpts != None:
            cmd += pkg.installOpts
        
        cmd += [pkg.envar+"="+location, "install"]
        returnCode = subprocess.run(cmd).returncode
        if returnCode != 0:
            handleFailedScript("make install")

def handleFailedScript(scriptName):
    print("[Build] Script returned non-zero value: " + scriptName)
    shouldContinue = input("\tShould we continue with the installation process? [y/N] ")
    if shouldContinue != 'Y' and shouldContinue != 'y':
        sys.exit(1)

def openPkgTarball(pkg):
    oldContents = pkg.dirContents

    with tarfile.open(pkg.tarballLocation, 'r') as f:
        f.extractall(path=pkg.directory)

    ## Determine what was just extracted
    pkg.dirContents = os.listdir(pkg.directory)
    pkg.extractedContents = os.listdir(pkg.directory) #Put everything in extracted
    for i in oldContents:
        pkg.extractedContents.remove(i) #Remove old stuff from extracted
                                            #This ensures that if a new file
                                            #have the same name as an old one,
                                            #it gets counted as an extracted item

def runSh(pkg, scriptName):
    firstExtractedItem = pkg.directory + "/" + pkg.extractedContents[0]

    os.chdir(firstExtractedItem)
    scriptLocation = firstExtractedItem + "/" + os.path.basename(scriptName)
    shutil.copyfile(scriptName, scriptLocation)

    os.chmod(scriptLocation, stat.S_IEXEC) #marks compilation script as executable
    returnCode = subprocess.run([scriptLocation]).returncode
    if returnCode != 0:
        handleFailedScript(scriptName)


def runPkgCompileSh(pkg):
    runSh(pkg, pkg.compileShLoc)

def runPkgPostInstallSh(pkg):
    if pkg.postInstallShLoc == None:
        print("\tNo 'postinstall.sh' to run")
    else:
        runSh(pkg, pkg.postInstallShLoc)

def runPkgPostFakeSh(pkg):
    if pkg.postFakeShLoc == None:
        print("\tNo 'postfake.sh' to run")
    else:
        runSh(pkg, pkg.postFakeShLoc)

def installWithDepends(pkgName):
    print("[Install] Resolving dependencies for:", pkgName)

    pkgInfo = Repo.searchAll(pkgName)
    if pkgInfo == None:
        print("[Install] Could not find package in repository, attempting install from '*.dmi' file")
        shouldContinue = input("\tThis will result in installation without dependency resolution. Continue? [y/N] ")
        if shouldContinue == "Y" or shouldContinue == "y":
            install(pkgName)
        return

    pkgDepends = Depends.resolveFor(pkgInfo) #Locations of dependencies & the pkg in install order
    pkgsToInstall = [x for x in pkgDepends if not List.isInstalled(x)]

    print("[Install] Must install the following packages: ")
    for i in pkgsToInstall:
        print("\t" + i)
    
    consent = input("[Install] Do you consent to the above packages being installed? [y/N] ")
    if consent != "Y" and consent != "y":
        sys.exit(1)
    
    for i in pkgsToInstall:
        install(i)

    #The last entry of pkgLocations will be the name of the pkg installed
    #The rest are dependencies. We only want a list of the dependencies
    depends = pkgDepends[:-1]
    print("[Install] Logging dependencies:", pkgName, "--", depends)

    installedDepends.addToDependsTree(pkgName, depends)