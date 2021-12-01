import List
import Install.fakerootMapper as fakerootMapper
import List.packageMetadata as PkgMetadata
import Utils

'''
Even though it would make more sense
to put this functino in the List module,
it is here to avoid circular dependencies
'''

def mkListing():
    Utils.ensureLibDmi() #Ensure '/var/lib/dmi' exists for listing to go in

    pkgInfo = {}

    pkgInfo["name"] = input("Package name: ")
    pkgInfo["version"] = input("Package version: ")
    pkgInfo["description"] = input("Package description: ")
    pkgInfo["dependencies"] = []

    while True:
        hasDepends = input("Does this package have a dependency? [y/N] ")
        if hasDepends != "y" and hasDepends != "Y":
            break
        else:
            dependsName = input("Dependency name: ")
            pkgInfo["dependencies"].append(dependsName)

    fkRootMap = fakerootMapper.FakerootMap()
    pkgObj = PkgMetadata.pkgMetadata(pkgInfo, fkRootMap)
    List.saveListingOn(pkgObj)

