#$PREFIX/bin/python

from flask import Flask, url_for, request, redirect, send_file, make_response, Response
from PIL import Image
from io import BytesIO
from shutil import rmtree
from zipfile import ZipFile
from glob import glob
from moviepy.editor import ImageClip, CompositeVideoClip
import os, requests, numpy as np, json
a = Flask(__name__)
a.config["UPLOAD_FOLDER"] = "./uploads"
port = 4000

apiVersion="1549b3b1bd606f4dc00ac8bc0130e937422cae93"
@a.route("/")
def mein():
    return """
<!doctype html>
<head>
  <title>The HenrySck utility site</title>
</head>
<body>
  <p style="text-align:center">Choose a tool</p>
  <div style="margin: auto; width: 50%">
    <input type="button" onclick="window.location.href='/jpg'" style="height:20px" value="JPG to PNG converter"/>
    <input type="button" onclick="window.location.href='/ugoira'" style="height:20px" value="pixiv ugoira ZIP compiler"/>
  </div>
</body>
    """

@a.route("/debug/getmedia/<file>")
def no(file):
    return send_file(f"./media/{file}", as_attachment=True, download_name=file)
#~~~~~~~~~~~~~~~~~~~~
@a.route("/ugoira")
def zcui():
    return """
<!doctype html>
<head>
  <title>cunny animated</title>
</head>
<body>
  <form action="/ugoiraconv">
    <label for="illust">Illust ID:</label>
    <input type="number" id="idinp" name="illust" min="1">
    <input type="submit">
  </form>
</body>
    """

@a.route("/ugoiraconv")
def zipconvf(): return zipconv(request.args.get("illust"))
@a.route("/u/<illust>")
def zipconva(illust): return zipconv(illust)
def zipconv(illust):
    # return 400 whenever the browser tries to send the request 2 more times
    if os.path.exists(f"./media/{illust}.gif"): return make_response("omfg why is browsers sending 2 additional request here", 400)
    if illust==None: return "why"
    c=requests.get(f"https://www.pixiv.net/touch/ajax/illust/details?illust_id={illust}&ref=https%3A%2F%2Fwww.pixiv.net%2Fen%2F&lang=en&version={apiVersion}").json()

    d=c["body"]["illust_details"]
    if "ugoira_meta" not in d:
        return "Invalid file. Go back to use another ID"
    
    u_json=d["ugoira_meta"]
    u_src=u_json["src"]
    # Get the file size by requesting HEAD
    headers = requests.head(u_src, headers={"Accept": "*/*"}).headers

    f = requests.get(u_src, headers={"Range": f"bytes 0-{headers['content-length']}", "Referer":"https://www.pixiv.net/en/"})
    if f.status_code == 403: return ":("
    zip = ZipFile(BytesIO(f.content),"r")

    delayCount = {}
    lastTime=0
    compositeList = []
    for i in u_json["frames"]:
        nparr = np.array(Image.open(BytesIO(zip.read(i["file"]))))
        dur = i["delay"]/1000
        image = (ImageClip(nparr)
                 .set_duration(dur)
                 .set_start(lastTime))
        
        compositeList.append(image)
        lastTime+=dur
    final = CompositeVideoClip(compositeList)
    final.write_gif(f"./media/{illust}.gif", fps=30, program="ffmpeg")
    zip.close()
    final.close()
    for i in compositeList: i.close()
    return send_file(f"./media/{illust}.gif",as_attachment=True, download_name=f"{illust}.gif")



#~~~~~~~~~~~~~~~~~~~~~
@a.route("/jpg")
def jpgconv():
    return """
<!doctype html>
<head>
  <title>cunny</title>
  <script>
  function clear() {
    const h = new XMLHttpRequest();
    h.open("GET", "/clear")
    h.send()
  };
  function download() {
    pack = + document.getElementById("packdir").checked
    window.location.replace(`/download?packdir=${pack}`);
  };
  </script>
</head>
<body>
  <p>btn</p>
  <form action = "/upload" method="POST" enctype="multipart/form-data" target="result">
    NSFW Files 
    <input type="file" name="amethyst" id="ame" multiple />
    <input type="button" value="Clear" onclick="document.getElementById('ame').value=null" /><br/>
    Default Files 
    <input type="file" name="default" multiple /><br/>
    loli images
    <input type="file" name="lolicon" multiple /><br/>
    ecchi
    <input type="file" name="ecchi" multiple /><br/>
    <br/>
    <input type = "submit" value="Upload">
  </form>
  <input type="button" onclick="clear()" value="Clear converted"></input><br/>
  <input type="button" onclick="download()" value="Download" /></input><br/>
  <form action="/jpg">
    <label for="packdir">aaaaaa</label>
    <input type="checkbox" id="packdir" name="packdir" checked />
    <input type="submit" value="a" style="display: none">
  </form>
  <iframe id="result">
</body>
    """

@a.route("/upload", methods=["POST"])
def upload():
    ne = {}
    for folder in list(request.files.keys()):
        ne[folder] = []
        print(folder)
        for file in request.files.getlist(folder):
            fileio = BytesIO()
            file.save(fileio)
            try: img = Image.open(fileio)
            except: continue
            name = file.filename.replace(".jpg", ".png")
            img.save(os.path.join("./uploads", folder, name),format="PNG")
            ne[folder].append(name)
    return ne

#being both a converter and a proxy
@a.route("/j")
def uploadSingular():
    n = "https://i.pximg.net/img-original/img/"+request.args.get("date").replace(".","/")+"/"+request.args.get("name")
    resp=requests.get(n+".jpg", headers={"Referer":"https://www.pixiv.net/en","upgrade-insecure-requests":"1"})
    # it's jpg
    if resp.status_code == 200:
        nah=BytesIO()
        Image.open(BytesIO(resp.content)).save(nah,format="PNG")
        resp=nah
    # it's png so try again
    elif resp.status_code == 404:
        resp=BytesIO(requests.get(n+".png", headers={"Referer":"https://www.pixiv.net/en","upgrade-insecure-requests":"1"}).content)
    return Response(resp.getvalue(), mimetype="image/png", headers={"content-disposition": f'attachment;filename={n.split("/")[-1].replace(".jpg",".png")}'})

@a.route("/clear")
def clear():
    for i in os.listdir("./uploads"):
        rmtree(os.path.join("./uploads",i))
        os.makedirs(os.path.join("./uploads",i))
    return "done"

@a.route("/download")
def download():
    stream = BytesIO() 
    packdir = True if request.args.get("packdir", "1") == "1" else False
    with ZipFile(stream, 'w') as zf: 
        for i in os.listdir("./uploads"):
            for file in glob(os.path.join("./uploads", i, '*.png')):
                dir = os.path.basename(file)
                if packdir: dir = i + "/" + dir
                zf.write(file, dir) 
    stream.seek(0) 
    return send_file( stream, as_attachment=True, download_name='archive.zip' )

import socket 
def is_port_in_use() -> bool:
    print(port)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
        return s.connect_ex(('localhost', port)) == 0

while is_port_in_use():
    port+=1
a.run(port=port, debug=True)
