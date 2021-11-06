#!/usr/bin/python3
import argparse
import sys
import os

import Build
import Build.dmip as dmip
import Install
import List 
import Remove

parser = argparse.ArgumentParser(description='Dandified Make Install -- Package Manager')
parser.add_argument("-I", "--install",
                    metavar="<pkg_name>",
                    help="Install given package",
                    dest="inPkg")
parser.add_argument("-R", "--remove",
                    metavar="<pkg_name>",
                    help="Remove given package",
                    dest="rmPkg")
parser.add_argument("-L", "--list",
                    metavar="<pkg_name>",
                    help="List information on an installed package",
                    dest="lPkg")
parser.add_argument("-La", "--list_associated",
                    metavar="<pkg_name>",
                    help="List files and directories associated with a given package",
                    dest="laPkg")
parser.add_argument("-Am", "--make_association",
                    metavar="<file_or_dir_name> <pkg_name>",
                    help="Associate given file or dir with given package",
                    nargs=2,
                    dest="amArgs")
parser.add_argument("-Ar", "--remove_association",
                    metavar="<file_or_dir_name> <pkg_name>",
                    help="Remove association of file or dir with given package",
                    nargs=2,
                    dest="arArgs")
parser.add_argument('-B', "--build",
                   metavar="<dir>",
                   help="Build package from given directory",
                   dest="bPkg")
parser.add_argument('-Bd', "--make_build_dir",
                    metavar="<tarball>",
                    help="Create a directory with a given tarball that can be used to create a '.dmi' file",
                    dest="bdPkg")

def install(pkg):
    ensureRootPrivilege()

    Install.install(pkg)

def remove(pkg):
    ensureRootPrivilege()
    Remove.remove(pkg)


def listPkg(pkg):
    List.listPkg(pkg)

def listAssociated(pkg):
    List.listAssociated(pkg)

def makeAssociation(item, pkg):
    ensureRootPrivilege()
    List.associateNewItemWithPkg(item, pkg)

def removeAssociation(item, pkg):
    ensureRootPrivilege()
    List.rmAssocItemFromPkg(item, pkg)

def build(pkg):
    Build.build(pkg)

def mkDmipDir(pkg):
    dmip.mkDmipDir(pkg)

def ensureRootPrivilege():
    if os.getuid() != 0:
        sys.exit("Can only run this operation as root")

if __name__ == '__main__':
    args = parser.parse_args()

    if args.inPkg != None:
        install(args.inPkg)
    elif args.rmPkg != None:
        remove(args.rmPkg)
    elif args.lPkg != None:
        listPkg(args.lPkg)
    elif args.bPkg != None:
        build(args.bPkg)
    elif args.bdPkg != None:
        mkDmipDir(args.bdPkg)
    elif args.laPkg != None:
        listAssociated(args.laPkg)
    elif args.amArgs != None:
        makeAssociation(args.amArgs[0], args.amArgs[1])
    elif args.arArgs != None:
        removeAssociation(args.arArgs[0], args.arArgs[1])
    else:
        parser.print_help()

