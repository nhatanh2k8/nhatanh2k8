import requests
import json
import time
import random
import asyncio
from bs4 import BeautifulSoup
import sys
import os

# ==== BANNER ASCII ====
def print_slow(text, speed=0.002):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

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
        " █████╗ ███╗   ██╗██╗  ██╗ ██████╗  ██████╗ ██████╗ ███████╗",
        "██╔══██╗████╗  ██║╚██╗██╔╝██╔═══██╗██╔═══██╗██╔══██╗██╔════╝",
        "███████║██╔██╗ ██║ ╚███╔╝ ██║   ██║██║   ██║██████╔╝█████╗  ",
        "██╔══██║██║╚██╗██║ ██╔██╗ ██║   ██║██║   ██║██╔═══╝ ██╔══╝  ",
        "██║  ██║██║ ╚████║██╔╝ ██╗╚██████╔╝╚██████╔╝██║     ███████╗",
        "╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝     ╚══════╝",
        "                   🅐🅝🅗🅒🅞🅓🅔 . 🅣🅔🅐🅜"
    ]

    os.system("cls" if os.name == "nt" else "clear")
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


# --- Cấu hình API Mail.gw ---
BASE_URL = "https://api.mail.gw"
HEADERS = {"Content-Type": "application/json"}

def get_domains():
    try:
        response = requests.get(f"{BASE_URL}/domains", headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        domains = [member['domain'] for member in data.get('hydra:member', []) if member.get('isActive')]
        return domains
    except Exception as e:
        print(f"[❌] Lỗi khi lấy domains: {e}")
        return []

def create_account(username, domain, password):
    address = f"{username}@{domain}"
    payload = {"address": address, "password": password}
    try:
        response = requests.post(f"{BASE_URL}/accounts", headers=HEADERS, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[❌] Lỗi khi tạo tài khoản {address}: {e}")
        return None

def get_token(address, password):
    payload = {"address": address, "password": password}
    try:
        response = requests.post(f"{BASE_URL}/token", headers=HEADERS, data=json.dumps(payload))
        response.raise_for_status()
        return response.json().get('token')
    except Exception as e:
        print(f"[❌] Lỗi khi lấy token cho {address}: {e}")
        return None

def get_messages(auth_token):
    headers_with_auth = HEADERS.copy()
    headers_with_auth["Authorization"] = f"Bearer {auth_token}"
    try:
        response = requests.get(f"{BASE_URL}/messages", headers=headers_with_auth)
        response.raise_for_status()
        return response.json().get('hydra:member', [])
    except Exception as e:
        print(f"[❌] Lỗi khi lấy tin nhắn: {e}")
        return []

def get_message_detail(msg_id, auth_token):
    headers_with_auth = HEADERS.copy()
    headers_with_auth["Authorization"] = f"Bearer {auth_token}"
    try:
        response = requests.get(f"{BASE_URL}/messages/{msg_id}", headers=headers_with_auth)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[❌] Lỗi khi lấy chi tiết tin nhắn {msg_id}: {e}")
        return None

async def check_inbox_loop(token):
    checked_ids = set()
    print("\n📬 Đang kiểm tra thư đến mỗi 10 giây...")
    while True:
        messages = get_messages(token)
        new_messages = [msg for msg in messages if msg['id'] not in checked_ids]

        for msg in new_messages:
            checked_ids.add(msg['id'])
            detail = get_message_detail(msg['id'], token)
            if detail:
                sender = detail['from']['address']
                subject = detail.get('subject', '(Không có chủ đề)')
                text = detail.get('text', '')
                if not text and detail.get('html'):
                    soup = BeautifulSoup(detail['html'][0], 'html.parser')
                    text = soup.get_text(separator='\n', strip=True)
                print(f"\n🆕 Tin nhắn mới:")
                print(f"  📧 Từ: {sender}")
                print(f"  📝 Chủ đề: {subject}")
                print(f"  📄 Nội dung:\n{text}\n{'-'*50}")
        await asyncio.sleep(10)

def main():
    banner_logo()  # ← THÊM LOGO TRƯỚC KHI CHẠY TOOL
    print("🔧 Tool Tạo Email Ảo | Mail.GW")
    domains = get_domains()
    if not domains:
        print("[❌] Không thể lấy danh sách domain!")
        return

    domain = random.choice(domains)
    username = f"user_{int(time.time())}"
    password = "AnhCode!"

    print(f"🛠 Đang tạo email ảo...")
    acc = create_account(username, domain, password)
    if not acc:
        print("[❌] Không thể tạo email.")
        return

    address = acc['address']
    token = get_token(address, password)
    if not token:
        print("[❌] Không lấy được token.")
        return

    print(f"✅ Tạo thành công email: {address}")
    print(f"🔑 Password: {password}")

    asyncio.run(check_inbox_loop(token))

if __name__ == "__main__":
    main()
