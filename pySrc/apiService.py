from quart import Quart
import uvicorn
import threading
import fileService
import asyncio
import json
import mimetypes
import cv2
import os

PLAYERS = []
CAPTURES = []
IP = "127.0.0.1"
PORT = 28012
app = Quart(__name__)
pid = 1
eventLoop = None




@app.route("/captures/{id}}")
def getCapImage(id: int):
    try:
        return np.array(cv2.imencode(".png",CAP_LIST[id].currentImage)[1]).toBytes(), 200, {"Content-Type":mimetypes.guess_type(".png")}
    except:
        return

@app.route("/players")
def playerData():
    return json.dumps([p.exportData() for p in PLAYERS])
@app.route("/Overlays/<overlay>/")
async def getOverlayIndex(overlay):
    if(overlay[-len(".zip"):]==".zip"):
        return await getOverlayFromZip(overlay,"index.html")
    return await getOverlay(overlay,"index.html")


async def getOverlayFromZip(overlay,path):
    file = fileService.loadFile(f"./Overlays/{overlay}",overlay).fileData

    return file.read(path), 200, {'Content-Type': mimetypes.guess_type(path)}


@app.route("/Overlays/<overlay>/<path:path>")
async def getOverlay(overlay,path):
    if(overlay[-len(".zip"):]==".zip"):
        return await getOverlayFromZip(overlay,path)
    with open(f"Overlays/{overlay}/{path}", 'rb') as f:
        return f.read(), 200, {'Content-Type': mimetypes.guess_type(path)}

def startApi(players, captures, event_signal, ip=IP,port=PORT):
    global PLAYERS 
    global eventLoop
    PLAYERS = players
    global CAPTURES 
    CAPTURES = captures
    global pid
    pid = os.getpid()
    eventLoop = asyncio.new_event_loop()
    config = uvicorn.Config(app=app,host=ip,port=port,loop=eventLoop)
    server = uvicorn.Server(config=config)
    eventLoop.run_until_complete(server.serve())