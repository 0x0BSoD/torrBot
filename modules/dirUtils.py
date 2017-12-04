import pathlib
import config as cfg

def getFolderItems():
    files = ""
    try:
        currentDirectory = pathlib.Path(cfg.downloadsDir)
        for currentFile in currentDirectory.iterdir():
            if currentFile.startswith('/'):
            files += "{}\n".format(currentFile)
        return {"status": True,
                "message": files
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
