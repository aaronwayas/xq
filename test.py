import os
import platform
import calendar
import datetime
import json

import psutil
import argparse
from colorama import Style, Fore
from cpuinfo import get_cpu_info as cpuinfo

VERSION = "v0.1"
DATA_FILE = "data.json"

# Funciones para obtener información del sistema


def get_user_info() -> str:
    """
    Returns a string with user information.
    """
    name_machine = (
        load_color() + str(os.getenv("COMPUTERNAME")).lower() + Style.RESET_ALL
    )
    user_name = load_color() + os.getenv("USERNAME") + Style.RESET_ALL
    user_plus_machine = f"{name_machine}@{user_name}"

    return user_plus_machine


def get_cpu_info() -> str:
    """
    Returns a string with CPU information.
    """

    # Verifica si existe el archivo de datos
    if not os.path.exists(DATA_FILE):
        # Si el archivo de datos no existe, obtén la información de la CPU y guárdala en el archivo de datos
        cpu_info = cpuinfo()["brand_raw"]
        data = {"cpu_info": cpu_info}
        with open(DATA_FILE, "w") as file:
            json.dump(data, file)
        return cpu_info

    # Carga los datos del archivo de datos
    with open(DATA_FILE, "r") as file:
        try:
            data = json.load(file)
        except json.decoder.JSONDecodeError:
            # Si el archivo está vacío o no es JSON válido, obtén la información de la CPU y guárdala en el archivo de datos
            cpu_info = cpuinfo()["brand_raw"]
            data = {"cpu_info": cpu_info}
            with open(DATA_FILE, "w") as new_file:
                json.dump(data, new_file)
            return cpu_info

    # Verifica si la información de la CPU está en los datos
    if "cpu_info" in data:
        return data["cpu_info"]

    # Si la información de la CPU no está en los datos, obténla usando el módulo cpuinfo
    cpu_info = cpuinfo()["brand_raw"]

    # Guarda la información de la CPU en el archivo de datos
    data["cpu_info"] = cpu_info
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

    # Devuelve la información de la CPU
    return cpu_info


def get_color_items() -> list[str]:
    """
    Returns a list of color items. (Print "██")
    """
    colors = [
        Fore.BLACK,  # negro
        Fore.RED,  # rojo
        Fore.GREEN,  # verde
        Fore.YELLOW,  # amarillo
        Fore.BLUE,  # azul
        Fore.MAGENTA,  # magenta
        Fore.CYAN,  # cian
        Fore.WHITE,  # blanco
    ]

    color_items = [c + "██" + Style.RESET_ALL for c in colors]
    return color_items


def get_os_info() -> str:
    """
    Returns a string with OS information.
    """
    return (
        platform.system()
        + " "
        + platform.release()
        + f" ({platform.version()})"
        + " "
        + "x"
        + platform.architecture()[0]
    )


def get_uptime_info() -> str:
    """
    Returns a string with system uptime.
    """
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


def get_calendar_info() -> str:
    """
    Returns a string with calendar information.
    """
    now_month = datetime.datetime.now().month
    now_year = datetime.datetime.now().year
    calendar_month = calendar.month(now_year, now_month, 0, 0)

    date_today = (
        f"{datetime.date.today()}, {datetime.datetime.now().strftime('%I:%M:%S %p')}"
    )

    return calendar_month, date_today


def get_ram_info() -> str:
    """
    Returns a string with RAM information.
    """
    ram_used = round(psutil.virtual_memory().used / (1024.0**3), 2)
    ram_total = round(psutil.virtual_memory().total / (1024.0**3), 2)
    ram_info = f"{ram_used}/ {ram_total} GB"
    return ram_info


def load_color():
    """
    Load the color data from the JSON file.
    """

    with open(DATA_FILE, "r") as file:
        data = json.load(file)
        data = data["color"].lower()

    if data:
        return getattr(Fore, data.upper())

    return Fore.WHITE


