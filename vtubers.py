# to search for major VTubers, use the All Pages page

import json, traceback, sys
from bs4 import BeautifulSoup
import requests
rb = lambda s: s.replace("(", "").replace(")", "")
"Remove curved brackets"

urlMap = {
    "Twitch":["twitch.tv"],
    "Twitcasting":["twitcasting.tv"],
    "17live":["17.live"],
    "SHOWROOM":["showroom-live.com"],
    "NicoNico":["nicovideo.jp"],
    "OPENREC.tv":["openrec.tv"],
    "Mildom":["mildom.com"],
    "REALITY":["reality.app"],
    "Mixch":["mixch.tv"],
    "Mirrativ":["mirrativ.com"],
    "bilibili":["bilibili.com","bilibili.tv"],
    "fanbox":["fanbox.cc"],
    "TikTok":["tiktok.com"],
    "LINE Live":["live.line.me"],
    "YouTube":["youtube.com"],
    "Twitter":["twitter.com"],
    "Facebook":["facebook.com"],
    "Instagram":["instagram.com"],
    "Carrd":["carrd.co"],
    "Discord":["discord.com","discord.gg"],
    "Weibo":["weibo.com"],
    "Kick":["kick.com"],
    "Reddit":["reddit.com"],
    "pixiv":["pixiv.net"],
    "Spotify":["spotify.com"],
    "Apple Music":["music.apple.com"],
    "DeviantArt":["deviantart.com"],
    "Marshmallow":["marshmallow-qa.com"],
    "SoundCloud":["soundcloud.com"],
    "VT Social":["vt.social"],
    "Ko-Fi":["ko-fi.com"]
}

def getServiceByUrl(url):
    for i in urlMap.keys():
        if any(j in url for j in urlMap[i]): return i

    print(f"An undefined service detected: {url}")
    name = input("Please enter the service name: ")
    host = input("Please enter host url: ").split(", ")

    urlMap[name] = host

    return name



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
resName = ''
vtubers = []
def minor_vtubers():
    resName = "Minor VTubers.json"
    try:vtubers = json.load(open(resName,"r"))
    except:vtubers=[]
    for url in urls:
        print(f"---------- Fetching {url}")
        for idx, item in enumerate(BeautifulSoup(requests.get(url).text,"lxml").select("#minor-vtuber-table tbody tr")):
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
                    vtUrls["Twitter"] = test.attrs["href"]
                    if (the:=temp.select_one("p")) != None:
                        vtUrls["Twitter"] = [vtUrls["Twitter"]]
                        the = the.select("a")
                        for i in range(len(the)):
                            vtUrls["Twitter"].append(the[i].attrs["href"])
                    del temp
                else: 
                    vtUrls["Twitter"] = ""
                    del test
            
            entry["urls"] = vtUrls
            
            vtubers.append(entry)

        json.dump(vtubers, open(resName,"w"), indent=4)

def relativeURL(url):
    if "https://" not in url: url = "https://virtualyoutuber.fandom.com" + url
    return url

def major_vtubers(startFrom=None):
    global vtubers, resName
    resName = "Major VTubers.json"
    try:vtubers = json.load(open(resName,"r"))
    except:vtubers=[]
    apUrl = "https://virtualyoutuber.fandom.com/wiki/Special:AllPages"
    if startFrom!=None:
        apUrl+=f"?from={startFrom.replace(' ', '+').replace('/','%%2F')}&to=&namespace=0" # there's no need for urldecode bc page names are already in english
    prevPage = ""
    while True:
        mainsoup = BeautifulSoup(requests.get(relativeURL(apUrl)).text,"lxml")
        anchors = mainsoup.select_one(".mw-allpages-nav").select("a")
        apUrl = anchors[-1].attrs["href"]
        if apUrl == prevPage: break
        pages = mainsoup.select(".mw-allpages-chunk li a")
        for anchor in pages:
            if any(b in anchor.text for b in ["/Gallery", "Discography", "(disambiguation)", "Historical Milestones"]) or anchor.attrs.get("class",None) is not None: continue
            print(f"---------- Fetching {relativeURL(anchor.attrs['href'])}")
            soup = BeautifulSoup(requests.get(relativeURL(anchor.attrs["href"])).text,"lxml")
            # if this is not a page for agency, continue
            if soup.select_one("#Members") == None:
                entry = {}
                entry["name"] = soup.select_one(".page-header__title").text[1:-1]

                origName = soup.select_one("[data-source='original_name'] div")
                entry["originalName"] = origName.text if origName != None else ""
                extUrl = {}
                try:
                    for u in soup.select(".portable-infobox section")[1].select("a"):
                        smile = u.parent
                        if smile.name != 'div': smile = smile.parent
                        if "Official Website" in smile.parent.select_one("h3").text: continue
                        t=u.attrs["href"]
                        if "#cite_note-" in t: continue
                        svc=getServiceByUrl(u.attrs["href"])
                        if svc in extUrl:
                            if type(extUrl[svc]) != list:
                                extUrl[svc] = [extUrl[svc]]
                            extUrl[svc].append(t)
                        else: extUrl[svc] = t
                    entry["urls"] = extUrl
                except IndexError:continue # https://virtualyoutuber.fandom.com/wiki/A.I._Channel or any similar wiki pages
                vtubers.append(entry)
            else: print("^ agency page")
        prevPage = anchors[-1].attrs["href"]
    json.dump(vtubers, open(resName,"w"), indent=4)

try: 
    globals()[sys.argv[1]](*tuple(sys.argv[2:]))
except KeyboardInterrupt:
    print("Keyboard interrupted")
    json.dump(vtubers, open(resName,"w"), indent=4)
except Exception as e:
    traceback.print_exc()
    json.dump(vtubers, open(resName,"w"), indent=4)
    
