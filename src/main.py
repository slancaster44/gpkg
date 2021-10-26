#!/usr/bin/python3
import argparse
import sys
import os

import UserMgmt
import Installation
import PkgCreation
import Listing
import Removal
import Init


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
parser.add_argument("-i", "--init",
                    help="Initialize gpkg system",
                    action="store_true")
parser.add_argument('-B', "--build",
                   metavar="<dir>",
                   help="Build package from given directory",
                   dest="bPkg")

def install(pkg):
    Installation.install(os.path.abspath(pkg))

def remove(pkg):
    Removal.remove(pkg)

def listPkg(pkg):
    pkgInfo = Listing.getInfoFor(pkg)
    print(pkgInfo)

def init():
    Init.initGpkg()

def build(pkg):
    name = os.path.basename(pkg)
    PkgCreation.mkPkgFrom(name, os.path.abspath(pkg))

if __name__ == '__main__':
    args = parser.parse_args()

    if os.getuid() != 0:
        parser.print_help()
        sys.exit("Must run gpkg as root")

    if args.inPkg != None:
        install(args.inPkg)
    elif args.rmPkg != None:
        remove(args.rmPkg)
    elif args.lPkg != None:
        listPkg(args.lPkg)
    elif args.bPkg != None:
        build(args.bPkg)
    elif args.init:
        init()
    else:
       sys.exit("No valid arguments")
