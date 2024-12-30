import os
import json
import MAS_Submod_Manager.lib.structure as structure
import basicutils
import decompress

class stemLogic():
    def __init__(self, gamedir):
        self.selfdir, self.gamedir = os.path.split(os.path.realpath(__file__))[0], gamedir
        if self.__class__.__name__ == "stemLogic":
            selfStructure = structure.selfStructure
            for folder in selfStructure:
                dir = basicutils.getParent(self.selfdir) + "/" + folder
                if not os.path.exists(dir):
                    os.makedirs(dir)
            self.decInst = decompress.decLogic(self)


if __name__ == "__main__":
    a = stemLogic(r"D:\0submanager\mas_dummy")