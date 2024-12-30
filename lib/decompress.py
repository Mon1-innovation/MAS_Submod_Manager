import os
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
    # Verify if an archive is intact. None indicates path/fs issue.
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
    
    def recuRead(self, pathdir) -> dict:
    # Recursively list the structure of selected path
        pass

    def analyzeSubmod(self, moddir) -> bool:
    # Analyze and store the structure of selected submod
        pass

    def installSubmod(self, moddir) -> bool:
    # Install the desired submod to gamedir.
        pass

if __name__ == "__main__":
    b=decLogic()
    b.decompArc(r"D:\0submanager\dummy\submod_dummy\MAICA_ChatSubmod-1.1.18.zip")

