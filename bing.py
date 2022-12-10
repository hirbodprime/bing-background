import requests
import json
import os
import random
from datetime import date
from pathlib import Path


TODAY = date.today()
CWD = os.getcwd()
HOME = Path.home()
BING_FILE_WALLPAPER_PATH = "/Pictures/bing"
FULL_WALLPAPER_PATH = f"{HOME}{BING_FILE_WALLPAPER_PATH}"
BING_URI_BASE = "http://www.bing.com"
BING_URI_WALLPAPER_PATH = "/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US"

if CWD != HOME:
    if os.path.exists(FULL_WALLPAPER_PATH):
        os.chdir(FULL_WALLPAPER_PATH)
    else:
        os.makedirs(FULL_WALLPAPER_PATH)
        os.chdir(FULL_WALLPAPER_PATH)
else:
    pass

# open the Bing HPImageArchive URI and ask for a JSON response
resp = requests.get(BING_URI_BASE + BING_URI_WALLPAPER_PATH)

if resp.status_code == 200:
    json_response = json.loads(resp.content)
    wallpaper_path = json_response['images'][0]['url']
    randomnum = random.randint(0 , 294821)
    filename = f"Image-{TODAY}-{randomnum}.jpg"
    print(filename)
    wallpaper_uri = BING_URI_BASE + wallpaper_path

    # open the actual wallpaper uri, and write the response as an image on the filesystem
    response = requests.get(wallpaper_uri)
    if resp.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
            f.close()
        os.system(f"/usr/bin/gsettings set org.gnome.desktop.background picture-uri {FULL_WALLPAPER_PATH}/{filename}")
        
    else:
        raise ValueError(f"[ERROR] non-200 response from Bing server for {wallpaper_uri}")
else: 
    raise ValueError(f"[ERROR] non-200 response from Bing server for {BING_URI_BASE + BING_URI_WALLPAPER_PATH}")