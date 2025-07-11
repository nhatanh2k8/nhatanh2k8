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
    'Authorization': author,
    't': token,
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    'Referer': 'https://app.golike.net/account/manager/tiktok',
}
scraper = cloudscraper.create_scraper()
def chonacc():
    json_data = {}
    response = scraper.get(
        'https://gateway.golike.net/api/tiktok-account',
        headers=headers,
        json=json_data
    ).json()
    return response
def nhannv(account_id):
    try:
        params = {
            'account_id': account_id,
            'data': 'null',
        }
        response = scraper.get(
            'https://gateway.golike.net/api/advertising/publishers/tiktok/jobs',
            headers=headers,
            params=params,
            json={}
        )
        return response.json()
    except Exception as e:
        print()
        return {}
def hoanthanh(ads_id, account_id):
    try:
        json_data = {
            'ads_id': ads_id,
            'account_id': account_id,
            'async': True,
            'data': None,
        }
        response = scraper.post(
            'https://gateway.golike.net/api/advertising/publishers/tiktok/complete-jobs',
            headers=headers,
            json=json_data,
            timeout=6
        )
        return response.json()
    except Exception as e:
        print()
        return {}
def baoloi(ads_id, object_id, account_id, loai):
    try:
        json_data1 = {
            'description': 'Tôi đã làm Job này rồi',
            'users_advertising_id': ads_id,
            'type': 'ads',
            'provider': 'tiktok',
            'fb_id': account_id,
            'error_type': 6,
        }
        scraper.post('https://gateway.golike.net/api/report/send', headers=headers, json=json_data1)
        json_data2 = {
            'ads_id': ads_id,
            'object_id': object_id,
            'account_id': account_id,
            'type': loai,
        }
        scraper.post(
            'https://gateway.golike.net/api/advertising/publishers/tiktok/skip-jobs',
            headers=headers,
            json=json_data2,
        )
    except Exception as e:
        print()
# Gọi chọn tài khoản một lần và xử lý lỗi nếu có
chontktiktok = chonacc()
def dsacc():
  if chontktiktok.get("status") != 200:  
    print("\033[1;31mAuthorization hoăc T sai   ")
    quit()
  for i in range(len(chontktiktok["data"])):
    print(f'\033[1;36m[{i+1}]\033[1;93m {chontktiktok["data"][i]["nickname"]} \033[1;97m|\033[1;31m\033[1;32m Hoạt Động')
dsacc() 
print(f"{Fore.MAGENTA}═══════════════════════════════════")
while True:
  try:
    luachon = int(input("\033[1;32mChọn tài khoản TIKTOK: \033[1;33m"))
    while luachon > len((chontktiktok)["data"]):
      luachon = int(input("\033[1;32mAcc Này Không Có Trong Danh Sách , Nhập Lại : \033[1;33m"))
    account_id = chontktiktok["data"][luachon - 1]["id"]
    break  
  except:
    print("\033[1;31mSai Định Dạng   ") 
while True:
  try:
    delay = int(input(f"\033[1;32mDelay: \033[1;33m"))
    break
  except:
    print("\033[1;31mSai Định Dạng  ")
while True:
  try: 
    doiacc = int(input(f"\033[1;32mThất bại bao nhiêu lần thì đổi acc: \033[1;33m"))
    break
  except:
    print("\033[1;31mNhập Vào 1 Số  ")  
print("\033[1;35m╔═════════════════════════════════╗")
print("\033[1;35m║     \033[1;33m  CHỌN LOẠI NHIỆM VỤ        \033[1;35m║")
print("\033[1;35m╚═════════════════════════════════╝")
print("\033[1;36m[1] \033[1;32mFollow")
print("\033[1;36m[2] \033[1;32mLike")
print("\033[1;36m[3] \033[1;32mCả hai (\033[1;33mFollow và Like\033[1;32m)")
while True:
    try:
        loai_nhiem_vu = int(input("\033[1;32mChọn loại nhiệm vụ: \033[1;33m"))
        if loai_nhiem_vu in [1, 2, 3]:
            break
        else:
            print("\033[1;31mVui lòng chọn số từ 1 đến 3!")
    except:
        print("\033[1;31mSai định dạng! Vui lòng nhập số.")  
