import os
import sys
if sys.version_info[0] < 3 or sys.version_info[1] < 4:
    raise Exception("Must be using Python Version <= 3.4, please update at https://www.python.org/downloads/")
print("Installing discord.py...")
os.system("pip install discord")
print("Installing requests...")
os.system("pip install requests")
print("Done!")