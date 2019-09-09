#!/usr/bin/python3
import sys
import json

if __name__ == "__main__":

    with open(sys.argv[1],"r") as pl_file:
        old_errs_list = list(dict(json.load(pl_file)).values())

    with open(sys.argv[2],"r") as pl_file:
        new_errs_list = list(dict(json.load(pl_file)).values())

    old_contexts = [err["context"] for err in old_errs_list]
    new_contexts = [err["context"] for err in new_errs_list]

    solved_indexes = []
    broken_indexes = []

    for index, context in enumerate(old_contexts):
        if context not in new_contexts:
            solved_indexes.append(index)

    for index, context in enumerate(new_contexts):
        if context not in old_contexts:
            broken_indexes.append(index)

    if len(broken_indexes) > 0 or "--generate-report" in sys.argv:
        print("New errors:")
        for index in broken_indexes:
            print("file: %s" % new_errs_list[index]["path"])
            print("line: %s" % new_errs_list[index]["line"])
            print("message: %s" % new_errs_list[index]["msg"])
            print("context:\n %s" % new_errs_list[index]["context"])
        print("Fixed errors:")
        for index in solved_indexes:
            print("file: %s" % old_errs_list[index]["path"])
            print("line: %s" % old_errs_list[index]["line"])
            print("message: %s" % old_errs_list[index]["msg"])
            print("context:\n %s" % old_errs_list[index]["context"])


    if len(broken_indexes) > 0:
        sys.exit(1)
    else:
        sys.exit(0)
