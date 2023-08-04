from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as driverWait
from selenium.webdriver.remote.webelement import WebElement
import json
from pygments.lexers.data import JsonLexer
from pygments.formatters import NullFormatter
from pygments import highlight
from bs4 import BeautifulSoup

resName = "inaccurate list of VTubers, like, it doesn't update new vtuber since march 2023.json"
vtubers = json.load(open(resName,"r"))
rb = lambda s: s.replace("(", "").replace(")", "")
"Remove curved brackets"
#"https://virtualyoutuber.fandom.com/wiki/List_of_minor_VTubers_(A%E2%80%94B)",
urls = [
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
    driver = webdriver.Edge("msedgedriver.exe")
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
            print(len(items))
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
                otherUrls[temp.text.replace(a[0].text,"").replace(" ", "").replace("\n\n\n","")] = a[0].attrs["href"]
                if (the:=temp.select_one("p")) != None:
                    the = the.select("*")
                    for i in range(len(the)):
                        if i%2 == 0: otherUrls[rb(the[i].text)] = the[i].attrs["href"]
            entry["otherUrls"] = otherUrls
            del temp

            try: 
                temp = items[5]
                entry["twitterUrl"] = temp.select_one("a").attrs["href"]
                if (the:=temp.select_one("p")) != None:
                    entry["twitterUrl"] = {rb(item.select("*")[1].text).replace(" ",""): entry["twitterUrl"]}
                    the = the.select("*")
                    for i in range(len(the)):
                        if i%2 == 0: entry["twitterUrl"][rb(the[i+1].text)] = the[i].text
                del temp
            except: entry["twitterUrl"] = ""

            try: entry["notes"] = items[7].text.replace("\n"," ")
            except: entry["notes"] = ""

            print(highlight(json.dumps(entry), JsonLexer(), NullFormatter()))
            vtubers.append(entry)

        json.dump(vtubers, open(resName,"w"), indent=4)
        driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 't')

except KeyboardInterrupt:
    print("Keyboard interrupted")
finally: 
    driver.close()
    
