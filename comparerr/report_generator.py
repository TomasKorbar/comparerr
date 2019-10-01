"""Module containing ReportGenerator class"""
import os
import sys
import glob
import shutil
import tempfile
import linecache
import git
import pylint.lint
from pylint.utils import Message as PylintMessage

from comparerr.utils import ComparerrReporter, ComparerrMessage

class ReportGenerator:
    """Class containing methods for work with 2 versions of python software
    versioned in git.
    """
    def __init__(self, location, targets, only_errors=False, precision=2):
        self.error_only = only_errors
        self.precision = precision
        self.location = location
        self.targets = targets

    def compare_versions(self, ref1, ref2):
        """Analyze both versions of software according to references and return
        comparison

        Positional arguments:
        ref1 -- first git reference to a specific version
        ref2 -- second reference to a specific version

        Return value:
        tuple -- (list(fixed_errors), list(added_errors))
        """

        changed_files = self._get_changed_files(ref1, ref2)

        old_version_errors = self.analyze_version(ref1, changed_files)
        new_version_errors = self.analyze_version(ref2, changed_files)

        old_contexts = [err.context for err in old_version_errors]
        new_contexts = [err.context for err in new_version_errors]

        new_errors = []
        fixed_errors = []

        # errors which are not in new_version but were in old_version
        # are errors that have been fixed
        for index, error in enumerate(old_version_errors):
            if error.context not in new_contexts:
                fixed_errors.append(index)

        # errors which were not in old_version but are in new_version
        # are errors that have been created
        for index, error in enumerate(new_version_errors):
            if error.context not in old_contexts:
                new_errors.append(index)

        return ([old_version_errors[index] for index in fixed_errors],
                [new_version_errors[index] for index in new_errors]
               )

    def analyze_version(self, ref, concrete_targets=None):
        """Analyze specific version of python software according to git
        reference

        Positional arguments:
        ref -- Git reference to version

        Return value:
        list(ComparerrMessage) -- list of messages about errors
        """
        # create temporary directory for copied repository
        workdir = tempfile.mkdtemp()

        # copy repository
        shutil.copytree(self.location, os.path.join(workdir, ".git"))
        cloned_repo = git.Repo(path=workdir)
        cloned_repo.head.reset(commit=ref, working_tree=True)

        # use pylint to analyze source code
        msgs = self._get_messages(workdir, concrete_targets)

        # delete temporary directory and its contents
        cloned_repo.close()
        shutil.rmtree(workdir)

        # check if pylint did not report failure and if so then inform about it
        # user
        for msg in msgs:
            if msg.original_message.C == "F":
                print("Pylint reported failure while analyzing %s reference %s"
                      % (self.location, ref),
                      file=sys.stderr)
                print(msg.original_message.msg)
                sys.exit(2)

        # return all messages and their contexts
        return msgs

    def _targets2abspaths(self, abspath):
        abspaths = []
        for target in self.targets:
            new_path = glob.glob(os.path.join(abspath, target), recursive=True)
            if isinstance(new_path, list):
                abspaths.extend(new_path)
            else:
                abspaths.append(new_path)
        return abspaths

    def _filter_paths(self, root, paths, focused_paths):
        filtered_paths = []
        for target in list(paths):
            if os.path.isdir(target):
                for pfile in glob.glob(os.path.join(target, "**/*"), recursive=True):
                    if pfile.replace(root + "/", "") in focused_paths:
                        filtered_paths.append(pfile)
            else:
                if target.replace(root, "") in focused_paths:
                    filtered_paths.append(target)
        return filtered_paths

    def _strip_path_from_pylint_errors(self, root, pylint_errors):
        new_errors = []
        for err in pylint_errors:
            new_errors.append(PylintMessage(
                err.msg_id,
                err.symbol,
                (err.abspath,
                 err.path.replace(root, ""),
                 err.module,
                 err.obj,
                 err.line,
                 err.column
                ),
                err.msg,
                err.confidence,
            ))
        return new_errors

    def _get_messages(self, path, concrete_targets=None):
        # reporter will hold errors
        rprtr = ComparerrReporter()
        # add absolute path to targets
        abspath_targets = self._targets2abspaths(path)

        final_targets = []
        # if we know which files changed than we can scan only them and save time
        if concrete_targets:
            final_targets = self._filter_paths(path, abspath_targets, concrete_targets)
        else:
            final_targets = abspath_targets

        args = ["-sn", "--exit-zero"]
        if self.error_only:
            args.append("-E")
        args.extend(final_targets)
        pylint.lint.Run(args, reporter=rprtr, do_exit=False)

        # pylint is adding path of temporary folder to the path of errors
        # this is redundant so we will strip it
        rprtr.errors = self._strip_path_from_pylint_errors(path, rprtr.errors)

        return self._get_message_context(rprtr.errors)

    def _get_message_context(self, messages):
        msgs_with_context = []
        for message in messages:
            context = ""
            # if it is possible then save line with error and number of lines
            # specified in _precision before + after error
            minl = message.line - self.precision
            maxl = message.line + self.precision

            for linenum in range(minl if minl > self.precision else 1,
                                 maxl):
                context += linecache.getline(message.abspath, linenum)
            msgs_with_context.append(ComparerrMessage(message, context))
        return msgs_with_context

    def _get_changed_files(self, ref1, ref2):
        # create temporary directory for copied repository
        workdir = tempfile.mkdtemp()

        # copy repository
        shutil.copytree(self.location, os.path.join(workdir, ".git"))
        cloned_repo = git.Repo(path=workdir)
        # get names of files which changed between two refs
        names_string = cloned_repo.git.diff(ref1, ref2, "--name-only")
        names_list = [name for name in names_string.splitlines()]
        return names_list
