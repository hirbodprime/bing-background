import requests
import json
import os
import random
from datetime import date , datetime
from pathlib import Path
from optparse import OptionParser

# %prog is built in for OptionParser 
usage = "usage: %prog --day 2"

# creates a instance of OptionParser to parser
parser = OptionParser(usage=usage)

parser.add_option("-d", "--day",type="int" ,action="store",dest="day",
    help="set the background to --day n by date")

(options, args) = parser.parse_args()

TODAY = date.today()
CWD = os.getcwd()
HOME = Path.home()

BING_FILE_WALLPAPER_PATH = f"/Pictures/bing"
FULL_WALLPAPER_PATH = f"{HOME}{BING_FILE_WALLPAPER_PATH}/{TODAY}"
BING_URI_BASE = "http://www.bing.com"
TODAY_BING_URI_WALLPAPER_PATH = "/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US"
_7DAYS_BING_URI_WALLPAPER_PATH = "/HPImageArchive.aspx?format=js&idx=0&n=7&mkt=en-US"

os.makedirs(FULL_WALLPAPER_PATH , exist_ok=True)
os.chdir(FULL_WALLPAPER_PATH)
randomnum = random.randint(0 , 294821)

class BingBackground:


    url_date_list = []
    url_date_dict = {}
    url_pure_list = []
    _7DAYSresp = requests.get(BING_URI_BASE + _7DAYS_BING_URI_WALLPAPER_PATH)
    _7DAYSjson_response = json.loads(_7DAYSresp.content)


    # open the Bing HPImageArchive URI and ask for a JSON response
    TODAY_resp = requests.get(BING_URI_BASE + TODAY_BING_URI_WALLPAPER_PATH)
    today_json_response = json.loads(TODAY_resp.content)
    

    def __init__(self):
        self.today_wallpaper_path = self.today_json_response['images'][0]['url']
        self.from_today_previous_image = self.today_json_response['tooltips']['previous']
        for index in range(len(self._7DAYSjson_response['images'])):
            self.start_date , self.end_date = self._7DAYSjson_response['images'][index]['startdate'],\
            self._7DAYSjson_response['images'][index]['enddate']
            self._7DAYS_url = self._7DAYSjson_response['images'][index]['url']
            self.url_date_dict = {
                'url':self._7DAYS_url,
                'start_date':self.start_date,
                'end_date':self.end_date
            }
            self.url_pure_list.append(self._7DAYS_url)
            self.url_date_list.append(self.url_date_dict)


    def get_day_url_date(self,day):
        self.number_error = False
        self._st = self.url_date_list[-1]['start_date'][-2:]
        self._ed = self.url_date_list[0]['start_date'][-2:]
        self._day = str(day)
        if not self._day.isnumeric():
            raise ValueError('day value must be number')
        for index in range(len(self.url_date_list)):
            if self.url_date_list[index]['start_date'][-2:] == self._day:
                url = BING_URI_BASE + self.url_date_list[index]['url']
                self.number_error = True
                return url
        if not self.number_error:
            return f"value must be between {self._st} {self._ed}"


    def get_day_url(self,day):
        self.number_error = False
        self._day = str(day)
        if not self._day.isnumeric():
            raise ValueError('day value must be number')
        for index in range(len(self.url_date_list)):
            if self._day in str(index):
                url = BING_URI_BASE + self.url_date_list[index]['url']
                self.number_error = True
                return url
        if not self.number_error:
            return f"value must be between 0 & 7"


    def get_day_url_list(self , start , end):
        urls_list = []
        for i in range(start,end):
            urls_list.append(BING_URI_BASE + self.url_pure_list[i])
        return urls_list
    
    
    def set_image_day(self,day):
        currentMonth = datetime.now().month     
        currentYear = datetime.now().year
        self._day = day
        the_image_day = int(self.url_date_list[0]['start_date'][-2:]) - self._day
        print(the_image_day)
        if not the_image_day >= 10:
            the_image_day = str(0) + str(the_image_day)
            print(the_image_day)
        filename = f"Image-{currentYear}{currentMonth}{the_image_day}-{randomnum}.jpg"
        for index in range(len(self.url_date_list)):
            if self.url_date_list[index]['start_date'][-2:] == the_image_day:
                url = BING_URI_BASE + self.url_date_list[index]['url']
                self.number_error = True
                return BingBackground.set_background(self,url,filename)
    
        # BingBackground.set_background(self,wallpaper_uri,filename)


    def set_image_default(self):
        filename = f"Image-{TODAY}-{randomnum}.jpg"
        wallpaper_uri = BING_URI_BASE + self.today_wallpaper_path
        BingBackground.set_background(self,wallpaper_uri,filename)

    def set_background(self,wallpaper_uri , filename):
        self._wallpaper_uri = wallpaper_uri
        self._filename = filename
    # open the actual wallpaper uri, and write the response as an image on the filesystem
        response = requests.get(self._wallpaper_uri)
        with open(self._filename, 'wb') as f:
            f.write(response.content)
        f.close()
        print("am i")
        os.system(f"/usr/bin/gsettings set org.gnome.desktop.background picture-uri {FULL_WALLPAPER_PATH}/{self._filename}")
        return "Done!"

if __name__ == "__main__":
    b = BingBackground()
    # print(b.get_day_url('0'))
    # print(b.get_day_url_date('04'))
    # print(b.get_day_url_list(0,7))
    if options.day:
        b.set_image_day(options.day)
    else:
        b.set_image_default()
