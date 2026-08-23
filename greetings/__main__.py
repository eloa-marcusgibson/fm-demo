import argparse
import json
import sys

from .catalog import language_codes
from .farewell import farewell
from .greet import greet
from .greet_all import greet_all


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if not argv or argv == ["--json"]:
        print(greet("captain"))
        print(farewell("crew"))
        return 0

    parser = argparse.ArgumentParser(prog="greetings")
    parser.add_argument("--json", action="store_true")
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
    sub.add_parser("langs")
    args = parser.parse_args(argv)
    if args.command == "greet":
        if args.lang is None:
            line = greet(args.username)
        else:
            line = greet(args.username, language=args.lang)
        if args.json:
            print(json.dumps({"message": line}))
        else:
            print(line)
        return 0
    if args.command == "farewell":
        if args.lang is None:
            line = farewell(args.name)
        else:
            line = farewell(args.name, language=args.lang)
        if args.json:
            print(json.dumps({"message": line}))
        else:
            print(line)
        return 0
    if args.command == "langs":
        for code in language_codes():
            print(code)
        return 0
    if args.command == "greet-all":
        if args.lang is None:
            lines = greet_all(args.names)
        else:
            lines = greet_all(args.names, language=args.lang)
        if args.json:
            print(json.dumps(lines))
        else:
            for line in lines:
                print(line)
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
