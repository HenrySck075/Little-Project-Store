# to search for major VTubers, use the All Pages page
import threading as thread
from copy import deepcopy
import json, sys
from time import thread_time
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
  "REALITY":["reality.app","reality.wrightflyer.net"],
  "Mixch":["mixch.tv"],
  "Mirrativ":["mirrativ.com"],
  "bilibili":["bilibili.com","bilibili.tv"],
  "fanbox":["fanbox.cc"],
  "TikTok":["tiktok.com"],
  "LINE Live":["live.line.me"],
  "YouTube":["youtube.com"],
  "Twitter/X":["twitter.com","t.co"],
  "Facebook":["facebook.com","fb.com"],
  "Instagram":["instagram.com"],
  "Carrd":["carrd.co"],
  "Discord":["discord.com","discord.gg","dsc.gg","discordapp.com"],
  "Weibo":["weibo.com","weibo.cn"],
  "Kick":["kick.com"],
  "Reddit":["reddit.com"],
  "pixiv":["pixiv.net"],
  "Spotify":["spotify.com"],
  "Apple Music":["music.apple.com"],
  "DeviantArt":["deviantart.com"],
  "Marshmallow":["marshmallow-qa.com"],
  "SoundCloud":["soundcloud.com"],
  "VT Social":["vt.social"],
  "Ko-Fi":["ko-fi.com"],
  "VTuber's website":["bunnyayumi.com","cyannyan.com","vjoi.cn"],
  "Patreon":["patreon.com"],
  "Douyin":["douyin.com"],
  "tape":["tapechat.net"],
  "Afdian":["afdian.net"],
  "Tumblr":["tumblr.com"],
  "Google+":["plus.google.com"],
  "Yahoo":["yahoo.com"],
  "Fanicon":["fanicon.net"],
  "Baidu":["baidu.com"],
  "Nimo TV":["nimo.tv"],
  "Telegram":["t.me"],
  "Peing":["peing.net"],
  "VK":["vk.com"],
  "GitHub":["github.com"],
  "ArtStation":["artstation.com"],
  "Teespring":["teespring.com"],
  "CuddlyOctopus":["cuddlyoctopus.com"],
  "Donate":["streamelements.com"],
  "Hatena Blog":["hatenablog.com"],
  "pixiv Fantia":["fantia.jp"],
  "Archives":["archive."],
  "Douyu":["douyu.com"],
  "Line":["lin.ee"],
  "Lit Link":["lit.link"],
  "tapeclub":["tapeclub.net"],
  "Throne":["throne.me","throne.com"],
  "Linktree":["linktr.ee"],
  "POME":["pome.ink"],
  "Mastodon":["ieji.de"]
}

def getServiceByUrl(url:str):
  global droid
  url = url.lower()
  for i in urlMap.keys():
    if any(j in url for j in urlMap[i]): return i
  # linux 
  # os.system("paplay SSNotify.wav")
  print(f"An undefined service detected: {url}. Using host URL for name")
  root = url[:url.find("/",9)]
  name = root[root.find("/",root.find("/")+1):].replace("/","")
  host = [] if name not in urlMap else urlMap[name]
  host.append(name)

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
# ~~~~~~~~~~~~~~~~~~~Minor~~~~~~~~~~~~~~~~~~~
resName = './vtnew.json'
UpdateFlag=False
vtubers = []
def minor_vtubers():
  resName = "Minor VTubers.json"
  try:vtubers = json.load(open(resName,"r"))
  except:
    if not UpdateFlag: vtubers=[]
    else: raise AttributeError("File does not exist")
  diff = []
  updVtubers = deepcopy(vtubers)
  for url in urls:
    print(f"---------- Fetching {url}")
    for idx, item in enumerate(BeautifulSoup(requests.get(url).text,"lxml").select("#minor-vtuber-table tbody tr")):
      print(f"---------- Item ID: {idx}", end="\r")
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
      
      if not UpdateFlag: vtubers.append(entry)
      if UpdateFlag:
        if entry not in updVtubers:
          diff.append(entry)
        updVtubers.append(entry)

    json.dump(vtubers if UpdateFlag else updVtubers, open(resName,"w"), indent=4)
    if UpdateFlag: 
      json.dump(diff,open(resName+"_diff","w"),indent=4)

# ~~~~~~~~~~~~~~~~~~~Major~~~~~~~~~~~~~~~~~~~

def relativeURL(url):
  if "https://" not in url: url = "https://virtualyoutuber.fandom.com" + url
  return url

def major_vtubers(startFrom=None):
  global vtubers, resName
  resName = "Major VTubers.json"
  try:vtubers = json.load(open(resName,"r"))
  except:vtubers=[]
  diff = []
  vt = [i["name"] for i in vtubers]
  apUrl = "https://virtualyoutuber.fandom.com/wiki/Special:AllPages"
  if startFrom!=None:
    apUrl+=f"?from={startFrom.replace(' ', '+').replace('/','%%2F')}&to=&namespace=0" # there's no need for urldecode bc page names are already in english
  prevPage = ""
  try:
    while True:
      if input("Continue processing page? [y/n]: ") == "n": break
      mainsoup = BeautifulSoup(requests.get(relativeURL(apUrl)).text,"lxml")
      anchors = mainsoup.select_one(".mw-allpages-nav").select("a")
      apUrl = anchors[-1].attrs["href"]
      if apUrl == prevPage: break
      pages = mainsoup.select(".mw-allpages-chunk li a")
      for anchor in pages:
        if any(b in anchor.text for b in ["Gallery", "Discography", "(disambiguation)", "Historical Milestones", "List of ", "Con Appearances"]) or anchor.attrs.get("class",None) is not None: continue
        if UpdateFlag: 
          # NOTE for pyright: can't unbound if uses same condition :thumbsup:
          if anchor.text in vt: continue
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
              while smile.name != "div": smile = smile.parent
              if "Official Website" in smile.parent.select_one("h3").text: continue
              t=u.attrs["href"]
              if "#cite_note-" in t or "autonumber" in u.attrs["class"]: continue
              svc=getServiceByUrl(u.attrs["href"])
              if svc in extUrl:
                if type(extUrl[svc]) != list:extUrl[svc] = [extUrl[svc]]
                extUrl[svc].append(t)
              else: extUrl[svc] = t
            entry["urls"] = extUrl
          except IndexError:continue # https://virtualyoutuber.fandom.com/wiki/A.I._Channel or any similar wiki pages
          vtubers.append(entry)
          if UpdateFlag: 
            diff.append(entry)
            # these are guarranteed to be the last item because i said so 
        else: print("^ agency page")
      prevPage = anchors[-1].attrs["href"]
  except KeyboardInterrupt: print("Keyboard interrupted")
  finally:
    json.dump(vtubers, open(resName,"w"), indent=4)
    for i in diff:
      if i not in vtubers: diff.remove(i)
    json.dump(diff, open(resName+"_diff","w"), indent=4)

# the
UpdateFlag = len(sys.argv) >= 2
major_vtubers(sys.argv[2] if len(sys.argv) ==3 else None)
