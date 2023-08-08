import os, sys
import datetime
import subprocess

current_time = datetime.datetime.now()
adj_month=str(current_time.month)
adj_day=str(current_time.day)

if len(adj_month)==1: adj_month="0"+adj_month
if len(adj_day)==1: adj_day="0"+adj_day

dateToday=str(current_time.year)+"-"+adj_month+"-"+adj_day
recordingsOfToday=subprocess.check_output(['ls','-t','/data/output/Camera1/'+str(dateToday)]) #just now thinking os.listdir() would be easier...

blank_list=[]
blank_filename=''
for item in recordingsOfToday: #the formatting was weird, splitting the list up normally did not work
	#print(recordingsOfToday.index(item),item)
	if item!='\n':
		blank_filename+=str(item)
	else:
		blank_list.append(blank_filename)
		blank_filename=''

#print(blank_list)

if str(blank_list[0])[-6:]==".thumb":
	uploadThis=blank_list[1]
else:
	uploadThis=blank_list[0]

#before doing this you need to have done the whole ssh-keygen, then ssh-copy-id user@target-ip so it is known as a trusted host
os.system('scp /data/output/Camera1/'+str(dateToday)+'/'+str(uploadThis)+' pi@192.168.11.19:/media/pi/MyExternalDrive/scp/'+str(uploadThis))



