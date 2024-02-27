import sys, os, subprocess


def echo(filepath):
    temp=open(filepath,'r')
    temp_line=temp.read().split('\n')[0]
    temp.close()
    return temp_line


def get_usb_devices():

    usbdevices = []
    base="/sys/bus/usb/devices/"
    for subdir in os.listdir(base):
        if os.path.isdir(os.path.join(base, subdir)):

            newbase=os.path.join(base, subdir)
            listedSubDir= os.listdir(newbase)

            #for the love of god make this look better
            if "idVendor" in listedSubDir and "idProduct" in listedSubDir and "busnum" in listedSubDir and "devnum" in listedSubDir:
                usbdevices.append([echo(newbase+"/idVendor"),echo(newbase+"/idProduct"),echo(newbase+"/busnum"),echo(newbase+"/devnum"),str(newbase)])

    return usbdevices


whiteListed=[("04f2","0408")]
print('Whitelisted: ',whiteListed)

usbdevices=get_usb_devices()
for device in usbdevices: #vendorID, prodID, bus#, dev#
    index=str(device[4]).rfind('/')
    substring=str(device[4])[index+1:]

    if (device[0],device[1]) not in whiteListed and str(substring) not in ['1-0:1.0','2-0:1.0','3-0:1.0','4-0:1.0','usb1','usb2','usb3','usb4']: #The rest of these are the "root" hubs that MUST stay active - they are not individual devices
        device_identifier = str(device[2])+"-"+str(device[3])

        #print('Device: ',device[0],device[1],' not found in white list. Bus# and dev#: ',device[2],device[3],' --basefolder at: ',device[4])
        command = "echo '"+str(substring)+"' | sudo tee /sys/bus/usb/drivers/usb/unbind"
        #print('Confirm command: ',command)

        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
