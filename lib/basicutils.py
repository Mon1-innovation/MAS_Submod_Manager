import os
import re

def getFilename(dir) -> str:
    parent = re.search(r"^.*/(.*?)$", os.path.normpath(dir).replace("\\", "/"))[1]
    return parent
    
def stripFilename(filename) -> str:
    try:
        striped = re.match(r"^(.+)\.", filename)[1]
        return striped
    except:
        return filename

def getParent(dir) -> str:
    parent = re.search(r"^(.*)/.*?$", os.path.normpath(dir).replace("\\", "/"))[1]
    return parent

def breakDir(dir) -> list:
    chops = re.split("/", os.path.normpath(dir).replace("\\", "/"))
    return chops

def shovelDict(dict, chops) -> None:
    for chop in chops:
        if not chop in dict:
            dict[chop] = {}
        dict = dict[chop]

def stripDict(dict, chops) -> dict:
    for chop in chops:
        if chop in dict:
            dict = dict[chop]
        else:
            break
    return dict

            


if __name__ == "__main__":
    print(stripFilename(r"MAICA_ChatSubmod-1.1.18.zip"))