"""checks source code for pylint errors"""
import os
import pylint.lint


def rec_get_files(files, path=None):
    """recursively returns all .py files from path"""
    if path is None:
        path = "./"
    directory = os.listdir(path)
    for file in directory:
        if os.path.isdir(path + file):
            rec_get_files(files, path + file + "/")
        elif os.path.isfile(path + file) and file.endswith(".py"):
            files.append(path + file)
    return files


pylint_opts = rec_get_files([])
pylint.lint.Run(pylint_opts)
