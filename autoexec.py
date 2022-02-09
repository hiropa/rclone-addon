#!/usr/bin/python3.4
import os, sys, xbmc, time, stat, xbmcvfs
from daemon import Daemon

src = xbmc.translatePath("special://masterprofile/rclone-android-16-arm")
loc = xbmc.translatePath("special://xbmcbin/../../../cache/lib/rclone-android-16-arm")

if not xbmcvfs.exists(loc):
    xbmcvfs.copy(src, loc)
    st = os.stat(loc)
    os.chmod(loc, st.st_mode | stat.S_IEXEC)

loc2 = xbmc.translatePath("special://masterprofile/rclone.conf")
pidfile  = xbmc.translatePath("special://temp/librclone.pid")
logfile  = xbmc.translatePath("special://temp/librclone.log")
cachepath  = xbmc.translatePath("special://temp")
if os.path.isfile(pidfile):
    os.remove(pidfile)

class MyDaemon(Daemon):
    def run(self):
        os.popen(loc + " serve webdav onedrive: --addr 127.0.0.1:23457 --config " + loc2 + " --log-file=" + logfile + " --dir-cache-time 2400h --poll-interval 10m &")

if __name__ == "__main__":
    monitor = xbmc.Monitor()
    rclonedaemon = MyDaemon(pidfile)
    rclonedaemon.start()
    while not monitor.abortRequested():
        if monitor.waitForAbort(10):
            rclonedaemon.stop()
            break