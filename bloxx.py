from sys import argv
from requests import get
import subprocess
import os
import ctypes
import winreg

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def add_self_to_path():
    import sys
    if getattr(sys, 'frozen', False):
        current_dir = os.path.dirname(os.path.abspath(sys.executable))
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, 
            r"Environment", 
            0, 
            winreg.KEY_ALL_ACCESS
        )
        
        try:
            existing_path, data_type = winreg.QueryValueEx(key, "PATH")
        except FileNotFoundError:
            existing_path = ""
            data_type = winreg.REG_EXPAND_SZ

        path_list = [p.strip().rstrip('\\').lower() for p in existing_path.split(';') if p.strip()]
        normalized_current = current_dir.rstrip('\\').lower()

        if normalized_current in path_list:
            winreg.CloseKey(key)
            return

        new_path = existing_path + f";{current_dir}" if existing_path else current_dir
        winreg.SetValueEx(key, "PATH", 0, data_type, new_path)
        winreg.CloseKey(key)

        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        ctypes.windll.user32.SendMessageW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment")


    except Exception as e:
        print(e)
        return

Arguments = argv

def Install(ArgumentIndex: int):
    ItemIndex = ArgumentIndex + 1
    try:
        Item = Arguments[ItemIndex]
    except IndexError:
        print("You can't install nothing!")
        return
    try:
        url = f"https://download.bloxxer.dev/applications/{Item}/Install.py"
        response = get(url)
        if response.status_code != 200:
            print(f"{Item} could not be found on the server. (Status: {response.status_code})")
            return
            
        temp_filename = f"temp_install_{Item}.py"
        with open(temp_filename, "w", encoding="utf-8") as f:
            f.write(response.text)
            
        subprocess.run(["python", temp_filename])
        os.remove(temp_filename)

    except Exception as e:
        print(f"An error occurred during installation: {e}")

Commands = [
    ["install", "Installs an application", Install]
]

def run_bloxparse():
    for argIndex in range(len(Arguments)):
        for comIndex in range(len(Commands)):
            if Commands[comIndex][0] == Arguments[argIndex]:
                Commands[comIndex][2](argIndex)

if __name__ == "__main__":
    import sys
    if is_admin():
        add_self_to_path()
        run_bloxparse()
    else:
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_READ)
            existing_path, _ = winreg.QueryValueEx(key, "PATH")
            winreg.CloseKey(key)
            
            if getattr(sys, 'frozen', False):
                cd = os.path.dirname(os.path.abspath(sys.executable))
            else:
                cd = os.path.dirname(os.path.abspath(__file__))
                
            if cd.rstrip('\\').lower() in [p.strip().rstrip('\\').lower() for p in existing_path.split(';') if p.strip()]:
                run_bloxparse()
                sys.exit()
        except Exception:
            pass
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )