#!/usr/bin/python3

import argparse

import Repo.Dmirepo as Repo
import Repo.Search as Search

parser = argparse.ArgumentParser(description="dmir - DMI Repository management tool")
parser.add_argument("-M", "--mkrepo",
                    metavar="<repo_name>",
                    help="create directory of given name, and initialize repo in that directory",
                    dest="mArg")
parser.add_argument("-A", "--addpkg",
                    metavar=("<pkg>", "<repo>"),
                    help="add given package to a given repo",
                    nargs=2,
                    dest="aArgs")
parser.add_argument("-R", "--rmpkg",
                    metavar=("<pkg>", "<repo>"),
                    help="remove given pkg from a given repo",
                    nargs=2,
                    dest="rArgs")
parser.add_argument("-S", "--search",
                    metavar=("<pkg>", "<repo>"),
                    help="search for given package in given repo",
                    nargs=2,
                    dest="sArgs")

if __name__ == "__main__":
    args = parser.parse_args()

    if args.mArg != None:
        Repo.mkRepo(args.mArg)
    elif args.aArgs != None:
        Repo.addPkg(args.aArgs[0], args.aArgs[1])
    elif args.rArgs != None:
        Repo.rmPkg(args.rArgs[0], args.rArgs[1])
    elif args.sArgs != None:
        print(Search.search(args.sArgs[0], args.sArgs[1]))
    else:
        parser.print_help()
