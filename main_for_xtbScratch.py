from websocket import create_connection
import json
from utils import *


ws=create_connection("wss://ws.xtb.com/demo")
ws.send(json.dumps(openFile('xtb_login.json')))
res=json.loads(ws.recv())
ssID=res["streamSessionId"]

json_doc=openFile('cmd_no_streaming.json')
#json_doc['streamSessionId']=ssID

json_send=json.dumps(json_doc)
ws.send(json_send)
res=json.loads(ws.recv())
print(res)