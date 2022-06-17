import os
import re
from sys import path
try:
    import setuptools
except Exception:
    os.system("sudo python3.6 -m pip install setuptools")
try:
    import requests
except Exception:
    os.system("sudo python3.6 -m pip install requests")
try:
    import pyrogram
except Exception:
    os.system("sudo python3.6 -m pip install pyrogram")
try:
    import redis
except Exception:
    os.system("sudo python3.6 -m pip install redis")
try:
    import collections
except Exception:
    os.system("sudo python3.6 -m pip install collections")
try:
    import asyncio
except Exception:
    os.system("sudo python3.6 -m pip install asyncio")
try:
    import sqlite3
except Exception:
    os.system("sudo python3.6 -m pip install sqlite3")


v = str(os.system("sudo python3.6 -V"))

os.system("sudo chmod +x *")

if re.search(v,"3.6.13"):
    print(True)
else:
    os.system("sudo ./install.sh")
    os.system("cd "+str(path[0]))
os.system("sudo python3.6 -m pip install redis-server")
os.system("sudo systemctl enable redis-server.service")
os.system("sudo service redis-server start")
os.system("sudo python3.6 -m pip install tgcrypto")

if os.path.exists(str(path[0])+"/utils/config.py"):
    print(True)
else:
    token = str(input("+ Enter Your Bot Token Here :- "))
    print("===========================================")
    sudo = str(input("+ Enter Your Sudo Id Here :- "))
    sp = token.split(sep=":")
    bot_id = str(sp[0])
    f = open("utils/config.py","w")
    f.write("""
token='{}'
sudo='{}'
bot_id='{}'
    """.format(token,sudo,bot_id))
    f.close()
    os.system("clear")

os.system("screen -S python-media ./ts.sh")
