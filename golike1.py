import threading
import base64
import os
import time
import re
import json
import random
import requests
import socket
import sys
from time import sleep  # Đã sửa lỗi ở đây
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Kiểm tra và cài đặt thư viện cần thiết
try:
    from faker import Faker
    from requests import session
    from colorama import Fore, Style
    import pystyle
except ImportError:
    os.system("pip install faker requests colorama bs4 pystyle")
    os.system("pip3 install requests pysocks")
    print('__Vui Lòng Chạy Lại Tool__')
    sys.exit()

# Tạo hoặc đọc khóa mã hóa bằng base64
secret_key = base64.urlsafe_b64encode(os.urandom(32))

# Mã hóa và giải mã dữ liệu bằng base64
def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

def decrypt_data(encrypted_data):
    return base64.b64decode(encrypted_data.encode()).decode()

# Màu sắc cho hiển thị
xnhac = "\033[1;36m"
do = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
xduong = "\033[1;34m"
hong = "\033[1;35m"
trang = "\033[1;39m"
end = '\033[0m'

def bes4(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            version_tag = soup.find('span', id='version_vip')
            maintenance_tag = soup.find('span', id='maintenance_vip')
            version = version_tag.text.strip() if version_tag else None
            maintenance = maintenance_tag.text.strip() if maintenance_tag else None
            return version, maintenance
    except requests.RequestException:
        return None, None
    return None, None

def checkver():
    url = 'https://checkserver.hotrommo.com/'
    version, maintenance = bes4(url)
    if maintenance == 'on':
        print("\033[1;31mTool đang được bảo trì. Vui lòng thử lại sau. \nHoặc vào nhóm Tele: \033[1;32mhttps://t.me/shareanhcode")
        sys.exit()
    return version

current_version = checkver()
if current_version:
    print(f"Phiên bản hiện tại: {current_version}")
else:
    print("Không thể lấy thông tin phiên bản hoặc tool đang được bảo trì.")
    sys.exit()

def banner():
 os.system("cls" if os.name == "nt" else "clear")
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
def get_ip_address():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_data = response.json()  # Trả về từ điển JSON
        ip_address = ip_data['ip']  # Lấy giá trị từ trường 'ip'
        return ip_address
    except Exception as e:
        print(f"Lỗi khi lấy địa chỉ IP: {e}")
        return None

# Hàm để hiển thị địa chỉ IP của thiết bị
def display_ip_address(ip_address):
    if ip_address:
        banner()
        print(f"\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;31mĐịa chỉ IP : {ip_address}")
    else:
        print("Không thể lấy địa chỉ IP của thiết bị.")

def luu_thong_tin_ip(ip, key, expiration_date):
    data = {ip: {'key': key, 'expiration_date': expiration_date.isoformat()}}
    encrypted_data = encrypt_data(json.dumps(data))

    with open('ip_key.json', 'w') as file:
        file.write(encrypted_data)

def tai_thong_tin_ip():
    try:
        with open('ip_key.json', 'r') as file:
            encrypted_data = file.read()
        data = json.loads(decrypt_data(encrypted_data))
        return data
    except FileNotFoundError:
        return None

def kiem_tra_ip(ip):
    data = tai_thong_tin_ip()
    if data and ip in data:
        expiration_date = datetime.fromisoformat(data[ip]['expiration_date'])
        if expiration_date > datetime.now():
            return data[ip]['key']
    return None

def generate_key_and_url(ip_address):
    ngay = int(datetime.now().day)
    key1 = str(ngay * 27 + 27)
    ip_numbers = ''.join(filter(str.isdigit, ip_address))
    key = f'anhcode{key1}{ip_numbers}'
    expiration_date = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
    url = f'https://anhcode.sbs/client/key.php?key={key}'
    return url, key, expiration_date

def da_qua_gio_moi():
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    return now >= midnight

def get_shortened_link(link_key_yeumoney):
    try:
        response = requests.get(f'https://link4m.co/api-shorten/v2?api=674701e4b29cad72ca685685&format=json&url={link_key_yeumoney}')
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        return None
def get_shortened_link_phu(url):
    token_yeumoney = '56e38d42f495932dba2473dbb05a8a66974cd4db289dc9529985fbf75a4983f3'
    try:
        yeumoney_response = requests.get(f'https://yeumoney.com/QL_api.php?token={token_yeumoney}&format=json&url={url}')
        if yeumoney_response.status_code == 200:
            return yeumoney_response.json()
    except requests.RequestException:
        return None
def main():
    ip_address = get_ip_address()
    display_ip_address(ip_address)

    if ip_address:
        existing_key = kiem_tra_ip(ip_address)
        if existing_key:
            print(f"\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;35mTool còn hạn, mời bạn dùng tool.")
            time.sleep(2)
        else:
            if da_qua_gio_moi():
                print("\033[1;33mQuá giờ sử dụng tool!")
                return

            url, key, expiration_date = generate_key_and_url(ip_address)

            with ThreadPoolExecutor(max_workers=2) as executor:
                print("\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập 1 Để Lấy Key \033[1;33m( Free )")
                print("\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập 2 Để Lấy Key \033[1;33m( Key Mua)")
                

                while True:
                    try:
                        try:
                            choice = input("\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;34mChọn lựa chọn: ")
                            print("\033[97m════════════════════════════════════════════════")
                        except KeyboardInterrupt:
                            print("\n\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;31mCảm ơn bạn đã dùng Tool Hướng Dev. Thoát...")
                            sys.exit()
                        
                        if choice == "1":  # Kiểm tra chuỗi "1"
                            yeumoney_future = executor.submit(get_shortened_link_phu, url)
                            yeumoney_data = yeumoney_future.result()
                            if yeumoney_data and yeumoney_data.get('status') == "error":
                                print(yeumoney_data.get('message'))
                                return
                            else:
                                link_key_yeumoney = yeumoney_data.get('shortenedUrl')
                                token_link4m = '674701e4b29cad72ca685685'
                                link4m_response = requests.get(f'https://link4m.co/api-shorten/v2?api={token_link4m}&format=json&url={link_key_yeumoney}', timeout=5)
                                print("\033[1;31mLưu Ý: \033[1;33mTool Free Nhé Cả Nhà Yêu \033[1;91m❣\033[1;32m")
                                
                                if link4m_response.status_code == 200:
                                    link4m_data = link4m_response.json()
                                    if link4m_data.get('status') == "error":
                                        print(link4m_data.get('message'))
                                        return
                                    else:
                                        link_key_4m = link4m_data.get('shortenedUrl')
                                        print('\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mLink Để Vượt Key Là:', link_key_4m)
                                else:
                                    print('Không thể kết nối đến dịch vụ rút gọn URL')
                                    return
                        
                            while True:
                                keynhap = input('Key Đã Vượt Là: ')
                                if keynhap == key:
                                    print('Key Đúng Mời Bạn Dùng Tool')
                                    sleep(2)
                                    luu_thong_tin_ip(ip_address, keynhap, expiration_date)
                                    return  
                                else:
                                    print('\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mKey Sai Vui Lòng Vượt Lại Link:', link_key_4m)
                        

                        elif choice == "2":
                            while True:
                                nhap_key = input(f"\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;35mNhập key đã mua: \033[1;32m").strip()
                                try:
                                    check = requests.get(f"https://anhcode.sbs/check-key.php?key={nhap_key}", timeout=5).json()
                                except Exception as e:
                                    print(f"\033[1;31mKhông thể kết nối tới server. Vui lòng thử lại sau.")
                                    continue

                                if check.get("status") == "error":
                                    print(f"\033[1;31mKey không hợp lệ hoặc đã hết hạn. Vui lòng nhập lại.")
                                    continue

                                total_seconds = int(check.get("time_remaining", 0))
                                if total_seconds <= 0:
                                    print(f"\033[1;31mKey đã hết hạn. Vui lòng nhập lại.")
                                    continue

                                # Hiển thị thời gian còn lại theo năm, tháng, ngày, ...
                                years = total_seconds // (365*24*3600)
                                total_seconds %= (365*24*3600)
                                months = total_seconds // (30*24*3600)
                                total_seconds %= (30*24*3600)
                                days = total_seconds // (24*3600)
                                total_seconds %= (24*3600)
                                hours = total_seconds // 3600
                                total_seconds %= 3600
                                minutes = total_seconds // 60
                                seconds = total_seconds % 60

                                print(f"\033[1;32mKey còn hạn: {years} năm {months} tháng {days} ngày {hours} giờ {minutes} phút {seconds} giây")
                                sleep(5)
                                luu_thong_tin_ip(ip_address, nhap_key, datetime.now() + timedelta(seconds=int(check.get("time_remaining", 0))))
                                return
                        else:
                            
                            banner()
                            print("\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;91m✈  Lựa chọn không hợp lệ. Vui lòng chọn lại.")
                            print("\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập 1 Để Lấy Key \033[1;33m( Free )")
                            print("\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;32mNhập 2 Để Lấy Key \033[1;33m( Key Mua )")
                            continue  
                    except ValueError:
                        print("Vui lòng nhập số hợp lệ.")

        if da_qua_gio_moi():
            print("Key của bạn đã hết hạn. Đợi 2 giây để lấy key mới từ ngày mới...")
            time.sleep(2)
            main()  # Gọi lại main() để lấy key mới từ ngày mới
    else:
        print("Không thể lấy địa chỉ IP.")
if __name__ == '__main__':
    main()
import json
import os,time
import cloudscraper
import requests
import socket
import subprocess
from time import strftime
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import time
from colorama import Fore, init
import sys
import base64
import subprocess
from pystyle import Colors, Colorate
from rich.console import Console
from rich.panel import Panel
from rich.console import Console
from rich.text import Text
def kiem_tra_mang():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
    except OSError:
        print("Mạng không ổn định hoặc bị mất kết nối. Vui lòng kiểm tra lại mạng.")
kiem_tra_mang()
scraper = cloudscraper.create_scraper()
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
os.system('cls' if os.name== 'nt' else 'clear')
print(banner)
print("\033[1;35m╔═════════════════════════════════╗")
print("\033[1;35m║       \033[1;33m  LOGIN GOLIKE        \033[1;35m║")
print("\033[1;35m╚═════════════════════════════════╝") 
    # Nhập Auth
try:
  Authorization = open("Authorization.txt","x")
  t = open("token.txt","x")
except:
  pass
Authorization = open("Authorization.txt","r")
t = open("token.txt","r")
author = Authorization.read()
token = t.read()
if author == "":
  author = input("\033[1;32mNHẬP AUTHORIZATION : \033[1;33m")
  token = input("\033[1;32mNHẬP T : \033[1;33m")
  Authorization = open("Authorization.txt","w")
  t = open("token.txt","w")
  Authorization.write(author)
  t.write(token)
else:
  print(f"\033[1;32m       Nhấn Enter để vào TOOL")
  print(f"\033[38;2;0;220;255m               HOẶC ")
  select = input(f"\033[1;32mNhập AUTHORIZATION {Fore.RED}(tại đây) \033[1;32mđể vào acc khác: \033[1;33m")
  kiem_tra_mang()
  if select != "":
    author = select
    token = input("\033[1;32mNhập T (Token) : \033[1;33m")
    Authorization = open("Authorization.txt","w")
    t = open("token.txt","w")
    Authorization.write(author)
    t.write(token)
Authorization.close()
t.close()
os.system('cls' if os.name== 'nt' else 'clear')
print(banner)
print("\033[1;35m╔═════════════════════════════════╗")
print("\033[1;35m║   \033[1;33m   LIST ACC TIKTOK       \033[1;35m║")
print("\033[1;35m╚═════════════════════════════════╝")  
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=utf-8',
}  
