import config as cfg

helpText = """
== * == * == Torrents ☠
/show_downladed - Showd Downloaded file in {0}
/start_all_downlads - ▶️
/stop_all_downlads - 💤
== * == * == Server Health ☣️
/get_cpu_t - Show CPU cores temperature
/dfH - Show free space on drive
""".format(cfg.downloadsDir)

helloText = "Load torrent file or insert magent link to start downloading! ☠"

ok = "✅ Added: {} \n Tracker[s]: {}"

statusText = """
Actve Torrents: {}
Paused Torrents: {}
Torrents Count: {}
== * == * == * ==
Download Speed: {}
Upload Speed: {}
== * == * == * ==
Uploaded: {}
Downloaded: {}
"""

getLastAct = """
ID: {0}
Name: {1}
== * == * == * ==
Status: {2}
/Info_{0} | {3}
-----------------
"""

getTorrInfo = """
{0}
Name: {1}
Add Date: {8}
Size: {7}
⬇️ Downloading: {4} | ⬆️ Uploading: {5}
Peers: {6}
== * == * == * ==
Status: {2}
{3}
-----------------
"""
