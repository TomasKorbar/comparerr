#!/usr/bin/python3

import sys
import re
import json
import linecache

if __name__ == "__main__":
    errors = {}

    with open(sys.argv[1],"r") as pl_file:
        pl_output = pl_file.read()

    # get rid of module names
    pl_output = re.sub(r"\*\*\*\*\*\*\*\*\*\*\*\*\*.*\n", "", pl_output)

    # we use custom pylint message format which looks like this:
    # {abspath}:{path}:{line}:{msg_id}:{msg}
    err_num = 0
    for line in pl_output.splitlines():
        fields = line.split(":")
        context = ""

        err_linenum = int(fields[2])
        for linenum in range(err_linenum-2 if err_linenum > 2 else 0,
                             err_linenum+2):
            context += linecache.getline(fields[0], linenum)

        error_dict = {"path":    fields[1],
                      "line":    fields[2],
                      "msg_id":  fields[3],
                      "msg":     fields[4],
                      "context": context
                     }
        errors[str(err_num)] = error_dict
        err_num += 1

    with open(sys.argv[2], "w") as out_file:
        json.dump(errors, out_file)