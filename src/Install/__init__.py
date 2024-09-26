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
import Utils

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

    if not os.path.isfile(pkgLocation):
        sys.exit("[Install] Can only install from file")

    print("[Install] Creating temporary build environment")
    os.mkdir(tmpDir)

    print("[Install] Opening '.dmi' file")
    unTarPkg(pkgLocation)

    pkgLocation = getPkgDirLocation()
    pkgObj = package.package(pkgLocation)
    if List.findPkg(pkgObj.name) != None:
        sys.exit("[Install] Package is already installed: " + pkgObj.name)

    print("[Install] Check dependencies")
    checkDepends(pkgObj)

    print("[Install] Opening source code tarball")
    openPkgTarball(pkgObj)

    print("[Install] Running 'compile.sh'")
    extractedDir = pkgLocation + "/" + pkgObj.extractedContents[0]
    print(extractedDir)
    runPkgCompileSh(pkgObj, extractedDir)

    print("[Install] Installing to fakeroot")
    print("[Install] Creating copy of tarball files...")

    extractedDirCopy = extractedDir + ".copy.d"

    shutil.copytree(extractedDir, extractedDirCopy,  
        symlinks=True, ignore_dangling_symlinks=True)

    os.chdir(extractedDirCopy)
    fakeRootLoc = mkFakeroot(pkgObj)

    if pkgObj.runMakeInstall:
        installPkgToFakeRoot(pkgObj, fakeRootLoc)

    print("[Install] Running postfake.sh")
    runPkgPostFakeSh(pkgObj, fakeRootLoc, extractedDirCopy)

    print("[Install] Mapping fakeroot")
    fkrtMap = fakerootMapper.mapFakeroot(fakeRootLoc)
    
    print(fkrtMap)
    print("The above files and directories will be installed")
    Utils.shouldContinue()

    print("[Install] Installing to trueroot")
    os.chdir(extractedDir)

    if pkgObj.runMakeInstall:
        installPkgToTrueRoot(pkgObj)
        
    runPkgPostFakeSh(pkgObj, "/", extractedDir) 

    print("[Install] Running 'postinstall.sh'")
    runPkgPostInstallSh(pkgObj, extractedDir)
    
    pkgData = PkgMetadata.pkgMetadata(pkgObj.pkgInfoContents, fkrtMap)
    List.saveListingOn(pkgData)
    
    print("[Install] Removing temporary build environment")
    shutil.rmtree(tmpDir)

def unTarPkg(pkgLocation):
    pkgFileName = tmpDir + "/" + os.path.basename(pkgLocation)
    shutil.copy(pkgLocation, tmpDir)
        
    with tarfile.open(pkgFileName, 'r') as f:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(f, path=tmpDir)

def getPkgDirLocation():
    for i in os.listdir(tmpDir):
        if os.path.isdir(tmpDir + "/" + i):
            return tmpDir + "/" + i

def mkFakeroot(pkgObj):
    fakeRootLoc = tmpDir + "/" + pkgObj.name + "_fakeroot"
    os.mkdir(fakeRootLoc)
    return fakeRootLoc

def installPkgToTrueRoot(pkg):
    extractedDir = os.path.abspath(os.curdir)

    if pkg.installFromBuildDir != "":
        buildpath = extractedDir + "/" + pkg.installFromBuildDir
        if not os.path.exists(buildpath):
            os.makedirs(buildpath)

        os.chdir(buildpath)

    cmd = mkInstallCmd(pkg, "/")
    
    print("[Install] Running 'make install'")
    returnCode = subprocess.run(cmd).returncode
    if returnCode != 0:
        handleFailedScript(str(cmd), returnCode)

def installPkgToFakeRoot(pkg, fkrtlocation):
    extractedDir = os.path.abspath(os.curdir)
    
    if pkg.installFromBuildDir != "":
        buildpath = extractedDir + "/" + pkg.installFromBuildDir
        if not os.path.exists(buildpath):
            os.makedirs(buildpath)

        os.chdir(buildpath)

    cmd = mkInstallCmd(pkg, fkrtlocation)

    returnCode = subprocess.run(cmd).returncode
    if returnCode != 0:
        handleFailedScript(str(cmd), returnCode)

def mkInstallCmd(pkg, fkrootLocation):

    cmd = ["make"]

    #If the DESTDIR is set as a cmd option, we need to insert
    #the fakeroot location into DESTDIR option so that 
    #DESTDIR=$FAKEROOT/<install location>

    hasSetEnvar = False
    for i in pkg.installOpts:
        if '=' in i:
            parts = i.split('=')
            if parts[0] == pkg.envar:
                opt = pkg.envar + "=" + fkrootLocation + ''.join(parts[1:])
                cmd.append(opt)
                hasSetEnvar = True
            else:
                cmd.append(i)
        else:
            cmd.append(i)

    if not hasSetEnvar:
        cmd += [pkg.envar+"="+fkrootLocation]

    return cmd + ["install"]

def handleFailedScript(scriptName, retCode):
    print("[Build] Script returned non-zero value ("+str(retCode)+"): " + scriptName)
    Utils.shouldContinue()
    
def openPkgTarball(pkg):
    oldContents = pkg.dirContents

    with tarfile.open(pkg.tarballLocation, 'r') as f:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(f, path=pkg.directory)

    ## Determine what was just extracted
    pkg.dirContents = os.listdir(pkg.directory)
    pkg.extractedContents = os.listdir(pkg.directory) #Put everything in extracted
    for i in oldContents:
        pkg.extractedContents.remove(i) #Remove old stuff from extracted
                                        #This ensures that if a new file
                                        #have the same name as an old one,
                                        #it gets counted as an extracted item

def runSh(pkg, scriptName, cwd, args=[]):
    extractedDir = pkg.directory + "/" + pkg.extractedContents[0]

    os.chdir(cwd)
    scriptLocation = extractedDir + "/" + os.path.basename(scriptName)
    shutil.copyfile(scriptName, scriptLocation)

    os.chmod(scriptLocation, stat.S_IEXEC) #marks script as executable

    returnCode = 0
    try:
        returnCode = subprocess.run([scriptLocation] + args).returncode
    except:
        returnCode = 0.5

    if returnCode != 0:
        handleFailedScript(scriptName, returnCode)


def runPkgCompileSh(pkg, cwd):
    if pkg.compileShLoc == None:
        print("\tNo 'compile.sh' to run")
    else:
        runSh(pkg, pkg.compileShLoc, cwd)
    

def runPkgPostInstallSh(pkg, cwd):
    if pkg.postInstallShLoc == None:
        print("\tNo 'postinstall.sh' to run")
    else:
        runSh(pkg, pkg.postInstallShLoc, cwd)

def runPkgPostFakeSh(pkg, postFakeLoc, cwd):
    if pkg.postFakeShLoc == None:
        print("\tNo 'postfake.sh' to run")
    else:
        runSh(pkg, pkg.postFakeShLoc, cwd, args=[postFakeLoc])

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
    
    consent = input("[Install] The above files will be installed")
    Utils.shouldContinue()
    
    for i in pkgsToInstall:
        install(i)

    #The last entry of pkgLocations will be the name of the pkg installed
    #The rest are dependencies. We only want a list of the dependencies
    depends = pkgDepends[:-1]
    print("[Install] Logging dependencies:", pkgName, "--", depends)

    installedDepends.addToDependsTree(pkgName, depends)

def checkDepends(pkgObj):
    for i in pkgObj.dependencies:
        if not List.isInstalled(i):
            print("[Install] Could not find dependency: " + i)
            Utils.shouldContinue()

