import hashlib
import random
import requests
import time
from datetime import datetime
import json
import sys
import urllib3
import os

# Hàm in chậm từng ký tự
def print_slow(text, speed=0.002):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

# Hàm in banner/logo
def banner_logo():
    colors = [
        "\033[1;31m",  # Đỏ
        "\033[1;33m",  # Vàng
        "\033[1;32m",  # Xanh lá
        "\033[1;36m",  # Xanh ngọc
        "\033[1;34m",  # Xanh dương
        "\033[1;35m",  # Tím
        "\033[1;37m"   # Trắng
    ]

    logo = [
        "█████╗ ███╗   ██╗██╗  ██╗     ██████╗  ██████╗ ██████╗ ███████╗",
        "██╔══██╗████╗  ██║╚██╗██╔╝    ██╔════╝ ██╔═══██╗██╔══██╗██╔════╝",
        "███████║██╔██╗ ██║ ╚███╔╝     ██║  ███╗██║   ██║██████╔╝█████╗  ",
        "██╔══██║██║╚██╗██║ ██╔██╗     ██║   ██║██║   ██║██╔═══╝ ██╔══╝  ",
        "██║  ██║██║ ╚████║██╔╝ ██╗    ╚██████╔╝╚██████╔╝██║     ███████╗",
        "╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝     ╚═════╝  ╚═════╝ ╚═╝     ╚══════╝"
    ]

    os.system("clear")  # Xoá màn hình

    for i, line in enumerate(logo):
        print(colors[i % len(colors)], end="")
        print_slow(line, 0.0015)
    print("\033[0m")

    print("\033[1;33m")
    print_slow("═════════════ THÔNG TIN LIÊN HỆ ═════════════", 0.002)
    print("\033[0m")

    print("\033[1;36m Tele:     \033[0m", end=""); print_slow("https://t.me/anhcodeclick", 0.002)
    print("\033[1;35m Zalo:     \033[0m", end=""); print_slow("https://zalo.me/g/nsilph288", 0.002)
    print("\033[1;31m YouTube:  \033[0m", end=""); print_slow("https://youtube.com/@anhhcode", 0.002)

    print("\033[1;31m" + "─" * 50 + "\033[0m")

# Hiển thị banner
banner_logo()

# ==== Phần màu, khung ====
mo_ngoac_1 = "\033[1m["
mo_ngoac = "\033[1m[\x1b[1;38;2;173;255;47m"  
dong_ngoac = "\033[0m\033[1m]"  
mo_ngoac_do = "\033[0m\033[1m[\033[1;31m" 
mo_ngoac_xl = "\033[0m\033[1m[\033[1;32m" 
mo_ngoac_cam = "\033[0m\033[1m[\x1b[1;38;2;255;165;0m" 
xanhchuoi = "\x1b[1;38;2;173;255;47m"  
do = "\033[1;31m"  
resetmau = "\033[0m\33[1m" 
xanhduong = "\x1b[1;38;2;135;206;250m"  

que = ''.join(['─'] * 50)
thanh = f"{xanhduong}{que}{resetmau}"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = {
    'api_key': '882a8490361da98702bf97a021ddc14d',
    'secret': '62f8ce9f74b12f84c123cc23437a4a32',
    'key': ['ChanHungCoder_KeyRegFBVIP_9999', 'DCHVIPKEYREG']
}

email_prefix = ['gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com']