x_like, y_like, x_follow, y_follow = None, None, None, None
print("\033[1;35m╔═════════════════════════════════╗")
print("\033[1;35m║       \033[1;33m  ADB Tự Ðộng             \033[1;35m║")
print("\033[1;35m╚═════════════════════════════════╝")
print(f"\033[1;36m[1] yes")
print(f"\033[1;36m[2] no")
adbyn = input(f"\033[1;32mNhập lựa chọn: \033[1;33m")
if adbyn == "1":
    def setup_adb():
      config_file = "adb_config.txt"
      like_coords_file = "toa_do_tim.txt"
      follow_coords_file = "toa_do_follow.txt"
    # Nhập IP và port ADB
      print(f"{Fore.MAGENTA}═══════════════════════════════════")
      print("\033[1;33mBạn có thể xem video hướng dẫn kết nối ADB")
      print("\033[1;33mLink video: \033[38;2;0;220;255mhttps://youtu.be/vcWNzu2XRSE?si=_jFVm9nhSkNGBK_-\033[0m")
      ip = input("\033[1;32mNhập IP của thiết bị ví dụ (192.168.1.2): \033[1;33m")
      adb_port = input("\033[1;32mNhập port của thiết bị ví dụ (39327): \033[1;33m")
      # Kiểm tra và đọc tọa độ từ file nếu tồn tại
      x_like, y_like, x_follow, y_follow = None, None, None, None    
      if os.path.exists(like_coords_file):
           with open(like_coords_file, "r") as f:
              coords = f.read().split("|")
              if len(coords) == 2:
                   x_like, y_like = coords
                   print(f"\033[1;32mĐã tìm thấy tọa độ nút tim: X={x_like}, Y={y_like}")    
      if os.path.exists(follow_coords_file):
          with open(follow_coords_file, "r") as f:
               coords = f.read().split("|")
               if len(coords) == 2:
                   x_follow, y_follow = coords
                   print(f"\033[1;32mĐã tìm thấy tọa độ nút follow: X={x_follow}, Y={y_follow}")
      if not os.path.exists(config_file):
           print("\033[1;36mLần đầu chạy, nhập mã ghép nối (6 SỐ) và port ghép nối.\033[0m")
           pair_code = input("\033[1;32mNhập mã ghép nối 6 số ví dụ (322763): \033[1;33m")
           pair_port = input("\033[1;32mNhập port ghép nối ví dụ (44832): \033[1;33m")
           with open(config_file, "w") as f:
               f.write(f"{pair_code}|{pair_port}")
      else:
          with open(config_file, "r") as f:
               pair_code, pair_port = [s.strip() for s in f.read().split("|")]  
      print("\n\033[1;36m  Đang ghép nối với thiết bị\033[0m")
      os.system(f"adb pair {ip}:{pair_port} {pair_code}")
      time.sleep(2)  
      print("\033[1;36m  Đang kết nối ADB\033[0m")
      os.system(f"adb connect {ip}:{adb_port}")
      time.sleep(2)  
      devices = os.popen("adb devices").read()
      if ip not in devices:
        print(f"{Fore.RED} Kết nối thất bại{Fore.WHITE}")
        exit()    
       # Yêu cầu nhập tọa độ nếu chưa có
      print("\033[1;35m╔═════════════════════════════════╗")
      print("\033[1;35m║     \033[1;33m  NHẬP TỌA ĐỘ NÚT         \033[1;35m║")
      print("\033[1;35m╚═════════════════════════════════╝")    
      if loai_nhiem_vu in [1, 3] and (x_follow is None or y_follow is None):
           x_follow = input("\033[1;32mNhập tọa độ X của nút follow: \033[1;33m")
           y_follow = input("\033[1;32mNhập tọa độ Y của nút follow: \033[1;33m")
           with open(follow_coords_file, "w") as f:
               f.write(f"{x_follow}|{y_follow}")    
      if loai_nhiem_vu in [2, 3] and (x_like is None or y_like is None):
           x_like = input("\033[1;32mNhập tọa độ X của nút tim: \033[1;33m")
           y_like = input("\033[1;32mNhập tọa độ Y của nút tim: \033[1;33m")
           with open(like_coords_file, "w") as f:
              f.write(f"{x_like}|{y_like}")
      return x_like, y_like, x_follow, y_follow
# Khi gọi hàm setup_adb()
    x_like, y_like, x_follow, y_follow = setup_adb()
elif adbyn == "2":
    pass
