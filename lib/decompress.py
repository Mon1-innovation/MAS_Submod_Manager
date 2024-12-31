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
    # Verify if an archive is intact
        try:
            patoolib.test_archive(arcdir)
            return True
        except:
            return False

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
        readSignal = []
        filesDict, dirsDict = {}, {}
        for base, dirs, files in os.walk(pathdir, topdown=False):
            for dir in files:
                dlist = breakDir(os.path.join(base, dir))
                shovelDict(filesDict, dlist)
            for dir in dirs:
                dlist = breakDir(os.path.join(base, dir))
                if dlist[-2] == "Submods" and not readSignal:
                # A submod detected
                    signalAppending = [dlist[-1], 1, os.path.join(*dlist[:-3])[len(pathdir):]]
                    if not signalAppending in readSignal:
                        readSignal.append(signalAppending)
                elif dlist[-1] == "mod_assets" and not "Submods" in stripDict(dirsDict, dlist[:-1]):
                # A spritepack detected
                    signalAppending = [dlist[-2], 2, os.path.join(*dlist[:-1])[len(pathdir):]]
                    if not signalAppending in readSignal:
                        readSignal.append(signalAppending)
                shovelDict(dirsDict, dlist)
        filesDict = stripDict(filesDict, breakDir(pathdir))
        dirsDict = stripDict(dirsDict, breakDir(pathdir))
        dictCombined = [readSignal, filesDict, dirsDict]
        return dictCombined
    
    def findModbase(self, dict1) -> str:
    # Find the mod basedir, like containing game folder
    # Will combine a signal of which type this mod belongs
    # Signal 1 for simple submod containing Submods folder only
    # Signal 2 for submods with game folder
    # Signal 3 for submods with game sibling folders like lib
    # Only applies to submods. Spritepacks should be processed already
        typeSignal = 0
        searchSignal = None
        def recuSearch(dict0, pattern, recuCarriage=[], searchAll=False):
            nonlocal searchSignal
            if searchSignal == None or searchAll:
                for k, v in dict0.items():
                    if not k == pattern:
                        pass
                    else:
                        if not searchAll:
                            searchSignal = recuCarriage
                        else:
                            if searchSignal == None:
                                searchSignal = []
                            searchSignal.append(recuCarriage)
                for k, v in dict0.items():
                    spawnedCarriage = copy.copy(recuCarriage)
                    spawnedCarriage.append(k)
                    recuSearch(dict0[k], pattern, spawnedCarriage)
        recuSearch(dict1, "Submods")
        if isinstance(searchSignal, list):
        # It is a submod
            typeSignal += 1
            # now we want to know if it has game folder
            if len(searchSignal) and searchSignal[-1] == "game":
            # Sure it does
                typeSignal += 1
                # And if any siblings
                dictTemp = dict1
                sibsList = []
                ignList = [r"\.vscode", r"\.git", r"\.gitignore", r".*readme.*", r".*copyright.*", r".*document.*", r".*\.txt", r".*\.md"]
                comIgnList = []
                for i in ignList:
                    comIgnList.append(re.compile(i, re.I))
                for f in searchSignal[:-1]:
                    dictTemp = dictTemp[f]
                for k, v in dictTemp.items():
                    sibsList.append(k)
                for c in comIgnList:
                    for k in sibsList:
                        if c.match(k):
                            sibsList.remove(k)
                if len(sibsList) > 1:
                # Sure there are
                    typeSignal += 1
                    basedir = os.path.join(*searchSignal[:-1])
                else:
                #Setting basedir to game
                    basedir = os.path.join(*searchSignal)
            else:
            # Setting basedir to Submods
                basedir = os.path.join(*searchSignal, "Submods")
        return basedir

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
    
    def storStruct(self, struct, name, cato='') -> None:
    # Just writting something into a file
    # Maybe we should use SQLite instead?
        if cato:
            cato += "/"
        with open(os.path.join(self.selfdir, f"storage/{cato}{name}.json"), "w", encoding="utf-8") as store:
            store.write(json.dumps(struct))

    def analyzeSubmod(self, moddir) -> bool:
    # Analyze and store the structure of selected submod
        if self.verifyArc(moddir):
            moddir = self.decompArc(moddir)
        struct = self.recuRead(moddir)
        # This may contain multiple mods
        for metadata in struct[0]:
            modname = metadata[0]
            subOrSpr = metadata[1]
            relPath = metadata[2]
            print(relPath)
            modver = tryVersion(getFilename(relPath))
            if modver == "unknown":
                modver = tryVersion(getFilename(moddir))
            storing = []
            for s in struct[1:]:
                storing.append(stripDict(s, breakDir(relPath)))
            uname = combUname(modname, subOrSpr, modver)
            match subOrSpr:
                case 1:
                    cato = "submods"
                case 2:
                    cato = "spritepacks"
            self.storStruct(storing, uname, cato)

    def findConflicts(self, name1, name2) -> list:
        pass

    def installSubmod(self, moddir) -> bool:
    # Install the desired submod to gamedir.
        pass

if __name__ == "__main__":
    b=decLogic()
    #b.decompArc(r"D:\0submanager\dummy\submod_dummy\MAICA_ChatSubmod-1.1.18.zip")
    #print(b.recuRead(r"D:\0submanager\MAS_Submod_Manager\.tmp\MAICA_ChatSubmod-1.1.18\MAICA_ChatSubmod-1.1.18"))
    #b.recuComp({1:{},2:{3:{}}},{2:{4:{},3:{}}})
    b.analyzeSubmod(r"D:\0submanager\dummy\sprite_dummy")
    #b.findModbase(readJson(r"D:\0submanager\MAS_Submod_Manager\storage\MAICA_ChatSubmod&v=1.1.18.json")[1])

