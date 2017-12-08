import pathlib
from os.path import isdir
import subprocess
import config as cfg


def getFolderItems():
    dirs = ""
    files = ""
    try:
        currentDirectory = pathlib.Path(cfg.downloadsDir)
        for f in currentDirectory.iterdir():
            if str(f).startswith('/'):
                if isdir(str(f)):
                    dirs += "<pre>{}</pre>\n".format(str(f).split('/')[-1])
                else:
                    files += "{}\n".format(str(f).split('/')[-1])
        return {"status": True,
                "message": dirs + files
                }
    except FileNotFoundError as e:
        return {"status": False,
                "message": e
                }


def fixRights():
    proc = subprocess.Popen(["chmod", "777", "-R", cfg.downloadsDir],
                            stdout=subprocess.PIPE)
    out = proc.communicate()[0]
    result = out.decode()
    return {"status": True,
            "message": result
            }
