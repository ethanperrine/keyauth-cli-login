import os
import subprocess
import sys
from keyauth import api


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


class PythonNotInstalled(Exception):

    def __init__(self, message="Python is not installed"):
        self.message = message
        super().__init__(self.message)


while True:
    print("Checking Modules")
    cls()
    response = subprocess.check_output(sys.executable + " -m pip --version", shell=True, universal_newlines=True)

    if "No module named" in response:
        print("Installing Libraries")
        os.system("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
        os.system(f"{sys.executable} get-pip.py")
        os.system("del get-pip.py")
    try:
        import asyncio
        import aiohttp
        import easygui
        import requests
        import fade
        import hashlib
        import concurrent.futures
        import ctypes
        from datetime import datetime
        from time import sleep
        import re
        import configparser
        import requests_toolbelt

        break

    except ModuleNotFoundError as e:
        module = e.name
        print(f"{module} not found")
        subprocess.Popen([sys.executable, "-m", "pip", "install", module]).wait()


config = configparser.ConfigParser()


def login():
    ctypes.windll.kernel32.SetConsoleTitleW("Swiss Login")
    print("Initializing")
    sleep(1.2)
    cls()

    login_text = ("""\n
  _                 _         __  __                  
 | |               (_)       |  \/  |                 
 | |     ___   __ _ _ _ __   | \  / | ___ _ __  _   _ 
 | |    / _ \ / _` | | '_ \  | |\/| |/ _ \ '_ \| | | |
 | |___| (_) | (_| | | | | | | |  | |  __/ | | | |_| |
 |______\___/ \__, |_|_| |_| |_|  |_|\___|_| |_|\__,_|
               __/ |                                  
              |___/                                   
""")

    faded_login = fade.purpleblue(login_text)
    print(faded_login)

    def getchecksum():
        path = os.path.basename(__file__)
        if not os.path.exists(path):
            path = path[:-2] + "exe"
        md5_hash = hashlib.md5()
        a_file = open(path, "rb")
        content = a_file.read()
        md5_hash.update(content)
        digest = md5_hash.hexdigest()
        return digest

    keyauthapp = api(
        name="",
        ownerid="",
        secret="",
        version="1.0",
        hash_to_check=getchecksum()
    )

    def write_file():
        config.write(open('config.ini', 'w'))
    print("""
    \t \t1) Login
    \t \t2) Register
    \t \t3) Upgrade
    \t \t4) License Key Only
    """)
    chosen = False
    while not chosen:
        ans = input("\t \tSelect Option: ")
        if ans == "1":
            chosen = 1
            configExists = False
            try:
                configExists = True
                open("config.ini", "r")
            except Exception as ee:
                configExists = False
                print(ee)

                if configExists:
                    print("\t \tFound login!")
                    config.read('config.ini')
                    user = config['login']['username']
                    password = config['login']['password']
                    keyauthapp.login(user, password)
                else:
                    user = input('\t \tProvide username: ')
                    password = input('\t \tProvide password: ')
                    keyauthapp.login(user, password)
                    config['login'] = {'username': f'{user}', 'password': f'{password}'}
                    write_file()
        elif ans == "2":
            chosen = True
            user = input('\t \tProvide username: ')
            password = input('\t \tProvide password: ')
            license = input('\t \tProvide License: ')
            keyauthapp.register(user, password, license)
        elif ans == "3":
            chosen = True
            user = input('\t \tProvide username: ')
            license = input('\t \tProvide License: ')
            keyauthapp.upgrade(user, license)
        elif ans == "4":
            chosen = True
            key = input('\t \tEnter your license: ')
            keyauthapp.license(key)
        else:
            print("\n\t \tNot Valid Option\n")

        print("\nUser data: ")
        print("Username: " + keyauthapp.user_data.username)
        print("Subcription: " + keyauthapp.user_data.subscription)
        print(
            "Created at: " + datetime.utcfromtimestamp(int(keyauthapp.user_data.createdate)).strftime(
                '%Y-%m-%d %H:%M:%S'))
        print(
            "Expires at: " + datetime.utcfromtimestamp(int(keyauthapp.user_data.expires)).strftime('%Y-%m-%d %H:%M:%S'))
        print(f"Current Session Validation Status: {keyauthapp.check()}")
login()
