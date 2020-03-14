import requests
import threading
import random
import atexit
import time
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
sem = threading.Semaphore(5)

listArr = [];
def download(id, no):
    global listArr;
    listArr.append(0);
    listArr.append(0);
    imgList= []
    
    cnt = 0
    while True:
        try:
            response = requests.get(listDomain + id + "_list.json", cookies=cookies, headers=headers, timeout=5)
            if response.ok:
                imgList = json.loads(response.text)
                break
        except:
            cnt+=1
            if cnt == 3:
                print(id + " is not exists!!")
                return
            else:
                print("can not find " + id + ". count : " + str(cnt))

    listArr[2*no+1] = len(imgList)

    print("start " + id);

    if not(os.path.isdir(id)):
        os.makedirs(os.path.join(id))

    th = []    
    for img in imgList:
        time.sleep(0.1)
        temp = threading.Thread(target=imgDown, args=(id, img["name"], no));
        temp.start()
        th.append(temp)
    for t in th:
        t.join()


def imgDown(id, imgName, no):
    sem.acquire()    

    url = imgDomain + id + '/' + imgName
    cnt = 0
    while True:
        try:
            response = requests.get(url , cookies=cookies, headers=headers, timeout=5)
            if response.ok:
                break
        except:
            cnt+=1
            if cnt == 5:
                print(id + " : " + imgName + " is passed...")
                break
            else:
                print(id + " : " + imgName + " is fail... count : " + str(cnt))

    f = open('./' + id + '/' + imgName, "wb")
    f.write(response.content)
    f.close()

    print('download : ' + id + " " + imgName);

    global listArr;
    listArr[no*2] = listArr[no*2]+1
    if listArr[no*2]==listArr[no*2+1]:
        print(id + " complete!")
    
    sem.release()

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
        print('server connect fail...')
        atexit.register(input, 'Press Enter to continue...')
        return;
    global listDomain
    global imgDomain
    listDomain = json.loads(res.text)['listDomain']
    imgDomain = json.loads(res.text)['imgDomain']
    
    no = 0
    global listArr;
    for id in noList:
        download(id, no);
        no = no+1
    atexit.register(input, 'Press Enter to continue...')

main();