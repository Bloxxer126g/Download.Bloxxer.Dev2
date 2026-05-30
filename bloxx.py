from sys import argv
from requests import get
import subprocess
import os

def Install(ArgumentIndex: int):
    ItemIndex = ArgumentIndex + 1
    try:
        Item = Arguments[ItemIndex]
    except IndexError:
        print("You can't install nothing!")
        return
    try:
        subprocess.run(["pip", "install", "requests"], check=True)
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

Arguments = argv

# Its the BloxParse!
# Its a stupid stystem that matches arguments to commands. 
for argIndex in range(len(Arguments)):
    for comIndex in range(len(Commands)):
        if Commands[comIndex][0] == Arguments[argIndex]:
            Commands[comIndex][2](argIndex)