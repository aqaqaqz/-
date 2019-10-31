import re
import os
import glob
import shutil

def lpad(str, l, c):
    while l>len(str) :
        str = c + str
    return str

files = glob.glob("./*.mp3")
order = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

for seq in range(0, len(order)):
    for f in files:
        fNm = f.replace(".\\", "")

        if fNm.find(order[seq]) != -1 :
            fNm = fNm.replace(fNm, lpad(str(seq+1), 2, '0') + ". " + fNm)
            shutil.move(f, "./"+fNm)
            break