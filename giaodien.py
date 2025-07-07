import threading, base64, os, time, re, json, random, subprocess
from datetime import datetime, timedelta
from time import sleep, strftime
from bs4 import BeautifulSoup
import requests, socket, sys

try:
    from faker import Faker
    from requests import session
    from colorama import Fore, Style
    from random import randint
    import pystyle
    import socks
except:
    os.system("pip install faker")
    os.system("pip install requests")
    os.system("pip install colorama")
    os.system("pip install bs4")
    os.system("pip install pystyle")
    print('__Vui Lòng Chạy Lại Tool__')
    exit()

from pystyle import Add, Center, Anime, Colors, Colorate, Write, System

# Màu sắc
xnhac = "\033[1;36m"
do = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
xduong = "\033[1;34m"
hong = "\033[1;35m"
trang = "\033[1;39m"
whiteb = "\033[1;39m"
red = "\033[0;31m"
redb = "\033[1;31m"
end = '\033[0m'
dev = "\033[1;39m[\033[1;31m×\033[1;39m]\033[1;39m"

# In banner
def banner():
    banner = f"""
\033[1;34m╔═══════════╗
\033[1;36m║▇◤▔▔▔▔▔▔▔◥▇║
\033[1;36m║▇▏◥▇◣┊◢▇◤▕▇║
\033[1;36m║▇▏▃▆▅▎▅▆▃▕▇║
\033[1;36m║▇▏╱▔▕▎▔▔╲▕▇║
\033[1;36m║▇◣◣▃▅▎▅▃◢◢▇║
\033[1;36m║▇▇◣◥▅▅▅◤◢▇▇║
\033[1;36m║▇▇▇◣╲▇╱◢▇▇▇║
\033[1;36m║▇▇▇▇◣▇◢▇▇▇▇║
\033[1;34m╚═══════════╝
\033[1;97mTool By: \033[1;32mAnhhCode            \033[1;97mPhiên Bản: \033[1;32m4.0     
\033[97m════════════════════════════════════════════════  
\033[1;97m[\033[1;91m❣\033[1;97m]\033[1;97m Youtube\033[1;31m  : \033[1;97m☞ \033[1;36mAnhCode\033[1;31m♔ \033[1;97m☜
\033[1;97m[\033[1;91m❣\033[1;97m]\033[1;97m Facebook\033[1;31m : \033[1;97mhttps://www.facebook.com/profile.php?id=61570408533569
\033[1;97m[\033[1;91m❣\033[1;97m]\033[1;97m Telegram\033[1;31m : \033[1;97m☞\033[1;32mhttps://t.me/shareanhcode🔫\033[1;97m☜
\033[97m════════════════════════════════════════════════
"""
    for X in banner:
        sys.stdout.write(X)
        sys.stdout.flush()
        sleep(0.000001)

# Hàm chạy code PHP từ URL
def run_php_code_from_url(url, filename="temp_script.php"):
    try:
        code = requests.get(url).text
        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)
        subprocess.run(["php", filename])
        os.remove(filename)
    except Exception as e:
        print(f"{dev} Lỗi khi chạy PHP: {e}")

# Hàm chạy code Python từ URL
def run_py_code_from_url(url):
    try:
        code = requests.get(url).text
        exec(code, globals())
    except Exception as e:
        print(f"{dev} Lỗi khi chạy Python: {e}")

