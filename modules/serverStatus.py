import subprocess
import config as cfg


def sysHealth():
    proc = subprocess.Popen(cfg.sensorsTarget, stdout=subprocess.PIPE)
    out = proc.communicate()[0]
    result = out.decode()
    toSend = []
    for item in result.split("\n"):
        if "Core" in item:
            toSend.append("<pre>{0}</pre>".format(" ".join(item.split())))
        else:
            toSend.append("{0}".format(" ".join(item.split())))
    return {"status": True,
            "message": "\n".join(toSend)
            }


def discFree():
    proc = subprocess.Popen(["df", "-H", cfg.partition],
                            stdout=subprocess.PIPE)
    out = proc.communicate()[0]
    result = out.decode()
    return {"status": True,
            "message": result
            }
