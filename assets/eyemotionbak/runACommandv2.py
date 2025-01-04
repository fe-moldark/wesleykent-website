# Backup local recordings from the EyeMotion RPi to my local network share
# Utilizes the 'Run a Command' under file storage to execute once a new recording is saved

import os, sys
import datetime
import subprocess

current_time = datetime.datetime.now()
adj_month=str(current_time.month)
adj_day=str(current_time.day)

# Standardize the formats for later
if len(adj_month)==1: adj_month="0"+adj_month
if len(adj_day)==1: adj_day="0"+adj_day
dateToday=str(current_time.year)+"-"+adj_month+"-"+adj_day

# This pulls the most recent mp4 and its "thumbnail" file, then filters out for just the recording
latestRecording=subprocess.check_output('ls -t /data/output/Camera1/ | head -n 2 | grep -v "thumb"', shell=True)
latestRecording="".join([char for char in latestRecording if char in ['.','m','p','-','0','1','2','3','4','5','6','7','8','9']]) # Ugly, but works

scp_command='scp "/data/output/Camera1/'+str(latestRecording)+'"'+' "pi@192.168.11.19:/media/pi/MyExternalDrive/scp/'+str(latestRecording)+'"' # Also ugly
os.system(scp_command)
