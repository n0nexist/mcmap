import os
import time
import re
import string
import random

filename = ""

def getrandstr():
    stri = string.ascii_letters+string.digits
    output = ""
    for x in range(5):
        output += stri[random.randint(0,len(stri)-1)]
    return output

# remove formatting from string
def purifica(testo):
    testo = re.sub(r'§.+', '', testo)
    testo = testo.replace("  ", "")
    testo = testo.replace("\n"," ")
    return testo

def startlogging(host,arguments):
    global filename
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    filename = f"outputs/{getrandstr()}_scan_{host}_.log"
    with open(filename, 'a') as file:
        file.write(f"[ mcmap - scanning \"{host}\" with ports \"{arguments}\"]")
        file.close()
        
def logline(text):
    print(text)
    f = open(filename,"a")
    f.write("\n"+purifica(text))
    f.close()
