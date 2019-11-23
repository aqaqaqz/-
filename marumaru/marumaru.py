import requests
import random
import atexit
import json
import os
import re
  
from urllib.request import urlopen
from urllib.request import Request  
from bs4 import BeautifulSoup

cookies = {'__cfduid': "ToumaKazusaDaisuki" + str(random.randint(1, 9)) }
headers = {
    "cache-control":"max-age=0",
    "sec-fetch-user" : "?1"
}

def lpad(str, l, c):
    while len(str)<l :
        str = c+str
    return str

def download(link):
    response = requests.get(link, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    list = soup.findAll(name="div", attrs={"class":"view-img"})[0].findAll(name="img")
    no = ""
    p = len(link)-1
    while link[p] != '/':
        no = link[p] + no
        p -= 1

    if not(os.path.isdir(no)):
        os.makedirs(os.path.join(no))
    seq = 0
    for img in list :
        seq += 1

        cnt = 0
        while True:
            response = requests.get(img["src"] , cookies=cookies, headers=headers)
            if response.ok:
                break
            cnt+=1
            if cnt == 10:
                print(no + " : " + img["name"] + " is passed...")
                break
            else:
                print(no + " : " + img["name"] + " is fail...")
        
        f = open('./' + no + '/' + lpad(str(seq), 3, '0') + '.jpg', "wb")
        f.write(response.content)
        f.close()

def main():
    readF = open('./info.txt', 'r')
    linkList = []
    while True:
        line = readF.readline()
        if not line: break
        linkList.append(line.strip())
    readF.close()

    for link in linkList:
        download(link)
    atexit.register(input, 'Press Enter to continue...')

main()