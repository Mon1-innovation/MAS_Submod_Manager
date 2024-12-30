import os
import json
import copy
import shutil
import patoolib
from basicutils import *

class decLogic():
    def __init__(self, stemInst=None):
    # Can be initialized with stemInst
        if stemInst:
            self.selfdir, self.gamedir = stemInst.selfdir, stemInst.gamedir
        else:
            self.selfdir = getParent(os.path.split(os.path.realpath(__file__))[0])
            self.gamedir = None

    def verifyArc(self, arcdir) -> bool:
    # Verify if an archive is intact. None indicates path/fs issue
        try:
            patoolib.test_archive(arcdir)
            return True
        except patoolib.PatoolError:
            return False
        except:
            return None

    def decompArc(self, arcdir, outdir=None) -> str:
    # Decompress an archive to .tmp or desired path
        if not outdir:
            outdir = os.path.join(self.selfdir, f"/.tmp/{stripFilename(getFilename(arcdir))}")
            if os.path.exists(outdir):
                shutil.rmtree(outdir)
        patoolib.extract_archive(arcdir, outdir=outdir)
        return outdir
    
    def recuRead(self, pathdir) -> list:
    # Recursively list the structure of selected path
        filesDict, dirsDict = {}, {}
        for base, dirs, files in os.walk(pathdir, topdown=False):
            for dir in files:
                dlist = breakDir(os.path.join(base, dir))
                shovelDict(filesDict, dlist)
            for dir in dirs:
                dlist = breakDir(os.path.join(base, dir))
                shovelDict(dirsDict, dlist)
        filesDict = stripDict(filesDict, breakDir(pathdir))
        dirsDict = stripDict(dirsDict, breakDir(pathdir))
        dictCombined = [filesDict, dirsDict]
        return dictCombined
    
    def recuComp(self, dict1, dict2) -> list:
    # Recursively compare two dicted file structures
        compSignal = []
        def launchComp(routeList):
            nonlocal compSignal
            dict0c = dict2
            for jump in routeList:
                if jump in dict0c:
                    dict0c = dict0c[jump]
                    if routeList.index(jump) >= len(routeList) - 1:
                        compSignal.append(os.path.join(*[str(s) for s in routeList]))
                else:
                    break
                    
        def recuTravel(dict0, callable, recuCarriage=[]):
            for k, v in dict0.items():
                spawnedCarriage = copy.copy(recuCarriage)
                spawnedCarriage.append(k)
                if len(v) > 0:
                    recuTravel(v, callable, spawnedCarriage)
                else:
                    callable(spawnedCarriage)
        recuTravel(dict1, launchComp)
        print(compSignal)
        return compSignal
    
    def storStruct(self, struct, name) -> None:
    # Just writting something into a file
    # Maybe we should use SQLite instead?
        with open(os.path.join(self.selfdir, f"storage/{name}.json"), "w", encoding="utf-8") as store:
            store.write(json.dumps(struct))

    def analyzeSubmod(self, moddir) -> bool:
    # Analyze and store the structure of selected submod
        if self.verifyArc(moddir):
            moddir = self.decompArc(moddir)
        modname = getFilename(moddir)
        struct = self.recuRead(moddir)
        self.storStruct(struct, modname)

    def installSubmod(self, moddir) -> bool:
    # Install the desired submod to gamedir.
        pass

if __name__ == "__main__":
    b=decLogic()
    #b.decompArc(r"D:\0submanager\dummy\submod_dummy\MAICA_ChatSubmod-1.1.18.zip")
    #b.recuRead(r"D:\0submanager\MAS_Submod_Manager\.tmp\MAICA_ChatSubmod-1.1.18\MAICA_ChatSubmod-1.1.18")
    #b.recuComp({1:{},2:{3:{}}},{2:{4:{},3:{}}})
    b.analyzeSubmod(r"D:\0submanager\dummy\submod_dummy\MAICA_ChatSubmod-1.1.18.zip")

