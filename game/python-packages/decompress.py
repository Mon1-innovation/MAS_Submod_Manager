import os
import json
import copy
import shutil
import sqlite3py
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
        self.conn = sqlite3py.connect(joinPath(self.selfdir, ".db/meta.db"))

    def __del__(self):
        self.conn.close()

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
            outdir = joinPath(self.selfdir, f".tmp/{stripFilename(getFilename(arcdir))}")
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
                dlist = breakDir(joinPath(base, dir))
                shovelDict(filesDict, dlist)
            for dir in dirs:
                dlist = breakDir(joinPath(base, dir))
                if dlist[-2] == "Submods" and not readSignal:
                # A submod detected
                    j = -3
                    for i in [-1, -2, -3]:
                    # Leak prevention: limit operations in pathdir
                        try:
                            if len(joinPath(*dlist[:i])) < len(pathdir):
                                j = i + 1
                        except:
                            j = i + 1
                    signalAppending = [dlist[-1], 1, joinPath(*dlist[:j])[len(pathdir):]]
                    if not signalAppending in readSignal:
                        readSignal.append(signalAppending)
                elif dlist[-1] == "mod_assets" and not "Submods" in stripDict(dirsDict, dlist[:-1]):
                # A spritepack detected
                    signalAppending = [dlist[-2], 2, joinPath(*dlist[:-1])[len(pathdir):]]
                    if not signalAppending in readSignal:
                        readSignal.append(signalAppending)
                shovelDict(dirsDict, dlist)
        filesDict = stripDict(filesDict, breakDir(pathdir))
        dirsDict = stripDict(dirsDict, breakDir(pathdir))
        dirsDict.update(filesDict)
        dictCombined = [readSignal, filesDict]
        return dictCombined
    
    def findModbase(self, dict1) -> str:
    # Find the mod basedir, like containing game folder
    # Will combine a signal of which type this mod belongs
    # Signal 0 for no signal; likely submod package only
    # Signal 1 for submods containing Submods folder
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
                    basedir = joinPath(*searchSignal[:-1])
                else:
                #Setting basedir to game
                    basedir = joinPath(*searchSignal)
            else:
            # Setting basedir to Submods
                basedir = joinPath(*searchSignal, "Submods")
        else:
        # No signal found, suspecting it should be installed directly
            basedir = None
        return typeSignal, basedir

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
                        compSignal.append(joinPath(*routeList))
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
        return compSignal
    
    def readStruct(self, table, conds, andor=True) -> tuple:
    # Just reading something from db
        sentence = ''
        for k, v in conds.items():
            if sentence:
                sentence += "AND" if andor else "OR"
            sentence += f'{k}="{v}"'
        cu = self.conn.cursor()
        res = cu.execute(f"SELECT * FROM {table} WHERE {sentence}")
        return tuple(res)

    def storStruct(self, table, conds, stores, andor=True) -> None:
    # Just writting something into db
        sentence = ''
        ids = []
        cu = self.conn.cursor()
        if conds:
            for k, v in conds.items():
                if sentence:
                    sentence += "AND" if andor else "OR"
                sentence += f'{k}="{v}"'
            res1 = cu.execute(f"SELECT * FROM {table} WHERE {sentence}")
            for r in res1:
                ids.append(r[0])
        if not len(ids):
            values = "','".join(stores)
            res2 = cu.execute(f'''INSERT INTO {table} (susp_name, real_name, susp_vers, real_vers, type, path, structure, props) VALUES ('{values}')''')
        else:
            for id in ids:
                storesWithId = copy.deepcopy(stores)
                storesWithId.append(id)
                res2 = cu.execute(f'UPDATE {table} SET susp_name=?, real_name=?, susp_vers=?, real_vers=?, type=?, path=?, structure=?, props=? WHERE id=?', (storesWithId))
        self.conn.commit()

    def analyzeSubmod(self, moddir) -> bool:
    # Analyze and store the structure of selected mod
        if self.verifyArc(moddir):
            moddir = self.decompArc(moddir)
        struct = self.recuRead(moddir)
        # This may contain multiple mods
        for metadata in struct[0]:
            modname = metadata[0]
            subOrSpr = metadata[1]
            relPath = metadata[2]
            modver = tryVersion(getFilename(relPath))
            if modver == "unknown":
                modver = tryVersion(getFilename(moddir))
            uname = combUname(modname, subOrSpr, modver)
            if subOrSpr == 1:
                categ = "submod"
            elif subOrSpr == 2:
                categ = "spritepack"
            stores = [modname, '', modver, '', categ, joinPath(moddir, relPath.strip("/").strip("\\")), json.dumps(stripDict(struct[1], breakDir(relPath)), ensure_ascii=False), '']
            self.storStruct("local_meta", {"susp_name": modname}, stores)

    def verifySubmod(self, metadata, basedir=None) -> list:
    # Check integrity of selected pathtree
        if not basedir:
            basedir = metadata["path"]
        verifySignal = []
        def recuVerify(dict0, recuCarriage=[]):
            nonlocal verifySignal, basedir
            for k, v in dict0.items():
                if os.path.exists(joinPath(basedir, *recuCarriage, k)):
                    pass
                else:
                    verifySignal.append(joinPath(basedir, *recuCarriage, k))
            for k, v in dict0.items():
                spawnedCarriage = copy.copy(recuCarriage)
                spawnedCarriage.append(k)
                recuVerify(dict0[k], spawnedCarriage)
        recuVerify(metadata["structure"])
        return verifySignal

    def listAvaliables(self, table) -> list:
    # Use this to list all avaliable mods from selected table
        cu = self.conn.cursor()
        res = cu.execute(f"SELECT * FROM {table}")
        return list(res)

    def findConflicts(self, name1, name2) -> list:
        pass

    def installSubmod(self, metadata) -> bool:
    # Install the desired submod to gamedir
        pass

if __name__ == "__main__":
    b=decLogic()
    persistent.submod_file_dir = "F:\Ren'Py_Projects\phone_messenger_fullscreen.zip"
    if persistent.submod_file_dir:
        b.decompArc(persistent.submod_file_dir)
    #print(b.recuRead(r"D:\0submanager\MAS_Submod_Manager\.tmp\MAICA_ChatSubmod-1.1.18\MAICA_ChatSubmod-1.1.18"))
        b.analyzeSubmod(selfdir + "/.tmp")
    #b.findModbase(readJson(r"D:\0submanager\MAS_Submod_Manager\storage\MAICA_ChatSubmod&v=1.1.18.json")[1])
    #b.verifySubmod(b.readStruct("MAICA_ChatSubmod&s=1&v=1.1.18", "submods"))
    #b.recuComp(b.readStruct("MAICA_ChatSubmod&s=1&v=1.1.18", "submods")["structure"], b.readStruct("MAICA_ChatSubmod&s=1&v=unknown", "submods")["structure"])
    filename = 'game/example.txt'
    # 使用with语句打开文件（以写入模式），并自动处理关闭文件
    with open(filename, 'w', encoding='utf-8') as file:
        # 写入内容到文件
        file.write(b.listAvaliables("local_meta"))
        pass