def create_account():
    random_birth_day = datetime.strftime(datetime.fromtimestamp(random.randint(
        int(time.mktime(datetime.strptime('1980-01-01', '%Y-%m-%d').timetuple())),
        int(time.mktime(datetime.strptime('1995-12-30', '%Y-%m-%d').timetuple()))
    )), '%Y-%m-%d')

    names = {
        'first': ['JAMES', 'JOHN', 'ROBERT', 'MICHAEL', 'WILLIAM', 'DAVID'],
        'last': ['SMITH', 'JOHNSON', 'WILLIAMS', 'BROWN', 'JONES', 'MILLER'],
        'mid': ['Alexander', 'Anthony', 'Charles', 'Dash', 'David', 'Edward']
    }

    random_first_name = random.choice(names['first'])
    random_name = f"{random.choice(names['mid'])} {random.choice(names['last'])}"
    password = f'anhcode{random.randint(0, 9999999)}?#@'
    full_name = f"{random_first_name} {random_name}"
    md5_time = hashlib.md5(str(time.time()).encode()).hexdigest()

    hash_ = f"{md5_time[0:8]}-{md5_time[8:12]}-{md5_time[12:16]}-{md5_time[16:20]}-{md5_time[20:32]}"
    email_rand = f"{full_name.replace(' ', '').lower()}{hashlib.md5((str(time.time()) + datetime.strftime(datetime.now(), '%Y%m%d')).encode()).hexdigest()[0:6]}@{random.choice(email_prefix)}"
    gender = 'M' if random.randint(0, 10) > 5 else 'F'

    req = {
        'api_key': app['api_key'],
        'attempt_login': True,
        'birthday': random_birth_day,
        'client_country_code': 'EN',
        'fb_api_caller_class': 'com.facebook.registration.protocol.RegisterAccountMethod',
        'fb_api_req_friendly_name': 'registerAccount',
        'firstname': random_first_name,
        'format': 'json',
        'gender': gender,
        'lastname': random_name,
        'email': email_rand,
        'locale': 'en_US',
        'method': 'user.register',
        'password': password,
        'reg_instance': hash_,
        'return_multiple_errors': True
    }

    sig = ''.join([f'{k}={v}' for k, v in sorted(req.items())])
    ensig = hashlib.md5((sig + app['secret']).encode()).hexdigest()
    req['sig'] = ensig

    api = 'https://b-api.facebook.com/method/user.register'

    def _call(url='', params=None, post=True):
        headers = {
            'User-Agent': '[FBAN/FB4A;FBAV/35.0.0.48.273;FBDM/{density=1.33125,width=800,height=1205};FBLC/en_US;FBCR/;FBPN/com.facebook.katana;FBDV/Nexus 7;FBSV/4.1.1;FBBK/0;]'
        }
        if post:
            response = requests.post(url, data=params, headers=headers, verify=False)
        else:
            response = requests.get(url, params=params, headers=headers, verify=False)
        return response.text

    reg = _call(api, req)
    reg_json = json.loads(reg)
    uid = reg_json.get('session_info', {}).get('uid')
    access_token = reg_json.get('session_info', {}).get('access_token')

    error_code = reg_json.get('error_code')
    error_msg = reg_json.get('error_msg')

    if uid and access_token:
        data_to_save = f"{random_birth_day}:{full_name}:{email_rand}:{password}:{uid}:{access_token}"
        with open(file_name, "a") as file:
            file.write(data_to_save + "\n")
        print("Birthday:", random_birth_day)
        print("Fullname:", full_name)
        print("Email:", email_rand)
        print("Password:", password)
        print("UID:", uid)
        print("Token:", access_token)
        print(thanh)
    else:
        if error_code and error_msg:
            print(f"Error Code: {error_code}")
            print(f"Error Message: {error_msg}")
        else:
            print(f"{do}Unknown error occurred.{resetmau}")
        print(f"{mo_ngoac_cam}×{dong_ngoac} Không Thể Lưu Thông Tin. Vui Lòng Đợi Reg Lại!")

# Nhập thông tin
while True:
    try:
        account_count = int(input(f"{mo_ngoac}*{dong_ngoac} Nhập Số Lượng Acc Muốn Reg: "))
        if account_count > 0:
            break
        else:
            print(f"{mo_ngoac_do}!{dong_ngoac} Số Lượng Acc Phải Lớn Hơn 0. Vui Lòng Nhập lại!")
    except ValueError:
        print(f"{mo_ngoac_do}!{dong_ngoac} Nội Dung Nhập Không Hợp Lệ!")

while True:
    file_name = input(f"{mo_ngoac}*{dong_ngoac} Nhập Tên File Lưu Thông Tin: ")
    if file_name.strip():
        if not file_name.endswith(".txt"):
            file_name += ".txt"
        break
    else:
        print(f"{mo_ngoac_do}!{dong_ngoac} Tên File Không Được Để Trống. Vui Lòng Nhập Lại!")

while True:
    try:
        delay = int(input(f"{mo_ngoac}*{dong_ngoac} Nhập Thời Gian Delay (Trên 180 Giây): "))
        if delay > 10:
            break
        else:
            print(f"{mo_ngoac_do}!{dong_ngoac} Delay Phải Lớn Hơn 179 Giây. Vui Lòng Nhập Lại!")
    except ValueError:
        print(f"{mo_ngoac_do}!{dong_ngoac} Nội Dung Nhập Không Hợp Lệ!")

print(thanh)

for _ in range(account_count):
    create_account()
    print(f"Chờ {delay} Giây...", end='')
    for remaining in range(delay, 0, -1):
        print(f"\r{mo_ngoac}*{dong_ngoac} Vui Lòng Đợi: {remaining} Giây", end='', flush=True)
        time.sleep(1)
    print()
    print(thanh)

print(f"{mo_ngoac}✓{dong_ngoac} Tất Cả Thông Tin Đã Được Lưu Vào File: {xanhchuoi}{file_name}{resetmau}")
sys.exit()
