import socket
import json

DEFAULT_XAPI_ADDRESS= 'xapi.xtb.com'
DEFUALT_XAPI_STREAMING_PORT = 5125
DEFAULT_XAPI_PORT= 5124


url=''
json_to_send = {
	"command": "login",
	"arguments": {
		"userId": "12181707",
		"password": "xoh17643",
        "appId": ""
	}
}

data = json.dumps(json_to_send)


my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect((DEFAULT_XAPI_ADDRESS, DEFUALT_XAPI_STREAMING_PORT))
my_socket.sendall(bytes(data,encoding='utf-8'))
res=my_socket.recv(1024)
print(res.decode("utf-8"))

