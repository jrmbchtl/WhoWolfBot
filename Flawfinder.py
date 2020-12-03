import os
import flawfinder


files = []


def checkPath(path=None):
    if path is None:
        path = "./"
    p = os.listdir(path)
    for f in p:
        if os.path.isfile(path + f) and f.endswith(".py"):
            files.append(path + f)
        elif os.path.isdir(path + f):
            checkPath(path + f + "/")


checkPath()
flawfinder.flawfind(files)
