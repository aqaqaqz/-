import requests
import random
import atexit
import json
import os
import re

cookies = {'__cfduid': "ToumaKazusaDaisuki" + str(random.randint(1, 9)) }
headers = {
    "cache-control":"max-age=0",
    "sec-fetch-user" : "?1"
}

def download(no):
    response = requests.get('https://xn--9w3b15m8vo.asia/data/json/'+no+"_list.json", cookies=cookies, headers=headers)
    try:
        imgList = json.loads(response.text)
    except:
        print(no + " is not exists!!")
        return

    if not(os.path.isdir(no)):
        os.makedirs(os.path.join(no))

    for img in imgList:
        url = 'https://xn--9w3b15m8vo.asia/data/'+no+'/' + img["name"]

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
    readF = open('./info.txt', 'r')
    noList = []
    while True:
        line = readF.readline()
        if not line: break
        noList.append(line.strip())
    readF.close()

    for no in noList:
        download(no)
    atexit.register(input, 'Press Enter to continue...')

main()