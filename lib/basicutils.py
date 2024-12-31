import os
import re
import json

def readJson(dir) -> list:
    with open(dir, "r", encoding="utf-8") as j:
        return json.loads(j.read())

def getFilename(dir) -> str:
    try:
        parent = re.search(r"^.*/(.*?)$", os.path.normpath(dir).replace("\\", "/"))[1]
        return parent
    except:
        return dir
    
def stripFilename(filename) -> str:
    try:
        striped = re.match(r"^(.+)\.", filename)[1]
        return striped
    except:
        return filename

def tryVersion(filename) -> str:
    try:
        version = re.findall("([0-9][-_.0-9A-Fa-f]*[-_0-9A-Fa-f])", filename)[-1]
        return version
    except:
        return "unknown"
    
def combUname(filename, subspr, version) -> str:
    return f"{filename}&s={subspr}&v={version}"

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
    print(tryVersion(r"MAICA_ChatSubmod-1.1.18.zip"))