# Thêm phần chọn loại nhiệm vụ sau khi chọn tài khoản và trước khi bắt đầu làm nhiệm vụ   
dem = 0
tong = 0
checkdoiacc = 0
dsaccloi = []
accloi = ""
os.system('cls' if os.name== 'nt' else 'clear')
print(banner)
print("\033[1;37m════════════════════════════════════════════════════════════")
print("\033[1;31m| \033[1;36mSTT \033[1;37m| \033[1;33mThời gian \033[1;37m| \033[1;32mStatus \033[1;37m| \033[1;31mType job \033[1;37m| \033[1;32mID Acc \033[1;37m| \033[1;32mXu \033[1;37m| \033[1;33mTổng       ")
print("\033[1;37m════════════════════════════════════════════════════════════")
while True:
    if checkdoiacc == doiacc:
        dsaccloi.append(chontktiktok["data"][luachon - 1]["nickname"])
        print(f"{Fore.WHITE}════════════════════════════════════════════════════")
        print(f"\033[1;31m  Acc Tiktok {dsaccloi} gặp vấn đề ")
        print(f"{Fore.WHITE}════════════════════════════════════════════════════")
        dsacc()
        while True:
            try:
                print(f"{Fore.WHITE}════════════════════════════════════════════════════")
                luachon = int(input("\033[1;32mChọn tài khoản mới: \033[1;33m"))
                while luachon > len((chontktiktok)["data"]):
                    luachon = int(input("\033[1;31mAcc Này Không Có Trong Danh Sách, Hãy Nhập Lại : \033[1;33m"))
                account_id = chontktiktok["data"][luachon - 1]["id"]
                checkdoiacc = 0
                os.system('cls' if os.name== 'nt' else 'clear')
                for h in banner:
                    print(h,end = "")
                break  
            except:
                print("\033[1;31mSai Định Dạng !!!")
    print('\033[1;35mĐang Tìm Nhiệm Vụ', end="\r")
    max_retries = 3
    retry_count = 0
    nhanjob = None
    while retry_count < max_retries:
        try:
            nhanjob = nhannv(account_id)
            if nhanjob and nhanjob.get("status") == 200 and nhanjob["data"].get("link") and nhanjob["data"].get("object_id"):
                break
            else:
                retry_count += 1
                time.sleep(2)
        except Exception as e:
            retry_count += 1
            time.sleep(1)
    if not nhanjob or retry_count >= max_retries:
        continue
    ads_id = nhanjob["data"]["id"]
    link = nhanjob["data"]["link"]
    object_id = nhanjob["data"]["object_id"]
    job_type = nhanjob["data"]["type"]
    # Kiểm tra loại nhiệm vụ
    if (loai_nhiem_vu == 1 and job_type != "follow") or \
       (loai_nhiem_vu == 2 and job_type != "like") or \
       (job_type not in ["follow", "like"]):
        baoloi(ads_id, object_id, account_id, job_type)
        continue
    # Mở link và kiểm tra lỗi
    try:
        if adbyn == "1":
            os.system(f'adb shell am start -a android.intent.action.VIEW -d "{link}" > /dev/null 2>&1')
        else:
            #os.system(f"termux-open-url {link}")
            subprocess.run(["termux-open-url", link])        
        for remaining in range(3, 0, -1):
            time.sleep(1)
        print("\r" + " " * 30 + "\r", end="")
    except Exception as e:
        baoloi(ads_id, object_id, account_id, job_type)
        continue
    # Thực hiện thao tác ADB
    if job_type == "like" and adbyn == "1" and x_like and y_like:
        os.system(f"adb shell input tap {x_like} {y_like}")
    elif job_type == "follow" and adbyn == "1" and x_follow and y_follow:
        os.system(f"adb shell input tap {x_follow} {y_follow}")
    # Đếm ngược delay
    for remaining_time in range(delay, -1, -1):
        color = "\033[1;36m" if remaining_time % 2 == 0 else "\033[1;33m"
        print(f"\r{color}AnhCode | ○.O | {remaining_time}s           ", end="")
        time.sleep(1)    
    print("\r                          \r", end="") 
    print("\033[1;35mĐang Buss    ",end = "\r")
    # Hoàn thành job
    max_attempts = 2
    attempts = 0
    nhantien = None
    while attempts < max_attempts:
        try:
            nhantien = hoanthanh(ads_id, account_id)
            if nhantien and nhantien.get("status") == 200:
                break
        except:
            pass  
        attempts += 1
    if nhantien and nhantien.get("status") == 200:
        dem += 1
        tien = nhantien["data"]["prices"]
        tong += tien
        local_time = time.localtime()
        hour = local_time.tm_hour
        minute = local_time.tm_min
        second = local_time.tm_sec
        h = hour
        m = minute
        s = second
        if hour < 10:
            h = "0" + str(hour)
        if minute < 10:
            m = "0" + str(minute)
        if second < 10:
            s = "0" + str(second)                                      
        chuoi = (f"\033[1;31m| \033[1;36m{dem}"
                f" \033[1;37m| \033[1;33m{h}:{m}:{s}"
                f" \033[1;37m| \033[1;32msuccess"
                f" \033[1;37m| \033[1;31m{job_type}"
                f" \033[1;37m| \033[1;32mẨn ID"
                f" \033[1;37m| \033[1;32m+{tien}"
                f" \033[1;37m| \033[1;33m{tong}")
        print("                                                    ", end="\r")
        print(chuoi)
        time.sleep(0.7)
        checkdoiacc = 0
    else:
        try:
            baoloi(ads_id, object_id, account_id, nhanjob["data"]["type"])
            print("                                              ", end="\r")
            print("\033[1;31mBỏ qua nhiệm vụ ", end="\r")
            sleep(1)
            checkdoiacc += 1
        except:
            pass
