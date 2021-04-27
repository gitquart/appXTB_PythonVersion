"""
main.py
The xAPIConnector.py works well but it's a wrapper, so this main.py
file will aim to send any API command described in http://developers.xstore.pro/documentation/#introduction
"""

import socket
import json
import time

DEFAULT_XAPI_ADDRESS= 'xapi.xtb.com'
DEFUALT_XAPI_STREAMING_PORT = 5125
DEFAULT_XAPI_PORT= 5124
API_SEND_TIMEOUT = 100


url=''
json_command = {"command": "login",
	            "arguments": {
		                "userId": "12181707",
		                "password": "xoh17643",
		                "appName": ""
	                      }
	            }



def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((DEFAULT_XAPI_ADDRESS, DEFUALT_XAPI_STREAMING_PORT))
    api_command= json.dumps(json_command)
    if my_socket:
        sent = 0
        api_command_encoded = api_command.encode('utf-8')
        while sent < len(api_command_encoded):
            sent += my_socket.send(api_command_encoded[sent:])
            time.sleep(API_SEND_TIMEOUT/1000)
    
    receivedData=''
    decoder = json.JSONDecoder()
    if not my_socket:
        raise RuntimeError("socket connection broken")
    while True:
        char = my_socket.recv(4096).decode()
        receivedData += char
        try:
            (resp, size) = decoder.raw_decode(receivedData)
            if size == len(receivedData):
                receivedData = ''
                break
            elif size < len(receivedData):
                receivedData = receivedData[size:].strip()
                break
        except ValueError as e:
            continue
        
    print(resp)
    
    
    
   







if __name__ == "__main__":
    main()	