# Menu chính
while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()
    print("\033[1;37m╔══════════════════════╗")
    print("\033[1;37m║  \033[1;32mTool Tương Tác Chéo \033[1;37m║")
    print("\033[1;37m╚══════════════════════╝")
    print(f"\033[1;97m[\033[1;32m*\033[1;97m] \033[1;33m1 \033[1;97m: \033[1;34mTool TTC Facebook \033[1;32m[Online]")
    print(f"\033[1;97m[\033[1;32m*\033[1;97m] \033[1;33m1.1 \033[1;97m: \033[1;34mTool TTC Instagram \033[1;32m[Online]")
    print("\033[1;37m╔══════════════════════╗")
    print("\033[1;37m║  \033[1;32mTool TraoDoiSub.com \033[1;37m║")
    print("\033[1;37m╚══════════════════════╝")
    print(f"\033[1;97m[\033[1;32m*\033[1;97m] \033[1;33m2 \033[1;97m: \033[1;34mTool TDS Facebook \033[1;32m[Online]")
    print("\033[1;37m╔══════════════════════╗")
    print("\033[1;37m║  \033[1;32mTool Tiện Ích \033[1;37m      ║")
    print("\033[1;37m╚══════════════════════╝")
    print(f"\033[1;97m[\033[1;32m*\033[1;97m] \033[1;33m3 \033[1;97m: \033[1;34mTool Get Token Facebook \033[1;32m[Online]")
    print(f"\033[1;97m[\033[1;32m*\033[1;97m] \033[1;33m3.1 \033[1;97m: \033[1;34mTool Enc Php\033[1;32m[Online]")
    print(f"\033[1;97m[\033[1;32m*\033[1;97m] \033[1;33m3.2\033[1;97m: \033[1;34mTool Enc Py\033[1;32m[Online]")
    print(f"\033[1;97m[\033[1;32m*\033[1;97m] \033[1;33m3.3\033[1;97m: \033[1;34mTool Reg Fb\033[1;32m[Online]")
    print(f"\033[1;97m[\033[1;32m*\033[1;97m] \033[1;33m3.4\033[1;97m: \033[1;34mTool Reg Mail\033[1;32m[Online]")
    print(f"\033[1;97m[\033[1;32m*\033[1;97m] \033[1;33m3.5\033[1;97m: \033[1;34mTool Share Fb Max Speed\033[1;32m[Online]")
     print(f"\033[1;97m[\033[1;32m*\033[1;97m] \033[1;33m3.6\033[1;97m: \033[1;34mTool Spam Ngl\033[1;32m[Online]")
    print(f"\033[97m════════════════════════════════════════════════════════")

    chon = input('\033[1;91m┌─╼\033[1;97m[\033[1;91m<\033[1;97m/\033[1;91m>\033[1;97m]--\033[1;91m>\033[1;97m Nhập lựa chọn \n\033[1;91m└─╼\033[1;91m✈ \033[1;33m : ')
    print('\033[1;39m───────────────────────────────────────────────────────────')

    if chon == '1':
        run_php_code_from_url('https://raw.githubusercontent.com/nhatanh2k8/nhatanh2k8/refs/heads/main/anhcode1.php')
    elif chon == '1.1':
        run_php_code_from_url('https://raw.githubusercontent.com/nhatanh2k8/nhatanh2k8/refs/heads/main/anhcode.php_10.php')
    elif chon == '2':
        run_py_code_from_url('https://raw.githubusercontent.com/nhatanh2k8/nhatanh2k8/refs/heads/main/tds.py')
    elif chon == '3':
        run_php_code_from_url('https://raw.githubusercontent.com/nhatanh2k8/nhatanh2k8/refs/heads/main/fb.php')
    elif chon == '3.1':
        run_php_code_from_url('https://raw.githubusercontent.com/nhatanh2k8/nhatanh2k8/refs/heads/main/enc_10.php')
    elif chon == '3.2':
        run_py_code_from_url('https://raw.githubusercontent.com/nhatanh2k8/nhatanh2k8/refs/heads/main/enc.py')
    elif chon == '3.3':
        run_py_code_from_url('https://raw.githubusercontent.com/nhatanh2k8/nhatanh2k8/refs/heads/main/anhcode-regfb.py')
    elif chon == '3.4':
        run_py_code_from_url('https://raw.githubusercontent.com/nhatanh2k8/nhatanh2k8/refs/heads/main/anhcode-regmail.py')
    elif chon == '3.5':
        run_py_code_from_url('https://raw.githubusercontent.com/nhatanh2k8/nhatanh2k8/refs/heads/main/anhcode-share.py')
        else:
        print(f"{dev} Không có lựa chọn này!")
        sleep(2)
