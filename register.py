import platform
import time
import binascii
import random
import os
import urllib.request
import subprocess
import re

os.environ['WORKON_HOME']="value"

def getrandommc():
    mc = '{}:{}:{}:{}:{}:{}'.format("".join(random.choices(mcrandom,k=2)),"".join(random.choices(mcrandom,k=2)),"".join(random.choices(mcrandom,k=2)),"".join(random.choices(mcrandom,k=2)),"".join(random.choices(mcrandom,k=2)),"".join(random.choices(mcrandom,k=2)))
    return mc

def getsystem():
    system = platform.system()
    if system.startswith("Win"):
        return "win"+platform.machine()[-2:]
    elif system.startswith("Lin"):
        return "linux" + platform.machine()[-2:]
    else:
        return "osx64"

system = getsystem()

nativate_path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),"app"),"app")


jar_path = os.path.join(nativate_path,"unidbg.jar")

jni_path = os.path.join(os.path.join(nativate_path,"prebuilt"),system)


os.chdir(nativate_path)
for x in range(10):
    mcrandom = ["a","1","2","3","4","5","6","7","8","9"]

    headers = {
        'User-Agent':'okhttp/3.8.1',
        'Content-Type':'application/octet-stream;tt-data=a'
    }

    gentime = str(int(time.time()*1000))
    ud_id = str(random.randint(221480502743165,821480502743165))
    openu_did = "".join([random.choice("abcdefghijklmn1234567890") 
    for i in range(16)])
    mc = getrandommc()

    message = " ".join([gentime,ud_id,openu_did,mc])

    command = r"java -jar -Djna.library.path={} -Djava.library.path={} unidbg.jar {}".format(jni_path,jni_path,message)
    stdout,stderr = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).communicate()
    hex_str = re.search(r'hex=([\s\S]*?)\nsize',stdout.decode()).group(1)

    def hexStrtostr(hex_str):
        hexadecimal = hex_str.encode('utf-8')
        str_bin = binascii.unhexlify(hexadecimal)
        return str_bin


    astr = hexStrtostr(hex_str)
    register = 'https://log-va.tiktokv.com/service/2/device_register/'
    request = urllib.request.Request(url=register,data=astr,headers=headers)
    response = urllib.request.urlopen(request)
    print(response.read(), "\n")
