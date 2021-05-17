from websocket import create_connection
import json
from utils import *


ws=create_connection("wss://ws.xtb.com/demo")
ws.send(json.dumps(openFile('xtb_login.json')))
res=json.loads(ws.recv())
ssID=res["streamSessionId"]
print(ssID)