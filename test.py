import os
import platform
import calendar
import datetime
import json

import psutil
import argparse
from colorama import Style, Fore
from cpuinfo import get_cpu_info as cpuinfo

# Se elimina la variable global VERSION
# Se define la ruta del archivo de datos de forma relativa al script
DATA_FILE = "data.json"
VERSION = "v0.1"
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
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            if "cpu_info" in data:
                return data["cpu_info"]
    except (
        FileNotFoundError,
        json.decoder.JSONDecodeError,
        KeyError,
        TypeError,
        AttributeError,
    ) as err:
        # Si no se puede cargar el archivo o no se encuentra la clave "cpu_info"
        # se ignora y se vuelve a cargar la información
        print(f"Warning: Error loading CPU info from {DATA_FILE}: {err}")

    cpu_info = cpuinfo()["brand_raw"]

    try:
        with open(DATA_FILE, "w") as file:
            json.dump({"cpu_info": cpu_info}, file)
    except (
        FileNotFoundError,
        json.decoder.JSONDecodeError,
        TypeError,
        AttributeError,
    ) as err:
        # Si no se puede guardar el archivo, se ignora
        print(f"Warning: Error saving CPU info to {DATA_FILE}: {err}")

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

    with open(DATA_FILE, "r") as file:
        data = json.load(file)["settings"]["date"]

    if data["format_hour"] == "24":
        if data["format_date"] == "full":
            return (
                calendar.day_name[datetime.datetime.now().weekday()]
                + ", "
                + datetime.datetime.now().strftime("%H:%M:%S")
                + ", "
                + datetime.datetime.now().strftime("%d-%m-%Y")
            )
        elif data["format_date"] == "short":
            return (
                datetime.datetime.now().strftime("%H:%M")
                + ", "
                + datetime.datetime.now().strftime("%d/%m")
            )

    elif data["format_hour"] == "12":
        if data["format_date"] == "full":
            return (
                calendar.day_name[datetime.datetime.now().weekday()]
                + ", "
                + datetime.datetime.now().strftime("%I:%M:%S %p")
                + ", "
                + datetime.datetime.now().strftime("%d-%m-%Y")
            )
        elif data["format_date"] == "short":
            return (
                datetime.datetime.now().strftime("%I:%M %p")
                + ", "
                + datetime.datetime.now().strftime("%d/%m")
            )


def get_ram_info() -> str:
    """
    Returns a string with RAM information.
    """

    with open(DATA_FILE, "r") as file:
        data = json.load(file)["settings"]["ram"]
        data = data

    if data["unit"].upper() == "GB":  # 8.4/16gb
        return f"{round(psutil.virtual_memory().used / (1024.0**3), 2)}/{round(psutil.virtual_memory().total / (1024.0**3), 2)} GB ({psutil.virtual_memory().percent}%)"

    elif data["unit"].upper() == "MB":  # 8.4/16gb
        return f"{round(psutil.virtual_memory().used / (1024.0**2), 2)}/{round(psutil.virtual_memory().total / (1024.0**2), 2)} MB ({psutil.virtual_memory().percent}%)"


def load_color():
    """
    Load the color data from the JSON file.
    """
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            data = data["settings"]
            color = data.get(
                "color", "blue"
            )  # Si no se encuentra la clave "color", se establece el color predeterminado como "blue"
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        color = "blue"

    return getattr(Fore, color.upper())


def fetch_data():
    os_info = f"{load_color()}OS{Style.RESET_ALL}: \t{get_os_info()}"
    uptime_info = f"{load_color()}Uptime{Style.RESET_ALL}:\t{get_uptime_info()}"
    cpu_info = f"{load_color()}CPU{Style.RESET_ALL}:\t{get_cpu_info()}"
    ram_info = f"{load_color()}RAM{Style.RESET_ALL}:\t{get_ram_info()}"
    date_info = f"{load_color()}Date{Style.RESET_ALL}:\t{get_calendar_info()}"
    version_info = f"{load_color()}XQ{Style.RESET_ALL}:\t {VERSION}"

    return os_info, uptime_info, cpu_info, ram_info, date_info, version_info


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
        os.remove(DATA_FILE)
        print("All data deleted.")
    else:
        print("No data to delete.")


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

        data["settings"]["color"] = color.lower()
        with open(DATA_FILE, "w") as file:
            json.dump(data, file)
        print(f"Color changed to '{color.lower()}'.")
    else:
        print(
            "Invalid color. Available colors are: black, red, green, yellow, blue, magenta, cyan, white."
        )


def change_settings(setting, value):
    """
    Function to change settings.
    """
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

        if setting == "ram":
            if value.lower() in ["mb", "gb"]:
                data["settings"]["ram"]["unit"] = value.lower()
                with open(DATA_FILE, "w") as file:
                    json.dump(data, file)
                print(f"RAM unit changed to '{value.lower()}'.")
                exit()
            else:
                print("Invalid unit. Available units are: 'MB' or 'GB'.")
                exit()

        elif setting == "date":
            format_hour = input("Enter the format for hour (12/24): ").strip().lower()
            format_date = (
                input("Enter the format for date (full/short): ").strip().lower()
            )

            if format_hour in ["12", "24"] and format_date in ["full", "short"]:
                data["settings"]["date"]["format_hour"] = format_hour
                data["settings"]["date"]["format_date"] = format_date
                with open(DATA_FILE, "w") as file:
                    json.dump(data, file)
                print("Date format changed successfully.")
                exit()
            else:
                print(
                    "Invalid formats. Hour format should be '12' or '24', and date format should be 'full' or 'short'."
                )
                exit()
    except FileNotFoundError:
        print(
            "Data file not found. Please run the script without options first to create the data file."
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
parser.add_argument(
    "-s",
    "--settings",
    metavar="setting",
    help="Change the settings",
    choices=["ram", "date"],
    nargs="?",
    type=str,
)

args = parser.parse_args()

# Ejecutando funciones basadas en los argumentos proporcionados

if args.delete:
    delete_data()

if args.color:
    change_color(args.color)

if args.settings:
    if args.settings == "date":
        change_settings(args.settings, None)  # We don't need value for date setting
    else:
        change_settings(args.settings, input("Enter the value: ").strip().lower())


# Imprimiendo información del sistema

if __name__ == "__main__" and not (args.delete or args.color):
    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
        default_data = {
            "cpu_info": get_cpu_info(),
            "settings": {
                "color": "blue",
                "ram": {"unit": "GB"},
                "date": {"format_hour": "24", "format_date": "full"},
            },
        }
        with open(DATA_FILE, "w") as file:
            json.dump(default_data, file)

    print(fetch_info())
