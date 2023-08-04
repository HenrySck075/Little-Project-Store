# to search for major VTubers, use the All Pages page

# if termux (termux-clipboard-set is just 1 command) (you can troll this by creating a script with same name in PATH idk)
termux=(__import__("shutil").which("termux-clipboard-set") is not None)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as driverWait
from selenium.webdriver.remote.webelement import WebElement

import json
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
    "OPENREC.tv":"openrec.tv"
}
def getServiceByUrl(url):
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

class SoupSyntaxWebElement:
    "nerissa"
    def __init__(self,a:WebElement):
        self.elem = a
    
    def select(self, selector:str): 
        """Finds a list of elements within this element's children by CSS selector.

        :Args:
            - selector - CSS selctor string, ex: 'a.nav#home'
        """

        return [SoupSyntaxWebElement(i) for i in self.elem.find_elements_by_css_selector(selector)]
    
    def select_one(self, selector:str): 
        """Finds element within this element's children by CSS selector.

        :Args:
            - selector - CSS selctor string, ex: 'a.nav#home'
        """
        if (x:=self.elem.find_element_by_css_selector(selector)) == None: return SoupSyntaxWebElement(x)
        else: return None

    @property
    def children(self):
        "Avoid using this shit as much as possible"
        return [SoupSyntaxWebElement(i) for i in self.elem.find_elements_by_css_selector("*")]

    @property
    def text(self):
        return self.elem.text
    
    def attr(self, attribute):
        return self.elem.get_attribute(attribute)

try:
    chrOpt = webdriver.ChromeOptions()
    chrOpt.page_load_strategy = "eager"
    chrOpt.add_argument("--no-sandbox") 
    chrOpt.add_argument("--disable-dev-shm-usage") 
    chrOpt.add_argument("--headless=new")
    driver = webdriver.Edge("msedgedriver.exe") if not termux else webdriver.Chrome(options=chrOpt)
    for url in urls:
        print(f"---------- Fetching {url}")
        driver.get(url)
        tableBody:WebElement = driverWait(driver,10).until(ec.presence_of_element_located(("css selector", "#minor-vtuber-table > tbody")))
        print("---------- Iterating table...")
        driver.execute_script("document.title='MASTER CHEF 🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥'")
        for idx, item in enumerate(BeautifulSoup(tableBody.get_attribute("outerHTML")).select("tr")):
            print(f"---------- Item ID: {idx}")
            items = item.select("td")
            if len(items) < 2: continue
            entry={}
            
            try: temp = items[1].select_one("b").text
            except: temp = items[1].text

            temp = temp.split("(")
            name, jpName = tuple(temp) if len(temp)==2 else (temp[0],"")
            entry["name"] = name
            entry["jpName"] = rb(jpName)
            del temp

            langs = items[2].text

            try:entry["ytUrl"] = items[3].select_one("a").attrs["href"]
            except:entry["ytUrl"] = ""
            
            otherUrls = {}
            temp = items[4]
            a = temp.select("*")
            # nah bro :skull:
            if len(a) > 0:
                otherUrls[getServiceByUrl(a[0].attrs["href"])] = a[0].attrs["href"]
                if (the:=temp.select_one("p")) != None:
                    the = the.select("*")
                    for i in range(len(the)):
                        otherUrls[(the[i].attrs["href"])] = the[i].attrs["href"]
            entry["otherUrls"] = otherUrls
            del temp

            try:
                # TODO: wacky language
                temp = items[5]
                entry["twitterUrl"] = temp.select_one("a").attrs["href"]
                if (the:=temp.select_one("p")) != None:
                    entry["twitterUrl"] = [entry["twitterUrl"]]
                    the = the.select("*")
                    for i in range(len(the)):
                        entry["twitterUrl"].append(the[i].attrs["href"])
                del temp
            except: entry["twitterUrl"] = ""

            try: entry["notes"] = items[7].text.replace("\n"," ")
            except: entry["notes"] = ""

            vtubers.append(entry)

        json.dump(vtubers, open(resName,"w"), indent=4)

except KeyboardInterrupt:
    print("Keyboard interrupted")
    driver.close()
finally: 
    driver.close()
    
