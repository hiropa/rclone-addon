#!/usr/bin/python3.4
from __future__ import absolute_import, division, unicode_literals
from future import standard_library
from future.builtins import *
standard_library.install_aliases()

import os, sys, xbmc, time, stat, xbmcvfs, xbmcaddon, xbmcplugin, xbmcgui, gzip, subprocess, urllib.request

sourceurl = xbmcaddon.Addon().getSetting("rclonedownload")

PY3 =  sys.version_info > (3, 0)
if PY3:
	zippath  = xbmcvfs.translatePath("special://temp/rclone.gz")
	loc = xbmcvfs.translatePath("special://xbmcbin/../../../cache/lib/rclone-android-16-arm")
	locwin = xbmcvfs.translatePath("special://xbmcbin/rclone.exe")
	loc2 = xbmcvfs.translatePath("special://masterprofile/rclone.conf")
	pidfile  = xbmcvfs.translatePath("special://temp/librclone.pid")
	logfile  = xbmcvfs.translatePath("special://temp/librclone.log")
	cachepath  = xbmcvfs.translatePath("special://temp") 
	src = xbmcvfs.translatePath("special://masterprofile/rclone-android-16-arm")
else:
	zippath  = xbmc.translatePath("special://temp/rclone.gz")
	loc = xbmc.translatePath("special://xbmcbin/../../../cache/lib/rclone-android-16-arm")
	locwin = xbmc.translatePath("special://xbmcbin/rclone.exe")
	loc2 = xbmc.translatePath("special://masterprofile/rclone.conf")
	pidfile  = xbmc.translatePath("special://temp/librclone.pid")
	logfile  = xbmc.translatePath("special://temp/librclone.log")
	cachepath  = xbmc.translatePath("special://temp") 	
	src = xbmc.translatePath("special://masterprofile/rclone-android-16-arm")

if os.name == 'nt':
	loc = locwin

if not xbmcvfs.exists(loc):
    xbmcvfs.copy(src, loc)
    st = os.stat(loc)
    os.chmod(loc, st.st_mode | stat.S_IEXEC)

command = xbmcaddon.Addon().getSetting("parameters")

def run(cmd):
	os.environ['PYTHONUNBUFFERED'] = "1"
	if os.name == 'nt':
		proc = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines = True  )
	else:
		proc = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines = True, shell = True  )
	xbmc.log(msg='RCLONE: Executing ' + cmd, level=xbmc.LOGINFO)
	stdout = []
	stderr = []
	mix = []
	while proc.poll() is None:
		line = proc.stdout.readline()
		if line != "":
			stdout.append(line)
			mix.append(line)
			xbmc.log(msg='RCLONE:' + line, level=xbmc.LOGINFO)
		line = proc.stderr.readline()
		if line != "":
			stderr.append(line)
			mix.append(line)
			xbmc.log(msg='RCLONE:' + line, level=xbmc.LOGINFO)
	return proc.returncode, stdout, stderr, mix

while True:
	if os.name == 'nt':
		code, out, err, mix = run("\"" + loc + "\" " + command + " --config \"" + loc2 + "\" --log-file \"" + logfile + "\" --cache-dir \"" + cachepath + "\"")
	else:
		code, out, err, mix = run(loc + " " + command + " --config " + loc2 + " --log-file=" + logfile + " --cache-dir " + cachepath + " &")
	time.sleep(2)
