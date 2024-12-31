import os
import json
import sqlite3
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
                conn = sqlite3.connect(joinPath(self.selfdir, ".db/meta.db"), )
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
                # A type can be either "submods" or "spritepacks".
            finally:
                conn.commit()
                conn.close()
            self.decInst = decompress.decLogic(self)

if __name__ == "__main__":
    a = stemLogic(r"D:\0submanager\dummy\mas_dummy")
