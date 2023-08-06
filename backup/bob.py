import os, json, time
import sys
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import traceback

scopes = ["youtube.force-ssl"]

def fetch_channels():
    channels = json.load(open("channels.json","r",encoding="utf-8"))
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "creds/client_secret.json"

    # Get credentials and create an API client
    youtube = __import__("Google").create_service(client_secrets_file, api_service_name, api_version, scopes)
    token = open("last","r").read()
    requestedTime=0
    while True:
        try:
            if requestedTime==100:
                open("last","w").write(token)
                json.dump(channels, open("channels.json","w"), indent=4)
                break
            response = youtube.search().list(pageToken=token,part="snippet",maxResults=50,q="Ch.",type="channel").execute()
            channels.extend(i["snippet"] for i in response["items"])
            token = response.get("nextPageToken",None)
            print(f"{len(channels)} channels fetched")
            if token==None:break
            time.sleep(1)
            requestedTime+=1
        except Exception as e:
            traceback.print_exc()
            open("last","w").write(token)
            json.dump(channels, open("channels.json","w"), indent=4)
            break

def filter_channels():
    channels = json.load(open("channels.json","r",encoding="utf-8"))
    idxoff=0
    channelNames = []
    def removeCurrentEntry(idx):
        nonlocal idxoff
        del channels[idx-idxoff]
        idxoff += 1
    for idx,i in enumerate(channels):
        if "- Topic" in i["channelTitle"] or "CH" in i["channelTitle"]:
            print("")
            print(f"Removed invalid entry: {i['channelTitle']}")
            removeCurrentEntry(idx)
        if "clip" in i["description"].lower() or "Soju" in i["channelTitle"]:
            print("")
            if input("Possible clip channel detected\nName: {t}\nDescription: {d}\nURL: https://youtube.com/channel/{c}\nshould delete yay or nay: ".format(t=i["channelTitle"],d=i["description"],c=i["channelId"])) == "yay": removeCurrentEntry(idx)
        else:
            no = i["channelTitle"]
            if no in channelNames:
                print("")
                print(f"Removed duplicate entry: {i['channelTitle']}")
                removeCurrentEntry(idx)
            else: channelNames.append(no)

    json.dump(channels,open("channels.json","w",encoding="utf-8"),indent=4)
def noparams():
    print("dude what")

globals().get(sys.argv[1] if len(sys.argv)==2 else "noparams", "noparams")()
