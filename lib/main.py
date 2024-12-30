import os
import json
import structure
import decompress
from basicutils import *

class stemLogic():
    def __init__(self, gamedir):
        self.selfdir, self.gamedir = getParent(os.path.split(os.path.realpath(__file__))[0]), gamedir
        if self.__class__.__name__ == "stemLogic":
            selfStructure = structure.selfStructure
            for folder in selfStructure:
                dir = self.selfdir + "/" + folder
                if not os.path.exists(dir):
                    os.makedirs(dir)
            self.decInst = decompress.decLogic(self)


if __name__ == "__main__":
    a = stemLogic(r"D:\0submanager\dummy\mas_dummy")
