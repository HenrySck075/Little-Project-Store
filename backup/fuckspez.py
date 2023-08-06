import requests, traceback, time, threading, json, sys
#black=[[int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])]]
black=[]
for i in range(1195, 1204):
    for j in range(989,996):
        black.append([-i,j,27])
def mein():
    global black
    waitTime = 240
    while True:
        if len(black)==0: break
        canvas=3
        if 1500-(-black[0][0])>999: canvas+=1
        if 1500-(-black[0][0])>1999: canvas+=1
        res = requests.post("https://gql-realtime-2.reddit.com/query", json={
            "operationName": "setPixel",
            "query":"mutation setPixel($input: ActInput!) {  act(input: $input) {    data {      ... on BasicMessage {        id        data {          ... on GetUserCooldownResponseMessageData {            nextAvailablePixelTimestamp            __typename          }          ... on SetPixelResponseMessageData {            timestamp            __typename          }          __typename        }        __typename      }      __typename    }    __typename  }}",
            "variables":{
                "input": {
                    "actionName": "r/replace:set_pixel",
                    "PixelMessageData": {
                        "coordinate": {
                            "x": 1500-(-black[0][0])-(1000*(canvas-3)),
                            "y": black[0][1]
                        },
                        "colorIndex": black[0][2] or 27,
                        "canvasIndex": canvas
                    }
                }
            }
        }, headers={
            "Authorization": "you dont",
            "Origin":"https://garlic-bread.reddit.com", 
            "Referer":"https://garlic-bread.reddit.com/", 
            "Apollographql-Client-Name":"garlic-bread",
            "Apollographql-Client-Version": "0.0.1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183"
        })

        print(f"Status: {res.status_code}. Pixel: {black[0][0]} {black[0][1]}\nResponse: {res.json()}")
        if "errors" in res.json():
            from datetime import datetime
            nextAvalai=res.json()["errors"][0]["extensions"]["nextAvailablePixelTs"]/1000
            waitTime = nextAvalai-int(datetime.utcnow().timestamp())
        else:
            del black[0]
        time.sleep(waitTime)
def j():
    global black
    while True:
        m=input("Add pixel to queue: ").split()
        black.append([int(i) for i in m])
threading.Thread(target=mein).start()
threading.Thread(target=j).start()

