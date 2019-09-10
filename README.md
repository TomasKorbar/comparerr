# comparerr

Comparerr uses pylint to analyze 2 versions of python software versioned with git and lists you messages which did not occur in old version and messages which are no longer emitted. It is an alternative to pylints disabling of some messages because they are not useful or they are false positives.

## Example
We have 2 branches. Master is the most recent stable development and pull request is my new changes which add new feature to my software.
 - master
 - pullrequest

I want to know if i did not add some new warning to those which were already occurring.
So i will run:

    $ comparerr "./.git" "master" "pullrequest" --error-only --targets src/ tests/ \*.py
Let me explain what happens here.

 1. `"./.git"` first argument is a location of the git repository
 2. `"master"` first git reference for comparison
 3. `"pullrequest"` second git reference for comparison
 4. `--error-only` options which forces pylint and comparerr to work only with errors in code and
 not search for example coding style issues.
 4. `--targets src/ tests/ \*.py` these are folders and files which we want to analyze with pylint. *Please note escaped asterisk symbol. You can use regex but you must escape it, because your shell could and most probably will resolve them in context of your current working directory*

Now lets see the output.
```
Fixed errors:
Message: Instance of 'JunkClass' has no '_non_existent' member
File: /junk.py
Line: 4
Context:

class JunkClass:
    def __init__(self):
        self._non_existent += 1


Added errors:
Message: Undefined variable 'variabble'
File: /junk.py
Line: 9
Context:
    def great_method(self, keyword=None):
        variable = 1
        print(variabble)
```

First block `Fixed errors:` shows us what messages have not been present in analysis of new version.

Second block `Added errors:` shows us what messages have been added in analysis of new version.
