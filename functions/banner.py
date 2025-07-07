from colorama import Fore, Style, init
from datetime import datetime
from functions.thanhngang import thanhngang

init(autoreset=True)

def banner():
  print(
    f"{Fore.CYAN}╔══════════════════════════════════════════════════════╗\n"
    f"{Fore.CYAN}║                                                      ║\n"
    f"{Fore.CYAN}║  {Fore.WHITE} █████╗ ███╗  ██╗██╗  ██╗ ██████╗ ██████╗ ███████╗  {Fore.CYAN}║\n"
    f"{Fore.CYAN}║ {Fore.WHITE}██╔══██╗████╗ ██║██║ ██╔╝██╔════╝██╔═══██╗██╔════╝  {Fore.CYAN}║\n"
    f"{Fore.CYAN}║ {Fore.WHITE}███████║██╔██╗██║█████═╝ ██║     ██║   ██║█████╗    {Fore.CYAN}║\n"
    f"{Fore.CYAN}║ {Fore.WHITE}██╔══██║██║╚████║██╔═██╗ ██║     ██║   ██║██╔══╝    {Fore.CYAN}║\n"
    f"{Fore.CYAN}║ {Fore.WHITE}██║  ██║██║ ╚███║██║ ╚██╗╚██████╗╚██████╔╝███████╗  {Fore.CYAN}║\n"
    f"{Fore.CYAN}║ {Fore.WHITE}╚═╝  ╚═╝╚═╝  ╚══╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝  {Fore.CYAN}║\n"
    f"{Fore.CYAN}║                                                      ║\n"
    f"{Fore.CYAN}║        {Fore.YELLOW}Admin: AnhCode | Box: https://zalo.me/g/nsilph288    {Fore.CYAN}║\n"
    f"{Fore.CYAN}║              {Fore.GREEN}Time: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}               {Fore.CYAN}║\n"
    f"{Fore.CYAN}╚══════════════════════════════════════════════════════╝\n"
)
thanhngang(55)
