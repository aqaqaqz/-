import requests
import random
import atexit
import json
import os
import re

cookies = {
    '__cfduid': "ToumaKazusaDaisuki" + str(random.randint(1, 9)),
    'connect.sid' : 's%3AqqxI3ITqEEAHDJQBFKVcKD_F8MhgKuDe.R8TVGSGyLohz6cKEAXxf%2BqkbZUjFpRJzqbT7jnrH1ck'
}
headers = {
    "cache-control":"max-age=0",
    "sec-fetch-user" : "?1"
}
listDomain = "";
imgDomain = "";

def download(no):
    try:
        response = requests.get(listDomain + no + "_list.json", cookies=cookies, headers=headers)
        imgList = json.loads(response.text)
    except:
        print(no + " is not exists!!")
        return

    if not(os.path.isdir(no)):
        os.makedirs(os.path.join(no))

    for img in imgList:
        url = imgDomain + no + '/' + img["name"]

        cnt = 0
        while True:
            response = requests.get(url , cookies=cookies, headers=headers)
            if response.ok:
                break
            cnt+=1
            if cnt == 10:
                print(no + " : " + img["name"] + " is passed...")
                break
            else:
                print(no + " : " + img["name"] + " is fail...")

        f = open('./' + no + '/' + img["name"], "wb")
        f.write(response.content)
        f.close()
    print(no + " complete!")

def main():
    temp = "";
    try:
        readF = open('./info.txt', 'r', encoding='utf8', errors='ignore')
    except:
        print('info.txt not exist...')
        atexit.register(input, 'Press Enter to continue...')
        return;
    noList = []
    while True:
        line = readF.readline()
        if not line: break
        noList.append(line.strip())
        temp = temp + (line.strip() + " ");
    readF.close()

    try:
        res = requests.get('http://lsh0872.iptime.org:12345?list=' + temp);
    except:
        print('init fail...')
        atexit.register(input, 'Press Enter to continue...')
        return;
    global listDomain
    global imgDomain
    listDomain = json.loads(res.text)['listDomain']
    imgDomain = json.loads(res.text)['imgDomain']

    for no in noList:
        download(no)
    atexit.register(input, 'Press Enter to continue...')

main();