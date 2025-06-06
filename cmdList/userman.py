import base64  # 加解密库
from colorama import Fore  # 彩色文字库
import json  # 解析和保存json配置文件
import pwinput  # 密码输入库
from textwrap import dedent  # 格式化输出库
from utils.man import ErrorCodeManager
from utils.config import *

__doc__ = "PyOS User Manager"

__usage__ = {
    "log": "Show current login user",
    "list": "List all users",
    "create": "Create a new user",
    "change": "Change current user password",
    "auto": "Set auto login user"
}

def execute(self, args):
    if not args:  # 检查是否提供了参数
        print(f"Error: {Fore.RED}No arguments provided. Please specify a valid command.")
        print("Usage:")
        for command, description in __usage__.items():
            print(f"  {command}: {description}")
        self.error_code = ErrorCodeManager().get_code(SyntaxError)
        return

    match args[0]:
        case "log":
            print(f"Now login: {Fore.GREEN}{self.username}")
        case "list":
            show_all_users(self)
        case "create":
            create_user()
        case "change":
            change_passwd(self)
        case "auto":
            set_auto_login(args)
        case _:
            print(f"Error: {Fore.RED}Unknown command '{args[0]}'.")
            print("Usage:")
            for command, description in __usage__.items():
                print(f"  {command}: {description}")
            self.error_code = ErrorCodeManager().get_code(SyntaxError)

def show_all_users(self):
    print("All users:")
    for user in ACCOUNTS:
        if user == self.username:
            print(f"- {Fore.BLUE}{user} {Fore.RESET}(Current user)")
            continue
        print(f"- {Fore.BLUE}{user}")

def create_user():
    newname = input('Name: ')
    newpwd = pwinput.pwinput("Password: ")
    repwd = pwinput.pwinput("Re-enter Password: ")
    if newpwd != repwd:
        raise SyntaxError("The two passwords do not match!")
        return
    if newname in ACCOUNTS:
        print(f"{Fore.YELLOW}WARNING: The name was created!")
        return
    ACCOUNTS[newname] = base64.b64encode(newpwd.encode("utf-8")).decode("utf-8")
    with open(os.path.join("configs", "profiles.json"), "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=4)
    print(f'• {Fore.GREEN}Created successfully.')

def change_passwd(self):
    stpasswd = base64.b64decode(profiles["accounts"][self.username].strip()).decode("utf-8")
    oldpwd = pwinput.pwinput("Old Password: ")
    reoldpwd = pwinput.pwinput("Re-enter Old Password: ")
    if oldpwd != reoldpwd:
        raise SyntaxError("The two passwords do not match!")
        return
    if oldpwd == stpasswd:
        newpwd = pwinput.pwinput("New Password: ")
        ACCOUNTS[self.username] = base64.b64encode(newpwd.encode("utf-8")).decode("utf-8")
        with open(os.path.join("configs", "profiles.json"), "w", encoding="utf-8") as f:
            json.dump(profiles, f, ensure_ascii=False, indent=4)
        print(f'• {Fore.GREEN}Resetted successfully.')
    else:
        print(f"Error: {Fore.RED}Invalid username or password!")

def set_auto_login(args):
    if len(args) < 2:
        print(f"Error: {Fore.RED}Please input a username.")
        return
    
    if args[1] == "disable":
        profiles["auto_login"] = None
        with open(os.path.join("configs", "profiles.json"), "w", encoding="utf-8") as f:
            json.dump(profiles, f, ensure_ascii=False, indent=4)
        print(f"• {Fore.GREEN}Auto login disabled.")
        return
    elif args[1] not in ACCOUNTS:
        print(f"Error: {Fore.RED}Unknown user '{args[1]}'.")
        return
    profiles["auto_login"] = args[1]
    with open(os.path.join("configs", "profiles.json"), "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=4)
    print(f"• {Fore.GREEN}Auto login set to '{args[1]}'.")