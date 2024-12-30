import os
import json
import patoolib
import main

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

    def installFromArc(self, arcdir) -> bool:
    # Install the desired archive to gamedir.
        pass

if __name__ == "__main__":
    pass

