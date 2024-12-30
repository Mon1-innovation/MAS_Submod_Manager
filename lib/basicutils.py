import os
import re

def getFilename(dir) -> str:
    try:
        if os.name == "nt":
            filename = re.search(r"^.*\\(.*?)$", dir)[1]
        else:
            filename = re.search(r"^.*/(.*?)$", dir)[1]
        return filename
    except:
        return False
    
def stripFilename(filename) -> str:
    try:
        striped = re.match(r"^(.+)\.", filename)[1]
        return striped
    except:
        return filename

def getParent(dir) -> str:
    try:
        if os.name == "nt":
            parent = re.search(r"^(.*)\\.*?$", dir)[1]
        else:
            parent = re.search(r"^(.*)/.*?$", dir)[1]
        return parent
    except:
        return False
   

if __name__ == "__main__":
    print(stripFilename(r"MAICA_ChatSubmod-1.1.18.zip"))