def fetch_data():
    os = f"{load_color()}OS{Style.RESET_ALL}: \t{get_os_info()}"
    uptime = f"{load_color()}Uptime{Style.RESET_ALL}:\t{get_uptime_info()}"
    cpu = f"{load_color()}CPU{Style.RESET_ALL}:\t{get_cpu_info()}"
    ram = f"{load_color()}RAM{Style.RESET_ALL}:\t{get_ram_info()}"
    date = f"{load_color()}Date{Style.RESET_ALL}:\t{get_calendar_info()[1]}"
    xq = f"{load_color()}XQ{Style.RESET_ALL}:\t{VERSION}"

    return os, uptime, cpu, ram, date, xq


def fetch_info():
    """
    Returns a string with all system information.
    """

    return f"""

            {Fore.YELLOW}.++######++.                       
         .################+                         {get_user_info()}
        {Fore.YELLOW} +################-{Style.RESET_ALL}                         {"-" * 26}
         {Fore.YELLOW}#################{Style.RESET_ALL}   {Fore.GREEN}###+            +-     {fetch_data()[0]}
        {Fore.YELLOW}#################-{Style.RESET_ALL} {Fore.GREEN} .#################      {fetch_data()[1]}
       {Fore.YELLOW}-#################{Style.RESET_ALL}  {Fore.GREEN} #################.      {fetch_data()[2]}
       {Fore.YELLOW}#################{Style.RESET_ALL}   {Fore.GREEN}.#################       {fetch_data()[3]}
      {Fore.YELLOW}+################+{Style.RESET_ALL}   {Fore.GREEN}#################-       {fetch_data()[4]}
      {Fore.YELLOW}###+        +####.{Style.RESET_ALL}  {Fore.GREEN}.#################        {fetch_data()[5]}
      {Fore.YELLOW}                .{Style.RESET_ALL}   {Fore.GREEN}#################.        
      {Fore.BLUE}-+##########+{Style.RESET_ALL}      {Fore.GREEN}##################         
    {Fore.BLUE}+#################     {Fore.GREEN}.############+.     
    {Fore.BLUE}#################   {Style.BRIGHT}{Fore.YELLOW}.{Style.RESET_ALL}                      
   {Fore.BLUE}#################.      {Style.BRIGHT}{Fore.YELLOW}#####.       .###        {Style.DIM}{''.join(get_color_items())}
  {Fore.BLUE}.#################      {Style.BRIGHT}{Fore.YELLOW}+################+        {Style.BRIGHT}{''.join(get_color_items())}
  {Style.RESET_ALL}{Fore.BLUE}+################.      {Style.BRIGHT}{Fore.YELLOW}#################        
 {Style.RESET_ALL}{Fore.BLUE}.#################      {Style.BRIGHT}{Fore.YELLOW}#################-       
 {Style.RESET_ALL}{Fore.BLUE}#################-     {Style.BRIGHT}{Fore.YELLOW}-#################        
{Style.RESET_ALL}{Fore.BLUE}-#.          -####  {Style.BRIGHT}{Fore.YELLOW}   #################.        
                       {Style.BRIGHT}{Fore.YELLOW}.################+         
                       {Style.BRIGHT}{Fore.YELLOW}.################.         
                          {Style.BRIGHT}{Fore.YELLOW}.+#######++.{Style.RESET_ALL}     
   
    """


# Funciones para manipular argumentos de línea de comandos


def delete_data():
    """
    Function to delete data.
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as file:
            file.truncate()

    print("All data deleted.")


def change_color(color):
    """
    Function to change color.
    """
    if color.lower() in [
        "black",
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "white",
    ]:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

        data["color"] = color.lower()
        with open(DATA_FILE, "w") as file:
            json.dump(data, file)
        print(f"Color changed to '{color.lower()}'.")
    else:
        print(
            "Invalid color. Available colors are: black, red, green, yellow, blue, magenta, cyan, white."
        )


# Configuración del analizador de argumentos de línea de comandos

parser = argparse.ArgumentParser(description="Fetch on Windows")

parser.add_argument("-d", "--delete", help="Delete the data", action="store_true")
parser.add_argument(
    "-c",
    "--color",
    metavar="color",
    help="Change the color",
    type=str,
)

args = parser.parse_args()

# Ejecutando funciones basadas en los argumentos proporcionados

if args.delete:
    delete_data()

if args.color:
    change_color(args.color)

# Imprimiendo información del sistema

if __name__ == "__main__" and not (args.delete or args.color):
    print(fetch_info())
