import argparse
import sys

from .farewell import farewell
from .greet import greet
from .greet_all import greet_all


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print(greet("captain"))
        print(farewell("crew"))
        return 0

    parser = argparse.ArgumentParser(prog="greetings")
    sub = parser.add_subparsers(dest="command")
    greet_parser = sub.add_parser("greet")
    greet_parser.add_argument("username")
    greet_parser.add_argument("--lang")
    farewell_parser = sub.add_parser("farewell")
    farewell_parser.add_argument("name")
    farewell_parser.add_argument("--lang")
    greet_all_parser = sub.add_parser("greet-all")
    greet_all_parser.add_argument("names", nargs="+")
    greet_all_parser.add_argument("--lang")
    args = parser.parse_args(argv)
    if args.command == "greet":
        if args.lang is None:
            print(greet(args.username))
        else:
            print(greet(args.username, language=args.lang))
        return 0
    if args.command == "farewell":
        if args.lang is None:
            print(farewell(args.name))
        else:
            print(farewell(args.name, language=args.lang))
        return 0
    if args.command == "greet-all":
        if args.lang is None:
            lines = greet_all(args.names)
        else:
            lines = greet_all(args.names, language=args.lang)
        for line in lines:
            print(line)
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
