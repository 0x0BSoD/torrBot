import subprocess
import config as cfg


def sys_health():
    p = subprocess.Popen(cfg.sensorsTarget, stdout=subprocess.PIPE)
    out = p.communicate()[0]
    result = out.decode()
    to_send = []
    for item in result.split("\n"):
        if "Core" in item:
            to_send.append("<pre>{0}</pre>".format(" ".join(item.split())))
        else:
            to_send.append("{0}".format(" ".join(item.split())))
    return {"status": True,
            "message": "\n".join(to_send),
            'keyboard': False
            }


def disc_free():
    p = subprocess.Popen(["df", "-H", cfg.partition], stdout=subprocess.PIPE)
    out = p.communicate()[0]
    result = out.decode()
    return {"status": True,
            "message": result,
            'keyboard': False
            }
