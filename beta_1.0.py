from colorama import Fore
from time import sleep as rest
from json import load, dump
from os import system, SEEK_END
from os import path as PATHS
from re import search

with open("data/data.json", "r") as file: black = load(file)
def follow(file):
    file.seek(0, SEEK_END)
    while True:
        line = file.readline()
        if not line:
            rest(0.1)
            continue
        yield line
path = PATHS.join(PATHS.expanduser("~"), ".lunarclient", "logs", "launcher", "renderer.log")
title = Fore.WHITE + """
Tenki Alpha Build 1.0 - Use /who To Refresh
===========================================
TAG       NAME                   ENCOUNTERS
==========================================="""

def gap(player, encounters):
    gap = ""; gap2 = ""
    for i in range(0,(22 - len(player))):
        gap += " "

    for i in range(0,(10 - len(str(encounters)))):
        gap2 += " "
    return gap, gap2
def get(player):
    try:
        with open("data/encounters.json", "r") as f:
            data = load(f)
            encounters = data[player]
            data[player] += 1
        with open("data/encounters.json", "w") as f:
            dump(data, f)
        return encounters
    except:
        with open("data/encounters.json", "r") as f:
            data = load(f)
            data[player] = 1
        with open("data/encounters.json", "w") as f:
            dump(data, f)
        return 1
class Overlay:
    def __init__(self) -> None:
        self.create()
        self.list = []

    def create(self):
        self.list = []
        system("cls")
        print(title)

    def add(self, player):
        if player not in self.list:
            self.list.append(player)
        encounters = get(player)
        if player in black:
            status = black[player]
            if status == "sniper":
                print(Fore.RED + f"Sniper    {player}{gap(player, encounters)[0]}{gap(player, encounters)[1]}{encounters}")
            else:
                print(Fore.YELLOW + f"Cheater   {player}{gap(player, encounters)[0]}{gap(player, encounters)[1]}{encounters}")
        else:
            print(Fore.GREEN + f"Player    {player}{gap(player, encounters)[0]}{gap(player, encounters)[1]}{encounters}")

    def remove(self, player):
        self.list.remove(player)
        self.create()
        for name in self.list:
            self.add(name)


if __name__ == "__main__":

    overlay = Overlay()
    while True:
        file = open(path, "r", encoding='utf-8')
        lines = follow(file)
        for line in lines:
            if "ONLINE:" in line:
                pattern = r'\[CHAT\] ONLINE: (.*)'
                match = search(pattern, line)
                if match: usernames = match.group(1).split(", ")
                for username in usernames: overlay.add(username)
            if "has joined" in line:
                pattern = r'\[CHAT\] (\w+) has joined'
                match = search(pattern, line)
                if match: 
                    try: overlay.add(match.group(1))
                    except: pass
            if "has quit!" in line:
                pattern = r'\[CHAT\] (\w+) has quit!'
                match = search(pattern, line)
                if match: 
                    try: overlay.remove(match.group(1)) 
                    except: pass
            if "Sending you to" in line:
                overlay.create()