import os
import platform
import psutil
from colorama import Style, Fore
import calendar
import datetime
from cpuinfo import get_cpu_info as cpu_info

# Configurations (Comming soon!)


# User Info
name_machine = Fore.RED + str(os.getenv("COMPUTERNAME")).lower() + Style.RESET_ALL
user_name = Fore.RED + os.getenv("USERNAME") + Style.RESET_ALL
user_plus_machine = f"{name_machine}@{user_name}"
cpuInfo = cpu_info()["brand_raw"]


# All Colors
def get_color_items():
    colors = [
        Fore.BLACK,
        Fore.RED,
        Fore.GREEN,
        Fore.YELLOW,
        Fore.BLUE,
        Fore.MAGENTA,
        Fore.CYAN,
        Fore.WHITE,
    ]
    color_items = [c + "██" + Style.RESET_ALL for c in colors]
    return color_items


# OS Info
os_info = (
    platform.system()
    + " "
    + platform.release()
    + f" ({platform.version()})"
    + " "
    + "x"
    + platform.architecture()[0]
)

# Ram Info
ram_used = round(psutil.virtual_memory().used / (1024.0**3), 2)
ram_total = round(psutil.virtual_memory().total / (1024.0**3), 2)
Ram_info = f"{ram_used}/ {ram_total} GB"


# Uptime
def get_uptime_info():
    boot_time_timestamp = psutil.boot_time()
    boot_time_datetime = datetime.datetime.fromtimestamp(boot_time_timestamp)
    now = datetime.datetime.now()
    uptime = now - boot_time_datetime
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        uptime_str = f"{hours} hours, {minutes} minutes"
    elif minutes > 0:
        uptime_str = f"{minutes} minutes, {seconds} seconds"
    else:
        uptime_str = f"{seconds} seconds"
    return uptime_str


# Calendar
now_month = datetime.datetime.now().month
now_year = datetime.datetime.now().year
calendar_month = calendar.month(now_year, now_month, 0, 0)

print(
    f"""
{user_plus_machine}
{"-" * 26}
{Fore.RED}OS{Style.RESET_ALL}:\t {os_info}
{Fore.RED}Uptime{Style.RESET_ALL}:  {get_uptime_info()}
{Fore.RED}CPU{Style.RESET_ALL}:\t {cpuInfo}
{Fore.RED}RAM{Style.RESET_ALL}:\t {Ram_info}                              
{Fore.RED}Date{Style.RESET_ALL}:\t {datetime.date.today()}, {datetime.datetime.now().strftime('%I:%M:%S %p')}

{calendar_month}                                                                                                                                        
{Style.DIM}{''.join(get_color_items())}
{Style.BRIGHT}{''.join(get_color_items())}
"""
)
