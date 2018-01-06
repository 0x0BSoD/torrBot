import config as cfg

helpText = """
== * == * == Torrents ☠
/show_downloaded - Show Downloaded file in {0}
/start_all_downloads - ▶️
/stop_all_downloads - 💤
== * == * == Server Health ☣️
/get_cpu_t - Show CPU cores temperature
/dfH - Show free space on drive
""".format(cfg.downloadsDir)

helloText = "Load torrent file or insert magnet link to start downloading! ☠"

ok = "✅ Added: {} \n Tracker[s]: {}"

statusText = """
Active Torrents: {}
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

start = "/Stop_{0} | /Delete_{0}"
stop = "/Start_{0} | /Delete_{0}"
