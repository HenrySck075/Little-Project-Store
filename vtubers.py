# to search for major VTubers, use the All Pages page

# if termux (termux-clipboard-set is just 1 command) (you can troll this by creating a script with same name in PATH idk)
termux=(__import__("shutil").which("termux-clipboard-set") is not None)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as driverWait
from selenium.webdriver.remote.webelement import WebElement

import json, traceback
from bs4 import BeautifulSoup

resName = "Minor VTubers.json"
try:vtubers = json.load(open(resName,"r"))
except:vtubers=[]
rb = lambda s: s.replace("(", "").replace(")", "")
"Remove curved brackets"

urlMap = {
    "Twitch":"twitch.tv",
    "Twitcasting":"twitcasting.tv",
    "17live":"17.live",
    "SHOWROOM":"showroom-live.com",
    "NicoNico":"nicovideo.jp",
    "OPENREC.tv":"openrec.tv",
    "Mildom":"mildom.com",
    "REALITY":"reality.app",
    "Mixch":"mixch.tv",
    "Mirrativ":"mirrativ.com",
    "bilibili":"bilibili.com",
    "fanbox":"fanbox.cc",
    "TikTok":"tiktok.com",
    "LINE Live":"live.line.me",
    "YouTube":"youtube.com",
    "Twitter":"twitter.com" #"x.com" # elon dum
}
def getServiceByUrl(url):
    if all(i not in url for i in urlMap.values()):
        print(f"An undefined service detected: {url}")
        name = input("Please enter the service name: ")
        host = input("Please enter host url: ")
        urlMap[name] = host
        return name

    else:
        for i in urlMap:
            if urlMap[i] in url: return i
        else: return ""


urls = [
    "https://virtualyoutuber.fandom.com/wiki/List_of_minor_VTubers_(A%E2%80%94B)",
    "https://virtualyoutuber.fandom.com/wiki/List_of_minor_VTubers_(C%E2%80%94D)",
    "https://virtualyoutuber.fandom.com/wiki/List_of_minor_VTubers_(E%E2%80%94F)",
    "https://virtualyoutuber.fandom.com/wiki/List_of_minor_VTubers_(G%E2%80%94H)",
    "https://virtualyoutuber.fandom.com/wiki/List_of_minor_VTubers_(I%E2%80%94J)",
    "https://virtualyoutuber.fandom.com/wiki/List_of_minor_VTubers_(K%E2%80%94L)",
    "https://virtualyoutuber.fandom.com/wiki/List_of_minor_VTubers_(M%E2%80%94N)",
    "https://virtualyoutuber.fandom.com/wiki/List_of_minor_VTubers_(O%E2%80%94P)",
    "https://virtualyoutuber.fandom.com/wiki/List_of_minor_VTubers_(Q%E2%80%94R)",
    "https://virtualyoutuber.fandom.com/wiki/List_of_minor_VTubers_(S%E2%80%94T)",
    "https://virtualyoutuber.fandom.com/wiki/List_of_minor_VTubers_(U%E2%80%94V)",
    "https://virtualyoutuber.fandom.com/wiki/List_of_minor_VTubers_(W%E2%80%94X)",
    "https://virtualyoutuber.fandom.com/wiki/List_of_minor_VTubers_(Y%E2%80%94Z)",
    "https://virtualyoutuber.fandom.com/wiki/List_of_minor_VTubers_(other)"
]
options = webdriver.ChromeOptions() if termux else webdriver.EdgeOptions()
options.page_load_strategy = "eager"
options.add_argument("--no-sandbox") 
options.add_argument("--disable-dev-shm-usage") 
options.add_argument("--disable-logging") 
#options.add_argument("--headless=new")
driver = webdriver.Edge(options) if not termux else webdriver.Chrome(options=options)

def minor_vtubers():
    for url in urls:
        print(f"---------- Fetching {url}")
        driver.get(url)
        tableBody:WebElement = driverWait(driver,10).until(ec.presence_of_element_located(("css selector", "#minor-vtuber-table > tbody")))
        print("---------- Iterating table...")
        driver.execute_script("document.title='MASTER CHEF 🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥'")
        for idx, item in enumerate(BeautifulSoup(tableBody.get_attribute("outerHTML")).select("tr")):
            print(f"---------- Item ID: {idx}")
            items = item.select("td")
            cursed = len(items)
            if cursed < 2: continue
            entry={}
            
            try: temp = items[1].select_one("b").text
            except: temp = items[1].text

            temp = temp.split("(")
            name, jpName = tuple(temp) if len(temp)==2 else (temp[0],"")
            entry["name"] = name
            entry["jpName"] = rb(jpName)
            del temp

            langs = items[2].text
            
            vtUrls = {}
            
            try:vtUrls["YouTube"] = items[3].select_one("a").attrs["href"]
            except:pass
            
            if cursed >=5:
                temp = items[4]
                a = temp.select("a")
                # nah bro :skull:
                if len(a) > 0:
                    vtUrls[getServiceByUrl(a[0].attrs["href"])] = a[0].attrs["href"]
                    if (the:=temp.select_one("p")) != None:
                        the = the.select("a")
                        for i in range(len(the)):
                            vtUrls[getServiceByUrl(the[i].attrs["href"])] = the[i].attrs["href"]
            temp = None
            del temp

            if cursed >= 6:
                temp = items[5]
                test = temp.select_one("a")
                if test != None:
                    vtUrls["twitter"] = test.attrs["href"]
                    if (the:=temp.select_one("p")) != None:
                        vtUrls["twitter"] = [vtUrls["twitter"]]
                        the = the.select("a")
                        for i in range(len(the)):
                            vtUrls["twitter"].append(the[i].attrs["href"])
                    del temp
                else: 
                    vtUrls["twitter"] = ""
                    del test
            
            entry["urls"] = vtUrls
            
            if cursed >=8:
                entry["notes"] = items[7].text.replace("\n"," ")
            else: entry["notes"] = ""

            vtubers.append(entry)

        json.dump(vtubers, open(resName,"w"), indent=4)

try: minor_vtubers()
except KeyboardInterrupt:
    print("Keyboard interrupted")
except Exception as e:
    traceback.print_exc(file=open("exceptionContent","w",encoding="utf-8"))
finally: 
    driver.close()
    
