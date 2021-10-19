#!/usr/bin/python3
import argparse
import sys
import os

import UserMgmt
import Installation
import PkgCreation


parser = argparse.ArgumentParser(description='gpkg Package Manager')
parser.add_argument("-I", "--install",
                    metavar="<pkg_name>",
                    help="Install given package",
                    dest="inPkg")
parser.add_argument("-R", "--remove",
                    metavar="<pkg_name>",
                    help="Remove given package",
                    dest="rmPkg")
parser.add_argument("-C", "--clean",
                    help="Clean dependencies",
                    action="store_true")
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
    print("Removing", pkg)

def clean():
    print("Removing unused dependencies")

def list(pkg):
    print("Listing", pkg)

def init():
    shouldContinue = input("This may only be executed upon first run of gpkg. Continue? (y/N) ")
    if shouldContinue != "y" and shouldContinue != "Y":
        sys.exit(1)

    UserMgmt.addInstallGroup()

def build(pkg):
    name = os.path.basename(pkg)
    PkgCreation.mkPkgFrom(name, os.path.abspath(pkg))

if __name__ == '__main__':
    if os.getuid() != 0:
        sys.exit("Must run gpkg as root")

    args = parser.parse_args()
    if args.inPkg != None:
        install(args.inPkg)
    elif args.rmPkg != None:
        remove(args.rmPkg)
    elif args.lPkg != None:
        list(args.lPkg)
    elif args.bPkg != None:
        build(args.bPkg)
    elif args.clean:
        clean()
    elif args.init:
        init()
    else:
        sys.exit("No valid arguments")
