from modules.torrUtils import postLink
from modules.dirUtils import getFolderItems
from modules.serverStatus import sysHealth, discFree


def parse(message):
    if message.startswith('magnet'):
        return postLink(message)
    # elif message.startswith('Show Downladed'):
    #     return getFolderItems()
    elif message.startswith('CPU'):
        return sysHealth()
    elif message.startswith('Free Space'):
        return discFree()
    elif message.startswith('chmod 777'):
        return fixRights()
    elif message.startswith('Dir Content'):
        return getFolderItems()
    else:
        return {"status": True,
                "message": "Don't get it (~ ~)"}
