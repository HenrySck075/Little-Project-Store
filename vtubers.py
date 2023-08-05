# to search for major VTubers, use the All Pages page

import json, traceback
from bs4 import BeautifulSoup
import requests
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

def minor_vtubers():
    resName = "Minor VTubers.json"
    try:vtubers = json.load(open(resName,"r"))
    except:vtubers=[]
    for url in urls:
        print(f"---------- Fetching {url}")
        for idx, item in enumerate(BeautifulSoup(requests.get(url).text).select("#minor-vtuber-table tbody tr")):
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

            entry["language"] = items[2].text
            
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

def relativeURL(url):
    if "https://" not in url: url = "https://virtualyoutuber.fandom.com" + url
    return url

def major_vtubers():
    resName = "Major VTubers.json"
    try:vtubers = json.load(open(resName,"r"))
    except:vtubers=[]
    apUrl = "https://virtualyoutuber.fandom.com/wiki/Special:AllPages"
    prevPage = ""
    while True:
        mainsoup = BeautifulSoup(requests.get(apUrl).text)
        anchors = mainsoup.select_one(".mw-allpages-nav").select("a")
        prevPage = anchors[0].attrs["href"]
        apUrl = anchors[-1].attrs["href"]
        pages = mainsoup.select_one(".mw-allpages-chunk").select("li")
        for i in pages:
            anchor = i.select_one("a")
            if any(b in anchor.attrs["href"] for b in ["/Gallery", "/Discography"]) or anchor.attrs.get("class",None) is not None: continue
            print(f"---------- Fetching {anchor.attrs['href']}")
            soup = BeautifulSoup(requests.get(relativeURL(anchor.attrs["href"])).text)
            # if this is not a page for agency, continue
            if soup.select_one("span#Members") == None:
                entry = {}
                entry["name"] = soup.select_one(".mw-parser-output p > b").text
                entry["urls"] = {getServiceByUrl(u.attrs["href"]): u.attrs["href"] for u in soup.select_one("span#Media").parent.find_next("ul").select("li")}
                vtubers.append(entry)
        if apUrl == prevPage: break
    json.dump(vtubers, open(resName,"w"), indent=4)

try: major_vtubers()
except KeyboardInterrupt:
    print("Keyboard interrupted")
except Exception as e:
    traceback.print_exc(file=open("exceptionContent","w",encoding="utf-8"))
    
