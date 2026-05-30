from sys import argv
from requests import get
import subprocess

def Install(ArgumentIndex:int):
    ItemIndex = ArgumentIndex + 1
    try:
        Item = Arguments[ItemIndex]
        try:
            subprocess.run(["pip install requests"])
            RequestedAsset = get(f"https://download.bloxxer.dev/applications/{Item}/Install.py")
        except:
            print(f"{Item} could not be found on the server.")
            return
    except:
        print("You can't install nothing!")
        return

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