#!/usr/bin/python3
import argparse
import sys
import os

import Build
import Install
import List 
import Remove

parser = argparse.ArgumentParser(description='gpkg Package Manager')
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
                    help="List given packages, or list all packages",
                    dest="lPkg")
parser.add_argument("-La", "--list_associated",
                    metavar="<pkg_name>",
                    help="List files and directories associated with a given package",
                    dest="laPkg")
parser.add_argument("-i", "--init",
                    help="Initialize gpkg system",
                    action="store_true")
parser.add_argument('-B', "--build",
                   metavar="<dir>",
                   help="Build package from given directory",
                   dest="bPkg")

def install(pkg):
    if os.getuid() != 0:
        sys.exit("Can only install package as root")

    Install.install(pkg)

def remove(pkg):
    if os.getuid() != 0:
        sys.exit("Can only remove package as root")

    Remove.remove(pkg)

def init():
    pass

def listPkg(pkg):
    List.listPkg(pkg)

def listAssociated(pkg):
    List.listAssociated(pkg)

def build(pkg):
    Build.build(pkg)

if __name__ == '__main__':
    args = parser.parse_args()

    vals = vars(args).values()
    selectedArgVals = [x for x in vals if x != False and x != None]
    if selectedArgVals == []:
        parser.print_help()
        sys.exit()

    if args.inPkg != None:
        install(args.inPkg)
    if args.rmPkg != None:
        remove(args.rmPkg)
    if args.lPkg != None:
        listPkg(args.lPkg)
    if args.bPkg != None:
        build(args.bPkg)
    if args.laPkg != None:
        listAssociated(args.laPkg)
    if args.init:
        init()


