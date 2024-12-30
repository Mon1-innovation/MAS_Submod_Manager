import os
import json
import patoolib
import main
import basicutils

class decLogic(main.stemLogic):
    def __init__(self, stemInst):
        super().__init__(stemInst.gamedir)

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
            outdir = self.selfdir + f"/{}/.tmp"
        patoolib.extract_archive(arcdir, outdir=outdir)

    def analyzeSubmod(self, moddir) -> bool:
    # Analyze and store the structure of selected submod


    def installSubmod(self, moddir) -> bool:
    # Install the desired submod to gamedir.
        pass

if __name__ == "__main__":
    pass

