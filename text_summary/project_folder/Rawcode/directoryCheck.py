import os

def dirCheck():
    dirpath = os.getcwd()
    if dirpath == None:
        return "here"
    else:
        return dirpath