import os
import json
import sqlite3py
import structure
import decompress
from basicutils import *

class stemLogic():
    def __init__(self, gamedir):
        self.selfdir, self.gamedir = getParent(os.path.split(os.path.realpath(__file__))[0]), gamedir
        if self.__class__.__name__ == "stemLogic":
            selfStructure = structure.selfStructure
            for folder in selfStructure:
                dir = os.path.join(self.selfdir, folder)
                if not os.path.exists(dir):
                    os.makedirs(dir)
            try:
                conn = sqlite3py.connect(joinPath(self.selfdir, ".db/meta.db"), )
                cu = conn.cursor()
                for table in structure.dbStructure:
                    res = cu.execute('SELECT * FROM sqlite_master WHERE type="table" AND name=?', (table,))
                    if not len(tuple(res)):
                        cu.execute(
                            f'''CREATE TABLE {table}
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            susp_name       TEXT,
                            real_name       TEXT,
                            susp_vers       TEXT,
                            real_vers       TEXT,
                            type            TEXT,
                            path            TEXT,
                            structure       TEXT,
                            props           TEXT
                            );'''
                        )
                # DB structure:
                # susp_name and susp_vers are names and versions extracted from file/folder name.
                # Once manager could communicate with the MAS exporter, we should compare susp_names
                # with corresponding path names, and add their real_name and real_vers.
                # A type can be either "submod" or "spritepack".
                # A path is where this mod is currently located. 
                # The structure of a row is its filestructure stored in json dict. Nothing about frontend
                # most likely.
                # The props are spares.
                #
                # Logics:
                # A row with susp_name and susp_vers, but not real ones indicates it's analyzed but not
                # installed/recognized.
                # A row with real_name and real_vers, but not susp ones indicates it's installed/recognized
                # but not analyzed
                # Both intact indicates full support
                # To uninstall an analyzed mod, manager will uninstall every recorded file in file structure
                # from MAS.
                # To install an analyzed mod, manager will move everything entirely into the destination
                # folder, likely with an exception list like .git.
                # To recognize if an analyzed/remotely known mod, manager will try to find every recorded
                # file under corresponding folder. Matches exceeding a certain percentage will make this mod
                # considered installed, and a full match will make it considered intergral.
                # Mods installed through manager will be analyzed. Can also be done manually with installation
                # compression or folder.
                # Mods unknown anyway but installed -- cross your fingers.
            finally:
                conn.commit()
                conn.close()
            self.decInst = decompress.decLogic(self)

if __name__ == "__main__":
    a = stemLogic()
