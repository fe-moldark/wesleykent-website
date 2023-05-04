---
layout: page
title: Two other random scripts
subtitle: One to check for RPi availability and one to do with Dilbert comics
permalink: /scripts/rpi_and_dilbert/
---

## Introduction
I've got a couple other scripts that I find both entertaining and useful, so I thought I would throw them up here as well. If you genuinely want to be put on one or more of these email lists by all means let me know. I think that would be hilarious and I've already got these running for myself anyways.<br><br>
<br>
## Raspberry Pi Stock Notification
Well it would seem the chip shortage is coming to gradual end, unfortunately Raspberry Pis still come in short supply. After having a Pi Zero and 3B+ just die on me after many years for no apparent reason, I needed to restock. So I learned a little bit about web scraping which was new to me and put together the following script. Currently it only collects data from Adafruit's website, as the other ones I found were either over-priced or more sketchy than I was comfortable buying from.<br>
<br>
Link to the full script can be found <a href="https://raw.githubusercontent.com/fe-moldark/wesleykent-website/gh-pages/assets/scripts/adafruit_stock.py" target="_blank" rel="noopener noreferrer">here</a>, and I will break down how it works below. There are two different types of product pages that I had to look at, one that listed different versions of the same product (RPi4 with varying amounts of RAM) and the other type that only showed a single product type.
<br><br>
That first type for RPi4 was identified with the following:
```python
log_adafruit=[]

#Page for RPi4
urlA_4='https://www.adafruit.com/product/4295'

#Request html data and locate the predetermined section
r=requests.get(urlA_4)
soup=BeautifulSoup(r.text,'html.parser')
prodTable=soup.find('ol',{'class':'meta_pid_boxes'})
```
Now to find the specific products listed there. If you aren't following what the code is doing, navigate to the url and after using the "inspect" tool you should be able to follow along better. The way this checks for the products' availability should make more sense after that.<br>
```python
#Cycle through and find em
for line in prodTable:
    line=str(line)
    if line !='\n': #some are empty lines...
        newline=line.split('\n')
        _type=newline[3][:3]
        _stock=newline[5][:-8]

        if _stock!='Out of stock':
            log_adafruit.append(('Adafruit',str(_type),urlA_4))
```
Pages that only host a single product on their page all follow a similar format, which made it easy to loop through for the remaining RPi boards based on their product ID:
```python
#Pages for RPi 3B+, 3B, Pi Zero (Not W), Pi Zero, Pi Zero 2 --> 4 digit number is the product ID
adafruit_single_products_list=[('3775','RPi 3B+'),('3055','RPi 3B'),('2885','RPi Zero (Not W)'),('3400','RPi Zero W'),('5291','RPi Zero 2')]

def single_prod_at_adafruit(_url,_type,log_adafruit):
    r=requests.get(_url)

    soup=BeautifulSoup(r.text,'html.parser')
    prod=soup.find('div',{'class':'oos-header'})
    for line in prod:
        _stock=str(line)

        if _stock!='Out of stock':
            log_adafruit.append(('Adafruit',_type,_url))

    return log_adafruit

#Cycle through them now
for url in adafruit_single_products_list:
    log_adafruit=single_prod_at_adafruit(str('https://www.adafruit.com/product/'+url[0]),url[1],log_adafruit)
```
<br>
If the `log_adafruit` list is not empty (i.e. one or more items _are_ in stock), the message body will fill out as:<br>
```python
for log in log_adafruit: #log=(_site, _type, _url)
    message+="RPi Board: "+log[1]+"\nSite: " +log[0]+"\n"+"Link: "+log[2]+"\n"+"\n"
```
If needed it will then send an email alerting me to the RPi board(s) now in stock. This is done practically the same way as on [this page](/scripts/websitehashing/), so I won't cover that again.
<br><br><br>


## Who doesn't need more Dilbert in their lives?
_**EDIT: As of early 2023 Dilbert is now behind a paywall and this script no longer works as it was once did. The code itself is fine, however, and can be applied to other sources and websites. I might try and get this to work for The Far Side comic instead but I haven't even begun looking into it.**_<br><br>

My thought process behind this - 1) Dilbert is an amusing comic strip, 2) Oh, they're still putting out daily comics, 3) Okay, I can automate this. Clearly I'm a genius ahead of my time. Link to the full script can be found <a href="https://raw.githubusercontent.com/fe-moldark/wesleykent-website/gh-pages/assets/scripts/daily_dilbert.py" target="_blank" rel="noopener noreferrer">here</a>, but I will go over the important parts down below.<br><br>
First to identify the date and corresponding url from the dilbert site, then to pull the html data from it using BeautifulSoup (bs4):<br>
```python
#Get date
date=datetime.now()
today=date.strftime('%Y-%m-%d')

#Today's comic strip
url="https://dilbert.com/strip/"+str(today)

def getdata(url): 
    r = requests.get(url) 
    return r.text

#Use BeautifulSoup module to pull html data from the page
htmldata = getdata(url) 
soup = BeautifulSoup(htmldata, 'html.parser') 
```
<br>
There are a limited number of images on the page, and the below loop will pull the right one for the day:<br>
```python
for item in soup.find_all('img'):
    #Location for all the images I need to search through always begin with this
    if item['src'][:31]=='https://assets.amuniversal.com/':
        got_this_url=str(item['src'])
        #There are more than one that meet this criteria but the first one is always it
        #Hence the 'break' once it finds one
        break
```
<br>
Now that we've pulled the correct url of where the image is stored, let's download it to our local machine and then send it out to the email list:<br>
```python
#Now to download the image
req = requests.get(got_this_url, stream=True)

#Where I happen to store this file locally
file_location="/media/pi/MyExternalDrive/save_wk_website/dilbert_0.gif"

#Double check the link is in fact valid
if req.status_code == 200:
    with open(file_location,'wb') as save:
        shutil.copyfileobj(req.raw, save)

    #Recipients of the email
    email_list=["recieving_email@gmail.com","recieving_email2@outlook.com"]
```
<br>
From there emails will be sent out according to the email list, but I've already covered how this works previously. It's worth noting that in order for both of these scripts to run properly they do need to be made accessible and executable by the user (or everyone) using `chmod +x script_name.py`, and configured with `sed -i -e 's/\r$//' script_name.py` to properly execute through the `crontab`.
<br><br>
Something else I've learned the annoying way is that regardless of where the script is located and executed from, when it runs as a `cronjob` you can no longer rely on it to run as though it is located where it is. In other words, do not assume that a file will automatically be saved in the same directory that your current script is in, because it won't any longer. You need to explicitly define the path every time, and that's always best practice anyway I suppose. Cheers.
