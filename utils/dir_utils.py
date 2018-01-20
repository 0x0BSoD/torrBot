from pathlib import Path
from os.path import isdir
import subprocess
import config as cfg


def get_folder_items():
    dirs = ''
    files = ''
    try:
        current_directory = Path(cfg.downloadsDir)
        for f in current_directory.iterdir():
            if str(f).startswith('/'):
                if isdir(str(f)):
                    dirs += f'<pre>{str(f).split("/")[-1]}</pre>\n'
                else:
                    files += str(f).split("/")[-1] + '\n'
        return {'status': True,
                'message': dirs + files,
                'keyboard': False
                }
    except FileNotFoundError as err:
        return {'status': False,
                'message': err,
                'keyboard': False
                }


def fix_rights():
    p = subprocess.Popen(['chmod', '777', '-R', cfg.downloadsDir],
                         stdout=subprocess.PIPE)
    out = p.communicate()[0]
    result = out.decode()
    if p.returncode == 0:
        return {'status': True,
                'message': '777 👍',
                'keyboard': False
                }
    else:
        return {'status': False,
                'message': f'Some Error, code {result}',
                'keyboard': False
                }
